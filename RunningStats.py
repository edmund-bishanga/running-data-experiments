#!usr/bin/python

import json
import parser
from pprint import pprint
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
    pprint({filepath: fdata})
    return fdata

rundata = getFileContents(runfile)

# parse data -> appropriate data structure
headings = list()
if rundata:
    for word in rundata[0].strip('\n').split(','):
        headings.append(word)
pprint(headings)

# 2. Calculate basic running Stats

# 3. Do Running Economy Analysis

# 4. Provide Recommendations


