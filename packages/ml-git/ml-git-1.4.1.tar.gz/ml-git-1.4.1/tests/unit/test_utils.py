"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import Mock

import humanize
import pytest

from ml_git.utils import json_load, yaml_load, yaml_save, RootPathException, get_root_path, change_mask_for_routine, \
    ensure_path_exists, yaml_load_str, get_yaml_str, run_function_per_group, unzip_files_in_directory, \
    remove_from_workspace, group_files_by_path, remove_other_files, remove_unnecessary_files


@pytest.mark.usefixtures('tmp_dir', 'switch_to_test_dir', 'yaml_str_sample', 'yaml_obj_sample')
class UtilsTestCases(unittest.TestCase):
    def test_json_load(self):
        jsn = {}
        self.assertFalse(bool(jsn))
        jsn = json_load('./udata/data.json')
        self.assertEqual(jsn['dataset']['categories'], 'imgs')
        self.assertEqual(jsn['dataset']['name'], 'dataex')
        self.assertEqual(jsn['dataset']['version'], 1)
        self.assertTrue(bool(jsn))

    def test_yaml_load(self):
        yal = {}
        self.assertFalse(bool(yal))
        yal = yaml_load('./udata/data.yaml')
        self.assertTrue(bool(yal))
        self.assertEqual(yal['store']['s3']['mlgit-datasets']['region'], 'us-east-1')

    def test_yaml_load_str(self):
        obj = yaml_load_str(self.yaml_str_sample)
        self.assertEqual(obj['store']['s3h']['bucket_test']['aws-credentials']['profile'], 'profile_test')
        self.assertEqual(obj['store']['s3h']['bucket_test']['region'], 'region_test')

    def test_get_yaml_str(self):
        self.assertEqual(self.yaml_obj_sample['store']['s3h']['bucket_test']['aws-credentials']['profile'], 'profile_test')
        self.assertEqual(self.yaml_obj_sample['store']['s3h']['bucket_test']['region'], 'region_test')
        self.assertEqual(get_yaml_str(self.yaml_obj_sample), self.yaml_str_sample)

    def test_yaml_save(self):

        with tempfile.TemporaryDirectory() as tmpdir:
            arr = tmpdir.split('\\')
            temp_var = arr.pop()

            yaml_path = os.path.join(tmpdir, 'data.yaml')

            shutil.copy('udata/data.yaml', yaml_path)

            yal = yaml_load(yaml_path)

            temp_arr = yal['dataset']['git'].split('.')
            temp_arr.pop()
            temp_arr.pop()
            temp_arr.append(temp_var)
            temp_arr.append('git')
            # create new git variable
            new_git_var = '.'.join(temp_arr)

            self.assertFalse(yal['dataset']['git'] == new_git_var)

            yal['dataset']['git'] = new_git_var

            yaml_save(yal, yaml_path)
            self.assertTrue(yal['dataset']['git'] == new_git_var)

    def test_get_root_path(self):

        path = get_root_path()
        yaml_path_src = os.path.join(path, '.ml-git', 'config.yaml')
        yaml_path_dst = os.path.join(path, '.ml-git', 'coasdasdasnfig.ylma')
        os.rename(yaml_path_src, yaml_path_dst)
        self.assertRaises(RootPathException, lambda: get_root_path())
        os.rename(yaml_path_dst, yaml_path_src)

    def test_change_mask_for_routine(self):

        default_path_permissions = ['777']
        is_linux = sys.platform.startswith('linux')
        if is_linux:
            default_path_permissions = ['775', '755']
        all_permissions = '777'
        path = os.path.join(self.tmp_dir, 'test_permission')

        shared_path = True

        with change_mask_for_routine(shared_path):
            ensure_path_exists(path)
            st_mode = oct(os.stat(path).st_mode)[-3:]
            if is_linux:
                self.assertNotIn(st_mode, default_path_permissions)
            self.assertEqual(st_mode, all_permissions)
            shutil.rmtree(path)

        ensure_path_exists(path)
        st_mode = oct(os.stat(path).st_mode)[-3:]
        self.assertIn(st_mode, default_path_permissions)
        shutil.rmtree(path)

        shared_path = False

        with change_mask_for_routine(shared_path):
            ensure_path_exists(path)
            st_mode = oct(os.stat(path).st_mode)[-3:]
            self.assertIn(st_mode, default_path_permissions)
            if is_linux:
                self.assertNotEqual(st_mode, all_permissions)
            shutil.rmtree(path)

    def test_run_function_per_group(self):
        mock_function = Mock(return_value=False)
        args = {}
        mock_iterable = [None]
        n = 10
        self.assertFalse(run_function_per_group(mock_iterable, n, function=mock_function, arguments=args))
        mock_function.assert_called()

        mock_function2 = Mock(return_value=True)
        self.assertTrue(run_function_per_group(mock_iterable, n, function=mock_function2, arguments=args))
        mock_function2.assert_called()

        self.assertTrue(run_function_per_group(mock_iterable, n, function=mock_function, arguments=args,
                                               exit_on_fail=False))
        mock_function.assert_called()

    def test_unzip_files_in_directory(self):
        zip_path = os.path.join('unzip', 'zipped.zip')
        file_path = os.path.join('unzip', 'zipped', 'zip-file.txt')
        self.assertTrue(os.path.exists(zip_path))
        self.assertFalse(os.path.exists(file_path))
        unzip_files_in_directory('unzip')
        self.assertFalse(os.path.exists(zip_path))
        self.assertTrue(os.path.exists(file_path))

    def test_remove_from_workspace(self):
        img = 'image.jpg'
        data_path = os.path.join(self.tmp_dir, 'data')
        ensure_path_exists(data_path)
        file1 = os.path.join(self.tmp_dir, img)
        file2 = os.path.join(data_path, img)
        with open(file1, 'w'), open(file2, 'w'):
            pass
        self.assertTrue(os.path.exists(file1))
        self.assertTrue(os.path.exists(file2))
        remove_from_workspace({img}, self.tmp_dir, 'dataex')
        self.assertFalse(os.path.exists(file1))
        self.assertFalse(os.path.exists(file2))

    def test_group_files_by_path(self):
        files = ['images1/example.jpg', 'images1/example2.jpg', 'example-x.jpg', 'images2/example3.jpg']
        group_files = group_files_by_path(files)
        keys = group_files.keys()
        images_one = 'images1'
        images_two = 'images2'
        images_three = ''
        self.assertIn(images_one, keys)
        self.assertIn(images_two, keys)
        self.assertIn(images_three, keys)
        self.assertTrue(len(group_files[images_one]) == 2)
        self.assertTrue(len(group_files[images_two]) == 1)
        self.assertTrue(len(group_files[images_three]) == 1)

    def test_remove_unnecessary_files(self):
        data_path = os.path.join(self.tmp_dir, 'data')
        os.mkdir(data_path)
        file1 = os.path.join(data_path, 'image1.jpg')
        file2 = os.path.join(data_path, 'image2.jpg')
        with open(os.path.join(file1), 'wt') as file:
            file.write('0' * 2048)
        with open(os.path.join(file2), 'wt') as file:
            file.write('1' * 2048)

        self.assertTrue(os.path.exists(file1))
        self.assertTrue(os.path.exists(file2))
        total_count, total_reclaimed_space = remove_unnecessary_files(['image1.jpg'], self.tmp_dir)
        expected_deleted_files = 58
        self.assertEqual(total_count, expected_deleted_files)
        expected_reclaimed_space = humanize.naturalsize(12860387)
        self.assertEqual(humanize.naturalsize(total_reclaimed_space), expected_reclaimed_space)

    def test_remove_other_files(self):
        file1 = os.path.join(self.tmp_dir, 'image1.jpg')
        file2 = os.path.join(self.tmp_dir, 'image2.jpg')
        with open(file1, 'w'), open(file2, 'w'):
            pass
        self.assertTrue(os.path.exists(file1))
        self.assertTrue(os.path.exists(file2))
        remove_other_files(['image1.jpg'], self.tmp_dir)
        self.assertTrue(os.path.exists(file1))
        self.assertFalse(os.path.exists(file2))
