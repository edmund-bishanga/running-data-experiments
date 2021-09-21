#!/usr/bin/python
"""
Interactive Script:
+ Takes Event and Athlete Details
+ Provides a Summary of ParkRun Analysis Info
+ Normalised Insights
"""

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=unused-import
# pylint: disable=missing-function-docstring

import argparse
import json
import sys
from pprint import pprint

from test_classes.Park import Park, TarRoad
from test_classes.ParkRun import ParkRun
from test_classes.ParkRunner import ParkRunner

DEFAULT_DATA_DIR = './data'
DEFAULT_ENCODING = 'utf-8'
DEFUALT_PARK_TEMP = 10
DEFAULT_PARK_RUNNER = {
    "surName" : "BISHANGA",
    "firstName" : "Josiah",
    "dateOfBirth_yyyy-mm-dd" : "1989-10-14",
    "parkrunner_id" : "A1619585",
    "homeParkRun" : "PeelPark",
    "parkrun_sb" : "00:18:30",
    "parkrun_pb" : "00:17:30",
    "prBMIDetails" : {
        "height_m" : 1.75,
        "weight_kg" : 67.5
    },
    "prVO2MaxDetails" : {
        "resting_hr_bpm" : 45,
        "max_hr_bpm" : 195,
        "age" : 32
    }
}

def validate_inputs(inputs):
    input_format_err_msg = "invalid format: details, see --help/-h"
    if inputs.time:
        err_msg_t = "{}: {}".format('--time, -t',  input_format_err_msg)
        assert ':' in inputs.time, err_msg_t

def get_pr_details(parkrunner_id):
    if parkrunner_id == DEFAULT_PARK_RUNNER.get('parkrunner_id'):
        pr_details = DEFAULT_PARK_RUNNER
    else:
        pr_json_file = f'{DEFAULT_DATA_DIR}/parkrunner_details_{parkrunner_id}.json'
        with open(pr_json_file, 'r', encoding=DEFAULT_ENCODING) as fileObj:
            pr_details = json.load(fileObj)
    return pr_details

def main():
    """ Interactive function: Inputs event details, provides normalised insights. """
    # Example input format
    # python3 ./TodaysParkRun.py -n "Bishanga, EM" -t 00:18:18 -d 3.1 -s "PocketPark"
    # python3 ./TodaysParkRun.py --name "Bishanga, EM" --time 00:18:18 --distance 3.1 --space "PocketPark"
    args = argparse.ArgumentParser()
    args.add_argument(
        '-p', "--parkrunner-id", default=DEFAULT_PARK_RUNNER.get('parkrunner_id'),
        help='str: ParkRun Number|ID'
    )
    args.add_argument(
        '-n', "--name", default=DEFAULT_PARK_RUNNER.get('surName'),
        help='str: Name of Athlete'
    )
    args.add_argument(
        '-d', "--distance", help='float: Distance, miles'
    )
    args.add_argument(
        '-t', "--time", help='strtime: RunTime, hh:mm:ss'
    )
    args.add_argument(
        '-s', "--space", default=DEFAULT_PARK_RUNNER.get('homeParkRun'),
        help="str: Park"
    )
    args.add_argument(
        '-T', "--temperature", default=DEFUALT_PARK_TEMP,
        help="int: Temperature on the day"
    )
    args.add_argument(
        '-A', "--age", help='int: Age of Athlete, years'
    )
    args.add_argument(
        '-P', "--pace", help='str: Pace of athlete, "mm:ss" min/mile'
    )
    args.add_argument(
        '-H', "--height", help='float: Height of Athlete, metres'
    )
    args.add_argument(
        '-W', "--weight", help='float: Weight of Athlete, kg'
    )
    args.add_argument(
        '-L', "--resting-hr", help='int: Resting HeartRate of Athlete, bpm'
    )
    args.add_argument(
        '-M', "--max-hr", help='int: Max HeartRate of Athlete, bpm'
    )
    inputs = args.parse_args()
    print('\nInput validation:')
    validate_inputs(inputs)
    pprint(inputs)

    # Prioritize ParkRunner JSON/Dictionary whenever available
    pr_details = get_pr_details(inputs.parkrunner_id)
    print('\nDEBUG: pr_details')
    pprint(pr_details, width=120)

    park_name = pr_details.get('homeParkRun') if pr_details else inputs.space
    parkrunner_name = pr_details.get('surName') if pr_details else inputs.name
    parkrun_temp = inputs.temperature

    # process run details
    Space = Park(park_name, temperature=parkrun_temp, precipitation=2, surface="mixed", inclination=2)
    print('\nPark: Venue: {}'.format(Space.venue))
    print('Park: Surface: {}'.format(Space.surface))
    print('Park: Temp: {} degCelcius'.format(Space.get_temperature()))

    if inputs.age or inputs.weight:
        err_msg = """
            For BMI, VO2_max analysis, please provide ALL:
            height, weight, resting_hr, max_hr
            Details, add ' --help'
        """
        assert inputs.height and inputs.weight and inputs.resting_hr and inputs.max_hr, err_msg
        Runner = ParkRunner(
                    parkrunner_name, age=int(inputs.age),
                    height=float(inputs.height), weight=float(inputs.weight),
                    resting_hr=int(inputs.resting_hr), max_hr=int(inputs.max_hr)
                 )    # pylint: disable=no-value-for-parameter
    else:
        # get parkrunner details as dictionary, from appropriate JSON dataStore
        Runner = ParkRunner(parkrunner_name, parkrunner_details=pr_details)
    print("\n{}: Ref: VO2max_potential: {}".format(Runner.name, Runner.get_vo2max_potential()))
    print("{}: Ref: Season's Best ParkRunTime: in hh:mm:ss {}".format(Runner.name, pr_details.get('parkrun_sb')))
    print("\n{}: Ref: BMI: {}".format(Runner.name, Runner.get_bmi()))
    print("{}: Ref: TrefethenBMI: {}".format(Runner.name, Runner.get_trefethen_bmi()))

    Race = ParkRun(park=Space, runner=Runner, dist_miles=inputs.distance, run_timestr=inputs.time, pace=inputs.pace)
    dist_run_today = inputs.distance if inputs.distance else Race.get_dist_miles()
    print("\n{}: Dist_run_today: in miles {}".format(Runner.name, dist_run_today))
    strtime_run_today = inputs.time if inputs.time else Race.convert_seconds_to_timestr_hh_mm_ss(Race.get_time_sec())
    print("\n{}: Time_run_today: in hh:mm:ss {}".format(Runner.name, strtime_run_today))
    print("{}: Estimated Pace: {} min/mile".format(Runner.name, Race.get_race_pace_str()))
    print("\n{}: Equivalent 5km_time: in hh:mm:ss {}".format(Runner.name, Race.get_t_parkrun_timestr()))
    print("{}: Estimated V02_current: {}".format(Runner.name, Race.get_vo2max_current()))

    normalised_effort = round(100 * (Race.get_vo2max_current() / Runner.get_vo2max_potential()), 1)
    print("{}: Normalised Effort: vs V02_max_potential: {}%".format(Runner.name, normalised_effort))

    normalised_5k_effort = round(100 * (1 - ((Race.get_t_parkrun_seconds() - Runner.get_pr_parkrun_sb_seconds()) / Runner.get_pr_parkrun_sb_seconds())), 1)
    print("{}: Normalised Effort: vs ParkRunSBTime {}%\n".format(Runner.name, normalised_5k_effort))

if __name__ == '__main__':
    main()
