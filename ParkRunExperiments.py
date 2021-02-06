#!usr/bin/python

import itertools
import json
import matplotlib.pyplot as pyplot
import numpy
import parser
import pylab
import scipy.stats as stats
import sys

from pprint import pprint

# exploring various statistical information keys from my running data
# average pace
# total mileage
# total time
# VO2Max estimate
# running economy analysis

# 1. Get Run instance Data
#    From a file, I/O input.
#    Possible formats: .csv, .txt
#    Parsing Data
#    into Appropriate Data Structure e.g. Dictionaries, Named Tuples, Lists etc.
args = sys.argv[1:]
help_txt = 'You can provide args [at least 2 or None at all]: ["InputFile.csv"] ["EventName"] ["year"]'
if len(args) == 0:
    print(help_txt)
    runfile = "./ParkRun_Pocket_Bishanga_Edmund.csv"
    event_name = "PocketParkRun"
    years = "2019"
elif len(args) >= 2:
    runfile = args[0]
    event_name = args[1]
    years = args[2].split(',') if len(args) > 2 else ['2019']
else:
    assert(help_txt)
print('Input validation: Inputs used: {}, {}, {}'.format(runfile, event_name, years))

def getFileContents(filepath):
    with open(filepath, 'r') as f:
        fdata = f.readlines()
    return fdata

rundata = getFileContents(runfile)

# parse data -> appropriate data structure
if not rundata:
    print("{} seems empty or it's data inaccessible".format(runfile))
    exit(1)

units = dict()
labels = list()
for header in rundata.pop(0).strip('\n').split(','):
    if header:
        label = header.split(' ')[0]
        unit = header.split(' ')[1].strip('(').strip(')') if len(header.split(' ')) == 2 else ''
        units.update({label:unit})
        labels.append(label)

rows = list()
for row in rundata:
    if len(row.strip('\n').strip(',')) > 0:
        vals = [val for val in row.strip('\n').split(',')]
        lrow = dict(zip(labels, vals))
        rows.append(lrow)

# 2. Calculate basic running Stats
y_values = list()
x_values = list()
event_x_axis = 'date'
event_y_axis = 'time'
for row in rows:
    if event_name in row.get('venue') and any(year in row.get('date') for year in years):
        str_time = row.get(event_y_axis)
        hr, mm, ss = tuple(str_time.split(':'))
        duration = round(float((int(hr) * 3600 + int(mm) * 60 + int(ss)) / 60), 1)
        y_values.append(duration)
        x_values.append(row.get(event_x_axis))
coordinates = tuple(zip(x_values, y_values))
print('title: {}'.format(event_name))
print('x_axis: {}'.format(event_x_axis))
print('y_axis: {}'.format(event_y_axis))
print('Coordinates: '); pprint(coordinates, width=1600)

# 2a: output basic stats summary
print('parkrun times: basic stats')
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

# Heart-rate based Vo2_max estimate
# Personal Data: HR_max, HR_rest
# Estimate: V02_max ~= 15.3 * HR_max / HR_rest

# Example: Ben: HR_max = 200, HR_rest = 45
# Estimate:
HR_max = 200
HR_rest = 45
print('MaxHR_runner_provided: {}'.format(HR_max))

# # Tanaka estimate of MaxHR
# Age = 36
# HR_max = 208 - (0.7 * Age)
# print('MaxHR_age: {}'.format(HR_max))

vo2_hr_estimate = 15.3 * HR_max / HR_rest
print('vo2_max HR potential ceiling: {}'.format(vo2_hr_estimate))

# VO2_max_per_parkrun
# using Cooper's estimate: VO2_max ~= (35.97 * d12) - 11.29
# where d12 = distances in miles, covered in 12min
# source: https://en.wikipedia.org/wiki/VO2_max

# Key assumptions:
# 1. Runner runs at average pace, entire parkrun
# 2. Parkrun is 5km in distance.
# 3. It might be wise to put in a pace adjustment constant
#    - assuming you'd run 12 min at a slightly faster pace than the ParkRun.

# V02_max ~= (k * 36 * 12 * 3.1/t_parkrun_min) - 11.3
# where, pace_adjustment, k ~= 1.02

k = 1.02
if 'parkrun' in event_name.lower():
    # evaluate vo2_data from parkrun times
    vo2_data = [round(((k * 36 * 12 * 3.1 / t_parkrun_minutes) - 11.3), 1) for t_parkrun_minutes in y_values]
    print('v02_max parkrun estimates: ')
    pprint(sorted(vo2_data), width=400)
    print('v02_max_parkrun_estimate: basic stats')
    pprint(stats.describe(vo2_data))

    # normalised v02_max data
    norm_vo2_data = [round((vo2_val / vo2_hr_estimate), 2) for vo2_val in vo2_data]
    print('Normalised v02_max parkrun estimates: ')
    pprint(norm_vo2_data, width=400)

    # plot vo2_data vs dates.
    pyplot.plot(
        x_values,
        norm_vo2_data,
        'x-', linewidth=3, color='g'
    )
    pyplot.xlabel('dates')
    pyplot.ylabel('Normalised V02_max Effort')
    pyplot.title('{event}: Normalised V02_max_Effort per Run'.format(event=event_name))
    pyplot.show()

# The Runner
# Key properties:
# + heart: believer|non-believer, courageous|fearful
# + mind: mature|immature, patient|impulsive
# + body: natural attributes: height, proportions, weight,  nurture attributes: diet


# 4. Provide Recommendations
