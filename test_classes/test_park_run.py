#!/usr/bin/python

""" Unit Tests for methods in Class: park_run.ParkRun. """

import unittest
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
        TestCase.assertEqual(self, first=3.16, second=self.parkrun.get_dist_miles())

    def test_parse_race_timestr_to_seconds(self):
        # input: '00:20:00', expOutput: 1200
        TestCase.assertEqual(self, 1200, self.parkrun.parse_race_timestr_to_seconds('00:20:00'))

    def tearDown(self):
        # clean up after unittest run
        pass
