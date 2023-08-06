"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import re
import time

from git import Repo, Git, InvalidGitRepositoryError, GitError, PushInfo
from halo import Halo

from ml_git import log
from ml_git.config import get_metadata_path
from ml_git.constants import METADATA_MANAGER_CLASS_NAME, HEAD_1, RGX_ADDED_FILES, RGX_DELETED_FILES, RGX_SIZE_FILES, \
    RGX_AMOUNT_FILES, TAG, AUTHOR, EMAIL, DATE, MESSAGE, ADDED, SIZE, AMOUNT, DELETED, SPEC_EXTENSION
from ml_git.manifest import Manifest
from ml_git.ml_git_message import output_messages
from ml_git.utils import get_root_path, ensure_path_exists, yaml_load, RootPathException, get_yaml_str


class MetadataRepo(object):

    def __init__(self, git, path):
        try:
            root_path = get_root_path()
            self.__path = os.path.join(root_path, path)
            self.__git = git
            ensure_path_exists(self.__path)
        except RootPathException as e:
            log.error(e, class_name=METADATA_MANAGER_CLASS_NAME)
            raise e
        except Exception as e:
            if str(e) == '\'Metadata\' object has no attribute \'_MetadataRepo__git\'':
                log.error('You are not in an initialized ml-git repository.', class_name=METADATA_MANAGER_CLASS_NAME)
            else:
                log.error(e, class_name=METADATA_MANAGER_CLASS_NAME)
            return

    def init(self):
        try:
            log.info('Metadata init [%s] @ [%s]' % (self.__git, self.__path), class_name=METADATA_MANAGER_CLASS_NAME)
            Repo.clone_from(self.__git, self.__path)
        except GitError as g:
            if 'fatal: repository \'\' does not exist' in g.stderr:
                raise GitError('Unable to find remote repository. Add the remote first.')
            elif 'Repository not found' in g.stderr:
                raise GitError('Unable to find ' + self.__git + '. Check the remote repository used.')
            elif 'already exists and is not an empty directory' in g.stderr:
                raise GitError('The path [%s] already exists and is not an empty directory.' % self.__path)
            elif 'Authentication failed' in g.stderr:
                raise GitError('Authentication failed for git remote')
            else:
                raise GitError(g.stderr)
            return

    def remote_set_url(self, mlgit_remote):
        try:
            if self.check_exists():
                repo = Repo(self.__path)
                repo.remote().set_url(new_url=mlgit_remote)
        except InvalidGitRepositoryError as e:
            log.error(e, class_name=METADATA_MANAGER_CLASS_NAME)
            raise e

    def check_exists(self):
        log.debug('Metadata check existence [%s] @ [%s]' % (self.__git, self.__path),
                  class_name=METADATA_MANAGER_CLASS_NAME)
        try:
            Repo(self.__path)
        except Exception:
            return False
        return True

    def checkout(self, sha):
        repo = Git(self.__path)
        repo.checkout(sha)

    def update(self):
        log.info('Pull [%s]' % self.__path, class_name=METADATA_MANAGER_CLASS_NAME)
        repo = Repo(self.__path)
        self.validate_blank_remote_url()
        o = repo.remotes.origin
        o.pull('--tags')

    def commit(self, file, msg):
        log.info('Commit repo[%s] --- file[%s]' % (self.__path, file), class_name=METADATA_MANAGER_CLASS_NAME)
        repo = Repo(self.__path)
        repo.index.add([file])
        return repo.index.commit(msg)

    def tag_add(self, tag):
        repo = Repo(self.__path)
        return repo.create_tag(tag, message='Automatic tag "{0}"'.format(tag))

    @Halo(text='Pushing metadata to the git repository', spinner='dots')
    def push(self):
        log.debug('Push [%s]' % self.__path, class_name=METADATA_MANAGER_CLASS_NAME)
        repo = Repo(self.__path)
        try:
            self.validate_blank_remote_url()
            for i in repo.remotes.origin.push(tags=True):
                if (i.flags & PushInfo.ERROR) == PushInfo.ERROR:
                    raise RuntimeError('Error on push metadata to git repository. Please update your mlgit project!')

            for i in repo.remotes.origin.push():
                if (i.flags & PushInfo.ERROR) == PushInfo.ERROR:
                    raise RuntimeError('Error on push metadata to git repository. Please update your mlgit project!')
        except GitError as e:
            err = e.stderr
            match = re.search("stderr: 'fatal:((?:.|\\s)*)'", err)
            if match:
                err = match.group(1)
                raise GitError(err)

    def fetch(self):
        try:
            log.debug(' fetch [%s]' % self.__path, class_name=METADATA_MANAGER_CLASS_NAME)
            repo = Repo(self.__path)
            self.validate_blank_remote_url()
            repo.remotes.origin.fetch()
        except GitError as e:
            err = e.stderr
            match = re.search('stderr: \'fatal:(.*)\'', err)
            if match:
                err = match.group(1)
                log.error(err, class_name=METADATA_MANAGER_CLASS_NAME)
            else:
                log.error(err, class_name=METADATA_MANAGER_CLASS_NAME)
            return False

    def list_tags(self, spec, full_info=False):
        tags = []
        try:
            repo = Repo(self.__path)
            r_tags = repo.tags if full_info else repo.git.tag(sort='creatordate').split('\n')
            for tag in r_tags:
                if f'__{spec}__' in str(tag):
                    tags.append(tag)

        except Exception:
            log.error('Invalid ml-git repository!', class_name=METADATA_MANAGER_CLASS_NAME)
        return tags

    def delete_tag(self, tag):
        """
        Method to delete a specific existent tag.
        Not implemented yet.
        """
        pass

    def _usrtag_exists(self, usrtag):
        repo = Repo(self.__path)
        sutag = usrtag._get()
        for tag in repo.tags:
            stag = str(tag)
            if sutag in stag:
                return True
        return False

    def _tag_exists(self, tag):
        tags = []
        repo = Repo(self.__path)
        if tag in repo.tags:
            tags.append(tag)
        model_tag = '__'.join(tag.split('__')[-3:])
        for r_tag in repo.tags:
            if model_tag == str(r_tag):
                tags.append(str(r_tag))
        return tags

    def __realname(self, path, root=None):
        if root is not None:
            path = os.path.join(root, path)
        result = os.path.basename(path)
        return result

    @staticmethod
    def get_metadata_path_and_prefix(metadata_path):
        prefix = 0
        if metadata_path != '/':
            if metadata_path.endswith('/'):
                metadata_path = metadata_path[:-1]
            prefix = len(metadata_path)
        return metadata_path, prefix

    def format_output_path(self, title, prefix, metadata_path):
        output = title + '\n'
        for root, dirs, files in os.walk(metadata_path):
            if root == metadata_path:
                continue
            if '.git' in root:
                continue

            level = root[prefix:].count(os.sep)
            indent = sub_indent = ''
            if level > 0:
                indent = '|   ' * (level - 1) + '|-- '
            sub_indent = '|   ' * (level) + '|-- '
            output += '{}{}\n'.format(indent, self.__realname(root))
            for d in dirs:
                if os.path.islink(os.path.join(root, d)):
                    output += '{}{}\n'.format(sub_indent, self.__realname(d, root=root))
        return output

    def list(self, title='ML Datasets'):
        metadata_path, prefix = self.get_metadata_path_and_prefix(self.__path)
        output = self.format_output_path(title, prefix, metadata_path)

        if output != (title + '\n'):
            print(output)
        else:
            log.error('You don\'t have any entity being managed.')

    @staticmethod
    def metadata_print(metadata_file, spec_name):
        md = yaml_load(metadata_file)

        sections = ['dataset', 'model', 'labels']
        for section in sections:
            if section in ['model', 'dataset', 'labels']:
                try:
                    md[section]  # 'hack' to ensure we don't print something useless
                    # 'dataset' not present in 'model' and vice versa
                    print('-- %s : %s --' % (section, spec_name))
                except Exception:
                    continue
            elif section not in ['model', 'dataset', 'labels']:
                print('-- %s --' % (section))
            try:
                print(get_yaml_str(md[section]))
            except Exception:
                continue

    def sha_from_tag(self, tag):
        try:
            r = Repo(self.__path)
            return r.git.rev_list(tag).split('\n', 1)[0]
        except Exception:
            return None

    def git_user_config(self):
        r = Repo(self.__path)
        reader = r.config_reader()
        config = {}
        types = ['email', 'name']
        for type in types:
            try:
                field = reader.get_value('user', type)
                config[type] = field
            except Exception:
                config[type] = None
        return config

    def metadata_spec_from_name(self, specname):
        specs = []
        for root, dirs, files in os.walk(self.__path):
            if '.git' in root:
                continue
            if specname in root:
                specs.append(os.path.join(root, specname + SPEC_EXTENSION))
        return specs

    def show(self, spec):
        specs = self.metadata_spec_from_name(spec)

        for specpath in specs:
            self.metadata_print(specpath, spec)

    def get(self, categories, model_name, file=None):
        if file is None:
            full_path = os.path.join(self.__path, os.sep.join(categories), model_name, model_name)
        else:
            full_path = os.path.join(self.__path, os.sep.join(categories), model_name, file)
        log.info('Metadata GET %s' % full_path, class_name=METADATA_MANAGER_CLASS_NAME)
        if os.path.exists(full_path):
            return yaml_load(full_path)
        return None

    def reset(self):
        repo = Repo(self.__path)
        # get current tag reference
        tag = self.get_current_tag()
        # reset
        try:
            repo.head.reset(HEAD_1, index=True, working_tree=True, paths=None)
        except GitError as g:
            if 'Failed to resolve \'HEAD~1\' as a valid revision.' in g.stderr:
                log.error('There is no commit to go back. Do at least two commits.',
                          class_name=METADATA_MANAGER_CLASS_NAME)
            raise g
        # delete the associated tag
        repo.delete_tag(tag)

    def get_metadata_manifest(self, path):
        if os.path.isfile(path):
            return Manifest(path)
        return None

    def remove_deleted_files_meta_manifest(self, manifest, deleted_files):
        if manifest is not None:
            for file in deleted_files:
                manifest.rm_file(file)
            manifest.save()

    def get_current_tag(self):
        repo = Repo(self.__path)
        tag = next((tag for tag in repo.tags if tag.commit == repo.head.commit), None)
        return tag

    def __sort_tag_by_date(self, elem):
        return elem.commit.authored_date

    def get_log_info(self, spec, fullstat=False):
        tags = self.list_tags(spec, True)
        formatted = ''
        if len(tags) == 0:
            raise RuntimeError('No log found for entity [%s]' % spec)

        tags.sort(key=self.__sort_tag_by_date)

        for tag in tags:
            formatted += '\n' + self.get_formatted_log_info(tag, fullstat)

        return formatted

    def get_formatted_log_info(self, tag, fullstat):
        commit = tag.commit
        info_format = '\n{}: {}'
        info = ''
        info += info_format.format(TAG, str(tag))
        info += info_format.format(AUTHOR, commit.author.name)
        info += info_format.format(EMAIL, commit.author.email)
        info += info_format.format(DATE, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(commit.authored_date)))
        info += info_format.format(MESSAGE, commit.message)

        if fullstat:
            added, deleted, size, amount = self.get_ref_diff(tag)
            if len(added) > 0:
                added_list = list(added)
                info += '\n\n{} [{}]:\n\t{}'.format(ADDED, len(added_list), '\n\t'.join(added_list))
            if len(deleted) > 0:
                deleted_list = list(deleted)
                info += '\n\n{} [{}]:\n\t{}'.format(DELETED, len(deleted_list), '\n\t'.join(deleted_list))
            if len(size) > 0:
                info += '\n\n{}: {}'.format(SIZE, '\n\t'.join(size))
            if len(amount) > 0:
                info += '\n\n{}: {}'.format(AMOUNT, '\n\t'.join(amount))

        return info

    def get_ref_diff(self, tag):
        repo = Repo(self.__path)
        commit = tag.commit
        parents = tag.commit.parents
        added_files = []
        deleted_files = []
        size_files = []
        amount_files = []
        if len(parents) > 0:
            diff = repo.git.diff(str(parents[0]), str(commit))
            added_files = re.findall(RGX_ADDED_FILES, diff)
            deleted_files = re.findall(RGX_DELETED_FILES, diff)
            size_files = re.findall(RGX_SIZE_FILES, diff)
            amount_files = re.findall(RGX_AMOUNT_FILES, diff)

        return added_files, deleted_files, size_files, amount_files

    def validate_blank_remote_url(self):
        blank_url = ''
        repo = Repo(self.__path)
        for url in repo.remote().urls:
            if url == blank_url:
                git_error = GitError()
                git_error.stderr = output_messages['ERROR_REMOTE_NOT_FOUND']
                raise git_error

    def delete_git_reference(self):
        try:
            self.remote_set_url('')
        except GitError as e:
            log.error(e.stderr, class_name=METADATA_MANAGER_CLASS_NAME)
            return False
        return True


class MetadataManager(MetadataRepo):
    def __init__(self, config, type='model'):
        self.path = get_metadata_path(config, type)
        self.git = config[type]['git']

        super(MetadataManager, self).__init__(self.git, self.path)


class MetadataObject(object):
    def __init__(self):
        pass
