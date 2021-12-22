#!/usr/bin/python

"""
Unit Tests for methods in Class: park_run.ParkRun.
+ run unit test on cmdline:
  python -m unittest discover -v -s <test_dir>
+ or via pytest:
  python -m pytest -v <test_dir>
"""

import pytest
from unittest import TestCase
from test_classes.park import Park
from test_classes.park_run import ParkRun
from test_classes.park_runner import ParkRunner

class TestParkRunMethods(TestCase):

    def setUp(self):
        # create relevant|necessary obj instances & pre-requisites
        self.parkrunner = ParkRunner()
        self.park = Park('peel_park', temperature=10, precipitation=2, surface="mixed", inclination=2)
        self.parkrun = ParkRun(self.park, self.parkrunner, dist_miles=3.16, run_timestr='00:19:30')

    def test_get_dist_miles(self):
        first = 3.16
        second = self.parkrun.get_dist_miles()
        TestCase.assertEqual(self, first, second)

    def test_parse_race_timestr_to_seconds(self):
        # input: '00:20:00', expOutput: 1200
        equiv_parts = [('00:20:00', 1200), ('00:00:01', 1), ('03:20:00', 12000)]
        for t_str, exp_seconds in equiv_parts:
            result = self.parkrun.parse_race_timestr_to_seconds(t_str)
            TestCase.assertEqual(self, exp_seconds, result)

    def tearDown(self):
        # clean up after unittest run
        pass
