from aocd.models import Puzzle
from aocd.transforms import lines, numbers
from aocbar import writebar

puzzle = Puzzle(year=2021, day=7)


def dist(x, input):
    res = 0
    for crab in input:
        res += abs(x - crab)

    return res


def dist_b(x, input):
    res = 0
    for crab in input:
        dst = abs(x - crab)
        res += (dst * (dst + 1)) // 2

    return res


def main_a():
    # input = numbers(puzzle.example_data)
    input = numbers(puzzle.input_data)

    res = {}

    min_ = None

    for i in range(min(input), max(input) + 1):
        dst = dist(i, input)
        if min_ is not None and dst > min_:
            print(min_)
            break
        else:
            min_ = dst


def main_b():
    # input = numbers(puzzle.example_data)
    input = numbers(puzzle.input_data)

    res = {}

    min_ = None

    for i in range(min(input), max(input) + 1):
        dst = dist_b(i, input)
        if min_ is not None and dst > min_:
            print(min_)
            break
        else:
            min_ = dst
    else:
        print(min_)

if __name__ == '__main__':
    writebar(puzzle.day, 'b')
    # main_a()
    main_b()
