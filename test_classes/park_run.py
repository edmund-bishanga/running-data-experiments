#!usr/bin/python
"""
This Class describes The ParkRun
Definition:
The Real-time Temporal-Spatial Event
of a ParkRunner completing a Run in a specific Space: a Park.
Ingredients:
+ attributes of the Parkrun: a temporal-spatial event
+ appropriate methods: time, pace, 5k equivalence
"""

# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
# pylint: disable=invalid-name

from pprint import pprint

PACE_ADJUST_5K_12MIN = 1.03
KMS_PER_MILE = 1.60934
DEF_RUN_TIMESTR = '00:18:44'
DEF_DIST_MILES = 3.16

class ParkRun():
    """
    Defines an Event|Race in the Park, by a Runner:
    distance covered, time taken, info gleaned
    """
    # Properties:
    # + sensible defaults.
    # + can be provided by user: not static.
    def __init__(self, park, runner, dist_miles=None, run_timestr=None, pace=None):
        self.park = park
        self.runner = runner
        self.dist_miles = float(dist_miles) if dist_miles else None
        self.run_timestr = run_timestr
        self.race_pace_str = pace
        self.race_pace = None
        self.distance_km = None
        self.t_parkrun_timestr = None
        self.t_parkrun_minutes = None
        self.t_parkrun_seconds = None
        self.time_min = None
        self.time_sec = None
        self.vo2max_current = None

    # Given pace & time, calculate distance run
    def get_dist_miles(self):
        if not self.dist_miles:
            if self.race_pace:
                time_min = self.parse_race_timestr_to_seconds(self.get_run_timestr()) / 60
                self.dist_miles = round(float(time_min / self.race_pace), 2)
            else:
                self.dist_miles = DEF_DIST_MILES
        return self.dist_miles

    def get_run_timestr(self):
        if not self.run_timestr:
            if not self.race_pace:
                self.run_timestr = DEF_RUN_TIMESTR
            else:
                self.run_timestr = self.convert_seconds_to_timestr_hh_mm_ss(self.get_time_sec())
        return self.run_timestr

    # Calculate time_sec
    def get_time_sec(self):
        if not self.time_sec:
            if not self.race_pace:
                self.time_sec = self.parse_race_timestr_to_seconds(self.get_run_timestr())
            else:
                self.time_sec = round(float(self.get_dist_miles() * self.get_race_pace() * 60), 2)
        return self.time_sec

    # Calculate Pace: miles/min: float
    def get_race_pace(self):
        if not self.race_pace:
            self.race_pace = round((float(self.get_time_sec() / 60) / self.get_dist_miles()), 1)
        return self.race_pace

    # Calculate Pace Str: mm:ss miles/min
    def get_race_pace_str(self):
        if not self.race_pace_str:
            self.race_pace_str = self.convert_min_float_to_timestr_hh_mm_ss(self.get_race_pace())
            if self.race_pace_str.startswith('00:'):
                self.race_pace_str = self.race_pace_str.split('00:')[-1]
        return self.race_pace_str

    # Methods: Add on need-to-add basis.
    @staticmethod
    def parse_race_timestr_to_seconds(time_str):
        """ convert hh:mm:ss into seconds """
        t_array = time_str.strip().split(':')
        if len(t_array) != 3:
            assert f'invalid time_str: {time_str}'
        race_time_seconds = 60 * 60 * int(t_array[0]) + 60 * int(t_array[1]) + int(t_array[2])
        return race_time_seconds

    @staticmethod
    def convert_seconds_to_timestr_hh_mm_ss(t_seconds):
        """ from machine calculable seconds to human readable hh:mm:ss """
        assert t_seconds >= 0, 'provide valid time_in_seconds'
        t_hours = int(t_seconds / (60 * 60))
        t_rem2_s = t_seconds - (t_hours * 60 * 60)
        t_mins = int(t_rem2_s / 60)
        t_seconds = t_rem2_s - (t_mins * 60)
        t_hr_str = '0' + str(t_hours) if t_hours < 10 else str(t_hours)
        t_min_str = '0' + str(t_mins) if t_mins < 10 else str(t_mins)
        t_sec_str = '0' + str(t_seconds) if t_seconds < 10 else str(t_seconds)
        timestr_hhmmss = ':'.join([t_hr_str, t_min_str, t_sec_str])
        return timestr_hhmmss

    @staticmethod
    def convert_min_float_to_timestr_hh_mm_ss(t_min_float):
        """ convert float to hh:mm:ss format """
        # mins: left of decimal point
        # secs: right of decimal point * 60
        assert t_min_float, 'provide valid time_in_min_float'
        t_hr = '00'
        t_min, t_frac = str(t_min_float).split('.')
        if int(t_min) > 60:
            t_hr_float = round((float(t_min) / 60), 3)
            t_hr, t_rem_min = str(t_hr_float).split('.')
            t_hr = t_hr if int(t_hr) >= 10 else '0' + t_hr
            t_min = str(int(float(t_rem_min) * 0.06))
        t_min = '0' + t_min if float(t_min) < 10 else t_min
        t_sec = str((int(t_frac) * 6))
        t_sec = '0' + t_sec if len(t_sec) < 2 else t_sec
        timestr_hhmmss = ':'.join([t_hr, t_min, t_sec])
        return timestr_hhmmss

    # Calculate t_parkrun_seconds
    def get_t_parkrun_seconds(self):
        if not self.t_parkrun_seconds:
            self.t_parkrun_seconds = int(5 * self.get_time_sec() / self.get_distance_km())
        return self.t_parkrun_seconds

    # Calculate t_parkrun_minutes
    def get_t_parkrun_minutes(self):
        if not self.t_parkrun_minutes:
            self.t_parkrun_minutes = round((5 * self.get_time_sec() / (60 * self.get_distance_km())), 1)
        return self.t_parkrun_minutes

    # Calculate t_parkrun_hh_mm_ss
    def get_t_parkrun_timestr(self):
        if not self.t_parkrun_timestr:
            self.t_parkrun_timestr = self.convert_seconds_to_timestr_hh_mm_ss(self.get_t_parkrun_seconds())
        return self.t_parkrun_timestr

    # CalculateVO2MaxCurrent: from latest Parkrun time.
    def get_vo2max_current(self):
        if not self.vo2max_current:
            self.vo2max_current = round(((PACE_ADJUST_5K_12MIN * 36 * 12 * 3.1 * 60 / self.get_t_parkrun_seconds()) - 11.3), 1)
        return self.vo2max_current

    def get_distance_km(self):
        if not self.distance_km:
            self.distance_km = round((float(self.get_dist_miles()) * KMS_PER_MILE), 1)
        return self.distance_km
