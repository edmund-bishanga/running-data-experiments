#!usr/bin/python

import pprint
import os

# Searching & I/O

# open file & get contents
# file = open("./john1_plaintext.txt")
# print(file.readlines())

# iteratively search contents - for keyword
keyword = "speak"
path = "./john1_plaintext.txt"
results = ['KEYWORD: "{}"'.format(keyword)]
file = open(path)

for line in file.readlines():
    if keyword in line:
        results.append(line.strip())
# print all instances of keyword
pprint.pprint(results, width=240)
