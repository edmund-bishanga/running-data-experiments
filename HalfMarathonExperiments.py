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


# 1. Get Run instance Data
#    From a file, I/O input.
#    Possible formats: .csv, .txt
#    Parsing Data
#    into Appropriate Data Structure e.g. Dictionaries, Named Tuples, Lists etc.
runfile = "./data/HalfMarathonBishangaEdmund.csv"

def get_file_contents(filepath):
    with open(filepath, 'r') as f:
        fdata = f.readlines()
    return fdata

file_generator = (line.strip() for line in open(runfile, 'r'))
for line in file_generator:
    if line and line[0].isalnum():
        print("'{}'".format(line))

rundata = get_file_contents(runfile)


# use pandas to get rundata_frame
run_dframe = pd.read_csv(runfile)
print('DEBUG: run_dframe:')
pprint(run_dframe)
# sys.exit(0)

# parse data -> appropriate data structure
if not rundata:
    print("{} seems empty or it's data inaccessible".format(runfile))
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
