"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os

from git import Repo, GitCommandError

from ml_git import log
from ml_git.config import mlgit_config_save, get_global_config_path
from ml_git.constants import ROOT_FILE_NAME, CONFIG_FILE, ADMIN_CLASS_NAME, StoreType
from ml_git.ml_git_message import output_messages
from ml_git.storages.store_utils import get_bucket_region
from ml_git.utils import get_root_path
from ml_git.utils import yaml_load, yaml_save, RootPathException, clear, ensure_path_exists


# define initial ml-git project structure
# ml-git-root/
# ├── .ml-git/config.yaml
# | 				# describe git repository (dataset, labels, nn-params, models)
# | 				# describe settings for actual S3/IPFS storage of dataset(s), model(s)


def init_mlgit():
    try:
        root_path = get_root_path()
        log.info('You already are in a ml-git repository (%s)' % (os.path.join(root_path, ROOT_FILE_NAME)),
                 class_name=ADMIN_CLASS_NAME)
        return
    except Exception:
        pass

    try:
        os.mkdir('.ml-git')
    except PermissionError:
        log.error('Permission denied. You need write permission to initialize ml-git in this directory.',
                  class_name=ADMIN_CLASS_NAME)
        return
    except FileExistsError:
        pass

    mlgit_config_save()
    root_path = get_root_path()
    log.info('Initialized empty ml-git repository in %s' % (os.path.join(root_path, ROOT_FILE_NAME)),
             class_name=ADMIN_CLASS_NAME)


def remote_add(repotype, ml_git_remote, global_conf=False):
    file = get_config_path(global_conf)
    conf = yaml_load(file)

    if repotype in conf:
        if conf[repotype]['git'] is None or not len(conf[repotype]['git']) > 0:
            log.info(output_messages['INFO_ADD_REMOTE'] % (ml_git_remote, repotype), class_name=ADMIN_CLASS_NAME)
        else:
            log.warn(output_messages['WARN_HAS_CONFIGURED_REMOTE'], class_name=ADMIN_CLASS_NAME)
            log.info(output_messages['INFO_CHANGING_REMOTE'] % (conf[repotype]['git'], ml_git_remote, repotype),
                     class_name=ADMIN_CLASS_NAME)
    else:
        log.info(output_messages['INFO_ADD_REMOTE'] % (ml_git_remote, repotype), class_name=ADMIN_CLASS_NAME)
    try:
        conf[repotype]['git'] = ml_git_remote
    except Exception:
        conf[repotype] = {}
        conf[repotype]['git'] = ml_git_remote
    yaml_save(conf, file)


def remote_del(repo_type, global_conf=False):
    file = get_config_path(global_conf)
    conf = yaml_load(file)

    if repo_type in conf:
        git_url = conf[repo_type]['git']
        if git_url is None or not len(conf[repo_type]['git']) > 0:
            log.error(output_messages['ERROR_REMOTE_UNCONFIGURED'] % repo_type, class_name=ADMIN_CLASS_NAME)
        else:
            log.info(output_messages['INFO_REMOVE_REMOTE'] % (git_url, repo_type), class_name=ADMIN_CLASS_NAME)
            conf[repo_type]['git'] = ''
            yaml_save(conf, file)
    else:
        log.error(output_messages['ERROR_ENTITY_NOT_FOUND'] % repo_type, class_name=ADMIN_CLASS_NAME)


def valid_store_type(store_type):
    store_type_list = [store.value for store in StoreType]
    if store_type not in store_type_list:
        log.error('Unknown data store type [%s], choose one of these %s.' % (store_type, store_type_list),
                  class_name=ADMIN_CLASS_NAME)
        return False
    return True


def store_add(store_type, bucket, credentials_profile, global_conf=False, endpoint_url=None):
    if not valid_store_type(store_type):
        return

    try:
        region = get_bucket_region(bucket, credentials_profile)
    except Exception:
        region = 'us-east-1'
    if store_type not in (StoreType.S3H.value, StoreType.S3.value):
        log.info('Add store [%s://%s]' % (store_type, bucket), class_name=ADMIN_CLASS_NAME)
    else:
        log.info('Add store [%s://%s] with creds from profile [%s]' %
                 (store_type, bucket, credentials_profile), class_name=ADMIN_CLASS_NAME)
    try:
        file = get_config_path(global_conf)
        conf = yaml_load(file)
    except Exception as e:
        log.error(e, class_name=ADMIN_CLASS_NAME)
        return

    if 'store' not in conf:
        conf['store'] = {}
    if store_type not in conf['store']:
        conf['store'][store_type] = {}
    conf['store'][store_type][bucket] = {}
    if store_type in [StoreType.S3.value, StoreType.S3H.value]:
        conf['store'][store_type][bucket]['aws-credentials'] = {}
        conf['store'][store_type][bucket]['aws-credentials']['profile'] = credentials_profile
        conf['store'][store_type][bucket]['region'] = region
        conf['store'][store_type][bucket]['endpoint-url'] = endpoint_url
    elif store_type in [StoreType.GDRIVEH.value]:
        conf['store'][store_type][bucket]['credentials-path'] = credentials_profile
    yaml_save(conf, file)


def store_del(store_type, bucket, global_conf=False):
    if not valid_store_type(store_type):
        return

    try:
        config_path = get_config_path(global_conf)
        conf = yaml_load(config_path)
    except Exception as e:
        log.error(e, class_name=ADMIN_CLASS_NAME)
        return

    store_exists = 'store' in conf and store_type in conf['store'] and bucket in conf['store'][store_type]

    if not store_exists:
        log.warn('Store [%s://%s] not found in configuration file.' % (store_type, bucket), class_name=ADMIN_CLASS_NAME)
        return

    del conf['store'][store_type][bucket]
    log.info('Removed store [%s://%s] from configuration file.' % (store_type, bucket), class_name=ADMIN_CLASS_NAME)

    yaml_save(conf, config_path)


def clone_config_repository(url, folder, track):
    try:
        if get_root_path():
            log.error('You are in initialized ml-git project.', class_name=ADMIN_CLASS_NAME)
            return False
    except RootPathException:
        pass

    git_dir = '.git'

    try:
        if folder is not None:
            project_dir = os.path.join(os.getcwd(), folder)
            ensure_path_exists(project_dir)
        else:
            project_dir = os.getcwd()

        if len(os.listdir(project_dir)) != 0:
            log.error('The path [%s] is not an empty directory. Consider using --folder to create an empty folder.'
                      % project_dir, class_name=ADMIN_CLASS_NAME)
            return False
        Repo.clone_from(url, project_dir)
    except Exception as e:
        error_msg = handle_clone_exception(e, folder, project_dir)
        log.error(error_msg, class_name=ADMIN_CLASS_NAME)
        return False

    if not check_successfully_clone(project_dir, git_dir):
        return False

    if not track:
        clear(os.path.join(project_dir, git_dir))

    return True


def handle_clone_exception(e, folder, project_dir):
    error_msg = str(e)
    if (e.__class__ == GitCommandError and 'Permission denied' in str(e.args[2])) or e.__class__ == PermissionError:
        error_msg = 'Permission denied in folder %s' % project_dir
    else:
        if folder is not None:
            clear(project_dir)
        if e.__class__ == GitCommandError:
            error_msg = 'Could not read from remote repository.'
    return error_msg


def check_successfully_clone(project_dir, git_dir):
    try:
        os.chdir(project_dir)
        get_root_path()
    except RootPathException:
        clear(project_dir)
        log.error('Wrong minimal configuration files!', class_name=ADMIN_CLASS_NAME)
        clear(git_dir)
        return False
    return True


def get_config_path(global_config=False):
    root_path = get_root_path()
    if global_config:
        file = get_global_config_path()
    else:
        file = os.path.join(root_path, CONFIG_FILE)
    return file
