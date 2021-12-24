import os

from aocd.models import Puzzle
from aocd.transforms import lines
from colorama import init

from aocbar import writebar
from day19math import *

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))

beacons = []
dists = []


def dist(v1, v2):
    return sum((a - b) * (a - b) for a, b in zip(v1, v2))


def generate_distances():
    for scanner in beacons:


def main_a():
    input = lines(puzzle.example_data)
    for line in input:
        if line.startswith('---'):
            beacons.append([])
        elif (not line):
            continue
        else:
            beacons[-1].append([int(x) for x in line.split(',')])
    # input = lines(puzzle.input_data)


def main_b():
    input = lines(puzzle.example_data)
    # input = lines(puzzle.input_data)


if __name__ == '__main__':
    init()
    generate_matrices()
    writebar(puzzle.day, 'a')
    main_a()
    # main_b()
