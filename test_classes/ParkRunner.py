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


class ParkRunner(object):
    # Properties:
    # + sensible defaults...
    # + can be provided by user: not static.
    def __init__(self, name, age=37, height=1.75, weight=67, resilience=2, consistency=2, restHR=45, maxHR=200):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.restHR = restHR
        self.maxHR = maxHR 
        self.resilience = resilience
        self.consistency = consistency
        self.bmi = None
        self.vo2max_potential = None
        self.t_parkrun_pb_seconds = 1050  # "00:17:30" 5k Season's Best

    # Methods: Add on need-to-add basis.
    # CalculateBMI: from height & weight.
    def get_bmi(self):
        if not self.bmi:
            self.bmi = round(self.weight / (self.height**2), 2)
        return self.bmi

    # CalculateVO2MaxPotential: from HR data: recent Range.
    def get_vo2max_potential(self):
        if not self.vo2max_potential:
            self.vo2max_potential = round(15.3 * float(self.maxHR / self.restHR), 2)
        return self.vo2max_potential

    # Other
