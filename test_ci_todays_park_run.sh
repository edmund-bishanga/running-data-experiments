#!/usr/bin/bash

# CI/CD: 
# Tests that should PASS: 100%
# before a change in todays_park_run.py is pushed to main Git Repo

cd ~/src/running-data-experiments

python ./todays_park_run.py 
python ./todays_park_run.py -p A1618581 -d 3.16 -t 00:21:07 -C False
python ./todays_park_run.py -p A1618582 -d 3.16 -t 00:31:07
python ./todays_park_run.py -p A1618583 -d 3.16 -t 00:26:07 -C True
pylint ./todays_park_run.py
