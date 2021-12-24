import os

from aocd.models import Puzzle
from aocd.transforms import lines, numbers

from colorama import init
from termcolor import colored

from aocbar import writebar

from collections import defaultdict

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))

caves = defaultdict(lambda: set())

paths = set()
path = []

small_caves = {}


def read_caves(input):
    for line in input:
        a, b = line.split('-')
        caves[a].add(b)
        caves[b].add(a)

        if str.lower(a) == a:
            small_caves[a] = 0

        if str.lower(b) == b:
            small_caves[b] = 0


def traverse_a(cv):
    path.append(cv)
    if cv == 'end':
        paths.add(','.join(path))
        path.pop()
        return

    for next_cv in list(caves[cv]):
        if next_cv in small_caves:
            if small_caves[next_cv] != 0:
                continue
            small_caves[next_cv] = 1

        traverse_a(next_cv)

        if next_cv in small_caves:
            small_caves[next_cv] = 0

    path.pop()
    return


def traverse_b(cv):
    path.append(cv)
    if cv == 'end':
        paths.add(','.join(path))
        path.pop()
        return

    for next_cv in list(caves[cv]):
        if next_cv == 'start':
            continue

        if next_cv in small_caves:
            if small_caves[next_cv] == 2:
                continue

            if small_caves[next_cv] == 1:
                if any(x == 2 for x in small_caves.values()):
                    continue

            small_caves[next_cv] += 1

        traverse_b(next_cv)

        if next_cv in small_caves:
            small_caves[next_cv] -= 1

    path.pop()
    return


def main_a():
    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)

    read_caves(input)
    traverse_a('start')
    # for path in paths:
    #     print(path)

    print(f"Total {len(paths)} paths")


def main_b():
    input = lines("""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""")
    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)

    read_caves(input)
    traverse_b('start')
    for path in paths:
        print(path)

    print(f"Total {len(paths)} paths")


if __name__ == '__main__':
    init()
    writebar(puzzle.day, 'b')
    # main_a()
    main_b()
