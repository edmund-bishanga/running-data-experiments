#!/usr/bin/python

"""
Example pytest experiment
+ informed by prior test_coverage analysis
+ extensible|scalable data-driven test coverage
+ run as: pytest -v --capture=tee-sys <file_name>
"""

# pylint: disable=missing-function-docstring

from pprint import pprint
import pytest
import half_marathon_experiments
from half_marathon_experiments import HalfMarathonExpts

hm_expt = HalfMarathonExpts()

DATA_DIR = './test_data'

valid_paths = [
    ('half_marathon_bishanga_edmund.csv', 'Half Marathon'),
    ('input_data_test_todays_park_run.json', 'PocketPark'),
    ('parkrunner_details_A1618583.json', 'surName')
]
@pytest.mark.parametrize('valid_file_tuple', valid_paths)
def test_get_file_contents_valid_path(valid_file_tuple):
    valid_file, search_str = valid_file_tuple
    path = f"{DATA_DIR}/{valid_file}"
    file_content = hm_expt.get_file_contents(path)
    assert search_str in repr(file_content)

invalid_paths = [
    f'{DATA_DIR}/foobar.json',
    './configs/none.ini',
    './efg/hijk.csv',
    'abc.txt'
]
@pytest.mark.parametrize('invalid_path', invalid_paths)
def test_get_file_contents_invalid_path(invalid_path):
    with pytest.raises(FileNotFoundError):
        file_content = hm_expt.get_file_contents(invalid_path)
        pprint(file_content)
