#!/usr/bin/python
"""
Interactive Script:
+ Takes Event and Athlete Details
+ Provides a Summary of ParkRun Analysis Info
+ Normalised Insights
"""

# pylint: disable=line-too-long

import argparse
import sys
from pprint import pprint

from test_classes.Park import Park
from test_classes.ParkRun import ParkRun
from test_classes.ParkRunner import ParkRunner


def main():
    """ Interactive function: Inputs event details, provides normalised insights. """
    # Example input format
    # python3 ./TodaysParkRun.py -a "Bishanga, EM" -t 00:18:18 -d 3.1 -s "PocketPark"
    # python3 ./TodaysParkRun.py --athlete "Bishanga, EM" --time 00:18:18 --distance 3.1 --space "PocketPark"
    args = argparse.ArgumentParser()
    args.add_argument(
        '-a', "--athlete", default='Bishanga, EM', help='str: Name of Athlete'
    )
    args.add_argument(
        '-d', "--distance", default=3.1, help='float: Distance in Miles'
    )
    args.add_argument(
        '-t', "--time", default=20, help='strtime: RunTime in hh:mm:ss'
    )
    args.add_argument(
        '-s', "--space", default="PocketPark", help="str: Park"
    )
    args.add_argument(
        '-T', "--temperature", default=10, help="int: Temperature on the day"
    )
    inputs = args.parse_args()
    print('\nInput validation:')
    pprint(inputs)

    park_name = inputs.space
    parkrunner_name = inputs.athlete
    parkrun_time = inputs.time
    parkrun_distance = inputs.distance
    parkrun_temp = inputs.temperature

    # process run details
    Space = Park(park_name, temperature=parkrun_temp, precipitation=2, surface="mixed", inclination=2)
    print('\nPark: Venue: {}'.format(Space.venue))
    print('Park: Temp: {} degCelcius'.format(Space.temperature))

    Runner = ParkRunner(parkrunner_name)    # pylint: disable=no-value-for-parameter
    print("\n{}: VO2max_potential: {}".format(Runner.name, Runner.get_vo2max_potential()))
    print("{}: BMI: {}".format(Runner.name, Runner.get_bmi()))

    Race = ParkRun(park=Space, runner=Runner, dist_miles=float(parkrun_distance), run_timestr=parkrun_time)
    print("\n{}: Time_run_today: in hh:mm:ss {}".format(Runner.name, parkrun_time))
    print("{}: Estimated Pace: {} min/mile".format(Runner.name, Race.get_race_pace()))
    print("{}: Equivalent 5km_time: in hh:mm:ss {}".format(Runner.name, Race.get_t_parkrun_timestr()))
    print("{}: Estimated V02_current: {}".format(Runner.name, Race.get_vo2max_current()))

    normalised_effort = round(100 * (Race.get_vo2max_current() / Runner.get_vo2max_potential()), 1)
    print("{}: Normalised Effort: {}%\n".format(Runner.name, normalised_effort))

if __name__ == '__main__':
    main()
