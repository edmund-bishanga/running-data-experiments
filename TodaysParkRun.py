#!/usr/bin/python

import argparse
import sys

from test_classes.Park import Park
from test_classes.ParkRunner import ParkRunner
from test_classes.ParkRun import ParkRun
from pprint import pprint

def main():
    # Example input format
    # python3 ./TodaysParkRun.py -r "Bishanga, EM" -t 18.18 -s "PocketPark"
    # python3 ./TodaysParkRun.py --runner "Bishanga, EM" --time 18.18 --space "PocketPark"
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
    pprint(inputs)

    park_name = inputs.space
    parkrunner_name = inputs.athlete
    parkrun_time = inputs.time
    parkrun_distance = inputs.distance
    parkrun_temp = inputs.temperature
    print('Input validation: Inputs used: {}, {}, {}'.format(park_name, parkrunner_name, parkrun_time))

    # process run details
    Space = Park(park_name, temperature=parkrun_temp, precipitation=2, surface="mixed", inclination=2)
    print('\nPark: Venue: {}'.format(Space.venue))
    print('Park: Temp: {} degCelcius'.format(Space.temperature))

    Runner = ParkRunner(parkrunner_name, age=36, height=1.75, weight=67, resilience=2, consistency=2, restHR=45, maxHR=200)
    print("\n{}: VO2max_potential: {}".format(Runner.name, Runner.get_vo2max_potential()))
    print("{}: BMI: {}".format(Runner.name, Runner.get_bmi()))

    def parse_race_time(parkrun_time_str):
        """ convert hh:mm:ss into seconds """
        time_array = parkrun_time_str.strip().split(':')
        if len(time_array) == 3:
            race_time_seconds = 3600 * int(time_array[0]) + 60 * int(time_array[1]) + int(time_array[2])
        else:
            assert('invalid parkrun_time_str: {}'.format(parkrun_time_str))
        return race_time_seconds

    distance_in_km = round((float(parkrun_distance) * 1.67), 1)
    race_time_float = round(float(parse_race_time(parkrun_time) / 60), 1)  # in minutes, at the moment
    Race = ParkRun(park=Space, runner=Runner, distance_km=distance_in_km, time_min=race_time_float)
    print("\n{}: Time_run_today: in hh:mm:ss {}".format(Runner.name, parkrun_time))
    print("{}: Equivalent 5km_time: in hh:mm:ss {}".format(Runner.name, Race.get_t_parkrun_timestr()))
    print("{}: Estimated V02_current: {}".format(Runner.name, Race.get_vo2max_current()))

    normalised_effort = 100 * round((Race.get_vo2max_current() / Runner.get_vo2max_potential()), 2)
    print("{}: Normalised Effort: {}%\n".format(Runner.name, normalised_effort))

if __name__ == '__main__':
    main()