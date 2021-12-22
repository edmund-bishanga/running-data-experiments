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
import csv
import json
import sys
from datetime import datetime
from pprint import pprint

from dateutil.relativedelta import relativedelta

from test_classes.park import Park
from test_classes.park_run import ParkRun
from test_classes.park_runner import ParkRunner

DEFAULT_DATA_DIR = './test_data'
CSV_DATASTORE = f'{DEFAULT_DATA_DIR}/parkrunners_db.csv'
DEFAULT_ENCODING = 'utf-8'
DEFUALT_PARK_TEMP = 10
DEFAULT_PARK_RUNNER = {
    "surName": "BISHANGA",
    "middleName": "E",
    "firstName": "Josiah",
    "dateOfBirth_yyyy-mm-dd": "1989-10-14",
    "parkrunner_id": "A1619585",
    "homeParkRun": "PeelPark",
    "todaysParkRun": "WorsleyWoodsPark",
    "parkrun_last4wks": "00:32:23",
    "parkrun_sb": "00:18:30",
    "parkrun_pb": "00:17:30",
    "prBMIDetails": {
        "height_m": 1.75,
        "weight_kg": 67.5
    },
    "prVO2MaxDetails": {
        "resting_hr_bpm": 45,
        "max_hr_bpm": 200,
        "age": 32
    }
}

def parse_inputs():
    args = argparse.ArgumentParser()
    args.add_argument(
        '-p', "--parkrunner-id", help='str: ParkRun Number|ID'
    )
    args.add_argument(
        '-n', "--name", help='str: Name of Athlete'
    )
    args.add_argument(
        '-d', "--distance", help='float: Distance, miles'
    )
    args.add_argument(
        '-t', "--time", help='strtime: RunTime, hh:mm:ss'
    )
    args.add_argument(
        '-s', "--space", help="str: Park"
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
    args.add_argument(
        '-C', "--covid-feedback", default=False,
        help='flag: Provide COVID Recovery Feedback'
    )
    inputs = args.parse_args()
    return inputs

def validate_inputs(inputs):
    print('\nInput validation:')
    input_format_err_msg = "invalid format: details, see --help/-h"
    if inputs.time:
        err_msg_t = f"--time, -t: {input_format_err_msg}"
        assert ':' in inputs.time, err_msg_t
    pprint(inputs)

def parse_pr_name(inputs_name):
    # parse ParkRunner Name: 'First Middle SurName'
    # 'Edmund M Bishanga': 'Edmund', 'M', 'BISHANGA'
    # 'Bishanga': '', '', Bishanga
    # 'John Taylor': 'John', '', 'Taylor'
    pr_names = inputs_name.split(' ')
    surName = pr_names[-1]
    firstName = pr_names[0] if len(pr_names) > 1 else ''
    middleName = pr_names[-2] if len(pr_names) > 2 else ''
    return (firstName, middleName, surName)

def augment_parkrunner_details(pr_details, inputs, using_csv):
    if inputs.space:
        pr_details['todaysParkRun'] = inputs.space
    if not pr_details.get('todaysParkRun'):
        pr_details['todaysParkRun'] = pr_details.get('homeParkRun')

    if inputs.name:
        firstName, middleName, surName = parse_pr_name(inputs.name)
        pr_details['firstName'] = firstName
        pr_details['middleName'] = middleName
        pr_details['surName'] = surName

    if pr_details.get('dateOfBirth_yyyy-mm-dd'):
        birthDate = datetime.strptime(pr_details.get('dateOfBirth_yyyy-mm-dd'), "%Y-%m-%d")
        age = relativedelta(datetime.today(), birthDate).years
        pr_details['age'] = age

    if using_csv:
        pr_details['prBMIDetails'] = {
            'height_m': float(pr_details.get('height_m')),
            'weight_kg': float(pr_details.get('weight_kg'))
        }
        pr_details['prVO2MaxDetails'] = {
            "resting_hr_bpm" : int(pr_details.get('resting_hr_bpm')),
            "max_hr_bpm" : int(pr_details.get('max_hr_bpm')),
            "age" : int(pr_details.get('age'))
        }
    print(f'\nDEBUG: fn::augment_parkrunner_details: pr_details after: \n{pr_details}')
    return pr_details

def get_parkrunner_details(inputs):
    pr_details = dict()

    using_csv = bool(CSV_DATASTORE and inputs.parkrunner_id)
    print(f'\nDEBUG: using_csv: {using_csv}')

    if not inputs.parkrunner_id:
        pr_details = DEFAULT_PARK_RUNNER
    elif using_csv:
        # read an appropriate row/JSON from the parkrunners_db/CSV datastore
        with open(CSV_DATASTORE, newline='', encoding=DEFAULT_ENCODING) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get('parkrunner_id') == inputs.parkrunner_id:
                    pr_details = row
    else:
        # or read from individual parkrunner JSON file
        pr_json_file = f'{DEFAULT_DATA_DIR}/parkrunner_details_{inputs.parkrunner_id}.json'
        with open(pr_json_file, 'r', encoding=DEFAULT_ENCODING) as fileObj:
            pr_details = json.load(fileObj)
    print(f'\nDEBUG: fn::get_parkrunner_details: pr_details before: \n{pr_details}')

    # Augment parkRunner Data/Info
    pr_details = augment_parkrunner_details(pr_details, inputs, using_csv)

    return pr_details

def main():
    """ Interactive function: Inputs event details, provides normalised insights. """
    # Example input format
    # python3 ./TodaysParkRun.py -n "Bishanga, EM" -t 00:18:18 -d 3.1 -s "PocketPark"
    # python3 ./TodaysParkRun.py --name "Bishanga, EM" --time 00:18:18 --distance 3.1 --space "PocketPark"
    inputs = parse_inputs()
    validate_inputs(inputs)

    # Prioritize ParkRunner JSON/Dictionary whenever available
    pr_details = get_parkrunner_details(inputs)
    assert pr_details, 'pr_details: Missing parkRunner Details: see --help/-h'

    park_name = pr_details.get('todaysParkRun')
    parkrunner_name = pr_details.get('surName')
    parkrun_temp = inputs.temperature

    # process run details
    Space = Park(park_name, temperature=parkrun_temp, precipitation=2, surface="mixed", inclination=2)

    # logging experiment
    # message tags: info, warning, debug, error
    import logging
    logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%a/%d.%b.%Y %H:%M:%S')
    logging.info('event ABC: var_name: %s was logged.', Space.venue)
    logging.warning(f'Park: Venue: %s', Space.venue)
    logging.debug(f'Park: Venue: %s', Space.venue)

    print(f'\nPark: Venue: {Space.venue}')
    print(f'Park: Surface: {Space.surface}')
    print(f'Park: Temp: {Space.get_temperature()} degCelcius')

    if inputs.age or inputs.weight:
        err_msg = """
            For BMI, VO2_max analysis, please provide ALL:
            height, weight, resting_hr, max_hr
            Details, add ' --help'
        """
        assert inputs.height and inputs.weight and inputs.resting_hr and inputs.max_hr, err_msg
        Runner = ParkRunner(
                    parkrunner_name, age=int(inputs.age), height=float(inputs.height),
                    weight=float(inputs.weight), resting_hr=int(inputs.resting_hr),
                    max_hr=int(inputs.max_hr)
                )    # pylint: disable=no-value-for-parameter
    else:
        # get parkrunner details as dictionary, from appropriate JSON dataStore
        Runner = ParkRunner(parkrunner_name, parkrunner_details=pr_details)
    ref_str = 'PreCOVID' if inputs.covid_feedback else 'Ref'
    # print("\n{}: Ref: VO2max_potential: {}".format(Runner.name, Runner.get_vo2max_potential()))
    # print("{}: Ref: Season's Best ParkRunTime: in hh:mm:ss {}".format(Runner.name, pr_details.get('parkrun_sb')))
    # print("\n{}: Ref: pBMI: {}".format(Runner.name, Runner.get_bmi()))
    print(f"\n{Runner.name}: {ref_str}: BMI: {Runner.get_trefethen_bmi()}")

    Race = ParkRun(park=Space, runner=Runner, dist_miles=inputs.distance, run_timestr=inputs.time, pace=inputs.pace)
    dist_run_today = inputs.distance if inputs.distance else Race.get_dist_miles()
    print(f"\n{Runner.name}: Dist_run_today: in miles {dist_run_today}")
    strtime_run_today = inputs.time if inputs.time else Race.convert_seconds_to_timestr_hh_mm_ss(Race.get_time_sec())
    print(f"{Runner.name}: This Week's Effort: RunTime: in hh:mm:ss {strtime_run_today}")
    print(f"{Runner.name}: This Week's Estimated Pace: {Race.get_race_pace_str()} min/mile")
    print(f"{Runner.name}: This Week's Equivalent ParkRun5kTime: in hh:mm:ss {Race.get_t_parkrun_timestr()}")


    print(f"\n{Runner.name}: {ref_str}: VO2max_potential: {Runner.get_vo2max_potential()}")
    print(f"{Runner.name}: Estimated V02max_current: This Week: {Race.get_vo2max_current()}")
    normalised_v02_pdiff = round(100 * (Race.get_vo2max_current() / Runner.get_vo2max_potential()) - 100, 1)
    if inputs.covid_feedback:
        print(f"{Runner.name}: This Week's Effort: vs PreCOVID V02_max_potential: {normalised_v02_pdiff}%")
        orange_v02_str = "V02max Recovery: ORANGE: still Concerning..."
        green_v02_str = "V02max Recovery: GREEN: OK, getting There..."
        v02_pThreshold = -12
        v02max_progress = orange_v02_str if normalised_v02_pdiff < v02_pThreshold else green_v02_str
        print(f"{Runner.name}: This Week's Effort: vs preCOVID V02_max_potential: {v02max_progress}")

    normalised_5k_effort = round(100 * (1 - ((Race.get_t_parkrun_seconds() - Runner.get_pr_parkrun_sb_seconds()) / Runner.get_pr_parkrun_sb_seconds())) - 100, 1)
    normalised_5k_effort = '+' + str(normalised_5k_effort) if normalised_5k_effort > 0 else str(normalised_5k_effort)
    print(f"{Runner.name}: This Week's Effort: vs Season's Best: {normalised_5k_effort}%\n")

    if inputs.covid_feedback:
        print(f"{Runner.name}: Last 4 Weeks' Average ParkRun5kTime: in hh:mm:ss {pr_details.get('parkrun_last4wks')}")
        progressed_5k_pdiff = round(100 * (1 - ((Race.get_t_parkrun_seconds() - Runner.get_pr_parkrun_4wks_seconds()) / Runner.get_pr_parkrun_sb_seconds())) - 100, 1)
        s_progressed_5k_pdiff = '+' + str(progressed_5k_pdiff) if progressed_5k_pdiff > 0 else str(progressed_5k_pdiff)
        print(f"{Runner.name}: This Week's Effort: vs Last 4 Weeks' Average: percentageDiff: {s_progressed_5k_pdiff}%")

        red_warning_str = "RED: REGRESSED: Please Consult GP Again..."
        green_ok_str = "GREEN: OK: Making Progress... Keep it Up..."
        parkrun5k_pThreshold = -10
        progress = red_warning_str if progressed_5k_pdiff < parkrun5k_pThreshold else green_ok_str
        print(f"{Runner.name}: This Week's Effort: vs Last 4 Weeks: Verdict: {progress}\n")


if __name__ == '__main__':
    main()
