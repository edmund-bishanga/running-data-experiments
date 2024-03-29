#!/usr/bin/python
"""
Purpose:
Post-ParkRun Data Processing:
+ Takes ParkRun Event and Athlete Details
+ Provides a Summary of ParkRun Analysis Info
+ Normalised Insights

Example input format:
python3 ./todays_park_run.py -n "Bishanga, EM"
                             -t 00:18:18 -d 3.1 -s "PocketPark"
python3 ./todays_park_run.py --name "Bishanga, EM"
                             --time 00:18:18 --distance 3.1
                             --space "PocketPark"
For more detail:
python3 ./todays_park_run.py --help
"""

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring

import argparse
import csv
import json
from datetime import datetime
from pprint import pprint

from dateutil.relativedelta import relativedelta

from test_classes.park import Park
from test_classes.park_run import ParkRun
from test_classes.park_runner import ParkRunner

DEFAULT_DATA_DIR = "./test_data"
CSV_DATASTORE = f"{DEFAULT_DATA_DIR}/parkrunners_db.csv"
DEF_ENCODING = "utf-8"
DEFUALT_PARK_TEMP = 10
DEFAULT_PARK_RUNNER = {
    "surName": "BISHANGA",
    "middleName": "E",
    "firstName": "Josiah",
    "dateOfBirth_yyyy-mm-dd": "1989-10-14",
    "parkrunner_id": "A1619585",
    "homeParkRunVenue": "PeelPark",
    "todaysParkRunVenue": "WorsleyWoodsPark",
    "parkrun_last4wks": "00:32:23",
    "parkrun_sb": "00:18:30",
    "parkrun_pb": "00:17:30",
    "prBMIDetails": {"height_m": 1.75, "weight_kg": 67.5},
    "prVO2MaxDetails": {"resting_hr_bpm": 45, "max_hr_bpm": 200, "age": 32},
}


def parse_inputs():
    args = argparse.ArgumentParser()
    args.add_argument("-p", "--parkrunner-id", help="str: ParkRun Number|ID")
    args.add_argument(
        "-n", "--name",
        help="str: Name of Athlete, format: 'First Middle SurName'"
    )
    args.add_argument("-d", "--distance", help="float: Distance, miles")
    args.add_argument("-t", "--time", help="strtime: RunTime, hh:mm:ss")
    args.add_argument("-s", "--space", help="str: Park")
    args.add_argument(
        "-T",
        "--temperature",
        default=DEFUALT_PARK_TEMP,
        help="int: Temperature on the day",
    )
    args.add_argument("-A", "--age", help="int: Age of Athlete, years")
    args.add_argument(
        "-P",
        "--pace",
        help='str: Pace of athlete, "mm:ss" min/mile'
    )
    args.add_argument("-H", "--height", help="float: Height of Athlete, metres")
    args.add_argument("-W", "--weight", help="float: Weight of Athlete, kg")
    args.add_argument(
        "-L", "--resting-hr", help="int: Resting HeartRate of Athlete, bpm"
    )
    args.add_argument(
        "-M",
        "--max-hr",
        help="int: Max HeartRate of Athlete, bpm"
    )
    args.add_argument(
        "-C",
        "--covid-feedback",
        action="store_true",
        help="flag: Provide COVID Recovery Feedback",
    )
    args.add_argument(
        "-m",
        "--minimal-pdata",
        action="store_true",
        help="flag: Provide minimal personal data",
    )
    inputs = args.parse_args()
    return inputs


def validate_inputs(inputs):
    print("\nInput validation:")
    input_format_err_msg = "invalid format: details, see --help/-h"
    # TODO: Add a simple but reasonable input validation check, for each input
    # List of Inputs
    # [-p PARKRUNNER_ID]
    # [-n NAME]
    # [-d DISTANCE]
    # [-t TIME]
    # [-s SPACE]
    # [-T TEMPERATURE]
    # [-A AGE]
    # [-P PACE]
    # [-H HEIGHT]
    # [-W WEIGHT]
    # [-L RESTING_HR]
    # [-M MAX_HR]
    # [-C]
    # [-m]
    if inputs.time:
        err_msg_t = f"--time, -t: {input_format_err_msg}"
        assert ":" in inputs.time, err_msg_t
    if inputs.distance:
        err_msg_d = f"--distance, -d: {input_format_err_msg}"
        assert isinstance(float(inputs.distance), float), err_msg_d
    if inputs.resting_hr:
        min_rhr = 20
        max_rhr = 100
        input_var = "--resting-hr, -L"
        err_msg_hr = f"{input_var}: should be between {min_rhr} and {max_rhr}"
        assert min_rhr < int(inputs.resting_hr) < max_rhr, err_msg_hr
    pprint(inputs)


def parse_pr_name(inputs_name):
    # parse ParkRunner Name: 'First Middle SurName'
    # 'Edmund M Bishanga': 'Edmund', 'M', 'BISHANGA'
    # 'Bishanga': '', '', Bishanga
    # 'John Taylor': 'John', '', 'Taylor'
    if "," in inputs_name:
        pr_names = inputs_name.split(",")
        sur_name = pr_names[0]
        rem_names = pr_names[-1].strip().split(" ")
        first_name = rem_names[0]
        mid_name = rem_names[-1] if len(rem_names) > 1 else ""
    else:
        pr_names = inputs_name.split(" ")
        sur_name = pr_names[-1]
        first_name = pr_names[0] if len(pr_names) > 1 else ""
        mid_name = pr_names[-2] if len(pr_names) > 2 else ""
    return (first_name, mid_name, sur_name)


def augment_parkrunner_db_details(pr_details, inputs, using_csv):
    if inputs.space:
        pr_details["todaysParkRunVenue"] = inputs.space
    if not pr_details.get("todaysParkRunVenue"):
        pr_details["todaysParkRunVenue"] = pr_details.get("homeParkRunVenue")

    if inputs.name:
        first_name, mid_name, sur_name = parse_pr_name(inputs.name)
        pr_details["firstName"] = first_name
        pr_details["middleName"] = mid_name
        pr_details["surName"] = sur_name

    if pr_details.get("dateOfBirth_yyyy-mm-dd"):
        pr_details_dob = pr_details.get("dateOfBirth_yyyy-mm-dd")
        birthDate = datetime.strptime(pr_details_dob, "%Y-%m-%d")
        age = relativedelta(datetime.today(), birthDate).years
        pr_details["age"] = age
        if pr_details.get("prVO2MaxDetails"):
            pr_details["prVO2MaxDetails"]["age"] = pr_details["age"]

    if using_csv:
        pr_details["prBMIDetails"] = {
            "height_m": float(pr_details.get("height_m")),
            "weight_kg": float(pr_details.get("weight_kg")),
        }
        pr_details["prVO2MaxDetails"] = {
            "resting_hr_bpm": int(pr_details.get("resting_hr_bpm")),
            "max_hr_bpm": int(pr_details.get("max_hr_bpm")),
            "age": int(pr_details.get("age")),
        }
    this_method = "fn::augment_parkrunner_db_details"
    print(f"\nDEBUG: {this_method}: pr_details after: \n{pr_details}")
    return pr_details


def get_parkrunner_db_details(inputs):
    pr_details = {}

    using_csv = bool(CSV_DATASTORE and inputs.parkrunner_id)
    print(f"\nDEBUG: using_csv: {using_csv}")

    if not inputs.parkrunner_id:
        pr_details = DEFAULT_PARK_RUNNER
    elif using_csv:
        # read an appropriate row/JSON from the parkrunners_db/CSV datastore
        with open(CSV_DATASTORE, newline="", encoding=DEF_ENCODING) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get("parkrunner_id") == inputs.parkrunner_id:
                    pr_details = row
    else:
        # or read from individual parkrunner JSON file
        pr_id = inputs.parkrunner_id
        pr_json_file = f"{DEFAULT_DATA_DIR}/parkrunner_db_details_{pr_id}.json"
        with open(pr_json_file, "r", encoding=DEF_ENCODING) as fileObj:
            pr_details = json.load(fileObj)
    this_method = "fn::get_parkrunner_db_details"
    print(f"\nDEBUG: {this_method}: pr_details before: \n{pr_details}")

    # Augment parkRunner Data/Info
    pr_details = augment_parkrunner_db_details(pr_details, inputs, using_csv)
    return pr_details


def update_runner_details(inputs, pr_details):
    parkrunner_name = pr_details.get("surName")
    if inputs.age or inputs.weight:
        err_msg = """
            For BMI, VO2_max analysis, please provide ALL:
            height, weight, resting_hr, max_hr
            Details, add ' --help'
        """
        rest_hr = inputs.resting_hr
        max_hr = inputs.max_hr
        assert inputs.height and inputs.weight and rest_hr and max_hr, err_msg
        runner = ParkRunner(
            parkrunner_name,
            age=int(inputs.age),
            height=float(inputs.height),
            weight=float(inputs.weight),
            resting_hr=int(inputs.resting_hr),
            max_hr=int(inputs.max_hr),
        )  # pylint: disable=no-value-for-parameter
    else:
        # get parkrunner details as dictionary, from appropriate JSON dataStore
        runner = ParkRunner(parkrunner_name, parkrunner_db_details=pr_details)
    return runner


def output_park_summary(space):
    # logging experiment
    # message tags: info, warning, debug, error
    import logging  # pylint: disable=import-outside-toplevel

    meb_df = "%a/%d.%b.%Y %H:%M:%S"
    logging.basicConfig(format="%(asctime)s: %(message)s", datefmt=meb_df)
    logging.info("event ABC: var_name: %s was logged.", space.venue)
    logging.warning("Park: Venue: %s", space.venue)
    logging.debug("Park: Venue: %s", space.venue)

    print(f"\nPark: Venue: {space.venue}")
    print(f"Park: Surface: {space.surface}")
    print(f"Park: Temp: {space.get_temperature()} degCelcius")


def output_covid_vo2max_progress(pr_name, era, normalised_v02_pdiff):
    weekly_diff_str = f"{era} Effort: vs PreCOVID V02_max_potential"
    print(f"{pr_name}: {weekly_diff_str}: {normalised_v02_pdiff}%")
    orange_v02_str = "V02max Recovery: ORANGE: still Concerning..."
    green_v02_str = "V02max Recovery: GREEN: OK, getting There..."
    v02_pThreshold = -12
    v02max_progress = green_v02_str
    if normalised_v02_pdiff < v02_pThreshold:
        v02max_progress = orange_v02_str
    print(f"{pr_name}: {weekly_diff_str}: {v02max_progress}")


def output_runners_covid_feedback(pr_details, runner, race, pr_name, era):
    four_wk_str = "Last 4 Weeks' Average ParkRun5kTime: in hh:mm:ss"
    print(f"{pr_name}: {four_wk_str}: {pr_details.get('parkrun_last4wks')}")
    progressed_5k_pdiff = round(
        100
        * (
            1
            - (
                (race.get_t_parkrun_seconds() - runner.get_pr_parkrun_4wks_seconds())
                / runner.get_pr_parkrun_sb_seconds()
            )
        )
        - 100,
        1,
    )
    s_progressed_5k_pdiff = str(progressed_5k_pdiff)
    if int(progressed_5k_pdiff) > 0:
        s_progressed_5k_pdiff = "+" + str(progressed_5k_pdiff)
    four_wk_diff_str = f"{era} Effort: vs Last 4 Weeks' Average: "
    print(f"{pr_name}: {four_wk_diff_str}: pcentDiff: {s_progressed_5k_pdiff}%")

    red_warning_str = "RED: REGRESSED: Please Consult GP Again..."
    green_ok_str = "GREEN: OK: Making Progress... Keep it Up..."
    parkrun5k_pThreshold = -10
    progress = green_ok_str
    if progressed_5k_pdiff < parkrun5k_pThreshold:
        progress = red_warning_str
    print(f"{pr_name}: {four_wk_diff_str}: Verdict: {progress}\n")


def output_todays_key_parkrunner_stats(inputs, pr_details, runner, race):
    pr_name = runner.name
    vo2max_potential = runner.get_vo2max_potential()
    print(f"\n{pr_name}: Ref: VO2max_potential: {vo2max_potential}")
    pr_sb = pr_details.get("parkrun_sb")
    print(f"{pr_name}: Ref: Season's Best ParkRunTime: in hh:mm:ss {pr_sb}")
    if not inputs.minimal_pdata:
        print(f"{pr_name}: Ref: pBMI: {runner.get_bmi()}")
    ref_str = "PreCOVID" if inputs.covid_feedback else "Ref"
    if not inputs.minimal_pdata:
        print(f"{pr_name}: {ref_str}: BMI: {runner.get_trefethen_bmi()}")

    dist_run_today = race.get_dist_miles()
    if inputs.distance:
        dist_run_today = inputs.distance
    print(f"\n{pr_name}: Distance Run Today: in miles {dist_run_today}")
    r_time = race.get_time_sec()
    run_time_tday = race.convert_seconds_to_timestr_hh_mm_ss(r_time)
    if inputs.time:
        run_time_tday = inputs.time
    era = "Today's"
    print(f"{pr_name}: {era} Effort: RunTime: (hh:mm:ss) {run_time_tday}")
    race_pace_tday = race.get_race_pace_str()
    print(f"{pr_name}: {era} Estimated Pace: {race_pace_tday} min/mile")
    eq_5k_time = race.get_t_parkrun_timestr()
    print(f"{pr_name}: {era} Equivalent ParkRun5kTime: (hh:mm:ss) {eq_5k_time}")

    current_vo2max = race.get_vo2max_current()
    print(f"\n{pr_name}: Estimated V02max_current: {era}: {current_vo2max}")

    pcent_vo2max = round(100 * (current_vo2max / vo2max_potential), 1)
    print(f"{pr_name}: {era} VO2max vs Potential VO2max: {pcent_vo2max}%")
    normalised_v02_pdiff = round(100 * (current_vo2max / vo2max_potential) - 100, 1)
    if inputs.covid_feedback:
        output_covid_vo2max_progress(pr_name, era, normalised_v02_pdiff)

    normalised_5k_effort = round(
        100
        * (
            1
            - (
                (race.get_t_parkrun_seconds() - runner.get_pr_parkrun_sb_seconds())
                / runner.get_pr_parkrun_sb_seconds()
            )
        )
        - 100,
        1,
    )
    normalised_5k_effort = str(normalised_5k_effort)
    if float(normalised_5k_effort) > 0:
        normalised_5k_effort = "+" + str(normalised_5k_effort)
    season_diff_str = f"{era} Effort: vs Season's Best"
    print(f"{pr_name}: {season_diff_str}: {normalised_5k_effort}%\n")

    if inputs.covid_feedback:
        output_runners_covid_feedback(pr_details, runner, race, pr_name, era)


def main():
    """Interactive: takes event details, gives normalised insights."""
    inputs = parse_inputs()
    validate_inputs(inputs)
    # Prioritize ParkRunner JSON/Dictionary whenever available
    pr_details = get_parkrunner_db_details(inputs)
    assert pr_details, "pr_details: Missing parkRunner Details: see --help/-h"
    # Process ParkRun details: Space, Time, Person
    # A: The Park
    park_name = pr_details.get("todaysParkRunVenue")
    space = Park(
        park_name,
        temperature=inputs.temperature,
        precipitation=2,
        surface="mixed",
        inclination=2,
    )
    output_park_summary(space)
    # B: The Runner
    runner = update_runner_details(inputs, pr_details)
    race = ParkRun(
        park=space,
        runner=runner,
        dist_miles=inputs.distance,
        run_timestr=inputs.time,
        pace=inputs.pace,
    )
    output_todays_key_parkrunner_stats(inputs, pr_details, runner, race)


if __name__ == "__main__":
    main()
