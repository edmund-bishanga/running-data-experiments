#!usr/bin/python

import json
import parser
from pprint import pprint
from scipy import stats
import sys

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
runfile = "./ParkRun_Pocket_Bishanga_Edmund.csv"

def getFileContents(filepath):
    with open(filepath, 'r') as f:
        fdata = f.readlines()
    # pprint({filepath: fdata})
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
print('UNITS:'); pprint(units, width=400)
print('LABELS'); pprint(labels, width=400)

rows = list()
for row in rundata:
    if len(row.strip('\n').strip(',')) > 0:
        vals = [val for val in row.strip('\n').split(',')]
        lrow = dict(zip(labels, vals))
        rows.append(lrow)
print('ROWS:'); pprint(rows, width=400)

# 2. Calculate basic running Stats
times = list()
event_search_str = 'pocket parkrun'
for row in rows:
    pprint(row)
    if event_search_str in row.get('venue'):
        str_time = row.get('time')
        hr, mm, ss = tuple(str_time.split(':'))
        duration = float((int(hr) * 3600 + int(mm) * 60 + int(ss)) / 60)
        times.append(duration)
print('TIMES: seconds'); pprint(times, width=400)

pprint(stats.describe(times))
# 3. Do Running Economy Analysis

# 4. Provide Recommendations


