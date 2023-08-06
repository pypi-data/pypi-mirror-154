"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os

from git import Repo, GitCommandError

from ml_git import log
from ml_git.config import mlgit_config_save, get_global_config_path
from ml_git.constants import ROOT_FILE_NAME, CONFIG_FILE, ADMIN_CLASS_NAME, StorageType, STORAGE_CONFIG_KEY
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
        log.info(output_messages['INFO_ALREADY_IN_RESPOSITORY'], class_name=ADMIN_CLASS_NAME)
        return
    except Exception:
        pass
    try:
        os.mkdir('.ml-git')
    except PermissionError:
        log.error(output_messages['ERROR_PERMISSION_DENIED_INITIALIZE_DIRECTORY'],
                  class_name=ADMIN_CLASS_NAME)
        return
    except FileExistsError:
        pass

    mlgit_config_save()
    root_path = get_root_path()
    log.info(output_messages['INFO_INITIALIZED_PROJECT_IN'] % (os.path.join(root_path, ROOT_FILE_NAME)),
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


def valid_storage_type(storage_type):
    storage_type_list = [storage.value for storage in StorageType]
    if storage_type not in storage_type_list:
        log.error(output_messages['ERROR_UNKNOWN_STORAGE_TYPE'] % (storage_type, storage_type_list),
                  class_name=ADMIN_CLASS_NAME)
        return False
    return True


def storage_add(storage_type, bucket, credentials_profile, global_conf=False, endpoint_url=None, sftp_configs=None):
    if not valid_storage_type(storage_type):
        return

    try:
        region = get_bucket_region(bucket, credentials_profile)
    except Exception:
        region = None
    if storage_type not in (StorageType.S3H.value, StorageType.S3.value) or credentials_profile is None:
        log.info(output_messages['INFO_ADD_STORAGE_WITHOUT_PROFILE'] % (storage_type, bucket), class_name=ADMIN_CLASS_NAME)
    else:
        log.info(output_messages['INFO_ADD_STORAGE'] % (storage_type, bucket, credentials_profile), class_name=ADMIN_CLASS_NAME)
    try:
        file = get_config_path(global_conf)
        conf = yaml_load(file)
    except Exception as e:
        log.error(e, class_name=ADMIN_CLASS_NAME)
        return

    if STORAGE_CONFIG_KEY not in conf:
        conf[STORAGE_CONFIG_KEY] = {}
    if storage_type not in conf[STORAGE_CONFIG_KEY]:
        conf[STORAGE_CONFIG_KEY][storage_type] = {}
    conf[STORAGE_CONFIG_KEY][storage_type][bucket] = {}
    if storage_type in [StorageType.S3.value, StorageType.S3H.value]:
        conf[STORAGE_CONFIG_KEY][storage_type][bucket]['aws-credentials'] = {}
        conf[STORAGE_CONFIG_KEY][storage_type][bucket]['aws-credentials']['profile'] = credentials_profile
        conf[STORAGE_CONFIG_KEY][storage_type][bucket]['region'] = region
        conf[STORAGE_CONFIG_KEY][storage_type][bucket]['endpoint-url'] = endpoint_url
    elif storage_type in [StorageType.GDRIVEH.value]:
        conf[STORAGE_CONFIG_KEY][storage_type][bucket]['credentials-path'] = credentials_profile
    elif storage_type in [StorageType.SFTPH.value]:
        conf[STORAGE_CONFIG_KEY][storage_type][bucket]['endpoint-url'] = endpoint_url
        conf[STORAGE_CONFIG_KEY][storage_type][bucket]['username'] = sftp_configs['username']
        conf[STORAGE_CONFIG_KEY][storage_type][bucket]['private-key'] = sftp_configs['private_key']
        conf[STORAGE_CONFIG_KEY][storage_type][bucket]['port'] = sftp_configs['port']
    yaml_save(conf, file)


def storage_del(storage_type, bucket, global_conf=False):
    if not valid_storage_type(storage_type):
        return

    try:
        config_path = get_config_path(global_conf)
        conf = yaml_load(config_path)
    except Exception as e:
        log.error(e, class_name=ADMIN_CLASS_NAME)
        return

    storage_exists = STORAGE_CONFIG_KEY in conf and storage_type in conf[STORAGE_CONFIG_KEY] and bucket in conf[STORAGE_CONFIG_KEY][storage_type]

    if not storage_exists:
        log.warn(output_messages['WARN_STORAGE_NOT_IN_CONFIG'] % (storage_type, bucket), class_name=ADMIN_CLASS_NAME)
        return

    del conf[STORAGE_CONFIG_KEY][storage_type][bucket]
    log.info(output_messages['INFO_REMOVED_STORAGE'] % (storage_type, bucket), class_name=ADMIN_CLASS_NAME)

    yaml_save(conf, config_path)


def clone_config_repository(url, folder, track):
    try:
        if get_root_path():
            log.error(output_messages['ERROR_IN_INTIALIZED_PROJECT'], class_name=ADMIN_CLASS_NAME)
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
            log.error(output_messages['ERROR_PATH_NOT_EMPTY']
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
        log.error(output_messages['ERROR_MINIMAL_CONFIGURATION'], class_name=ADMIN_CLASS_NAME)
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
