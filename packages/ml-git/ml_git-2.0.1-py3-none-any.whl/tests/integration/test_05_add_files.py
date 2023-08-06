"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import unittest
from stat import S_IWUSR, S_IREAD

import pytest

from ml_git.ml_git_message import output_messages
from ml_git.spec import get_spec_key
from tests.integration.helper import ML_GIT_DIR, create_spec, init_repository, ERROR_MESSAGE, MLGIT_ADD, \
    create_file, DATASETS, DATASET_NAME, MODELS, LABELS
from tests.integration.helper import clear, check_output, add_file, entity_init, yaml_processor


@pytest.mark.usefixtures('tmp_dir')
class AddFilesAcceptanceTests(unittest.TestCase):

    def set_up_add(self, repo_type=DATASETS):
        init_repository(repo_type, self)
        workspace = os.path.join(self.tmp_dir, repo_type, '{}-ex'.format(repo_type))
        clear(workspace)
        os.makedirs(workspace)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_01_add_files_to_dataset(self):
        entity_init(DATASETS, self)
        add_file(self, DATASETS, '', 'new')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_02_add_files_to_model(self):
        entity_init(MODELS, self)
        add_file(self, MODELS, '', 'new')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_03_add_files_to_labels(self):
        entity_init(LABELS, self)
        add_file(self, LABELS, '', 'new')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_04_add_files_with_bumpversion(self):
        entity_init(DATASETS, self)
        add_file(self, DATASETS, '--bumpversion', 'new')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_05_add_command_without_file_added(self):
        self.set_up_add()

        create_spec(self, DATASETS, self.tmp_dir)

        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_ADD % (DATASETS, DATASET_NAME, '')))
        self.assertIn(output_messages['INFO_NO_NEW_DATA_TO_ADD'], check_output(MLGIT_ADD % (DATASETS, DATASET_NAME, '--bumpversion')))

    def _check_index(self, index, files_in, files_not_in):
        with open(index, 'r') as file:
            added_file = yaml_processor.load(file)
            for file in files_in:
                self.assertIn(file, added_file)
            for file in files_not_in:
                self.assertNotIn(file, added_file)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_06_add_command_with_corrupted_file_added(self):
        entity_init(DATASETS, self)

        add_file(self, DATASETS, '--bumpversion', 'new')
        corrupted_file = os.path.join(self.tmp_dir, DATASETS, DATASET_NAME, 'newfile0')

        os.chmod(corrupted_file, S_IWUSR | S_IREAD)
        with open(corrupted_file, 'wb') as z:
            z.write(b'0' * 0)

        self.assertIn(output_messages['WARN_CORRUPTED_CANNOT_BE_ADD'], check_output(MLGIT_ADD % (DATASETS, DATASET_NAME, '--bumpversion')))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_07_add_command_with_multiple_files(self):
        self.set_up_add()

        create_spec(self, DATASETS, self.tmp_dir)
        workspace = os.path.join(self.tmp_dir, DATASETS, DATASET_NAME)

        os.makedirs(os.path.join(workspace, 'data'))

        create_file(workspace, 'file1', '0')
        create_file(workspace, 'file2', '1')
        create_file(workspace, 'file3', '1')

        self.assertIn(output_messages['INFO_ADDING_PATH'] % DATASETS,
                      check_output(MLGIT_ADD % (DATASETS, DATASET_NAME, os.path.join('data', 'file1'))))
        index = os.path.join(ML_GIT_DIR, DATASETS, 'index', 'metadata', DATASET_NAME, 'INDEX.yaml')
        self._check_index(index, ['data/file1'], ['data/file2', 'data/file3'])
        self.assertIn(output_messages['INFO_ADDING_PATH'] % DATASETS, check_output(MLGIT_ADD % (DATASETS, DATASET_NAME, 'data')))
        self._check_index(index, ['data/file1', 'data/file2', 'data/file3'], [])
        create_file(workspace, 'file4', '0')
        self.assertIn(output_messages['INFO_ADDING_PATH'] % DATASETS, check_output(MLGIT_ADD % (DATASETS, DATASET_NAME, '')))
        self._check_index(index, ['data/file1', 'data/file2', 'data/file3', 'data/file4'], [])

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_08_add_command_with_metric_option(self):
        repo_type = MODELS
        entity_name = '{}-ex'.format(repo_type)
        self.set_up_add(repo_type)

        create_spec(self, repo_type, self.tmp_dir)
        workspace = os.path.join(self.tmp_dir, repo_type, entity_name)

        os.makedirs(os.path.join(workspace, 'data'))

        create_file(workspace, 'file1', '0')

        metrics_options = '--metric Accuracy 1 --metric Recall 2'

        self.assertIn(output_messages['INFO_ADDING_PATH'] % repo_type, check_output(MLGIT_ADD % (repo_type, entity_name, metrics_options)))
        index = os.path.join(ML_GIT_DIR, repo_type, 'index', 'metadata', entity_name, 'INDEX.yaml')
        self._check_index(index, ['data/file1'], [])

        with open(os.path.join(workspace, entity_name + '.spec')) as spec:
            spec_file = yaml_processor.load(spec)
            spec_key = get_spec_key(repo_type)
            metrics = spec_file[spec_key].get('metrics', {})
            self.assertFalse(metrics == {})
            self.assertTrue(metrics['Accuracy'] == 1)
            self.assertTrue(metrics['Recall'] == 2)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_09_add_command_with_metric_for_wrong_entity(self):
        repo_type = DATASETS
        self.set_up_add()

        create_spec(self, repo_type, self.tmp_dir)
        workspace = os.path.join(self.tmp_dir, repo_type, DATASET_NAME)

        os.makedirs(os.path.join(workspace, 'data'))

        create_file(workspace, 'file1', '0')

        metrics_options = '--metric Accuracy 1 --metric Recall 2'

        self.assertIn(output_messages['INFO_ADDING_PATH'] % repo_type, check_output(MLGIT_ADD % (repo_type, DATASET_NAME, metrics_options)))
        index = os.path.join(ML_GIT_DIR, repo_type, 'index', 'metadata', DATASET_NAME, 'INDEX.yaml')
        self._check_index(index, ['data/file1'], [])

        with open(os.path.join(workspace, DATASET_NAME+'.spec')) as spec:
            spec_file = yaml_processor.load(spec)
            spec_key = get_spec_key(repo_type)
            metrics = spec_file[spec_key].get('metrics', {})
            self.assertTrue(metrics == {})

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir', 'create_csv_file')
    def test_10_add_command_with_metric_file(self):
        repo_type = MODELS
        entity_name = '{}-ex'.format(repo_type)
        self.set_up_add(repo_type)

        create_spec(self, repo_type, self.tmp_dir)
        workspace = os.path.join(self.tmp_dir, repo_type, entity_name)

        os.makedirs(os.path.join(workspace, 'data'))

        create_file(workspace, 'file1', '0')

        csv_file = os.path.join(self.tmp_dir, 'metrics.csv')

        self.create_csv_file(csv_file, {'Accuracy': 1, 'Recall': 2})

        metrics_options = '--metrics-file="{}"'.format(csv_file)

        self.assertIn(output_messages['INFO_ADDING_PATH'] % repo_type, check_output(MLGIT_ADD % (repo_type, entity_name, metrics_options)))
        index = os.path.join(ML_GIT_DIR, repo_type, 'index', 'metadata', entity_name, 'INDEX.yaml')
        self._check_index(index, ['data/file1'], [])

        with open(os.path.join(workspace, entity_name + '.spec')) as spec:
            spec_file = yaml_processor.load(spec)
            spec_key = get_spec_key(repo_type)
            metrics = spec_file[spec_key].get('metrics', {})
            self.assertFalse(metrics == {})
            self.assertTrue(metrics['Accuracy'] == 1)
            self.assertTrue(metrics['Recall'] == 2)
