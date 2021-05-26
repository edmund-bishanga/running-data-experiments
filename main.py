#!/usr/bin/python

import sys

from test_classes.Park import Park
from test_classes.ParkRunner import ParkRunner
from test_classes.ParkRun import ParkRun
from pprint import pprint

def main():
    print('this is the main program... Ta!')

    # check input args
    args = sys.argv[1:]
    print('DEBUG: args: length: {}'.format(len(args))); pprint(args)
    help_txt = 'You can provide args [all 3 or None at all]: ["ParkName"] ["ParkRunnerName"] ["ParkRunTime"]'
    if len(args) == 0:
        print(help_txt)
        park_name = "RiversidePark"
        parkrunner_name = "BishangaE"
        parkrun_time = "00:20:00"  #hh:mm:ss
    elif len(args) == 3:
        park_name = args[0]
        parkrunner_name = args[1]
        parkrun_time = args[2]
    else:
        print('DEBUG 2: args: length: {}'.format(len(args))); pprint(args)
        assert(help_txt)
    print('Input validation: Inputs used: {}, {}, {}'.format(park_name, parkrunner_name, parkrun_time))

    # process run details
    Space = Park(park_name, temperature=15, precipitation=2, surface="mixed", inclination=2)
    print('\nPark: Venue: {}'.format(Space.venue))
    print('Park: Temp: {}'.format(Space.temperature))

    Runner = ParkRunner(parkrunner_name, age=36, height=1.75, weight=67, resilience=2, consistency=2, restHR=45, maxHR=200)
    print("\n{}: VO2max_potential: {}".format(Runner.name, Runner.get_vo2max_potential()))
    print("{}: BMI: {}".format(Runner.name, Runner.get_bmi()))

    Race = ParkRun(park=Space, runner=Runner, dist_miles=float("3.16"), run_timestr=str(parkrun_time))
    print("\n{}: 5km_time_min: {}".format(Runner.name, Race.get_t_parkrun_timestr()))
    print("{}: V02_current: {}".format(Runner.name, Race.get_vo2max_current()))

    normalised_effort = 100 * round((Race.get_vo2max_current() / Runner.get_vo2max_potential()), 2)
    print("\n{}: Normalised Effort: {}%\n".format(Runner.name, normalised_effort))


if __name__ == '__main__':
    main()