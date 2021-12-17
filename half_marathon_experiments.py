#!usr/bin/python
"""
Half Marathon Post-Run Data Analysis:
Exploring various statistical information keys from my running data
+ average pace
+ total mileage
+ total time
+ VO2Max estimate
+ running economy analysis
"""

# pylint: disable=invalid-name
# pylint: disable=unused-import
# pylint: disable=missing-function-docstring

import itertools
import json
import sys
from pprint import pprint

import numpy
import pandas as pd
import pylab
import matplotlib.pyplot as pyplot
import scipy.stats as stats

from test_classes.park_runner import ParkRunner

# 1. Get Run instance Data
#    From a file, I/O input.
#    Possible formats: .csv, .txt
#    Parsing Data
#    into Appropriate Data Structure e.g. Dictionaries, Named Tuples, Lists etc.
runfile = "./test_data/half_marathon_bishanga_edmund.csv"

def get_file_contents(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        fdata = f.readlines()
    return fdata

# file_generator = (line.strip() for line in open(runfile, 'r'))
# for line in file_generator:
#     if line and line[0].isalnum():
#         print("'{}'".format(line))

# generator experiment: big data .csv processing
def collect_buffered_raw_data(unltd_raw_data_gen, max_length):
    ltd_raw_data = list()
    try:
        # get next raw data val, until buffer limit
        while len(ltd_raw_data) < max_length:
            ltd_raw_data.append(next(unltd_raw_data_gen))
    except StopIteration as drained:
        print(f'\nINFO: raw data emptied out: {len(ltd_raw_data)}')
        pprint(StopIteration)        
    finally:
        length_raw_data = len(ltd_raw_data)
        print(f'\nDEBUG: raw data length harvested: {len(ltd_raw_data)}')
    return (ltd_raw_data, length_raw_data)

def get_csv_column_raw_data(csv_file, heading, max_length=100):
    rows = (line for line in open(csv_file, 'r', encoding='utf-8'))
    row_items = (row.rstrip().split(',') for row in rows)
    
    # validate requested heading
    heading_keys = next(row_items)
    print(f'\nDEBUG: headings: {heading_keys}')
    assert heading in heading_keys, f'MissingHeadingErr: {heading} not in {heading_keys}'
    
    # get requested column data: raw
    row_dicts = (dict(zip(heading_keys, vals)) for vals in row_items)
    unltd_raw_data_gen = (
        row_dict.get(heading)
        for row_dict in row_dicts
    )
    # sum_raw_data = sum(unltd_raw_data_gen)

    # harvest up to the max_length: to a list
    ltd_raw_data, len_raw_data = collect_buffered_raw_data(unltd_raw_data_gen, max_length)

    # return a dictionary: of raw data
    col_raw_data = {heading: ltd_raw_data, 'length': len_raw_data}
    return col_raw_data

def transform_raw_to_int(raw_parkrun_times, times_heading):
    seconds_parkrun_times = raw_parkrun_times
    for i, val in enumerate(seconds_parkrun_times.get(times_heading)):
        s_val = ParkRunner.parse_race_timestr_to_seconds(val)
        seconds_parkrun_times.get(times_heading)[i] = s_val
    return seconds_parkrun_times

def main():
    """ Do ParkRun Data Experiments. """

    # 1: PROCESS LARGE CSV DATA: USING GENERATORS, DICTS
    parkrun_csv_file = './test_data/park_run_pocket_bishanga_edmund.csv'
    # get raw column data: 'times'
    times_heading = 'time (hh:mm:ss)'
    raw_parkrun_times = get_csv_column_raw_data(parkrun_csv_file, times_heading, max_length=30)
    print('\nDEBUG: raw_parkrun_times'); pprint(raw_parkrun_times)
    # transform the raw data: for statistical informational analysis
    # times: str -> int|seconds
    seconds_parkrun_times = transform_raw_to_int(raw_parkrun_times, times_heading)
    print('\nDEBUG: seconds_parkrun_times'); pprint(seconds_parkrun_times)

    # 2: PROCESS CSV DATA: USING PANDAS, ITERATORS, MATPLOTLIB
    hm_runfile = "./test_data/half_marathon_bishanga_edmund.csv"
    rundata = get_file_contents(hm_runfile)
    # use pandas to get rundata_frame
    run_dframe = pd.read_csv(hm_runfile)
    print('DEBUG: run_dframe:')
    pprint(run_dframe)
    # sys.exit(0)
    # parse data -> appropriate data structure
    if not rundata:
        print("{} seems empty or it's data inaccessible".format(hm_runfile))
        sys.exit(1)
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
    # 2. Calculate basic running Stats
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
    # 2a: output basic stats summary
    pprint(stats.describe(y_values))
    # 2b. Plot line graph
    pyplot.plot(x_values, y_values, 'o--r')
    pyplot.xlabel(event_x_axis)
    pyplot.ylabel(event_y_axis)
    pyplot.title(event_name)
    pyplot.show()
    # 2c. Plot normal distribution
    mean = round(numpy.mean(y_values), 2)
    print('mean: {}'.format(mean))

    std_dev = round(numpy.std(y_values), 4)
    print('std_dev: {}'.format(std_dev))

    variance = round(std_dev**2, 2)
    print('variance: {}'.format(variance))

    x_data = sorted(y_values)
    pyplot.plot(
        x_data,
        1/(std_dev * numpy.sqrt(2 * numpy.pi)) * numpy.exp( - (x_data - mean)**2 / (2 * std_dev**2) ),
        'o-', linewidth=3, color='r'
    )
    pyplot.xlabel('run times')
    pyplot.ylabel('likelihood')
    pyplot.title('{event}: estimated normal distribution'.format(event=event_name))
    pyplot.show()

    # 3. Do Running Economy Analysis

    # 4. Provide Recommendations

if __name__ == '__main__':
    main()
