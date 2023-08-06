"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""
import errno
import os
import re
import shutil

import humanize
from git import InvalidGitRepositoryError, GitError
from halo import Halo

from ml_git import log
from ml_git.admin import remote_add, storage_add, clone_config_repository, init_mlgit, remote_del
from ml_git.config import get_index_path, get_objects_path, get_cache_path, get_metadata_path, get_refs_path, \
    validate_config_spec_hash, validate_spec_hash, get_sample_config_spec, get_sample_spec_doc, \
    get_index_metadata_path, create_workspace_tree_structure, start_wizard_questions, config_load, \
    get_global_config_path, save_global_config_in_local
from ml_git.constants import REPOSITORY_CLASS_NAME, LOCAL_REPOSITORY_CLASS_NAME, HEAD, HEAD_1, MutabilityType, \
    StorageType, \
    RGX_TAG_FORMAT, EntityType, MANIFEST_FILE, SPEC_EXTENSION, MANIFEST_KEY, STATUS_NEW_FILE, STATUS_DELETED_FILE, \
    FileType, STORAGE_CONFIG_KEY
from ml_git.file_system.cache import Cache
from ml_git.file_system.hashfs import MultihashFS
from ml_git.file_system.index import MultihashIndex, Status, FullIndex
from ml_git.file_system.local import LocalRepository
from ml_git.file_system.objects import Objects
from ml_git.manifest import Manifest
from ml_git.metadata import Metadata, MetadataManager
from ml_git.ml_git_message import output_messages
from ml_git.plugin_interface.data_plugin_constants import COMPARE_SPECS, GET_STATUS_OUTPUT
from ml_git.plugin_interface.plugin_especialization import PluginCaller
from ml_git.refs import Refs
from ml_git.spec import spec_parse, search_spec_file, increment_version_in_spec, get_entity_tag, update_storage_spec, \
    validate_bucket_name, set_version_in_spec, get_entity_dir, SearchSpecException, get_spec_key
from ml_git.tag import UsrTag
from ml_git.utils import yaml_load, ensure_path_exists, get_root_path, \
    RootPathException, change_mask_for_routine, clear, get_yaml_str, unzip_files_in_directory, \
    remove_from_workspace, disable_exception_traceback, group_files_by_path


class Repository(object):
    def __init__(self, config, repo_type=EntityType.DATASETS):

        self._validate_entity_type(repo_type)
        self.__config = config
        self.__repo_type = repo_type

    '''initializes ml-git repository metadata'''

    def init(self):
        try:
            metadata_path = get_metadata_path(self.__config)
            m = Metadata('', metadata_path, self.__config, self.__repo_type)
            m.init()
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

    def repo_remote_add(self, repo_type, mlgit_remote, global_conf=False):
        try:
            remote_add(repo_type, mlgit_remote, global_conf)
            self.__config = config_load()
            metadata_path = get_metadata_path(self.__config)
            m = Metadata('', metadata_path, self.__config, self.__repo_type)
            m.remote_set_url(mlgit_remote)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

    def repo_remote_del(self, global_conf=False):
        try:
            metadata_path = get_metadata_path(self.__config)
            metadata = Metadata('', metadata_path, self.__config, self.__repo_type)
            if metadata.delete_git_reference():
                remote_del(self.__repo_type, global_conf)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

    '''Add dir/files to the ml-git index'''

    def add(self, spec, file_path, bump_version=False, run_fsck=False, metrics='', metrics_file_path=''):
        repo_type = self.__repo_type
        is_shared_objects = 'objects_path' in self.__config[repo_type]
        is_shared_cache = 'cache_path' in self.__config[repo_type]

        if not validate_config_spec_hash(self.__config):
            log.error(output_messages['ERROR_INVALID_YAML_CONFIG']
                      % get_yaml_str(get_sample_config_spec('somebucket', 'someprofile', 'someregion')),
                      class_name=REPOSITORY_CLASS_NAME)
            return None

        path, file = None, None
        try:

            refs_path = get_refs_path(self.__config, repo_type)
            index_path = get_index_path(self.__config, repo_type)
            metadata_path = get_metadata_path(self.__config, repo_type)
            cache_path = get_cache_path(self.__config, repo_type)
            objects_path = get_objects_path(self.__config, repo_type)
            repo = LocalRepository(self.__config, objects_path, repo_type)
            mutability, check_mutability = repo.get_mutability_from_spec(spec, repo_type)
            sampling_flag = os.path.exists(os.path.join(index_path, 'metadata', spec, 'sampling'))
            if sampling_flag:
                log.error(output_messages['INFO_CANNOT_ADD_NEW_DATA_AN_ENTITY'],
                          class_name=REPOSITORY_CLASS_NAME)
                return
            if not mutability:
                return
            if not check_mutability:
                log.error(output_messages['ERROR_MUTABILITY_CANNOT_CHANGE'], class_name=REPOSITORY_CLASS_NAME)
                return
            if not self._has_new_data(repo, spec):
                return None
            ref = Refs(refs_path, spec, repo_type)
            tag, sha = ref.branch()
            path, file = search_spec_file(self.__repo_type, spec)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

        if path is None:
            return
        spec_path = os.path.join(path, file)
        if not self._is_spec_valid(spec_path):
            return None
        try:
            repo.add_metrics(spec_path, metrics, metrics_file_path)
        except FileNotFoundError as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

        # Check tag before anything to avoid creating unstable state
        log.debug(output_messages['DEBUG_TAG_CHECK'], class_name=REPOSITORY_CLASS_NAME)

        m = Metadata(spec, metadata_path, self.__config, repo_type)

        if not m.check_exists():
            log.error(output_messages['ERROR_NOT_INITIALIZED'] % self.__repo_type, class_name=REPOSITORY_CLASS_NAME)
            return

        try:
            m.update()
        except Exception:
            pass

        # get version of current manifest file
        manifest = self._get_current_manifest_file(m, tag)

        try:
            # adds chunks to ml-git Index
            log.info(output_messages['INFO_ADDING_PATH_TO'] % (repo_type, path), class_name=REPOSITORY_CLASS_NAME)
            with change_mask_for_routine(is_shared_objects):
                idx = MultihashIndex(spec, index_path, objects_path, mutability, cache_path)
                idx.add(path, manifest, file_path)

            # create hard links in ml-git Cache
            self.create_hard_links_in_cache(cache_path, index_path, is_shared_cache, mutability, path, spec)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return None

        if bump_version and not increment_version_in_spec(spec_path, self.__repo_type):
            return None

        idx.add_metadata(path, file)

        self._check_corrupted_files(spec, repo)

        # Run file check
        if run_fsck:
            self.fsck()

    def _validate_entity_type(self, repo_type):
        another_valid_types = ['repository', 'project']
        type_list = EntityType.to_list() + another_valid_types

        if repo_type not in type_list:
            with disable_exception_traceback():
                raise RuntimeError(output_messages['ERROR_INVALID_ENTITY_TYPE'] % EntityType.to_list())

    def _get_current_manifest_file(self, m, tag):
        manifest = ''
        if tag is not None:
            m.checkout(tag)
            md_metadata_path = m.get_metadata_path(tag)
            manifest = os.path.join(md_metadata_path, MANIFEST_FILE)
            m.checkout()
        return manifest

    def _is_spec_valid(self, spec_path):
        spec_file = yaml_load(spec_path)
        entity_spec_key = get_spec_key(self.__repo_type)
        if not validate_spec_hash(spec_file, entity_spec_key):
            log.error(output_messages['ERROR_INVALID_SPEC_VALUE_IN'] %
                      (self.__repo_type, spec_path, get_sample_spec_doc('somebucket', entity_spec_key)),
                      class_name=REPOSITORY_CLASS_NAME)
            return False
        if not validate_bucket_name(spec_file[entity_spec_key], self.__config):
            return False
        return True

    def _has_new_data(self, repo, spec):
        _, deleted, untracked_files, _, changed_files = repo.status(spec, status_directory='', log_errors=False)
        if deleted is None and untracked_files is None and changed_files is None:
            return False
        elif len(deleted) == 0 and len(untracked_files) == 0 and len(changed_files) == 0:
            log.info(output_messages['INFO_NO_NEW_DATA_TO_ADD'], class_name=REPOSITORY_CLASS_NAME)
            return False
        return True

    @Halo(text='Creating hard links in cache', spinner='dots')
    def create_hard_links_in_cache(self, cache_path, index_path, is_shared_cache, mutability, path, spec):
        mf = os.path.join(index_path, 'metadata', spec, MANIFEST_FILE)
        with change_mask_for_routine(is_shared_cache):
            if mutability in [MutabilityType.STRICT.value, MutabilityType.FLEXIBLE.value]:
                cache = Cache(cache_path, path, mf)
                cache.update()

    def _check_corrupted_files(self, spec, repo):
        try:
            corrupted_files = repo.get_corrupted_files(spec)
            if corrupted_files is not None and len(corrupted_files) > 0:
                print('\n')
                log.warn(output_messages['WARN_CORRUPTED_CANNOT_BE_ADD'],
                         class_name=REPOSITORY_CLASS_NAME)
                for file in corrupted_files:
                    print('\t %s' % file)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

    def branch(self, spec):
        try:
            repo_type = self.__repo_type
            refs_path = get_refs_path(self.__config, repo_type)
            r = Refs(refs_path, spec, repo_type)
            print(r.branch())
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

    '''prints status of changes in the index and changes not yet tracked or staged'''

    def __load_plugin_caller(self, path, spec):
        spec_content = yaml_load(os.path.join(path, spec))
        entity_spec_key = get_spec_key(self.__repo_type)
        return PluginCaller(spec_content[entity_spec_key][MANIFEST_KEY])

    def status(self, spec, full_option, status_directory):
        repo_type = self.__repo_type
        try:
            objects_path = get_objects_path(self.__config, repo_type)
            repo = LocalRepository(self.__config, objects_path, repo_type)
            path, spec_file = search_spec_file(self.__repo_type, spec)
            plugin_caller = self.__load_plugin_caller(path, spec_file)
            log.info(output_messages['INFO_STATUS_OF'] % (repo_type, spec), class_name=REPOSITORY_CLASS_NAME)
            new_files, deleted_files, untracked_files, corruped_files, changed_files = repo.status(spec, status_directory)
            specialized_plugin_data = plugin_caller.call(GET_STATUS_OUTPUT, path, untracked_files, new_files, full_option)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

        untracked_specialized, new_files_specialized, total_registry = None, None, None
        if specialized_plugin_data:
            untracked_specialized, new_files_specialized, total_registry = specialized_plugin_data

        if new_files is not None and deleted_files is not None and untracked_files is not None:
            print('Changes to be committed:')

            if new_files_specialized:
                self._print_files(new_files_specialized, True, STATUS_NEW_FILE)
            else:
                self._print_files(new_files, full_option, STATUS_NEW_FILE)

            self._print_files(deleted_files, full_option, STATUS_DELETED_FILE)

            if total_registry:
                print(total_registry)

            print('\nUntracked files:')
            if untracked_specialized:
                self._print_files(untracked_specialized, True)
            else:
                self._print_files(untracked_files, full_option)

            print('\nCorrupted files:')
            self._print_files(corruped_files, full_option)

            if changed_files and len(changed_files) > 0:
                print('\nChanges not staged for commit:')
                self._print_files(changed_files, full_option)

    @staticmethod
    def _print_full_option(files, files_status=''):
        for file in files:
            print('\t%s%s' % (files_status, file))

    @staticmethod
    def _print_short(files, files_status):
        one_file = 1

        for base_path, path_files in files.items():
            if not base_path:
                print('\t%s%s' % (files_status, '\n\t'.join(path_files)))
            elif len(path_files) == one_file:
                print('\t%s%s' % (files_status, os.path.join(base_path, ''.join(path_files))))
            else:
                print('\t%s%s\t->\t%d FILES' % (files_status, base_path + '/', len(path_files)))

    def _print_files(self, files, full_option, files_status=''):

        print_method = self._print_full_option

        if not full_option:
            files = group_files_by_path(files)
            print_method = self._print_short

        print_method(files, files_status)

    @Halo(text='Checking removed files', spinner='dots')
    def _remove_deleted_files(self, idx, index_path, m, manifest, spec, deleted_files):
        fidx = FullIndex(spec, index_path)
        fidx.remove_deleted_files(deleted_files)
        idx.remove_deleted_files_index_manifest(deleted_files)
        m.remove_deleted_files_meta_manifest(manifest, deleted_files)

    def _update_metadata_directory(self, metadata, spec, ws_entity_dir, metadata_path):
        try:
            metadata_entity_dir = get_entity_dir(self.__repo_type, spec, root_path=metadata_path)
            if ws_entity_dir != metadata_entity_dir:
                metadata.move_metadata_dir(metadata_entity_dir, ws_entity_dir)
        except SearchSpecException:
            return

    '''commit changes present in the ml-git index to the ml-git repository'''
    def commit(self, spec, specs, version=None, run_fsck=False, msg=None):
        # Move chunks from index to .ml-git/objects
        repo_type = self.__repo_type
        try:
            index_path = get_index_path(self.__config, repo_type)
            objects_path = get_objects_path(self.__config, repo_type)
            metadata_path = get_metadata_path(self.__config, repo_type)
            refs_path = get_refs_path(self.__config, repo_type)
            repo = LocalRepository(self.__config, objects_path, repo_type)
            mutability, check_mutability = repo.get_mutability_from_spec(spec, repo_type)

            if not mutability:
                return

            if not check_mutability:
                log.error(output_messages['ERROR_MUTABILITY_CANNOT_CHANGE'], class_name=REPOSITORY_CLASS_NAME)
                return
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

        ref = Refs(refs_path, spec, repo_type)
        spec_path, spec_file = search_spec_file(repo_type, spec)
        entity_dir = os.path.relpath(spec_path, os.path.join(get_root_path(), repo_type))

        path, file = None, None
        try:
            path, file = search_spec_file(self.__repo_type, spec)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)

        if path is None:
            return None, None, None

        spec_path = os.path.join(path, file)
        idx = MultihashIndex(spec, index_path, objects_path)

        if version:
            set_version_in_spec(version, spec_path, self.__repo_type)
            idx.add_metadata(path, file)

        # Check tag before anything to avoid creating unstable state
        log.debug(output_messages['DEBUG_TAG_CHECK'], class_name=REPOSITORY_CLASS_NAME)
        m = Metadata(spec, metadata_path, self.__config, repo_type)

        if not m.check_exists():
            log.error(output_messages['ERROR_NOT_INITIALIZED'] % self.__repo_type, class_name=REPOSITORY_CLASS_NAME)
            return

        full_metadata_path, entity_sub_path, metadata = m.tag_exists(index_path)
        if metadata is None:
            return None

        log.debug(output_messages['DEBUG_MESSAGE_VALUE'] % (index_path, objects_path), class_name=REPOSITORY_CLASS_NAME)
        # commit objects in index to ml-git objects
        o = Objects(spec, objects_path)
        changed_files, deleted_files = o.commit_index(index_path, path)

        bare_mode = os.path.exists(os.path.join(index_path, 'metadata', spec, 'bare'))

        if not bare_mode:
            self._update_metadata_directory(m, spec, entity_dir, metadata_path)
            manifest_path = os.path.join(metadata_path, os.path.dirname(entity_dir), spec, MANIFEST_FILE)
            manifest = m.get_metadata_manifest(manifest_path)
            self._remove_deleted_files(idx, index_path, m, manifest, spec, deleted_files)
            m.remove_files_added_after_base_tag(manifest, path)
        else:
            tag, _ = ref.branch()
            self._checkout_ref(tag)
        # update metadata spec & README.md
        # option --dataset-spec --labels-spec
        tag, sha = m.commit_metadata(index_path, specs, msg, changed_files, mutability, path)

        # update ml-git ref spec HEAD == to new SHA-1 / tag
        if tag is None:
            return None
        ref = Refs(refs_path, spec, repo_type)
        ref.update_head(tag, sha)

        # Run file check
        if run_fsck:
            self.fsck()

        return tag

    def list(self):
        repo_type = self.__repo_type
        try:
            metadata_path = get_metadata_path(self.__config, repo_type)
            m = Metadata('', metadata_path, self.__config, repo_type)
            if not m.check_exists():
                raise RuntimeError(output_messages['INFO_NOT_INITIALIZED'] % self.__repo_type)
            m.checkout()
            m.list(title='ML ' + repo_type)
        except GitError as g:
            error_message = g.stderr
            if 'did not match any file(s) known' in error_message:
                error_message = 'You don\'t have any entity being managed.'
            log.error(error_message, class_name=REPOSITORY_CLASS_NAME)
            return
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

    def tag(self, spec, usr_tag):
        repo_type = self.__repo_type
        try:
            metadata_path = get_metadata_path(self.__config, repo_type)
            refs_path = get_refs_path(self.__config, repo_type)
            r = Refs(refs_path, spec, repo_type)
            curtag, sha = r.head()
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return False

        if curtag is None:
            log.error(output_messages['ERROR_NO_CURRENT_TAG_FOR'] % spec, class_name=REPOSITORY_CLASS_NAME)
            return False
        utag = UsrTag(curtag, usr_tag)

        # Check if usrtag exists before creating it
        log.debug(output_messages['DEBUG_TAG_CHECK_FOR'] % utag, class_name=REPOSITORY_CLASS_NAME)
        m = Metadata(spec, metadata_path, self.__config, repo_type)
        if m._usrtag_exists(utag) is True:
            log.error(output_messages['ERROR_TAG_ALREADY_EXISTS'] % utag, class_name=REPOSITORY_CLASS_NAME)
            return False

        # ensure metadata repository is at the current tag/sha version
        m = Metadata('', metadata_path, self.__config, repo_type)
        m.checkout(curtag)

        # TODO: format to something that could be used for a checkout:
        # format: _._user_.._ + curtag + _.._ + usrtag
        # at checkout with usrtag look for pattern _._ then find usrtag in the list (split on '_.._')
        # adds usrtag to the metadata repository

        m = Metadata(spec, metadata_path, self.__config, repo_type)
        try:
            m.tag_add(utag)
        except Exception as e:

            match = re.search("stderr: 'fatal:(.*)'$", e.stderr)
            err = match.group(1)
            log.error(err, class_name=REPOSITORY_CLASS_NAME)
            return
        log.info(output_messages['INFO_CREATE_TAG_SUCCESS'], class_name=REPOSITORY_CLASS_NAME)
        # checkout at metadata repository at master version
        m.checkout()
        return True

    def list_tag(self, spec):
        repo_type = self.__repo_type
        try:
            metadata_path = get_metadata_path(self.__config, repo_type)
            m = Metadata(spec, metadata_path, self.__config, repo_type)
            for tag in m.list_tags(spec):
                print(tag)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

    '''push all data related to a ml-git repository to the LocalRepository git repository and data storage'''

    def push(self, spec, retry=2, clear_on_fail=False):
        repo_type = self.__repo_type
        try:
            objects_path = get_objects_path(self.__config, repo_type)
            metadata_path = get_metadata_path(self.__config, repo_type)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

        met = Metadata(spec, metadata_path, self.__config, repo_type)
        fields = met.git_user_config()
        if None in fields.values():
            log.error(output_messages['ERROR_NAME_EMAIL_CONFIGURATION'], class_name=REPOSITORY_CLASS_NAME)

            log.error(output_messages['ERROR_USERNAME_CONFIG'], class_name=REPOSITORY_CLASS_NAME)
            log.error(output_messages['ERROR_USEREMAIL_CONFIG'], class_name=REPOSITORY_CLASS_NAME)
            return
        if met.fetch() is False:
            return

        spec_path, spec_file = None, None
        try:
            spec_path, spec_file = search_spec_file(self.__repo_type, spec)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)

        if spec_path is None:
            return

        full_spec_path = os.path.join(spec_path, spec_file)

        repo = LocalRepository(self.__config, objects_path, repo_type)
        ret = repo.push(objects_path, full_spec_path, retry, clear_on_fail)

        # ensure first we're on master !
        met.checkout()
        if ret == 0:
            # push metadata spec to LocalRepository git repository
            try:
                met.push()
            except Exception as e:
                log.error(e, class_name=REPOSITORY_CLASS_NAME)
                return
            MultihashFS(objects_path).reset_log()

    '''Retrieves only the metadata related to a ml-git repository'''

    def update(self):
        repo_type = self.__repo_type
        try:
            metadata_path = get_metadata_path(self.__config, repo_type)
            m = Metadata('', metadata_path, self.__config, repo_type)
            m.update()
        except GitError as error:
            log.error(output_messages['ERROR_METADATA_COULD_NOT_UPDATED'] % error.stderr, class_name=REPOSITORY_CLASS_NAME)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)

    '''Retrieve only the data related to a specific ML entity version'''

    def _fetch(self, tag, samples, retries=2, bare=False):
        repo_type = self.__repo_type
        try:
            objects_path = get_objects_path(self.__config, repo_type)
            metadata_path = get_metadata_path(self.__config, repo_type)
            # check if no data left untracked/uncommitted. othrewise, stop.
            local_rep = LocalRepository(self.__config, objects_path, repo_type)
            return local_rep.fetch(metadata_path, tag, samples, retries, bare)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

    def fetch_tag(self, tag, samples, retries=2):
        repo_type = self.__repo_type
        try:
            objects_path = get_objects_path(self.__config, repo_type)
            metadata_path = get_metadata_path(self.__config, repo_type)
            m = Metadata('', metadata_path, self.__config, repo_type)
            m.checkout(tag)

            fetch_success = self._fetch(tag, samples, retries)

            if not fetch_success:
                objs = Objects('', objects_path)
                objs.fsck(remove_corrupted=True)
                m.checkout()
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

        # restore to master/head
        self._checkout_ref()

    def _checkout_ref(self, ref=None):
        repo_type = self.__repo_type
        metadata_path = get_metadata_path(self.__config, repo_type)
        m = Metadata('', metadata_path, self.__config, repo_type)

        if ref is None:
            ref = m.get_default_branch()

        m.checkout(ref, force=True)

    '''Performs fsck on several aspects of ml-git filesystem.
        TODO: add options like following:
        * detect:
            ** fast: performs checks on all blobs present in index / objects
            ** thorough: perform check on files within cache
        * fix:
            ** download again corrupted blob
            ** rebuild cache'''

    def fsck(self):
        repo_type = self.__repo_type
        try:
            objects_path = get_objects_path(self.__config, repo_type)
            index_path = get_index_path(self.__config, repo_type)
        except RootPathException:
            return
        o = Objects('', objects_path)
        corrupted_files_obj = o.fsck()
        corrupted_files_obj_len = len(corrupted_files_obj)

        idx = MultihashIndex('', index_path, objects_path)
        corrupted_files_idx = idx.fsck()
        corrupted_files_idx_len = len(corrupted_files_idx)

        print('[%d] corrupted file(s) in Local Repository: %s' % (corrupted_files_obj_len, corrupted_files_obj))
        print('[%d] corrupted file(s) in Index: %s' % (corrupted_files_idx_len, corrupted_files_idx))
        print('Total of corrupted files: %d' % (corrupted_files_obj_len + corrupted_files_idx_len))

    def show(self, spec):
        repo_type = self.__repo_type
        try:
            metadata_path = get_metadata_path(self.__config, repo_type)
            refs_path = get_refs_path(self.__config, repo_type)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return
        r = Refs(refs_path, spec, repo_type)
        tag, sha = r.head()
        if tag is None:
            log.info(output_messages['INFO_NO_HEAD_FOR'] % spec, class_name=LOCAL_REPOSITORY_CLASS_NAME)
            return

        m = Metadata('', metadata_path, self.__config, repo_type)

        m.checkout(tag)

        m.show(spec)

        m.checkout()

    def _tag_exists(self, tag):
        md = MetadataManager(self.__config, self.__repo_type)
        # check if tag already exists in the ml-git repository
        tags = md._tag_exists(tag)
        if len(tags) == 0:
            log.error(output_messages['ERROR_TAG_NOT_EXISTS_REPOSITORY'] % tag, class_name=LOCAL_REPOSITORY_CLASS_NAME)
            return False
        return True

    def _initialize_repository_on_the_fly(self):
        if os.path.exists(get_global_config_path()):
            log.info(output_messages['INFO_INITIALIZING_PROJECT'], class_name=REPOSITORY_CLASS_NAME)
            init_mlgit()
            save_global_config_in_local()
            metadata_path = get_metadata_path(self.__config)
            if not os.path.exists(metadata_path):
                Metadata('', metadata_path, self.__config, self.__repo_type).init()
            return metadata_path
        raise RootPathException(output_messages['INFO_ARE_NOT_IN_INITIALIZED_PROJECT'])

    def checkout(self, tag, samples, options):
        try:
            metadata_path = get_metadata_path(self.__config)
        except RootPathException as e:
            log.warn(e, class_name=REPOSITORY_CLASS_NAME)
            metadata_path = self._initialize_repository_on_the_fly()
        dt_tag, lb_tag = self._checkout(tag, samples, options)
        options['with_dataset'] = False
        options['with_labels'] = False
        if dt_tag is not None:
            try:
                self.__repo_type = EntityType.DATASETS.value
                m = Metadata('', metadata_path, self.__config, self.__repo_type)
                log.info(output_messages['INFO_INITIALIZING_ENTITY_DOWNLOAD'] % self.__repo_type, class_name=REPOSITORY_CLASS_NAME)
                if not m.check_exists():
                    m.init()
                self._checkout(dt_tag, samples, options)
            except Exception as e:
                log.error(output_messages['ERROR_LOCALREPOSITORY_MESSAGE'] % e, class_name=REPOSITORY_CLASS_NAME)
        if lb_tag is not None:
            try:
                self.__repo_type = EntityType.LABELS.value
                m = Metadata('', metadata_path, self.__config, self.__repo_type)
                log.info(output_messages['INFO_INITIALIZING_ENTITY_DOWNLOAD'] % self.__repo_type, class_name=REPOSITORY_CLASS_NAME)
                if not m.check_exists():
                    m.init()
                self._checkout(lb_tag, samples, options)
            except Exception as e:
                log.error(output_messages['ERROR_LOCALREPOSITORY_MESSAGE'] % e, class_name=REPOSITORY_CLASS_NAME)

    '''Performs a fsck on remote storage w.r.t. some specific ML artefact version'''

    def remote_fsck(self, spec, retries=2, thorough=False, paranoid=False):
        repo_type = self.__repo_type
        try:
            metadata_path = get_metadata_path(self.__config, repo_type)
            objects_path = get_objects_path(self.__config, repo_type)
            refs_path = get_refs_path(self.__config, repo_type)
            ref = Refs(refs_path, spec, repo_type)
            tag, sha = ref.branch()
            self._checkout_ref(tag)
            spec_path, spec_file = search_spec_file(self.__repo_type, spec)

        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return
        if spec_path is None:
            return

        full_spec_path = os.path.join(spec_path, spec_file)

        r = LocalRepository(self.__config, objects_path, repo_type)

        r.remote_fsck(metadata_path, tag, full_spec_path, retries, thorough, paranoid)

        # ensure first we're on master !
        self._checkout_ref()

    def _update_entity_ws_path(self, spec, metadata_entity_dir, root_path):
        ws_path = os.path.join(root_path, self.__repo_type, metadata_entity_dir)
        try:
            ws_entity_dir = get_entity_dir(self.__repo_type, spec)
            if ws_entity_dir != metadata_entity_dir:
                old_entity_path = os.path.join(get_root_path(), self.__repo_type, ws_entity_dir)
                entity_path = os.path.join(get_root_path(), self.__repo_type, os.path.dirname(metadata_entity_dir))
                ensure_path_exists(entity_path)
                shutil.move(old_entity_path, entity_path)
                if not os.listdir(os.path.dirname(old_entity_path)):
                    clear(os.path.dirname(old_entity_path))
                ws_path = os.path.join(entity_path, spec)
        except (RootPathException, SearchSpecException):
            pass
        return ws_path

    '''Download data from a specific ML entity version into the workspace'''
    def _checkout(self, tag, samples, options):
        dataset = options['with_dataset']
        labels = options['with_labels']
        retries = options['retry']
        force_get = options['force']
        bare = options['bare']
        version = options['version']
        repo_type = self.__repo_type
        try:
            cache_path = get_cache_path(self.__config, repo_type)
            metadata_path = get_metadata_path(self.__config, repo_type)
            objects_path = get_objects_path(self.__config, repo_type)
            refs_path = get_refs_path(self.__config, repo_type)

            if not re.search(RGX_TAG_FORMAT, tag):
                metadata_path = get_metadata_path(self.__config, repo_type)
                metadata = Metadata(tag, metadata_path, self.__config, repo_type)
                tag = metadata.get_tag(tag, version)
                if not tag:
                    return None, None
            elif not self._tag_exists(tag):
                return None, None
            _, spec_name, _ = spec_parse(tag)
            root_path = get_root_path()
        except Exception as e:
            log.error(e, class_name=LOCAL_REPOSITORY_CLASS_NAME)
            return None, None

        ref = Refs(refs_path, spec_name, repo_type)
        cur_tag, _ = ref.branch()

        if cur_tag == tag:
            log.info(output_messages['INFO_ALREADY_TAG'] % tag, class_name=REPOSITORY_CLASS_NAME)
            return None, None

        local_rep = LocalRepository(self.__config, objects_path, repo_type)
        # check if no data left untracked/uncommitted. otherwise, stop.
        if not force_get and local_rep.exist_local_changes(spec_name) is True:
            return None, None

        try:
            self._checkout_ref(tag)
        except Exception:
            log.error(output_messages['ERROR_UNABLE_CHECKOUT'] % tag, class_name=REPOSITORY_CLASS_NAME)
            return None, None

        entity_dir = get_entity_dir(repo_type, spec_name, root_path=metadata_path)

        dataset_tag, labels_tag = self._get_related_tags(entity_dir, dataset, labels, metadata_path, repo_type, spec_name)
        fetch_success = self._fetch(tag, samples, retries, bare)
        if not fetch_success:
            objs = Objects('', objects_path)
            objs.fsck(remove_corrupted=True)
            self._checkout_ref()
            return None, None

        ws_path = self._update_entity_ws_path(spec_name, entity_dir, root_path)
        ensure_path_exists(ws_path)
        try:
            spec_index_path = os.path.join(get_index_metadata_path(self.__config, repo_type), spec_name)
        except Exception:
            return
        self._delete_spec_and_readme(spec_index_path, spec_name)

        try:
            r = LocalRepository(self.__config, objects_path, repo_type)
            r.checkout(cache_path, metadata_path, ws_path, tag, samples, bare, entity_dir)
        except OSError as e:
            self._checkout_ref()
            if e.errno == errno.ENOSPC:
                log.error(output_messages['ERROR_NOT_DISK_SPACE'],
                          class_name=REPOSITORY_CLASS_NAME)
            else:
                log.error(output_messages['ERROR_WHILE_CREATING_FILES'] % e,
                          class_name=REPOSITORY_CLASS_NAME)
                return None, None
        except Exception as e:
            self._checkout_ref()
            log.error(output_messages['ERROR_WHILE_CREATING_FILES'] % e,
                      class_name=REPOSITORY_CLASS_NAME)
            return None, None

        m = Metadata('', metadata_path, self.__config, repo_type)
        sha = m.sha_from_tag(tag)
        ref.update_head(tag, sha)

        # restore to master/head
        self._checkout_ref()
        return dataset_tag, labels_tag

    def _delete_spec_and_readme(self, spec_index_path, spec_name):
        if os.path.exists(spec_index_path):
            if os.path.exists(os.path.join(spec_index_path, spec_name + SPEC_EXTENSION)):
                os.unlink(os.path.join(spec_index_path, spec_name + SPEC_EXTENSION))
            if os.path.exists(os.path.join(spec_index_path, 'README.md')):
                os.unlink(os.path.join(spec_index_path, 'README.md'))

    def _get_related_tags(self, entity_dir, dataset, labels, metadata_path, repo_type, spec_name):
        dataset_tag, labels_tag = None, None
        spec_path = os.path.join(metadata_path, entity_dir, spec_name + '.spec')
        if dataset is True:
            dataset_tag = get_entity_tag(spec_path, repo_type, EntityType.DATASETS.value)
        if labels is True:
            labels_tag = get_entity_tag(spec_path, repo_type, EntityType.LABELS.value)
        return dataset_tag, labels_tag

    def reset(self, spec, reset_type, head):
        log.info(output_messages['INFO_INITIALIZING_RESET'] % (reset_type, head), class_name=REPOSITORY_CLASS_NAME)
        if (reset_type == '--soft' or reset_type == '--mixed') and head == HEAD:
            return
        try:
            repo_type = self.__repo_type
            metadata_path = get_metadata_path(self.__config, repo_type)
            index_path = get_index_path(self.__config, repo_type)
            refs_path = get_refs_path(self.__config, repo_type)
            object_path = get_objects_path(self.__config, repo_type)
            met = Metadata(spec, metadata_path, self.__config, repo_type)
            ref = Refs(refs_path, spec, repo_type)
            idx = MultihashIndex(spec, index_path, object_path)
            fidx = FullIndex(spec, index_path)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

        # current manifest file before reset
        entity_dir = get_entity_dir(repo_type, spec, root_path=metadata_path)
        manifest_path = os.path.join(metadata_path, entity_dir, MANIFEST_FILE)

        _manifest = Manifest(manifest_path).load()

        if head == HEAD_1:  # HEAD~1
            try:
                # reset the repo
                met.reset()
            except Exception:
                return

        # get tag after reset
        tag_after_reset = met.get_current_tag()
        sha = met.sha_from_tag(tag_after_reset)

        # update ml-git ref HEAD
        ref.update_head(str(tag_after_reset), sha)

        # # get path to reset workspace in case of --hard
        path, file = None, None
        try:
            path, file = search_spec_file(self.__repo_type, spec)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)

        if reset_type == '--hard' and path is None:
            return

        # get manifest from metadata after reset
        _manifest_changed = Manifest(manifest_path)

        hash_files, file_names = _manifest_changed.get_diff(_manifest)
        idx_mf = idx.get_index().load()

        if reset_type == '--soft':
            # add in index/metadata/<entity-name>/MANIFEST
            idx.update_index_manifest(idx_mf)
            idx.update_index_manifest(hash_files)
            fidx.update_index_status(file_names, Status.a.name)

        else:  # --hard or --mixed
            # remove hash from index/hashsh/storage.log
            file_names.update(*idx_mf.values())
            objs = MultihashFS(index_path)
            for key_hash in hash_files:
                objs.remove_hash(key_hash)
            idx.remove_manifest()
            fidx.remove_from_index_yaml(file_names)
            fidx.remove_uncommitted()

        if reset_type == '--hard':  # reset workspace
            remove_from_workspace(file_names, path, spec)
            md_entity_dir = get_entity_dir(repo_type, spec, root_path=metadata_path)
            self._update_entity_ws_path(spec, md_entity_dir, get_root_path())

    def import_files(self, object, path, directory, retry, bucket):
        err_msg = 'Invalid ml-git project!'

        try:
            root = get_root_path()
            root_dir = os.path.join(root, directory)
        except Exception:
            log.error(err_msg, class_name=REPOSITORY_CLASS_NAME)
            return

        local = LocalRepository(self.__config, get_objects_path(self.__config, self.__repo_type), self.__repo_type)
        bucket_name = bucket['bucket_name']
        storage_type = bucket['storage_type']
        local.change_config_storage(bucket['profile'], bucket_name, storage_type, region=bucket['region'], endpoint_url=bucket['endpoint_url'])
        local.import_files(object, path, root_dir, retry, '{}://{}'.format(storage_type, bucket_name))

    def unlock_file(self, spec, file_path):
        repo_type = self.__repo_type

        if not validate_config_spec_hash(self.__config):
            log.error(output_messages['ERROR_INVALID_YAML_CONFIG']
                      % get_yaml_str(get_sample_config_spec('somebucket', 'someprofile', 'someregion')),
                      class_name=REPOSITORY_CLASS_NAME)
            return None

        path, file = None, None
        try:
            objects_path = get_objects_path(self.__config, repo_type)
            index_path = get_index_path(self.__config, repo_type)
            cache_path = get_cache_path(self.__config, repo_type)
            path, file = search_spec_file(self.__repo_type, spec)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

        if path is None:
            return

        spec_path = os.path.join(path, file)
        spec_file = yaml_load(spec_path)

        try:
            entity_spec_key = get_spec_key(repo_type)
            mutability = spec_file[entity_spec_key]['mutability']
            if mutability not in MutabilityType.to_list():
                log.error(output_messages['ERROR_INVALID_MUTABILITY_TYPE'], class_name=REPOSITORY_CLASS_NAME)
                return
        except Exception:
            log.info(output_messages['INFO_SPEC_NOT_HAVE_MUTABILITY'],
                     class_name=REPOSITORY_CLASS_NAME)
            return

        if mutability != MutabilityType.STRICT.value:
            try:
                local = LocalRepository(self.__config, objects_path, repo_type)
                local.unlock_file(path, file_path, index_path, objects_path, spec, cache_path)
            except Exception as e:
                log.error(e, class_name=REPOSITORY_CLASS_NAME)
                return
        else:
            log.error(output_messages['INFO_MUTABILITY_CANNOT_BE_STRICT'],
                      class_name=REPOSITORY_CLASS_NAME)

    def create_config_storage(self, storage_type, credentials_path):
        bucket = {'credentials-path': credentials_path}
        self.__config[STORAGE_CONFIG_KEY][storage_type] = {storage_type: bucket}

    def create(self, kwargs):
        artifact_name = kwargs['artifact_name']
        categories = list(kwargs['category'])
        version = int(kwargs['version'])
        imported_dir = kwargs['import']
        storage_type = kwargs['storage_type']
        bucket_name = kwargs['bucket_name']
        start_wizard = kwargs['wizard_config']
        import_url = kwargs['import_url']
        unzip_file = kwargs['unzip']
        credentials_path = kwargs['credentials_path']
        repo_type = self.__repo_type
        try:
            create_workspace_tree_structure(repo_type, artifact_name, categories, storage_type, bucket_name,
                                            version, imported_dir, kwargs['mutability'], kwargs['entity_dir'])
            if start_wizard:
                has_new_storage, storage_type, bucket, profile, endpoint_url, git_repo = start_wizard_questions(repo_type)
                if has_new_storage:
                    storage_add(storage_type, bucket, profile, endpoint_url)
                update_storage_spec(repo_type, artifact_name, storage_type, bucket, kwargs['entity_dir'])
                remote_add(repo_type, git_repo)
            if import_url:
                self.create_config_storage(StorageType.GDRIVE.value, credentials_path)
                local = LocalRepository(self.__config, get_objects_path(self.__config, repo_type))
                destine_path = os.path.join(repo_type, kwargs['entity_dir'], artifact_name, 'data')
                local.import_file_from_url(destine_path, import_url, StorageType.GDRIVE.value)
            if unzip_file:
                log.info(output_messages['INFO_UNZIPPING_FILES'], CLASS_NAME=REPOSITORY_CLASS_NAME)
                data_path = os.path.join(get_root_path(), repo_type, kwargs['entity_dir'], artifact_name, 'data')
                unzip_files_in_directory(data_path)
            log.info(output_messages['INFO_PROJECT_CREATED'], CLASS_NAME=REPOSITORY_CLASS_NAME)
        except Exception as e:
            if not isinstance(e, PermissionError):
                clear(os.path.join(repo_type, artifact_name))
            if isinstance(e, KeyboardInterrupt):
                log.info(output_messages['INFO_CREATE_ABORTED'], class_name=REPOSITORY_CLASS_NAME)
            else:
                log.error(e, CLASS_NAME=REPOSITORY_CLASS_NAME)

    def clone_config(self, url, folder=None, track=False):
        if clone_config_repository(url, folder, track):
            self.__config = config_load()
            m = Metadata('', get_metadata_path(self.__config), self.__config)
            m.clone_config_repo()

    def export(self, bucket, tag, retry):
        try:
            _, spec_name, _ = spec_parse(tag)
            get_root_path()
            if not self._tag_exists(tag):
                return None, None
        except InvalidGitRepositoryError:
            log.error(output_messages['ERROR_NOT_IN_RESPOSITORY'], class_name=LOCAL_REPOSITORY_CLASS_NAME)
            return None, None
        except Exception as e:
            log.error(e, class_name=LOCAL_REPOSITORY_CLASS_NAME)
            return None, None

        try:
            self._checkout_ref(tag)
        except Exception:
            log.error(output_messages['ERROR_UNABLE_CHECKOUT'] % tag, class_name=REPOSITORY_CLASS_NAME)
            return None, None

        local = LocalRepository(self.__config, get_objects_path(self.__config, self.__repo_type), self.__repo_type)
        local.export_tag(get_metadata_path(self.__config, self.__repo_type), tag, bucket, retry)
        self._checkout_ref()

    def _log_compare_spec_from_versions(self, spec, metadata):
        refs_path = get_refs_path(self.__config, self.__repo_type)
        ref = Refs(refs_path, spec, self.__repo_type)
        tag, _ = ref.branch()
        path, spec_file = search_spec_file(self.__repo_type, spec)
        plugin_caller = self.__load_plugin_caller(path, spec_file)
        return plugin_caller.call(COMPARE_SPECS, metadata.get_specs_to_compare(spec))

    def log(self, spec, stat=False, fullstat=False):

        try:
            repo_type = self.__repo_type
            metadata_path = get_metadata_path(self.__config, repo_type)
            metadata = Metadata(spec, metadata_path, self.__config, repo_type)
            index_path = get_index_path(self.__config, repo_type)
            specialized_data_compared = self._log_compare_spec_from_versions(spec, metadata)
            log_info = metadata.get_log_info(spec, fullstat, specialized_data_compared)
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return
        fidx = FullIndex(spec, index_path)
        if stat or fullstat:
            workspace_size = fidx.get_total_size()

            amount_message = 'Total of files: %s' % fidx.get_total_count()
            size_message = 'Workspace size: %s' % humanize.naturalsize(workspace_size)

            workspace_info = '------------------------------------------------- \n{}\t{}' \
                .format(amount_message, size_message)

            log_info = '{}\n{}'.format(log_info, workspace_info)

        log.info(log_info, class_name=REPOSITORY_CLASS_NAME)

    def get_models_metrics(self, entity_name, export_path, export_type, log_export_info=True):
        try:
            repo_type = self.__repo_type
            self._check_is_valid_entity(repo_type, entity_name)
            metadata_path = get_metadata_path(self.__config, repo_type)
            metadata = Metadata(entity_name, metadata_path, self.__config, repo_type)
            metrics_by_tag = metadata.get_metrics_info(entity_name, export_path)

            if export_path:
                if not export_type:
                    export_type = FileType.JSON.value
                export_data = metadata.export_metrics(entity_name, export_path, export_type, metrics_by_tag, log_export_info)
                return export_data
        except Exception as e:
            log.error(e, class_name=REPOSITORY_CLASS_NAME)
            return

    def metadata_exists(self, entity):
        self.__repo_type = entity
        entity_metadata_path = get_metadata_path(self.__config, self.__repo_type)
        metadata = Metadata('', entity_metadata_path, self.__config, self.__repo_type)
        return metadata.check_exists()

    def update_entities_metadata(self):
        any_metadata = False
        for entity in EntityType:
            if self.metadata_exists(entity.value):
                self.update()
                any_metadata = True
        if not any_metadata:
            log.error(output_messages['ERROR_UNINITIALIZED_METADATA'], class_name=REPOSITORY_CLASS_NAME)

    def _check_is_valid_entity(self, repo_type, spec):
        ref = Refs(get_refs_path(self.__config, repo_type), spec, repo_type)
        tag, _ = ref.branch()
        search_spec_file(repo_type, spec)

    def _get_blobs_hashes(self, index_path, objects_path, repo_type):
        blobs_hashes = []
        for root, dirs, files in os.walk(os.path.join(index_path, 'metadata')):
            for spec in dirs:
                try:
                    self._check_is_valid_entity(repo_type, spec)
                    idx = MultihashIndex(spec, index_path, objects_path)
                    blobs_hashes.extend(idx.get_hashes_list())
                except Exception:
                    log.debug(output_messages['INFO_ENTITY_DELETED'] % spec, class_name=REPOSITORY_CLASS_NAME)
        return blobs_hashes

    def garbage_collector(self):
        any_metadata = False
        removed_files = 0
        reclaimed_space = 0
        for entity in EntityType:
            repo_type = entity.value
            if self.metadata_exists(repo_type):
                log.info(output_messages['INFO_STARTING_GC'] % repo_type, class_name=REPOSITORY_CLASS_NAME)
                any_metadata = True
                index_path = get_index_path(self.__config, repo_type)
                objects_path = get_objects_path(self.__config, repo_type)
                blobs_hashes = self._get_blobs_hashes(index_path, objects_path, repo_type)

                cache = Cache(get_cache_path(self.__config, repo_type))
                count_removed_cache, reclaimed_cache_space = cache.garbage_collector(blobs_hashes)
                objects = Objects('', objects_path)
                count_removed_objects, reclaimed_objects_space = objects.garbage_collector(blobs_hashes)

                reclaimed_space += reclaimed_objects_space + reclaimed_cache_space
                removed_files += count_removed_objects + count_removed_cache
        if not any_metadata:
            log.error(output_messages['ERROR_UNINITIALIZED_METADATA'], class_name=REPOSITORY_CLASS_NAME)
            return
        log.info(output_messages['INFO_REMOVED_FILES'] % (humanize.intword(removed_files),
                                                          os.path.join(get_root_path(), '.ml-git')),
                 class_name=REPOSITORY_CLASS_NAME)
        log.info(output_messages['INFO_RECLAIMED_SPACE'] % humanize.naturalsize(reclaimed_space),
                 class_name=REPOSITORY_CLASS_NAME)
