"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import unittest

import pytest

from tests.integration.commands import MLGIT_COMMIT, MLGIT_ADD
from tests.integration.helper import check_output, add_file, ML_GIT_DIR, entity_init, create_spec, create_file, \
    init_repository
from tests.integration.output_messages import messages


@pytest.mark.usefixtures('tmp_dir')
class CommitFilesAcceptanceTests(unittest.TestCase):

    def _commit_entity(self, entity_type):
        entity_init(entity_type, self)
        add_file(self, entity_type, '--bumpversion', 'new')
        self.assertIn(messages[17] % (os.path.join(self.tmp_dir, ML_GIT_DIR, entity_type, 'metadata'),
                                      os.path.join('computer-vision', 'images', entity_type + '-ex')),
                      check_output(MLGIT_COMMIT % (entity_type, entity_type + '-ex', '')))
        HEAD = os.path.join(self.tmp_dir, ML_GIT_DIR, entity_type, 'refs', entity_type + '-ex', 'HEAD')
        self.assertTrue(os.path.exists(HEAD))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_01_commit_files_to_dataset(self):
        self._commit_entity('dataset')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_02_commit_files_to_labels(self):
        self._commit_entity('labels')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_03_commit_files_to_model(self):
        self._commit_entity('model')

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_04_commit_command_with_version(self):
        init_repository('dataset', self)
        create_spec(self, 'dataset', self.tmp_dir)
        workspace = os.path.join(self.tmp_dir, 'dataset', 'dataset-ex')

        os.makedirs(os.path.join(workspace, 'data'))

        create_file(workspace, 'file1', '0')
        self.assertIn(messages[13] % 'dataset',
                      check_output(MLGIT_ADD % ('dataset', 'dataset-ex', "")))
        self.assertIn(messages[17] % (os.path.join(self.tmp_dir, ML_GIT_DIR, 'dataset', 'metadata'),
                                      os.path.join('computer-vision', 'images', 'dataset' + '-ex')),
                      check_output(MLGIT_COMMIT % ('dataset', 'dataset' + '-ex', '')))

        create_file(workspace, 'file2', '1')
        self.assertIn(messages[13] % 'dataset',
                      check_output(MLGIT_ADD % ('dataset', 'dataset-ex', "")))

        self.assertIn(messages[96] % '-10',
                      check_output(MLGIT_COMMIT % ('dataset', 'dataset' + '-ex', ' --version=-10')))

        self.assertIn(messages[96] % 'test',
                      check_output(MLGIT_COMMIT % ('dataset', 'dataset' + '-ex', '--version=test')))

        self.assertIn(messages[17] % (os.path.join(self.tmp_dir, ML_GIT_DIR, 'dataset', 'metadata'),
                                      os.path.join('computer-vision', 'images', 'dataset' + '-ex')),
                      check_output(MLGIT_COMMIT % ('dataset', 'dataset' + '-ex', '--version=2')))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_05_commit_command_with_deprecated_version_number(self):
        init_repository('dataset', self)
        create_spec(self, 'dataset', self.tmp_dir)
        workspace = os.path.join(self.tmp_dir, 'dataset', 'dataset-ex')
        os.makedirs(os.path.join(workspace, 'data'))
        create_file(workspace, 'file1', '0')
        self.assertIn(messages[13] % 'dataset',
                      check_output(MLGIT_ADD % ('dataset', 'dataset-ex', "")))

        result = check_output(MLGIT_COMMIT % ('dataset', 'dataset' + '-ex', '--version-number=2'))

        self.assertIn(messages[106] % ('--version-number', '--version'), result)
        self.assertIn(messages[17] % (os.path.join(self.tmp_dir, ML_GIT_DIR, 'dataset', 'metadata'),
                                      os.path.join('computer-vision', 'images', 'dataset' + '-ex')), result)

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_06_commit_with_large_version_number(self):
        init_repository('dataset', self)
        create_spec(self, 'dataset', self.tmp_dir)
        self.assertIn(messages[96] % '9999999999',
                      check_output(MLGIT_COMMIT % ('dataset', 'dataset' + '-ex', ' --version=9999999999')))
        self.assertIn(messages[96] % '9999999999',
                      check_output(MLGIT_COMMIT % ('model', 'model' + '-ex', ' --version=9999999999')))
        self.assertIn(messages[96] % '9999999999',
                      check_output(MLGIT_COMMIT % ('labels', 'labels' + '-ex', ' --version=9999999999')))

    @pytest.mark.usefixtures('start_local_git_server', 'switch_to_tmp_dir')
    def test_05_commit_tag_that_already_exists(self):
        entity_type = 'dataset'
        self._commit_entity(entity_type)
        with open(os.path.join(self.tmp_dir, entity_type, entity_type + '-ex', 'newfile5'), 'wt') as z:
            z.write(str('0' * 100))
        self.assertIn(messages[13] % 'dataset', check_output(MLGIT_ADD % (entity_type, entity_type+'-ex', '')))
        self.assertIn(messages[104] % 'computer-vision__images__dataset-ex__2', check_output(MLGIT_COMMIT % (entity_type, entity_type+'-ex', '')))
        head_path = os.path.join(self.tmp_dir, ML_GIT_DIR, entity_type, 'refs', entity_type + '-ex', 'HEAD')
        self.assertTrue(os.path.exists(head_path))
