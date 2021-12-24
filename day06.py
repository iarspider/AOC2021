from collections import Counter

from aocd.models import Puzzle
from aocd.transforms import lines, numbers
from aocbar import writebar

import cProfile

puzzle = Puzzle(year=2021, day=6)


class IAmDone(Exception):
    pass


def main_a(dayz):
    # input = [3, 4, 3, 1, 2]
    input = numbers(puzzle.input_data)
    for day in range(1, dayz):
        l = len(input)
        for iFish in range(l):
            input[iFish] -= 1
            if input[iFish] < 0:
                input[iFish] = 6
                input.append(8)

        # input = copy.copy(new_input)
        # print("After {0:2d} day{1} {2}".format(day, 's: ' if day > 1 else ':  ', ','.join(str(x) for x in input)))

    print(len(input))


def main_aa(dayz):
    # input = [3, 4, 3, 1, 2]
    input = numbers(puzzle.input_data)
    input_c = Counter(input)

    for day in range(1, dayz):
        num_0 = input_c[0]
        for i in range(1, 9):
            input_c[i - 1] = input_c[i]

        input_c[6] += num_0
        input_c[8] = num_0

    print(sum(input_c.values()))


def main_aaa(dayz):
    # input = [3, 4, 3, 1, 2]
    input = numbers(puzzle.input_data)
    input_cc = Counter(input)
    input_c = [0] * 9
    for k, v in input_cc.items():
        input_c[k] = v

    for day in range(1, dayz):
        num_0 = input_c[0]
        for i in range(1, 9):
            input_c[i - 1] = input_c[i]

        input_c[6] += num_0
        input_c[8] = num_0

    print(sum(input_c))

def main_aaaa(dayz):
    # input = [3, 4, 3, 1, 2]
    input = numbers(puzzle.input_data)
    input_c = [0] * 9
    for k in input:
        input_c[k] += 1

    for day in range(1, dayz):
        num_0 = input_c[0]
        for i in range(1, 9):
            input_c[i - 1] = input_c[i]

        input_c[6] += num_0
        input_c[8] = num_0

    print(sum(input_c))

def main_b():
    return


if __name__ == '__main__':
    writebar(puzzle.day, 'b')
    # print(len(lines(puzzle.input_data)))
    # print(len(lines(puzzle.input_data)[0]))
    # cProfile.run('main_a(81)')
    # cProfile.run('main_aa(81)')
    # cProfile.run('main_a(257)')
    cProfile.run('main_aaa(257)')
    cProfile.run('main_aaaa(257)')
    # 385391
    # 1 728 611 055 389
    main_b()
