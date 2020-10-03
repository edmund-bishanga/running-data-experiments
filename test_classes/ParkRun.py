#!usr/bin/python

# The ParkRun
# The event of a ParkRunner completing a Run in the Park.

from test_classes.Park import Park
from test_classes.ParkRunner import ParkRunner
from pprint import pprint

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
        self.t_parkrun_min = None

    # Methods: Add on need-to-add basis.
    # Calculate t_parkrun_min
    def get_t_parkrun_min(self):
        if not self.t_parkrun_min:
            self.t_parkrun_min = 5 * self.time_min / self.distance_km
        return self.t_parkrun_min

    # CalculateVO2MaxCurrent: from latest Parkrun time.
    def get_vo2max_current(self):
        if not self.vo2max_current:
            self.vo2max_current = round(((1.03 * 36 * 12 * 3.1 / self.t_parkrun_min) - 11.3), 1)
        return self.vo2max_current
