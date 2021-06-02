#!usr/bin/python
"""
Half Marathon Post-Run Data Analysis: using Pandas

Exploring various statistical information keys from my running data
+ average pace
+ total mileage
+ total time
+ VO2Max estimate
+ running economy analysis
"""

# pylint: disable=invalid-name
# pylint: disable=unused-import
# pylint: disable=multiple-statements
# pylint: disable=missing-function-docstring

import argparse
import itertools
import json
import sys
from pprint import pprint

import matplotlib.pyplot as pyplot
import numpy
import pandas as pd
import pylab
import requests
import scipy.stats as stats
from requests.auth import HTTPBasicAuth

# 1. Get Run instance Data
#    From a file, I/O input.
#    Possible formats: .csv, .txt
#    Parsing Data
#    into Appropriate Data Structure e.g. Dictionaries, Named Tuples, Lists etc.
runfile = "./data/HalfMarathonBishangaEdmund.csv"

# def get_file_contents(filepath):
#     with open(filepath, 'r') as f:
#         fdata = f.readlines()
#     return fdata

# file_generator = (line.strip() for line in open(runfile, 'r'))
# for line in file_generator:
#     if line and line[0].isalnum():
#         print("'{}'".format(line))

# rundata = get_file_contents(runfile)

def parse_input_args():
    args = argparse.ArgumentParser()
    args.add_argument(
        '-f', "--run-file-path",
        default="./data/HalfMarathonBishangaEdmund.csv",
        help='str: filepath with RunData: CSV'
    )
    args.add_argument(
        '-l', "--run-url-link",
        default="https://www.strava.com/activities/4933282708",
        help='str: URL link for a run event: e.g. Strava'
    )
    inputs = args.parse_args()
    return inputs

def validate_inputs(inputs):
    assert inputs.run_file_path, "missing RunData filepath"
    assert '.csv' in inputs.run_file_path, "invalid file format: .csv expected"

# use pandas to get rundata_frame
def get_rundata_from_file(runfilepath):
    run_dframe = pd.read_csv(runfilepath)
    if run_dframe is None or not isinstance(run_dframe, pd.DataFrame):
        print("run_dframe: empty or invalid: DataFrame expected.\n{}".format(run_dframe))
        sys.exit(1)
    # print('DEBUG: run_dframe:'); pprint(run_dframe)
    return run_dframe

def get_rundata_from_url(run_url):
    # get appropriate json: requests
    response = requests.get(run_url, auth=HTTPBasicAuth('me.bishanga@gmail.com', 'gm!XYZ47'))
    # response = requests.get(run_url)
    print('DEBUG: response: entire'); pprint(response)
    print('DEBUG: response: status_code'); pprint(response.status_code)
    # assert '{' in response, "empty json, no rundata from {}".format(run_url)
    # print('DEBUG: response: json'); pprint(response.json())
    # print('DEBUG: response: text'); pprint(response.text)
    print('DEBUG: response: header'); pprint(response.headers)
    sys.exit(0)

    # convert json to data_frame: pandas
    run_dframe = pd.read_json(response.json())
    if run_dframe is None or not isinstance(run_dframe, pd.DataFrame):
        print("run_dframe: empty or invalid: DataFrame expected.\n{}".format(run_dframe))
        sys.exit(1)
    # print('DEBUG: run_dframe:'); pprint(run_dframe)
    return run_dframe

def main():
    # 0. Input validation
    inputs = parse_input_args()
    validate_inputs(inputs)

    # 1. Process HM Data
    # 1a: parse data -> appropriate data structure
    if inputs.run_file_path:
        listed_run_dframe = get_rundata_from_file(inputs.run_file_path)
        print('DEBUG: listed_run_dframe'); pprint(listed_run_dframe)

    if inputs.run_url_link:
        strava_run_dframe = get_rundata_from_url(inputs.run_url_link)
        print('DEBUG: strava_run_dframe'); pprint(strava_run_dframe)
    sys.exit(0)

    units = dict()
    labels = list()
    for header in rundata.pop(0).strip('\n').split(','):
        if header:
            label = header.split(' ')[0]
            unit = header.split(' ')[1].strip('(').strip(')') if len(header.split(' ')) == 2 else ''
            units.update({label:unit})
            labels.append(label)

    rows = list()
    iter_rundata = iter(rundata)
    done = False
    while not done:
        try:
            row = next(iter_rundata)
        except StopIteration:
            done = True
        else:
            if len(row.strip('\n').strip(',')) > 0:
                vals = row.strip('\n').split(',')
                lrow = dict(zip(labels, vals))
                rows.append(lrow)

    # 1b. Calculate basic running Stats
    y_values = list()
    x_values = list()
    event_name = 'Cambridge Half Marathon'
    event_x_axis = 'date'
    event_y_axis = 'time'

    iter_rows = iter(rows)
    done = False
    while not done:
        try:
            row = next(iter_rows)
        except StopIteration:
            done = True
        else:
            if event_name in row.get('venue'):
                str_time = row.get(event_y_axis)
                hr, mm, ss = tuple(str_time.split(':'))
                duration = round(float((int(hr) * 3600 + int(mm) * 60 + int(ss)) / 60), 1)
                y_values.append(duration)
                x_values.append(row.get(event_x_axis))
    coordinates = tuple(zip(x_values, y_values))
    print('title: {}'.format(event_name))
    print('x_axis: {}'.format(event_x_axis))
    print('y_axis: {}'.format(event_y_axis))
    print('Coordinates: ')

    pprint(coordinates, width=1600)

    # 1c: output basic stats summary
    pprint(stats.describe(y_values))

    # 1d. Plot line graph
    pyplot.plot(x_values, y_values, 'o--r')
    pyplot.xlabel(event_x_axis)
    pyplot.ylabel(event_y_axis)
    pyplot.title(event_name)
    pyplot.show()

    # 1e. Plot normal distribution
    mean = round(numpy.mean(y_values), 2)
    print('mean: {}'.format(mean))

    std_dev = round(numpy.std(y_values), 4)
    print('std_dev: {}'.format(std_dev))

    variance = round(std_dev**2, 2)
    print('variance: {}'.format(variance))

    x_data = sorted(y_values)
    pyplot.plot(
        x_data,
        1/(std_dev * numpy.sqrt(2 * numpy.pi)) * numpy.exp(-(x_data - mean)**2 / (2 * std_dev**2)),
        'o-', linewidth=3, color='r'
    )
    pyplot.xlabel('run times')
    pyplot.ylabel('likelihood')
    pyplot.title('{event}: estimated normal distribution'.format(event=event_name))
    pyplot.show()

    # 2. Do Running Economy Analysis

    # 3. Provide Recommendations


if __name__ == '__main__':
    main()
