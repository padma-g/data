# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Author: Padma Gundapaneni @padma-g
Date: 9/13/2021
Description: This script contains unit tests for the parse_data.py script.
@input_file         filepath to the original csv that needs to be cleaned
@output_total_pop   filepath to output the data for the total population
@output_stratified  filepath to output the stratified data
python3 parse_data_test.py input_file output_total_pop output_stratified
"""

import unittest
import os
from .parse_data import clean_data

TEST_CASE_FILES = [
    # Input CSV and expected CSV files.
    ('test_data/sample_raw_data.csv', 'test_data/sample_count_expected.csv',
     'test_data/sample_percent_expected.csv')
]


class TestParseData(unittest.TestCase):
    """
    Tests the functions in parse_data.py.
    """

    def test_clean_data(self):
        """
        Tests the clean_data function.
        """
        module_dir_ = os.path.dirname(__file__)
        print(module_dir_)
        for input_file, expected_count,\
        expected_percent in TEST_CASE_FILES:
            print('\n')
            print('Input File: ' + input_file)
            test_csv = os.path.join(module_dir_, input_file)
            output_csv_count = os.path.join(
                module_dir_, (input_file[:-4] + '_output_count.csv'))
            output_csv_percent = os.path.join(module_dir_,
                                      (input_file[:-4] +\
                                        '_output_percent.csv'))
            clean_data(test_csv, output_csv_count, output_csv_percent)
            expected_count_file = os.path.join(module_dir_,\
                expected_count)
            expected_percent_file = os.path.join(module_dir_,\
                expected_percent)
        with open(output_csv_count, 'r') as test:
            test_str: str = test.read()
            with open(expected_count_file, 'r') as expected:
                expected_str: str = expected.read()
                self.assertEqual(test_str, expected_str)
        os.remove(output_csv_count)
        with open(output_csv_percent, 'r') as test:
            test_str: str = test.read()
            with open(expected_percent_file, 'r') as expected:
                expected_str: str = expected.read()
                self.assertEqual(test_str, expected_str)
        os.remove(output_csv_percent)
        print('Passed test!')


if __name__ == '__main__':
    unittest.main()
