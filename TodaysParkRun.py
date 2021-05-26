#!/usr/bin/python
"""
Interactive Script:
+ Takes Event and Athlete Details
+ Provides a Summary of ParkRun Analysis Info
+ Normalised Insights
"""

# pylint: disable=line-too-long
# pylint: disable=invalid-name

import argparse
import sys
from pprint import pprint

from test_classes.Park import Park, TarRoad
from test_classes.ParkRun import ParkRun
from test_classes.ParkRunner import ParkRunner


def main():
    """ Interactive function: Inputs event details, provides normalised insights. """
    # Example input format
    # python3 ./TodaysParkRun.py -n "Bishanga, EM" -t 00:18:18 -d 3.1 -s "PocketPark"
    # python3 ./TodaysParkRun.py --name "Bishanga, EM" --time 00:18:18 --distance 3.1 --space "PocketPark"
    args = argparse.ArgumentParser()
    args.add_argument(
        '-n', "--name", default='Bishanga, EM', help='str: Name of Athlete'
    )
    args.add_argument(
        '-d', "--distance", default=3.16, help='float: Distance, miles'
    )
    args.add_argument(
        '-t', "--time", default='00:18:44', help='strtime: RunTime, hh:mm:ss'
    )
    args.add_argument(
        '-s', "--space", default="PocketPark", help="str: Park"
    )
    args.add_argument(
        '-T', "--temperature", default=10, help="int: Temperature on the day"
    )
    args.add_argument(
        '-A', "--age", default=36, help='int: Age of Athlete, years'
    )
    args.add_argument(
        '-H', "--height", default=1.75, help='float: Height of Athlete, metres'
    )
    args.add_argument(
        '-W', "--weight", default=67.5, help='float: Weight of Athlete, kg'
    )
    args.add_argument(
        '-L', "--restHR", default=45, help='int: Resting HeartRate of Athlete, bpm'
    )
    args.add_argument(
        '-M', "--maxHR", default=200, help='int: Max HeartRate of Athlete, bpm'
    )
    inputs = args.parse_args()
    print('\nInput validation:')
    pprint(inputs)

    park_name = inputs.space
    parkrunner_name = inputs.name
    # parkrun_time = inputs.time
    # parkrun_distance = inputs.distance
    parkrun_temp = inputs.temperature

    # process run details
    Space = Park(park_name, temperature=parkrun_temp, precipitation=2, surface="mixed", inclination=2)
    # Space = TarRoad(park_name, temperature=parkrun_temp, precipitation=2, surface='gravel', inclination=2)
    print('\nPark: Venue: {}'.format(Space.venue))
    print('Park: Surface: {}'.format(Space.surface))
    print('Park: Temp: {} degCelcius'.format(Space.get_temperature()))

    Runner = ParkRunner(parkrunner_name, age=int(inputs.age), height=float(inputs.height), weight=float(inputs.weight), restHR=int(inputs.restHR), maxHR=int(inputs.maxHR))    # pylint: disable=no-value-for-parameter
    print("\n{}: VO2max_potential: {}".format(Runner.name, Runner.get_vo2max_potential()))
    print("{}: BMI: {}".format(Runner.name, Runner.get_bmi()))

    Race = ParkRun(park=Space, runner=Runner, dist_miles=float(inputs.distance), run_timestr=inputs.time)
    print("\n{}: Time_run_today: in hh:mm:ss {}".format(Runner.name, inputs.time))
    print("{}: Estimated Pace: {} min/mile".format(Runner.name, Race.get_race_pace()))
    print("{}: Equivalent 5km_time: in hh:mm:ss {}".format(Runner.name, Race.get_t_parkrun_timestr()))
    print("{}: Estimated V02_current: {}".format(Runner.name, Race.get_vo2max_current()))

    normalised_effort = round(100 * (Race.get_vo2max_current() / Runner.get_vo2max_potential()), 1)
    print("{}: Normalised Effort: %V02_max: {}%\n".format(Runner.name, normalised_effort))

if __name__ == '__main__':
    main()
