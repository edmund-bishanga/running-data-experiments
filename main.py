#!/usr/bin/python

from test_classes.Park import Park
from test_classes.ParkRunner import ParkRunner
from test_classes.ParkRun import ParkRun
from pprint import pprint

def main():
    print('this is the main program... Ta!')
    Space = Park("Eynesbury", temperature=15, precipitation=2, surface="mixed", inclination=2)
    print('Park: Venue: {}'.format(Space.venue))
    print('Park: Temp: {}'.format(Space.temperature))

    Runner = ParkRunner("Edmund M Bishanga", age=36, height=1.75, weight=67, resilience=2, consistency=2, restHR=45, maxHR=200)
    print("{}: VO2max_potential: {}".format(Runner.name, Runner.get_vo2max_potential()))
    print("{}: BMI: {}".format(Runner.name, Runner.get_bmi()))

    Race = ParkRun(park=Space, runner=Runner, distance_km=10, time_min=40)
    print("{}: 5km_time_min: {}".format(Runner.name, Race.get_t_parkrun_min()))
    print("{}: V02_current: {}".format(Runner.name, Race.get_vo2max_current()))

    normalised_effort = 100 * round((Race.get_vo2max_current() / Runner.get_vo2max_potential()), 2)
    print("{}: Normalised Effort: {}%".format(Runner.name, normalised_effort))

if __name__ == '__main__':
    main()