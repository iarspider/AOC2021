import os

from aocd.models import Puzzle
from aocd.transforms import lines, numbers

from colorama import init
from termcolor import colored

from aocbar import writebar

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))


def main_a():
    input = lines(puzzle.example_data)
    # input = lines(puzzle.input_data)


def main_b():
    input = lines(puzzle.example_data)
    # input = lines(puzzle.input_data)


if __name__ == '__main__':
    init()
    writebar(puzzle.day, 'a')
    main_a()
    # main_b()
