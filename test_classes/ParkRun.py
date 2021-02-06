#!usr/bin/python

# The ParkRun
# The event of a ParkRunner completing a Run in the Park.

from test_classes.Park import Park
from test_classes.ParkRunner import ParkRunner
from pprint import pprint

PACE_ADJUST_5K_12MIN = 1.03

class ParkRun(object):
    # Properties:
    # + sensible defaults.
    # + can be provided by user: not static.
    def __init__(self, park, runner, distance_km, time_min):
        self.park = park
        self.runner = runner
        self.distance_km = distance_km
        self.time_min = float(time_min)
        self.vo2max_current = None
        self.t_parkrun_minutes = None
        self.t_parkrun_timestr = None

    # Methods: Add on need-to-add basis.

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

    # Calculate t_parkrun_minutes
    def get_t_parkrun_minutes(self):
        if not self.t_parkrun_minutes:
            self.t_parkrun_minutes = round((5 * self.time_min / self.distance_km), 1)
        return self.t_parkrun_minutes

    # Calculate t_parkrun_minutes
    def get_t_parkrun_timestr(self):
        if not self.t_parkrun_timestr:
            self.t_parkrun_timestr = self.convert_to_timestr_hh_mm_ss(self.get_t_parkrun_minutes())
        return self.t_parkrun_timestr

    # CalculateVO2MaxCurrent: from latest Parkrun time.
    def get_vo2max_current(self):
        if not self.vo2max_current:
            self.vo2max_current = round(((PACE_ADJUST_5K_12MIN * 36 * 12 * 3.1 / self.t_parkrun_minutes) - 11.3), 1)
        return self.vo2max_current
