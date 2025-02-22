#!usr/bin/python
"""
Half Marathon Post-Run Data Analysis:
Exploring various statistical information keys from my running data
+ average pace
+ total mileage
+ total time
+ VO2Max estimate
+ running economy analysis
"""

# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=unused-import
# pylint: disable=missing-function-docstring

import itertools
import json
import sys
from pprint import pprint

import numpy
import pandas as pd
from matplotlib import pyplot
from scipy import stats

from test_classes.park_runner import ParkRunner


class HalfMarathonExpts:
    """Statistical and Graphical Data Analysis: Half Marathon Data."""

    def __init__(self, hm_runfile=None, event_name=None) -> None:
        self.hm_runfile = hm_runfile
        self.event_name = event_name
        if not self.hm_runfile:
            self.hm_runfile = "./test_data/half_marathon_bishanga_edmund.csv"
        if not self.event_name:
            self.event_name = "Cambridge Half Marathon"

    # 1. Get Run instance Data
    #    From a file, I/O input.
    #    Possible formats: .csv, .txt
    #    Parsing Data
    #    into Appropriate Data Structure
    #    e.g. Dictionaries, Named Tuples, Lists etc.
    # hm_runfile = "./test_data/half_marathon_bishanga_edmund.csv"

    @staticmethod
    def get_file_contents(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            fdata = f.readlines()
        return fdata

    # file_generator = (line.strip() for line in open(self.hm_runfile, 'r'))
    # for line in file_generator:
    #     if line and line[0].isalnum():
    #         print(f"'{line}'")

    # generator experiment: big data .csv processing
    @staticmethod
    def collect_buffered_raw_data(unltd_raw_data_gen, max_length):
        ltd_raw_data = []
        try:
            # get next raw data val, until buffer limit
            while len(ltd_raw_data) < max_length:
                ltd_raw_data.append(next(unltd_raw_data_gen))
        except StopIteration as IterDone:
            print(f"\nINFO: raw data emptied out: {len(ltd_raw_data)}")
            pprint(IterDone)
        finally:
            length_raw_data = len(ltd_raw_data)
            print(f"\nDEBUG: raw data length harvested: {len(ltd_raw_data)}")
        return (ltd_raw_data, length_raw_data)

    def get_csv_column_raw_data(self, csv_file, heading, max_length=100):
        rows = (line for line in open(csv_file, "r", encoding="utf-8"))
        row_items = (row.rstrip().split(",") for row in rows)

        # validate requested heading
        heading_keys = next(row_items)
        print(f"\nDEBUG: headings: {heading_keys}")
        err_msg = f"MissingHeadingErr: {heading} not in {heading_keys}"
        assert heading in heading_keys, err_msg

        # get requested column data: raw
        row_dicts = (dict(zip(heading_keys, vals)) for vals in row_items)
        unltd_raw_data_gen = (row_dict.get(heading) for row_dict in row_dicts)
        # sum_raw_data = sum(unltd_raw_data_gen)

        # harvest up to the max_length: to a list
        ltd_raw_data, len_raw_data = self.collect_buffered_raw_data(
            unltd_raw_data_gen, max_length
        )

        # return a dictionary: of raw data
        col_raw_data = {heading: ltd_raw_data, "length": len_raw_data}
        return col_raw_data

    @staticmethod
    def get_data_rows(rundata):
        units = {}
        labels = []
        for header in rundata.pop(0).strip("\n").split(","):
            if header:
                label = header.split(" ")[0]
                unit = ""
                if len(header.split(" ")) == 2:
                    unit = header.split(" ")[1].strip("(").strip(")")
                units.update({label: unit})
                labels.append(label)
        rows = []
        iter_rundata = iter(rundata)
        done = False
        while not done:
            try:
                row = next(iter_rundata)
            except StopIteration:
                done = True
            else:
                if len(row.strip("\n").strip(",")) > 0:
                    vals = row.strip("\n").split(",")
                    lrow = dict(zip(labels, vals))
                    rows.append(lrow)
        return rows

    @staticmethod
    def calculate_plotable_coordinates(rows, event_x_axis, event_y_axis, event_name):
        x_values = []
        y_values = []
        iter_rows = iter(rows)
        done = False
        while not done:
            try:
                row = next(iter_rows)
            except StopIteration:
                done = True
            else:
                if event_name in row.get("venue"):
                    str_time = row.get(event_y_axis)
                    hr, mm, ss = tuple(str_time.split(":"))
                    duration = round(
                        float((int(hr) * 3600 + int(mm) * 60 + int(ss)) / 60), 1
                    )  # Maths: readable equation: long line: OK
                    y_values.append(duration)
                    x_values.append(row.get(event_x_axis))
        return (x_values, y_values)

    @staticmethod
    # pylint: disable=too-many-arguments
    def plot_line_graph(x_vals, y_vals, title, x_label, y_label, lstyle="o--r"):
        pyplot.plot(x_vals, y_vals, lstyle)
        pyplot.xlabel(x_label)
        pyplot.ylabel(y_label)
        pyplot.title(title)
        pyplot.show()

    @staticmethod
    def plot_normal_distribution(title, data=None):
        mean = round(numpy.mean(data), 2)
        print(f"mean: {mean}")
        std_dev = round(numpy.std(data), 4)
        print(f"std_dev: {std_dev}")
        variance = round(std_dev**2, 2)
        print(f"variance: {variance}")
        x_data = sorted(data)
        pyplot.plot(
            x_data,
            1
            / (std_dev * numpy.sqrt(2 * numpy.pi))
            * numpy.exp(
                -((x_data - mean) ** 2) / (2 * std_dev**2)
            ),  # Maths: readable equation: long line: OK
            "o-",
            linewidth=3,
            color="r",
        )
        pyplot.xlabel("Run Times")
        pyplot.ylabel("Likelihood")
        pyplot.title(f"{title}: Estimated Normal Distribution")
        pyplot.show()

    @staticmethod
    def transform_raw_to_int(raw_parkrun_times, times_heading):
        seconds_parkrun_times = raw_parkrun_times
        for i, val in enumerate(seconds_parkrun_times.get(times_heading)):
            s_val = ParkRunner.parse_race_timestr_to_seconds(val)
            seconds_parkrun_times.get(times_heading)[i] = s_val
        return seconds_parkrun_times

    def main(self):
        """Do ParkRun Data Experiments."""
        # 2: PROCESS CSV DATA: USING PANDAS, ITERATORS, MATPLOTLIB
        rundata = self.get_file_contents(self.hm_runfile)
        # use pandas to get rundata_frame
        run_dframe = pd.read_csv(self.hm_runfile)
        print("DEBUG: run_dframe:")
        pprint(run_dframe)

        # parse data -> appropriate data structure
        if not rundata:
            print(f"{self.hm_runfile} seems empty or it's data inaccessible")
            sys.exit(1)
        rows = self.get_data_rows(rundata)

        # 2. Calculate plotable Data Series
        event_x_axis = "date"
        event_y_axis = "time"
        x_values, y_values = self.calculate_plotable_coordinates(
            rows, event_x_axis, event_y_axis, self.event_name
        )

        # 2a: Output basic Stats summary
        pprint(stats.describe(y_values))

        # 2b. Plot line graph
        coordinates = tuple(zip(x_values, y_values))
        print("Coordinates: ")
        pprint(coordinates, width=1600)
        self.plot_line_graph(x_values, y_values, self.event_name, event_x_axis, event_y_axis)

        # 2c. Plot normal distribution
        self.plot_normal_distribution(self.event_name, data=y_values)

        # 3. Do Running Economy Analysis

        # 4. Provide Recommendations


if __name__ == "__main__":
    hmexpt = HalfMarathonExpts(
        hm_runfile="./test_data/park_run_raw_data_bishanga_edmund_tres.csv",
        event_name="PocketParkRun"
    )
    hmexpt.main()
