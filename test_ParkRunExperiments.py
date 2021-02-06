#!usr/bin/python

# sample pytest experiment

import pytest
import ParkRunExperiments

args = ["./ParkRun_Pocket_Bishanga_Edmund.csv", "vPocketParkRun", "2019"]

def test_getFileContents_validPath():
    path = "./ParkRun_Pocket_Bishanga_Edmund.csv"
    print(path)
    assert 'parkrun' in ParkRunExperiments.getFileContents(path)

test_getFileContents_validPath()

# def test_getFileContents_invalidPath():
#     path = 'abc.csv'
#     assert FileNotFoundError in ParkRunExperiments.getFileContents(path)
