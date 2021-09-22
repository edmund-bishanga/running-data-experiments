#!usr/bin/python

"""
This Class describes: The ParkRunner
The Athlete: Psychologically and Physiologically
Mind:
  + Resilience: basic,1|intermediate,2|senior,3|elite,4
  + Consistency: basic,1|intermediate,2|senior,3|elite,4
Body:
  + BMI: height & weight metric
  + Vo2_max_potential: HR-based.
"""

# pylint: disable=missing-function-docstring
# pylint: disable=invalid-name

DEFAULT_PARKRUN_SB = 1050  # "00:17:30"

class ParkRunner():
    """ The Athlete: key attributes and methods. """
    # Properties:
    # + sensible defaults...
    # + can be provided by user: not static.
    def __init__(self, name=None, age=37, height=1.75, weight=67, resilience=2,
            consistency=2, resting_hr=45, max_hr=195, parkrunner_details=None
        ):
        self.name = name
        self.age = age
        self.pr_height = height
        self.pr_weight = weight
        self.resting_hr = resting_hr
        self.max_hr = max_hr
        self.resilience = resilience
        self.consistency = consistency
        self.bmi = None
        self.t_bmi = None
        self.vo2max_potential = None
        self.t_parkrun_sb_seconds = DEFAULT_PARKRUN_SB
        self.t_parkrun_l4wks_seconds = None
        self.parkrunner_details = parkrunner_details

    # PARKRUNNER: METHODS: Add on need-to-add basis.

    # CalculateVO2MaxPotential: from HR data: recent Range.
    # https://en.wikipedia.org/wiki/VO2_max#The_heart_rate_ratio_method
    def get_vo2max_potential(self):
        if not self.vo2max_potential:
            self.vo2max_potential = round(
                15.3 * float(self.get_pr_max_hr() / self.get_pr_resting_hr()), 1
            )
        return self.vo2max_potential

    # CalculateBMI: from height & weight.
    # https://en.wikipedia.org/wiki/Body_mass_index
    def get_bmi(self):
        if not self.bmi:
            self.bmi = round(self.get_pr_weight() / (self.get_pr_height()**2), 2)
        return self.bmi

    # https://en.wikipedia.org/wiki/Nick_Trefethen
    def get_trefethen_bmi(self):
        if not self.t_bmi:
            self.t_bmi = round(
                (1.3 * self.get_pr_weight() / (self.get_pr_height()**2.5)), 2
            )
        return self.t_bmi

    # Use parkrunner details dictionary, to calculate bmi & v02max_potential
    def get_pr_max_hr(self):
        if self.parkrunner_details:
            self.max_hr = self.parkrunner_details.get('prVO2MaxDetails').get('max_hr_bpm')
        return self.max_hr

    def get_pr_resting_hr(self):
        if self.parkrunner_details:
            self.resting_hr = self.parkrunner_details.get('prVO2MaxDetails').get('resting_hr_bpm')
        return self.resting_hr

    def get_pr_weight(self):
        if self.parkrunner_details:
            self.pr_weight = self.parkrunner_details.get('prBMIDetails').get('weight_kg')
        return self.pr_weight

    def get_pr_height(self):
        if self.parkrunner_details:
            self.pr_height = self.parkrunner_details.get('prBMIDetails').get('height_m')
        return self.pr_height

    # Other Functions
    @staticmethod
    def parse_race_timestr_to_seconds(time_str):
        """ convert hh:mm:ss into seconds """
        t_array = time_str.strip().split(':')
        if len(t_array) != 3:
            assert "invalid time_str: {}".format(time_str)
        race_time_seconds = 60 * 60 * int(t_array[0]) + 60 * int(t_array[1]) + int(t_array[2])
        return race_time_seconds

    def get_pr_parkrun_sb_seconds(self):
        if self.parkrunner_details:
            self.t_parkrun_sb_seconds = self.parse_race_timestr_to_seconds(
                self.parkrunner_details.get('parkrun_sb')
            )
        return self.t_parkrun_sb_seconds

    def get_pr_parkrun_l4wks_seconds(self):
        if self.parkrunner_details:
            self.t_parkrun_l4wks_seconds = self.parse_race_timestr_to_seconds(
                self.parkrunner_details.get('parkrun_last4wks')
            )
        return self.t_parkrun_l4wks_seconds
