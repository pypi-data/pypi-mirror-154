"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import unittest

import pytest

from tests.integration.commands import MLGIT_STATUS_DIRECTORY, MLGIT_ADD
from tests.integration.helper import check_output, init_repository, create_file
from ml_git.ml_git_message import output_messages


@pytest.mark.usefixtures('tmp_dir')
class StatusPathDirectoryAcceptanceTests(unittest.TestCase):

    def set_up_status(self, entity):
        init_repository(entity, self)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_01_status_after_put_on_new_file_in_dataset_without_directory(self):
        self.set_up_status('dataset')
        data_path = os.path.join(self.tmp_dir, 'dataset', 'dataset-ex', '')
        os.makedirs(data_path, exist_ok=True)
        create_file(data_path, 'file1', '0', '')

        self.assertRegex(check_output(MLGIT_STATUS_DIRECTORY % ('dataset', 'dataset-ex', '')),
                         r'Changes to be committed:\s+Untracked files:(\s|.)*file1(\s|.)*')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_02_status_after_put_on_new_file_in_dataset_with_directory(self):
        self.set_up_status('dataset')
        data_path = os.path.join(self.tmp_dir, 'dataset', 'dataset-ex', 'data')
        os.makedirs(data_path, exist_ok=True)
        create_file(data_path, 'file2', '0', '')
        self.assertRegex(check_output(MLGIT_STATUS_DIRECTORY % ('dataset', 'dataset-ex', 'data')),
                         r'Changes to be committed:\s+Untracked files:(\s|.)*file2(\s|.)*')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_03_status_after_put_more_than_one_file_in_dataset_with_directory(self):
        self.set_up_status('dataset')
        data_path = os.path.join(self.tmp_dir, 'dataset', 'dataset-ex', 'data')
        os.makedirs(data_path, exist_ok=True)
        create_file(data_path, 'file3', '0', '')
        create_file(data_path, 'file4', '0', '')
        self.assertRegex(check_output(MLGIT_STATUS_DIRECTORY % ('dataset', 'dataset-ex', 'data')),
                         r'Changes to be committed:\s+Untracked files:(\s|.)*data/\t->\t2 FILES(\s|.)*')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_04_status_after_put_more_than_one_file_in_dataset_with_invalid_directory(self):
        self.set_up_status('dataset')
        data_path = os.path.join(self.tmp_dir, 'dataset', 'dataset-ex', 'data')
        os.makedirs(data_path, exist_ok=True)
        create_file(data_path, 'file5', '0', '')
        create_file(data_path, 'file6', '0', '')
        self.assertIn(output_messages['ERROR_INVALID_STATUS_DIRECTORY'], check_output(MLGIT_STATUS_DIRECTORY % ('dataset', 'dataset-ex', 'invalid')))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_05_status_after_put_on_new_file_in_dataset_with_directory_and_add_command(self):
        self.set_up_status('dataset')
        data_path = os.path.join(self.tmp_dir, 'dataset', 'dataset-ex', 'data')
        os.makedirs(data_path, exist_ok=True)
        create_file(data_path, 'file7', '0', '')

        check_output(MLGIT_ADD % ('dataset', 'dataset-ex', '--bumpversion'))

        self.assertRegex(check_output(MLGIT_STATUS_DIRECTORY % ('dataset', 'dataset-ex', 'data')),
                         r'Changes to be committed:(\s|.)*New file: data(/|\\)file7(\s|.)*'
                         r'Untracked files:\n\nCorrupted files:')
