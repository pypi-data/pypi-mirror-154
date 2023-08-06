"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import unittest

import pytest

from ml_git.constants import STORAGE_CONFIG_KEY
from ml_git.ml_git_message import output_messages
from tests.integration.commands import MLGIT_INIT, MLGIT_STORAGE_ADD, MLGIT_STORAGE_DEL, MLGIT_STORAGE_ADD_WITH_TYPE, \
    MLGIT_STORAGE_ADD_WITH_ENDPOINT, MLGIT_STORAGE_ADD_WITHOUT_CREDENTIALS
from tests.integration.helper import check_output, ML_GIT_DIR, BUCKET_NAME, PROFILE, STORAGE_TYPE, yaml_processor, S3H, \
    AZUREBLOBH, GDRIVEH


@pytest.mark.usefixtures('tmp_dir')
class AddStoreAcceptanceTests(unittest.TestCase):

    def _add_storage(self):
        self.assertIn(output_messages['INFO_INITIALIZED_PROJECT_IN'] % self.tmp_dir, check_output(MLGIT_INIT))
        self.check_storage()
        self.assertIn(output_messages['INFO_ADD_STORAGE'] % (STORAGE_TYPE, BUCKET_NAME, PROFILE),
                      check_output(MLGIT_STORAGE_ADD % (BUCKET_NAME, PROFILE)))

        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertEqual(PROFILE, config[STORAGE_CONFIG_KEY][S3H][BUCKET_NAME]['aws-credentials']['profile'])

    def _del_storage(self):
        self.assertIn(output_messages['INFO_REMOVED_STORAGE'] % (STORAGE_TYPE, BUCKET_NAME),
                      check_output(MLGIT_STORAGE_DEL % BUCKET_NAME))
        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertEqual(config[STORAGE_CONFIG_KEY][S3H], {})

    def check_storage(self):
        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertNotIn(S3H, config[STORAGE_CONFIG_KEY])

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_01_add_storage_root_directory(self):
        self._add_storage()

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_02_add_storage_twice(self):
        self._add_storage()
        self.assertIn(output_messages['INFO_ADD_STORAGE'] % (STORAGE_TYPE, BUCKET_NAME, PROFILE), check_output(
            MLGIT_STORAGE_ADD % (BUCKET_NAME, PROFILE)))

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_03_add_storage_subfolder(self):
        self.assertIn(output_messages['INFO_INITIALIZED_PROJECT_IN'] % self.tmp_dir, check_output(MLGIT_INIT))
        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertNotIn(S3H, config[STORAGE_CONFIG_KEY])

        os.chdir(os.path.join(self.tmp_dir, ML_GIT_DIR))
        self.assertIn(output_messages['INFO_ADD_STORAGE'] % (STORAGE_TYPE, BUCKET_NAME, PROFILE),
                      check_output(MLGIT_STORAGE_ADD % (BUCKET_NAME, PROFILE)))

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_04_add_storage_uninitialized_directory(self):
        self.assertIn(output_messages['ERROR_NOT_IN_RESPOSITORY'],
                      check_output(MLGIT_STORAGE_ADD % (BUCKET_NAME, PROFILE)))

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_05_del_storage(self):
        self._add_storage()
        self._del_storage()

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_06_add_storage_type_s3h(self):
        storage_type = STORAGE_TYPE
        bucket_name = 'bucket_s3'
        profile = 'profile_s3'
        config = self.add_storage_type(bucket_name, profile, storage_type)
        self.assertEqual(profile, config[STORAGE_CONFIG_KEY][storage_type][bucket_name]['aws-credentials']['profile'])

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_07_add_storage_type_azure(self):
        storage_type = AZUREBLOBH
        bucket_name = 'container_azure'
        profile = 'profile_azure'
        config = self.add_storage_type(bucket_name, profile, storage_type)
        self.assertIn(bucket_name, config[STORAGE_CONFIG_KEY][storage_type])

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_08_add_storage_type_gdriveh(self):
        storage_type = GDRIVEH
        bucket_name = 'google'
        profile = 'path/to/cred.json'
        config = self.add_storage_type(bucket_name, profile, storage_type)
        self.assertEqual(profile, config[STORAGE_CONFIG_KEY][storage_type][bucket_name]['credentials-path'])

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def add_storage_type(self, bucket, profile, storage_type):
        self.assertIn(output_messages['INFO_INITIALIZED_PROJECT_IN'] % self.tmp_dir, check_output(MLGIT_INIT))
        result = check_output(MLGIT_STORAGE_ADD_WITH_TYPE % (bucket, profile, storage_type))
        if storage_type == STORAGE_TYPE:
            self.assertIn(output_messages['INFO_ADD_STORAGE'] % (storage_type, bucket, profile), result)
        else:
            self.assertIn(output_messages['INFO_ADD_STORAGE_WITHOUT_PROFILE'] % (storage_type, bucket), result)
        with open(os.path.join(ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
        return config

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_09_add_storage_with_endpoint_url(self):
        self.assertIn(output_messages['INFO_INITIALIZED_PROJECT_IN'] % self.tmp_dir, check_output(MLGIT_INIT))
        self.check_storage()
        endpoint = 'minio.endpoint.url'
        self.assertIn(output_messages['INFO_ADD_STORAGE'] % (STORAGE_TYPE, BUCKET_NAME, PROFILE),
                      check_output(MLGIT_STORAGE_ADD_WITH_ENDPOINT % (BUCKET_NAME, PROFILE, endpoint)))

        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertEqual(PROFILE, config[STORAGE_CONFIG_KEY][S3H][BUCKET_NAME]['aws-credentials']['profile'])
            self.assertEqual(endpoint, config[STORAGE_CONFIG_KEY][S3H][BUCKET_NAME]['endpoint-url'])

    @pytest.mark.usefixtures('switch_to_tmp_dir')
    def test_10_add_storage_without_credentials(self):
        self.assertIn(output_messages['INFO_INITIALIZED_PROJECT_IN'] % self.tmp_dir, check_output(MLGIT_INIT))
        self.check_storage()
        self.assertIn(output_messages['INFO_ADD_STORAGE_WITHOUT_PROFILE'] % (STORAGE_TYPE, BUCKET_NAME),
                      check_output(MLGIT_STORAGE_ADD_WITHOUT_CREDENTIALS % BUCKET_NAME))
        with open(os.path.join(self.tmp_dir, ML_GIT_DIR, 'config.yaml'), 'r') as c:
            config = yaml_processor.load(c)
            self.assertEqual(None, config[STORAGE_CONFIG_KEY][S3H][BUCKET_NAME]['aws-credentials']['profile'])
            self.assertEqual(None, config[STORAGE_CONFIG_KEY][S3H][BUCKET_NAME]['region'])
