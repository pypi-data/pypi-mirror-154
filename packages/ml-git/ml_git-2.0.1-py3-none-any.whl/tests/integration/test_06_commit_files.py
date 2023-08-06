"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import unittest

import pytest

from ml_git.ml_git_message import output_messages
from tests.integration.commands import MLGIT_COMMIT, MLGIT_ADD
from tests.integration.helper import check_output, add_file, ML_GIT_DIR, entity_init, create_spec, create_file, \
    init_repository, move_entity_to_dir, ERROR_MESSAGE, DATASETS, LABELS, MODELS, DATASET_NAME


@pytest.mark.usefixtures('tmp_dir')
class CommitFilesAcceptanceTests(unittest.TestCase):

    def _commit_entity(self, entity_type):
        entity_init(entity_type, self)
        add_file(self, entity_type, '--bumpversion', 'new')
        self.assertIn(output_messages['INFO_COMMIT_REPO'] % (os.path.join(self.tmp_dir, ML_GIT_DIR, entity_type, 'metadata'), entity_type + '-ex'),
                      check_output(MLGIT_COMMIT % (entity_type, entity_type + '-ex', '')))
        HEAD = os.path.join(self.tmp_dir, ML_GIT_DIR, entity_type, 'refs', entity_type + '-ex', 'HEAD')
        self.assertTrue(os.path.exists(HEAD))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_01_commit_files_to_dataset(self):
        self._commit_entity(DATASETS)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_02_commit_files_to_labels(self):
        self._commit_entity(LABELS)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_03_commit_files_to_model(self):
        self._commit_entity(MODELS)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_04_commit_command_with_version(self):
        init_repository(DATASETS, self)
        create_spec(self, DATASETS, self.tmp_dir)
        workspace = os.path.join(self.tmp_dir, DATASETS, DATASET_NAME)

        os.makedirs(os.path.join(workspace, 'data'))

        create_file(workspace, 'file1', '0')
        self.assertIn(output_messages['INFO_ADDING_PATH'] % DATASETS,
                      check_output(MLGIT_ADD % (DATASETS, DATASET_NAME, "")))
        self.assertIn(output_messages['INFO_COMMIT_REPO'] % (os.path.join(self.tmp_dir, ML_GIT_DIR, DATASETS, 'metadata'), DATASET_NAME),
                      check_output(MLGIT_COMMIT % (DATASETS, DATASET_NAME, '')))

        create_file(workspace, 'file2', '1')
        self.assertIn(output_messages['INFO_ADDING_PATH'] % DATASETS,
                      check_output(MLGIT_ADD % (DATASETS, DATASET_NAME, "")))

        self.assertIn(output_messages['ERROR_INVALID_VALUE_FOR'] % ('--version', '-10'),
                      check_output(MLGIT_COMMIT % (DATASETS, DATASET_NAME, ' --version=-10')))

        self.assertIn(output_messages['ERROR_INVALID_VALUE_FOR'] % ('--version', 'test'),
                      check_output(MLGIT_COMMIT % (DATASETS, DATASET_NAME, '--version=test')))

        self.assertIn(output_messages['INFO_COMMIT_REPO'] % (os.path.join(self.tmp_dir, ML_GIT_DIR, DATASETS, 'metadata'), DATASET_NAME),
                      check_output(MLGIT_COMMIT % (DATASETS, DATASET_NAME, '--version=2')))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_05_commit_command_with_deprecated_version_number(self):
        init_repository(DATASETS, self)
        create_spec(self, DATASETS, self.tmp_dir)
        workspace = os.path.join(self.tmp_dir, DATASETS, DATASET_NAME)
        os.makedirs(os.path.join(workspace, 'data'))
        create_file(workspace, 'file1', '0')
        self.assertIn(output_messages['INFO_ADDING_PATH'] % DATASETS,
                      check_output(MLGIT_ADD % (DATASETS, DATASET_NAME, "")))

        result = check_output(MLGIT_COMMIT % (DATASETS, DATASET_NAME, '--version-number=2'))

        self.assertIn(output_messages['ERROR_NO_SUCH_OPTION'] % '--version-number', result)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_06_commit_with_large_version_number(self):
        init_repository(DATASETS, self)
        create_spec(self, DATASETS, self.tmp_dir)
        self.assertIn(output_messages['ERROR_INVALID_VALUE_FOR'] % ('--version', '9999999999'),
                      check_output(MLGIT_COMMIT % (DATASETS, DATASET_NAME, ' --version=9999999999')))
        self.assertIn(output_messages['ERROR_INVALID_VALUE_FOR'] % ('--version', '9999999999'),
                      check_output(MLGIT_COMMIT % (MODELS, MODELS + '-ex', ' --version=9999999999')))
        self.assertIn(output_messages['ERROR_INVALID_VALUE_FOR'] % ('--version', '9999999999'),
                      check_output(MLGIT_COMMIT % (LABELS, LABELS + '-ex', ' --version=9999999999')))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_05_commit_tag_that_already_exists(self):
        entity_type = DATASETS
        self._commit_entity(entity_type)
        with open(os.path.join(self.tmp_dir, entity_type, entity_type + '-ex', 'newfile5'), 'wt') as z:
            z.write(str('0' * 100))
        self.assertIn(output_messages['INFO_ADDING_PATH'] % DATASETS, check_output(MLGIT_ADD % (entity_type, entity_type+'-ex', '')))
        self.assertIn(output_messages['INFO_TAG_ALREADY_EXISTS'] % 'computer-vision__images__datasets-ex__2',
                      check_output(MLGIT_COMMIT % (entity_type, entity_type+'-ex', '')))
        head_path = os.path.join(self.tmp_dir, ML_GIT_DIR, entity_type, 'refs', entity_type + '-ex', 'HEAD')
        self.assertTrue(os.path.exists(head_path))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_06_commit_entity_with_changed_dir(self):
        self._commit_entity(DATASETS)
        create_file(os.path.join(DATASETS, DATASET_NAME), 'newfile5', '0', '')
        move_entity_to_dir(self.tmp_dir, DATASET_NAME, DATASETS)
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_ADD % (DATASETS, DATASET_NAME, ' --bumpversion')))
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_COMMIT % (DATASETS, DATASET_NAME, '')))
