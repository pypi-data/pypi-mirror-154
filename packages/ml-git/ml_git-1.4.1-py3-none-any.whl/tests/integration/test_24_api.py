"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import unittest

import pytest

from ml_git import api
from ml_git.constants import Mutability, StoreType
from ml_git.ml_git_message import output_messages
from tests.integration.commands import MLGIT_INIT
from tests.integration.helper import ML_GIT_DIR, check_output, init_repository, create_git_clone_repo, \
    clear, yaml_processor, create_zip_file, CLONE_FOLDER, GIT_PATH, BUCKET_NAME, PROFILE, STORE_TYPE


@pytest.mark.usefixtures('tmp_dir', 'aws_session')
class APIAcceptanceTests(unittest.TestCase):

    objects = os.path.join(ML_GIT_DIR, 'dataset', 'objects')
    refs = os.path.join(ML_GIT_DIR, 'dataset', 'refs')
    cache = os.path.join(ML_GIT_DIR, 'dataset', 'cache')
    metadata = os.path.join(ML_GIT_DIR, 'dataset', 'metadata')
    spec_file = os.path.join('dataset', 'computer-vision', 'images', 'dataset-ex', 'dataset-ex.spec')
    file1 = os.path.join('dataset', 'computer-vision', 'images', 'dataset-ex', 'data', 'file1')
    file2 = os.path.join('dataset', 'computer-vision', 'images', 'dataset-ex', 'data', 'file2')
    file3 = os.path.join('dataset', 'computer-vision', 'images', 'dataset-ex', 'data', 'file3')
    file4 = os.path.join('dataset', 'computer-vision', 'images', 'dataset-ex', 'data', 'file4')
    dataset_tag = 'computer-vision__images__dataset-ex__10'
    data_path = os.path.join('dataset', 'computer-vision', 'images', 'dataset-ex')
    GIT_CLONE = 'git_clone.git'

    def create_file(self, path, file_name, code):
        file = os.path.join('data', file_name)
        with open(os.path.join(path, file), 'w') as file:
            file.write(code * 2048)

    def set_up_test(self):
        init_repository('dataset', self)

        workspace = os.path.join(self.tmp_dir, 'dataset', 'dataset-ex')

        os.makedirs(workspace, exist_ok=True)

        spec = {
            'dataset': {
                'categories': ['computer-vision', 'images'],
                'manifest': {
                    'files': 'MANIFEST.yaml',
                    'store': 's3h://mlgit'
                },
                'mutability': Mutability.STRICT.value,
                'name': 'dataset-ex',
                'version': 9
            }
        }

        with open(os.path.join(workspace, 'dataset-ex.spec'), 'w') as y:
            yaml_processor.dump(spec, y)

        os.makedirs(os.path.join(workspace, 'data'), exist_ok=True)

        self.create_file(workspace, 'file1', '0')
        self.create_file(workspace, 'file2', '1')
        self.create_file(workspace, 'file3', 'a')
        self.create_file(workspace, 'file4', 'b')

        api.add('dataset', 'dataset-ex', bumpversion=True)
        api.commit('dataset', 'dataset-ex')
        api.push('dataset', 'dataset-ex')

        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir, self.metadata)))

        clear(os.path.join(self.tmp_dir, ML_GIT_DIR))
        clear(workspace)
        init_repository('dataset', self)

    def check_metadata(self):
        self.assertTrue(os.path.exists(self.objects))
        self.assertTrue(os.path.exists(self.refs))
        self.assertTrue(os.path.exists(self.cache))
        self.assertTrue(os.path.exists(self.spec_file))

    def set_up_clone_test(self):
        os.makedirs(self.GIT_CLONE, exist_ok=True)
        create_git_clone_repo(self.GIT_CLONE, self.tmp_dir)

        self.assertFalse(os.path.exists('.ml-git'))

    def _checkout_fail(self, data_path):
        self.assertEqual(None, data_path)
        self.assertFalse(os.path.exists(self.file1))
        self.assertFalse(os.path.exists(self.file2))
        self.assertFalse(os.path.exists(self.file3))
        self.assertFalse(os.path.exists(self.file4))

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_01_checkout_tag(self):
        self.set_up_test()

        data_path = api.checkout('dataset', self.dataset_tag)

        self.assertEqual(self.data_path, data_path)
        self.check_metadata()

        self.assertTrue(os.path.exists(self.file1))
        self.assertTrue(os.path.exists(self.file2))
        self.assertTrue(os.path.exists(self.file3))
        self.assertTrue(os.path.exists(self.file4))

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_02_checkout_with_group_sample(self):
        self.set_up_test()

        data_path = api.checkout('dataset', self.dataset_tag, {'group': '1:2', 'seed': '10'})

        self.assertEqual(self.data_path, data_path)
        self.check_metadata()

        self.assertTrue(os.path.exists(self.file1))
        self.assertFalse(os.path.exists(self.file2))
        self.assertFalse(os.path.exists(self.file3))
        self.assertTrue(os.path.exists(self.file4))

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_03_checkout_with_range_sample(self):
        self.set_up_test()

        data_path = api.checkout('dataset', self.dataset_tag, {'range': '0:4:3'})

        self.assertEqual(self.data_path, data_path)
        self.check_metadata()

        self.assertTrue(os.path.exists(self.file1))
        self.assertFalse(os.path.exists(self.file2))
        self.assertTrue(os.path.exists(self.file3))
        self.assertFalse(os.path.exists(self.file4))

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_04_checkout_with_random_sample(self):
        self.set_up_test()

        data_path = api.checkout('dataset', self.dataset_tag, {'random': '1:2', 'seed': '1'})

        self.assertEqual(self.data_path, data_path)
        self.check_metadata()

        self.assertFalse(os.path.exists(self.file1))
        self.assertTrue(os.path.exists(self.file2))
        self.assertFalse(os.path.exists(self.file3))
        self.assertTrue(os.path.exists(self.file4))

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_05_checkout_with_group_sample_without_group(self):
        self.set_up_test()

        data_path = api.checkout('dataset', self.dataset_tag, {'seed': '10'})

        self._checkout_fail(data_path)

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_06_checkout_with_range_sample_without_range(self):
        self.set_up_test()

        data_path = api.checkout('dataset', self.dataset_tag, {'seed': '10'})

        self._checkout_fail(data_path)

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_07_checkout_with_random_sample_without_seed(self):
        self.set_up_test()

        data_path = api.checkout('dataset', self.dataset_tag, {'random': '1:2'})

        self._checkout_fail(data_path)

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_08_clone(self):
        self.set_up_clone_test()

        api.clone(self.GIT_CLONE)
        os.chdir(self.tmp_dir)
        self.assertTrue(os.path.exists('.ml-git'))

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_09_clone_with_track_and_folder(self):
        self.set_up_clone_test()

        clone_folder = os.path.join(self.tmp_dir, CLONE_FOLDER)

        self.assertFalse(os.path.exists(clone_folder))
        api.clone(self.GIT_CLONE, clone_folder, track=True)
        os.chdir(self.tmp_dir)
        self.assertTrue(os.path.exists(clone_folder))
        self.assertTrue(os.path.exists(os.path.join(clone_folder, '.ml-git')))
        self.assertTrue(os.path.exists(os.path.join(clone_folder, '.git')))

    def create_file_in_ws(self, entity, name, value):
        with open(os.path.join(entity, entity + '-ex', name), 'wt') as z:
            z.write(value * 100)

    def set_up_add_test(self, entity='dataset'):
        clear(os.path.join(self.tmp_dir, ML_GIT_DIR))
        clear(os.path.join(self.tmp_dir, entity))
        init_repository(entity, self)

        self.create_file_in_ws(entity, 'file', '0')
        self.create_file_in_ws(entity, 'file2', '1')

    def check_add(self, entity='dataset', files=['file', 'file2'], files_not_in=[]):
        metadata = os.path.join(self.tmp_dir, ML_GIT_DIR, entity, 'index', 'metadata', entity + '-ex')
        metadata_file = os.path.join(metadata, 'MANIFEST.yaml')
        index_file = os.path.join(metadata, 'INDEX.yaml')

        self.assertTrue(os.path.exists(metadata_file))
        self.assertTrue(os.path.exists(index_file))

        with open(metadata_file) as y:
            manifest = yaml_processor.load(y)
            for file in files:
                self.assertIn({file}, manifest.values())
            for file in files_not_in:
                self.assertNotIn({file}, manifest.values())

    def check_entity_version(self, version, entity='dataset'):
        spec_path = os.path.join(entity, entity+'-ex', entity+'-ex.spec')
        with open(spec_path) as y:
            ws_spec = yaml_processor.load(y)
            self.assertEqual(ws_spec[entity]['version'], version)

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_10_add_files(self):
        self.set_up_add_test()
        api.add('dataset', 'dataset-ex', bumpversion=False, fsck=False, file_path=[])
        self.check_add()

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_11_add_files_with_bumpversion(self):
        self.set_up_add_test()
        self.check_entity_version(1)

        api.add('dataset', 'dataset-ex', bumpversion=True, fsck=False, file_path=[])

        self.check_add()
        self.check_entity_version(2)

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_12_add_one_file(self):
        self.set_up_add_test()

        api.add('dataset', 'dataset-ex', bumpversion=False, fsck=False, file_path=['file'])

        self.check_add(files=['file'], files_not_in=['file2'])

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_13_commit_files(self):
        self.set_up_test()
        self.set_up_add_test()
        api.add('dataset', 'dataset-ex', bumpversion=True, fsck=False, file_path=['file'])
        api.commit('dataset', 'dataset-ex')
        HEAD = os.path.join(self.tmp_dir, ML_GIT_DIR, 'dataset', 'refs', 'dataset-ex', 'HEAD')
        self.assertTrue(os.path.exists(HEAD))

        init_repository('labels', self)
        self.create_file_in_ws('labels', 'file', '0')
        api.add('labels', 'labels-ex', bumpversion=True, fsck=False, file_path=['file'])
        api.commit('labels', 'labels-ex', related_dataset='dataset-ex')

        labels_metadata = os.path.join(self.tmp_dir, ML_GIT_DIR, 'labels', 'metadata')

        with open(os.path.join(labels_metadata, "computer-vision", "images", "labels-ex", "labels-ex.spec")) as y:
            spec = yaml_processor.load(y)

        HEAD = os.path.join(self.tmp_dir, ML_GIT_DIR, 'labels', 'refs', 'labels-ex', 'HEAD')
        self.assertTrue(os.path.exists(HEAD))

        self.assertEqual('computer-vision__images__dataset-ex__2', spec['labels']['dataset']['tag'])

    def check_created_folders(self, entity_type, store_type=StoreType.S3H.value, version=1, bucket_name='fake_store'):
        folder_data = os.path.join(self.tmp_dir, entity_type, entity_type + '-ex', 'data')
        spec = os.path.join(self.tmp_dir, entity_type, entity_type + '-ex', entity_type + '-ex.spec')
        readme = os.path.join(self.tmp_dir, entity_type, entity_type + '-ex', 'README.md')
        with open(spec, 'r') as s:
            spec_file = yaml_processor.load(s)
            self.assertEqual(spec_file[entity_type]['manifest']['store'], store_type + '://' + bucket_name)
            self.assertEqual(spec_file[entity_type]['name'], entity_type + '-ex')
            self.assertEqual(spec_file[entity_type]['version'], version)
        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as y:
            config = yaml_processor.load(y)
            self.assertIn(entity_type, config)

        self.assertTrue(os.path.exists(folder_data))
        self.assertTrue(os.path.exists(spec))
        self.assertTrue(os.path.exists(readme))

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_14_create_entity(self):
        entity_type = 'dataset'
        store_type = StoreType.S3H.value
        self.assertIn(output_messages['INFO_INITIALIZED_PROJECT'] % self.tmp_dir, check_output(MLGIT_INIT))
        api.create('dataset', 'dataset-ex', categories=['computer-vision', 'images'], mutability='strict')
        self.check_created_folders(entity_type, store_type)

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_15_create_entity_with_optional_arguments(self):
        entity_type = 'dataset'
        store_type = StoreType.AZUREBLOBH.value
        self.assertIn(output_messages['INFO_INITIALIZED_PROJECT'] % self.tmp_dir, check_output(MLGIT_INIT))
        api.create('dataset', 'dataset-ex', categories=['computer-vision', 'images'], version=5, store_type=store_type, bucket_name='test', mutability='strict')
        self.check_created_folders(entity_type, store_type, version=5, bucket_name='test')

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_16_create_entity_with_import(self):
        entity_type = 'dataset'
        IMPORT_PATH = 'src'
        self.assertIn(output_messages['INFO_INITIALIZED_PROJECT'] % self.tmp_dir, check_output(MLGIT_INIT))
        import_path = os.path.join(self.tmp_dir, IMPORT_PATH)
        os.makedirs(import_path)
        create_zip_file(IMPORT_PATH, 3)
        self.assertTrue(os.path.exists(os.path.join(import_path, 'file.zip')))
        api.create(entity_type, entity_type+'-ex', categories=['computer-vision', 'images'], unzip=True, import_path=import_path, mutability='strict')
        self.check_created_folders(entity_type, StoreType.S3H.value)
        folder_data = os.path.join(self.tmp_dir, entity_type, entity_type + '-ex', 'data', 'file')
        self.assertTrue(os.path.exists(folder_data))
        files = [f for f in os.listdir(folder_data)]
        self.assertIn('file0.txt', files)
        self.assertIn('file1.txt', files)
        self.assertIn('file2.txt', files)
        self.assertEqual(3, len(files))

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_17_init_repository(self):
        config = os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml')
        self.assertFalse(os.path.exists(config))
        api.init('repository')
        self.assertTrue(os.path.exists(config))

    def _add_remote(self, entity_type):
        api.init('repository')
        api.remote_add(entity_type, os.path.join(self.tmp_dir, GIT_PATH))
        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertEqual(os.path.join(self.tmp_dir, GIT_PATH), config[entity_type]['git'])

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_18_add_remote_dataset(self):
        self._add_remote(entity_type='dataset')

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_19_add_remote_laebls(self):
        self._add_remote(entity_type='labels')

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_20_add_remote_model(self):
        self._add_remote(entity_type='model')

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_21_add_store(self):
        api.init('repository')
        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertNotIn('s3h', config['store'])
        api.store_add(bucket_name=BUCKET_NAME, credentials=PROFILE)
        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertEqual(PROFILE, config['store']['s3h'][BUCKET_NAME]['aws-credentials']['profile'])

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_22_add_store_azure_type(self):
        bucket_type = 'azureblobh'
        bucket_name = 'container_azure'
        api.init('repository')
        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertNotIn(bucket_type, config['store'])
        api.store_add(bucket_name=bucket_name, bucket_type=bucket_type)
        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertIn(bucket_name, config['store'][bucket_type])

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_23_add_store_gdrive_type(self):
        bucket_type = 'gdriveh'
        bucket_name = 'my-drive'
        profile = 'path-to-credentials'
        api.init('repository')
        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertNotIn(bucket_type, config['store'])
        api.store_add(bucket_name=bucket_name, bucket_type=bucket_type, credentials=profile)
        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertEqual(profile, config['store'][bucket_type][bucket_name]['credentials-path'])

    def _initialize_entity(self, entity_type, git=GIT_PATH):
        api.init('repository')
        api.remote_add(entity_type, git)
        api.store_add(bucket_type=STORE_TYPE, bucket_name=BUCKET_NAME, credentials=PROFILE)
        api.init(entity_type)
        metadata_path = os.path.join(self.tmp_dir, ML_GIT_DIR, entity_type, 'metadata')
        self.assertTrue(os.path.exists(metadata_path))

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_24_init_dataset(self):
        self._initialize_entity('dataset')

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_25_init_labels(self):
        self._initialize_entity('labels')

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_26_init_model(self):
        self._initialize_entity('model')

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_27_create_with_invalid_entity(self):
        try:
            entity_type = 'dataset_invalid'
            store_type = StoreType.S3H.value
            self.assertIn(output_messages['INFO_INITIALIZED_PROJECT'] % self.tmp_dir, check_output(MLGIT_INIT))
            api.create('dataset_invalid', 'dataset-ex', categories=['computer-vision', 'images'], mutability='strict')
            self.check_created_folders(entity_type, store_type)
            self.assertTrue(False)
        except Exception as e:
            self.assertIn(output_messages['ERROR_INVALID_ENTITY_TYPE'], str(e))

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_28_checkout_tag_with_invalid_entity(self):
        try:
            self.set_up_test()
            data_path = api.checkout('dataset_invalid', self.dataset_tag)
            self.assertEqual(self.data_path, data_path)
            self.check_metadata()
            self.assertTrue(False)
        except Exception as e:
            self.assertIn(output_messages['ERROR_INVALID_ENTITY_TYPE'], str(e))
