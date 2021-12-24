import copy
import operator
import os
from collections import Counter
from itertools import tee

from aocd.models import Puzzle
from aocd.transforms import lines, numbers

from colorama import init
from termcolor import colored

from aocbar import writebar

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))


# from itertools import pairwise

def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


polymer = Counter()
element = Counter()
rules = {}


def load(input):
    global polymer, rules

    poly = input.pop(0)
    element.update(poly)
    for ab in pairwise(poly):
        polymer.update((''.join(ab),))

    input.pop(0)

    for line in input:
        rules[line[:2]] = line[-1]


def step():
    global polymer
    new_polymer = Counter()

    for pair, cnt in polymer.items():
        if cnt > 0 and pair in rules:
            a, b = pair
            c = rules[pair]
            new_polymer[a + c] += cnt
            new_polymer[c + b] += cnt
            element[c] += cnt

    polymer = new_polymer


def main_a():
    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)

    load(input)
    # print("Initial")
    # print(polymer)
    # print(element.most_common())
    for _ in range(10):
        print(f'After step {_ + 1}')
        step()
        # print(polymer)
        # print(element.most_common())

    most_common = element.most_common()[0]
    least_common = element.most_common()[-1]

    print("Answer is", most_common[1] - least_common[1])

def main_b():
    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)

    load(input)
    for _ in range(40):
        step()

    print(element.most_common())

    most_common = element.most_common()[0]
    least_common = element.most_common()[-1]

    print("Answer is", most_common[1] - least_common[1])


if __name__ == '__main__':
    init()
    writebar(puzzle.day, 'b')
    # main_a()
    main_b()
