#!/usr/bin/python

"""
Unit Tests for methods in Class: park_run.ParkRun.
+ run unit test on cmdline:
  python -m unittest discover -v -s <test_dir>
+ or via pytest:
  python -m pytest -v <test_dir>
"""

# pylint: disable=missing-function-docstring
# pylint: disable=import-error

from unittest import TestCase
from test_classes.Park import Park
from test_classes.park_run import ParkRun
from test_classes.park_runner import ParkRunner

PARKRUN_SCENARIOS = [
    ('00:18:58', 6.0, 3.16),
    # ('00:18:00', 6.0, 3.0),
    # ('00:36:00', 6.0, 6.0),
    # ('01:00:00', 6.0, 10.0)
]
TIMESTR_AND_SECONDS = [
    ('00:20:00', 1200),
    ('00:00:01', 1),
    ('03:20:00', 12000)
]

class TestParkRunMethods(TestCase):
    """
    Unit Tests for the Methods of Class: ParkRun
    """

    def setUp(self):
        # create relevant|necessary obj instances & pre-requisites
        self.parkrunner = ParkRunner()
        self.park = Park(
            'peel_park', temperature=10, precipitation=2,
            surface='mixed', inclination=2
        )
        self.parkrun = ParkRun(
            self.park, self.parkrunner, dist_miles=3.16,
            run_timestr='00:19:30'
        )

    def test_get_dist_miles_default_ok(self):
        first = 3.16
        second = self.parkrun.get_dist_miles()
        TestCase.assertEqual(self, first, second)

    def test_get_dist_miles_non_default(self):
        for run_timestr, pace, expected_miles in PARKRUN_SCENARIOS:
            print(
                f'\nScenario: run_timestr: {run_timestr}, \
                pace: {pace}, expected_miles: {expected_miles}'
            )
            self.parkrun = ParkRun(
                self.park, self.parkrunner,
                run_timestr=run_timestr, pace=pace
            )
            actual_miles = self.parkrun.get_dist_miles()
            TestCase.assertEqual(self, expected_miles, actual_miles)

    def test_parse_race_timestr_to_seconds(self):
        # input: '00:20:00', expOutput: 1200
        for t_str, exp_seconds in TIMESTR_AND_SECONDS:
            result = self.parkrun.parse_race_timestr_to_seconds(t_str)
            TestCase.assertEqual(self, exp_seconds, result)

    def tearDown(self):
        # clean up after unittest run
        pass
