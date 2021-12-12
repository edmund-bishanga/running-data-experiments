#!/usr/bin/python
"""
Interactive Script:
+ Tests APIs of 'TodaysParkRun.py'
"""

# pylint: disable=line-too-long
# pylint: disable=multiple-statements  # DEBUG statements
# pylint: disable=unused-import
# pylint: disable=invalid-name

import argparse
import json
import re
from pprint import pprint

import requests

def validate_api_cmd(cmd):
    print('validate: api_cmd:'); pprint(cmd)
    err_msg = f'invalid api_cmd: {cmd}'
    assert 'python ' in cmd, err_msg

    reg_str = r"\w+ .\/Today"
    matched = re.search(reg_str, cmd)
    print('\nDEBUG: matched'); pprint(matched)
    reg_err_msg = f'invalid api_cmd format: expected regex: {reg_str} actual: {cmd}'
    assert matched, reg_err_msg

def run_api_check(relevant_inputs):
    outputs = relevant_inputs
    for key in relevant_inputs:
        print(relevant_inputs[key])
        # form API cmd
        api_cmd = 'python ./TodaysParkRun.py '
        api_cmd_suffix = relevant_inputs[key][1]
        api_cmd = api_cmd + " ".join(api_cmd_suffix)
        print(f'API_cmd: "{api_cmd}"')

        validate_api_cmd(api_cmd)

        # run it
        # response = requests.get(api_cmd)
        response = {'status_code': 101, 'text': 'work in progress...'}
        # response = {'status_code': 200, 'text': 'OK'}
        # response = {'status_code': 303, 'text': 'http: redirection, further action req'}
        # response = {'status_code': 404, 'text': 'http: client error, check cli_syntax'}
        # response = {'status_code': 505, 'text': 'http: server error, server failure'}

        # verify outcome
        outcome = 'FAIL'
        if response["status_code"] == 200:
            outcome = 'PASS'
        outputs[key].append(outcome)
        assert outcome == relevant_inputs[key][-1], f"unexpected result: {key}"
    print('\nDEBUG: outputs'); pprint(outputs)
    return outputs


def test_api_name(inputs_json_file):
    """ API: -n, --name: test various inputs """
    # read json input
    with open(inputs_json_file, 'r') as inputs_file:
        inputs_data = json.load(inputs_file)
    print('\nDEBUG: inputs_data'); pprint(inputs_data)

    # get relevant test input data
    option = '-n'
    relevant_inputs = dict()
    for key in inputs_data:
        if option in inputs_data[key]:
            relevant_inputs[key] = inputs_data[key]
    print('\nDEBUG: relevant_inputs'); pprint(relevant_inputs)

    # run test
    run_api_check(relevant_inputs)


def main():
    """ Interactive function: API Testing. """
    # Input validation
    args = argparse.ArgumentParser()
    args.add_argument(
        '-f', "--input-file", default='./data/InputData_TestTodaysParkRun.json',
        help='str: path to JSON inputs file'
    )
    inputs = args.parse_args()
    print('\nInput validation:')
    pprint(inputs)

    # Test APIs
    test_api_name(inputs.input_file)


if __name__ == '__main__':
    main()
