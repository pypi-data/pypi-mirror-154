"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import shutil
from pathlib import Path

from halo import Halo

from ml_git import spec
from ml_git.constants import FAKE_STORE, BATCH_SIZE_VALUE, BATCH_SIZE, StoreType, GLOBAL_ML_GIT_CONFIG, \
    PUSH_THREADS_COUNT, SPEC_EXTENSION
from ml_git.utils import getOrElse, yaml_load, yaml_save, get_root_path, yaml_load_str

push_threads = os.cpu_count()*5

mlgit_config = {
    'mlgit_path': '.ml-git',
    'mlgit_conf': 'config.yaml',

    'dataset': {
        'git': '',
    },
    'model': {
        'git': '',
    },
    'labels': {
        'git': '',
    },

    'store': {
        's3': {
            'mlgit-datasets': {
                'region': 'us-east-1',
                'aws-credentials': {'profile': 'default'}
            }
        }
    },

    'batch_size': BATCH_SIZE_VALUE,

    'verbose': 'info',

    'index_path': '',
    'refs_path': '',
    'object_path': '',
    'cache_path': '',
    'metadata_path': '',

    PUSH_THREADS_COUNT: push_threads

}


def config_verbose():
    global mlgit_config
    try:
        return mlgit_config['verbose']
    except Exception:
        return None


def get_key(key, config=None):
    global mlgit_config

    conf = mlgit_config
    if config is not None:
        conf = config
    try:
        return getOrElse(conf, key, lambda: '')()
    except Exception:
        return getOrElse(conf, key, '')


def __config_from_environment():
    global mlgit_config

    for key in mlgit_config.keys():
        val = os.getenv(key.upper())
        if val is not None:
            mlgit_config[key] = val


def __get_conf_filepath():
    models_path = os.getenv('MLMODELS_PATH')
    if models_path is None:
        models_path = get_key('mlgit_path')
    try:
        root_path = get_root_path()
        return os.path.join(root_path, os.sep.join([models_path, get_key('mlgit_conf')]))
    except Exception:
        return os.sep.join([models_path, get_key('mlgit_conf')])


def config_load():
    global mlgit_config

    config_file_path = __get_conf_filepath()
    actx = yaml_load(config_file_path)

    for key, value in actx.items():
        mlgit_config[key] = value

    __config_from_environment()

    if os.path.exists(config_file_path):
        merge_local_with_global_config()

    return mlgit_config


# loads ml-git config.yaml file
def mlgit_config_load():
    mlgit_file = __get_conf_filepath()
    if os.path.exists(mlgit_file) is False:
        return {}

    return yaml_load(mlgit_file)


# saves initial config file in .ml-git/config.yaml
def mlgit_config_save(mlgit_file=__get_conf_filepath()):
    global mlgit_config

    if os.path.exists(mlgit_file) is True:
        return

    config = {
        'dataset': mlgit_config['dataset'],
        'model': mlgit_config['model'],
        'labels': mlgit_config['labels'],
        'store': mlgit_config['store'],
        'batch_size': mlgit_config['batch_size']
    }
    return yaml_save(config, mlgit_file)


def save_global_config_in_local(mlgit_file=__get_conf_filepath()):
    global mlgit_config

    merge_local_with_global_config()

    config = {
        'dataset': mlgit_config['dataset'],
        'model': mlgit_config['model'],
        'labels': mlgit_config['labels'],
        'store': mlgit_config['store'],
        'batch_size': mlgit_config['batch_size']
    }
    return yaml_save(config, mlgit_file)


def list_repos():
    global mlgit_config
    if 'repos' not in mlgit_config:
        return None
    return mlgit_config['repos'].keys()


def repo_config(repo):
    global mlgit_config
    return mlgit_config['repos'][repo]


def get_index_path(config, type='dataset'):
    root_path = get_root_path()
    default = os.path.join(root_path, config['mlgit_path'], type, 'index')
    return getOrElse(config[type], 'index_path', default)


def get_index_metadata_path(config, type='dataset'):
    default = os.path.join(get_index_path(config, type), 'metadata')
    return getOrElse(config[type], 'index_metadata_path', default)


def get_batch_size(config):
    try:
        batch_size = int(config.get(BATCH_SIZE, BATCH_SIZE_VALUE))
    except Exception:
        batch_size = -1

    if batch_size <= 0:
        raise RuntimeError('The batch size value is invalid in the config file for the [%s] key' % BATCH_SIZE)

    return batch_size


def get_objects_path(config, type='dataset'):
    root_path = get_root_path()
    default = os.path.join(root_path, config['mlgit_path'], type, 'objects')
    return getOrElse(config[type], 'objects_path', default)


def get_cache_path(config, type='dataset'):
    root_path = get_root_path()
    default = os.path.join(root_path, config['mlgit_path'], type, 'cache')
    return getOrElse(config[type], 'cache_path', default)


def get_metadata_path(config, type='dataset'):
    root_path = get_root_path()
    default = os.path.join(root_path, config['mlgit_path'], type, 'metadata')
    return getOrElse(config[type], 'metadata_path', default)


def get_refs_path(config, type='dataset'):
    root_path = get_root_path()
    default = os.path.join(root_path, config['mlgit_path'], type, 'refs')
    return getOrElse(config[type], 'refs_path', default)


def get_sample_config_spec(bucket, profile, region):
    doc = '''
      store:
        s3h:
          %s:
            aws-credentials:
              profile: %s
            region: %s
    ''' % (bucket, profile, region)
    c = yaml_load_str(doc)
    return c


def validate_config_spec_hash(config):
    if not config:
        return False
    if 'store' not in config:
        return False
    stores = valid_stores(config['store'])
    if not stores:
        return False
    for store in stores:
        if not validate_bucket_config(config['store'][store], store):
            return False
    return True


def validate_bucket_config(the_bucket_hash, store_type=StoreType.S3H.value):
    for bucket in the_bucket_hash:
        if store_type == StoreType.S3H.value:
            if 'aws-credentials' not in the_bucket_hash[bucket] or 'region' not in the_bucket_hash[bucket]:
                return False
            if 'profile' not in the_bucket_hash[bucket]['aws-credentials']:
                return False
        elif store_type == StoreType.GDRIVEH.value:
            if "credentials-path" not in the_bucket_hash[bucket]:
                return False
    return True


def get_sample_spec_doc(bucket, repotype='dataset'):
    doc = '''
      %s:
        categories:
        - vision-computing
        - images
        mutability: strict
        manifest:
          files: MANIFEST.yaml
          store: s3h://%s
        name: %s-ex
        version: 5
    ''' % (repotype, bucket, repotype)
    return doc


def get_sample_spec(bucket, repotype='dataset'):
    c = yaml_load_str(get_sample_spec_doc(bucket, repotype))
    return c


def validate_spec_hash(the_hash, repotype='dataset'):
    if the_hash in [None, {}]:
        return False

    if not spec.is_valid_version(the_hash, repotype):
        return False  # Also checks for the existence of 'dataset'

    if 'categories' not in the_hash[repotype] or 'manifest' not in the_hash[repotype]:
        return False

    if the_hash[repotype]['categories'] == {}:
        return False

    if 'store' not in the_hash[repotype]['manifest']:
        return False

    if not validate_spec_string(the_hash[repotype]['manifest']['store']):
        return False

    if 'name' not in the_hash[repotype]:
        return False

    if the_hash[repotype]['name'] == '':
        return False

    return True


def create_workspace_tree_structure(repo_type, artifact_name, categories, store_type, bucket_name, version,
                                    imported_dir, mutability):
    # get root path to create directories and files
    path = get_root_path()
    artifact_path = os.path.join(path, repo_type, artifact_name)
    if os.path.exists(artifact_path):
        raise PermissionError('An entity with that name already exists.')
    data_path = os.path.join(artifact_path, 'data')
    # import files from  the directory passed
    if imported_dir is not None:
        import_dir(imported_dir, data_path)
    else:
        os.makedirs(data_path)

    spec_path = os.path.join(artifact_path, artifact_name + SPEC_EXTENSION)
    readme_path = os.path.join(artifact_path, 'README.md')
    file_exists = os.path.isfile(spec_path)

    store = '%s://%s' % (store_type, FAKE_STORE if bucket_name is None else bucket_name)
    spec_structure = {
        repo_type: {
            'categories': categories,
            'manifest': {
                'store': store
            },
            'name': artifact_name,
            'mutability': mutability,
            'version': version
        }
    }

    # write in spec  file
    if not file_exists:
        yaml_save(spec_structure, spec_path)
        with open(readme_path, 'w'):
            pass
        return True
    else:
        return False


def start_wizard_questions(repotype):
    print('_ Current configured stores _')
    print('   ')
    store = config_load()['store']
    count = 1
    # temporary map with number as key and a array with store type and bucket as values
    temp_map = {}
    # list the buckets to the user choose one
    for store_type in store:
        for key in store[store_type].keys():
            print('%s - %s - %s' % (str(count), store_type, key))
            temp_map[count] = [store_type, key]
            count += 1
    print('X - New Data Store')
    print('   ')
    selected = input('_Which store do you want to use (a number or new data store)? _ ')
    profile = None
    endpoint = None
    git_repo = None
    config = mlgit_config_load()
    try:
        int(selected)  # the user select one store from the list
        has_new_store = False
        # extract necessary info from the store in spec
        store_type, bucket = extract_store_info_from_list(temp_map[int(selected)])
    except Exception:  # the user select create a new data store
        has_new_store = True
        stores_types = [item.value for item in StoreType]
        store_type = input('Please specify the store type ' + str(stores_types) + ': _ ').lower()
        if store_type not in stores_types:
            raise RuntimeError('Invalid store type.')
        bucket = input('Please specify the bucket name: _ ').lower()
        if store_type in (StoreType.S3.value, StoreType.S3H.value):
            profile = input('Please specify the credentials: _ ').lower()
            endpoint = input('If you are using S3 compatible storage (ex. minio), please specify the endpoint URL,'
                             ' otherwise press ENTER: _ ').lower()
        elif store_type == StoreType.GDRIVEH.value:
            profile = input('Please specify the credentials path: _ ').lower()
        git_repo = input('Please specify the git repository for ml-git %s metadata: _ ' % repotype).lower()
    if git_repo is None:
        try:
            git_repo = config[repotype]['git']
        except Exception:
            git_repo = ''
    return has_new_store, store_type, bucket, profile, endpoint, git_repo


def extract_store_info_from_list(array):
    store_type = array[0]
    bucket = array[1]
    return store_type, bucket


@Halo(text='Importing files', spinner='dots')
def import_dir(src_dir, dst_dir):
    shutil.copytree(src_dir, dst_dir)


def valid_stores(store):
    stores = [store_type.value for store_type in StoreType if store_type.value in store]
    return stores


def validate_spec_string(spec_str):
    for store in StoreType:
        pattern = '%s://' % store.value
        if spec_str.startswith(pattern):
            return True
    return False


def get_global_config_path():
    return os.path.join(Path.home(), GLOBAL_ML_GIT_CONFIG)


def global_config_load():
    return yaml_load(get_global_config_path())


def merge_conf(local_conf, global_conf):
    for key, value in local_conf.items():
        if value and isinstance(value, dict) and key in global_conf:
            merge_conf(value, global_conf[key])
        elif value:
            global_conf[key] = value

    local_conf.update(global_conf)


def merge_local_with_global_config():
    global mlgit_config
    global_config = global_config_load()
    merge_conf(mlgit_config, global_config)


def get_push_threads_count(config):
    try:
        push_threads_count = int(config.get(PUSH_THREADS_COUNT, push_threads))
    except Exception:
        raise RuntimeError('Invalid value in config file for the [%s] key. '
                           'This is should be a integer number greater than 0.' % PUSH_THREADS_COUNT)

    return push_threads_count
