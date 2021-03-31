#!usr/bin/python
"""
This Class: The ParkRun
Definition:
The event of a ParkRunner completing a Run in the Park.

Ingredients:
+ attributes of a parkrun event
+ appropriate methods: time, pace, 5k equivalence
"""

# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long

from pprint import pprint

from test_classes.Park import Park
from test_classes.ParkRunner import ParkRunner

PACE_ADJUST_5K_12MIN = 1.03
KMS_PER_MILE = 1.60934

class ParkRun(object):
    """
    Defines an Event/Race in the Park, by a Runner:
    distance covered, time taken, info gleaned
    """
    # Properties:
    # + sensible defaults.
    # + can be provided by user: not static.
    def __init__(self, park, runner, dist_miles, run_timestr):
        self.park = park
        self.runner = runner
        self.dist_miles = float(dist_miles)
        self.distance_km = round((float(dist_miles) * KMS_PER_MILE), 1)
        self.run_timestr = run_timestr
        self.t_parkrun_timestr = None
        self.vo2max_current = None
        self.t_parkrun_minutes = None
        self.t_parkrun_seconds = None
        self.time_min = None
        self.time_sec = None
        self.race_pace = None


    # Methods: Add on need-to-add basis.
    def parse_race_timestr_to_seconds(self, parkrun_time_str):
        """ convert hh:mm:ss into seconds """
        time_array = parkrun_time_str.strip().split(':')
        if len(time_array) == 3:
            race_time_seconds = 60 * 60 * int(time_array[0]) + 60 * int(time_array[1]) + int(time_array[2])
        else:
            assert 'invalid parkrun_time_str: {}'.format(parkrun_time_str)
        return race_time_seconds

    def convert_seconds_to_timestr_hh_mm_ss(self, t_seconds):
        """ from machine calculable seconds to human readable hh:mm:ss """
        assert t_seconds, 'provide valid time_in_seconds'
        print('DEBUG: t_seconds: {}'.format(t_seconds))
        # 1min == 60s, 1hr == 60 * 60s
        # get hours: t_sec: int divide by 60^2, hh = h_int, t_rem_2_s = t_sec - (h_int * 60^2)
        # get minutes: t_rem_2_s: int divide by 60^1; mm = m_int, t_rem_1_s = t_rem_2_s - (m_int * 60^1)
        # get remaining seconds: s_int = t_rem_1_s
        t_hours = int(t_seconds / (60 * 60))
        t_rem2_s = t_seconds - (t_hours * 60 * 60)
        t_mins = int(t_rem2_s / 60)
        t_seconds = t_rem2_s - (t_mins * 60)
        t_hr_str = '0' + str(t_hours) if t_hours < 10 else str(t_hours)
        t_min_str = '0' + str(t_mins) if t_mins < 10 else str(t_mins)
        t_sec_str = '0' + str(t_seconds) if t_seconds < 10 else str(t_seconds)
        timestr_hhmmss = ':'.join([t_hr_str, t_min_str, t_sec_str])
        print('DEBUG: t_hh_mm_ss: {}'.format(timestr_hhmmss))
        return timestr_hhmmss

    def convert_to_timestr_hh_mm_ss(self, t_min_float):
        """ convert float to hh:mm:ss format """
        # mins: left of decimal point
        # secs: right of decimal point * 60
        assert t_min_float, 'provide valid time_in_min_float'
        print('DEBUG: t_min_float: {}'.format(t_min_float))
        t_hr = '00'
        t_min, t_frac = str(t_min_float).split('.')
        if int(t_min) > 60:
            t_hr_float = round((float(t_min) / 60), 3)
            t_hr, t_rem_min = str(t_hr_float).split('.')
            t_hr = t_hr if int(t_hr) >= 10 else '0' + t_hr
            t_min = str(int(float(t_rem_min) * 0.06))
        t_sec = str((int(t_frac) * 6))
        timestr_hhmmss = ':'.join([t_hr, t_min, t_sec])
        print('DEBUG: t_hh_mm_ss: {}'.format(timestr_hhmmss))
        return timestr_hhmmss

    # Calculate time_sec
    def get_time_sec(self):
        if not self.time_sec:
            self.time_sec = self.parse_race_timestr_to_seconds(self.run_timestr)
        return self.time_sec

    # Calculate t_parkrun_seconds
    def get_t_parkrun_seconds(self):
        if not self.t_parkrun_seconds:
            self.t_parkrun_seconds = int(5 * self.get_time_sec() / self.distance_km)
        return self.t_parkrun_seconds

    # Calculate t_parkrun_minutes
    def get_t_parkrun_minutes(self):
        if not self.t_parkrun_minutes:
            self.t_parkrun_minutes = round((5 * self.get_time_sec() / (60 * self.distance_km)), 1)
        return self.t_parkrun_minutes

    # Calculate t_parkrun_hh_mm_ss
    def get_t_parkrun_timestr(self):
        if not self.t_parkrun_timestr:
            self.t_parkrun_timestr = self.convert_seconds_to_timestr_hh_mm_ss(self.get_t_parkrun_seconds())
        return self.t_parkrun_timestr

    # CalculateVO2MaxCurrent: from latest Parkrun time.
    def get_vo2max_current(self):
        if not self.vo2max_current:
            self.vo2max_current = round(((PACE_ADJUST_5K_12MIN * 36 * 12 * 3.1 * 60 / self.t_parkrun_seconds) - 11.3), 1)
        return self.vo2max_current

    # Calculate Pace: miles/min
    def get_race_pace(self):
        if not self.race_pace:
            self.race_pace = round((float(self.get_time_sec() / 60) / self.dist_miles), 2)
        return self.race_pace
