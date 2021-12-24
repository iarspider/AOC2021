import os

from aocd.models import Puzzle
from aocd.transforms import lines, numbers
from colorama import init
from termcolor import colored

from aocbar import writebar

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))

cave = []
flash = []
queue = []
sz = 0
cnt_flash = 0

example_data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


def step(print_c=False):
    global cave, flash, queue, cnt_flash

    res = False

    for i in range(1, sz + 1):
        for j in range(1, sz + 1):
            value = cave[i][j] + 1
            if value > 9:
                queue.append((i, j))

            cave[i][j] = value

    index = 0
    if print_c:
        print_cave()

    while index < len(queue):
        i, j = queue[index]
        if not flash[i][j]:
            flash[i][j] = True
            cnt_flash += 1
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    ii = i + di
                    jj = j + dj
                    if flash[ii][jj]:
                        continue

                    value = cave[ii][jj] + 1
                    cave[ii][jj] = value
                    if value > 9:
                        queue.append((ii, jj))

        index += 1
        if print_c:
            print_cave(i, j)

    queue.clear()

    res = all(all(x) for x in flash)

    for i in range(1, sz + 1):
        for j in range(1, sz + 1):
            if flash[i][j]:
                cave[i][j] = 0
                flash[i][j] = False

    return res


def print_cave(ii=1, jj=-1):
    def to18(val):
        if val < 16:
            return hex(val)[2:]
        elif val == 16:
            return 'g'
        elif val == 17:
            return 'h'
        elif val == 18:
            return 'i'
        else:
            return 'z'

    for i in range(sz):
        for j in range(sz):
            value = cave[i + 1][j + 1]
            fla = flash[i + 1][j + 1]
            if value == 0:
                print(colored(value, 'white', attrs=['bold']), end='')
            elif value > 9:
                if i == ii - 1 and j == jj - 1:
                    print(colored(to18(value), 'yellow'), end='')
                else:
                    print(colored(to18(value), 'red' if not fla else 'magenta', attrs=[]), end='')
            else:
                print(colored(value, 'white'), end='')
            # print(get_cell(cave, i, j), end='')
        print()
    print()


def load_cave(input):
    global cave, flash, queue, sz

    sz = len(input)

    cave.append([])
    flash.append([])
    for i in range(sz + 2):
        cave[-1].append(-1)
        flash[-1].append(True)

    for row in input:
        cave.append([-1])
        flash.append([True])
        for cell in row:
            cave[-1].append(int(cell))
            flash[-1].append(False)

        flash[-1].append(True)
        cave[-1].append(-1)

    cave.append([])
    flash.append([])
    for i in range(sz + 2):
        cave[-1].append(-1)
        flash[-1].append(True)

def main_a():
    # global cave, flash, queue, sz

    # input = lines(example_data)
    #input = lines(puzzle.input_data)
    load_cave(lines(example_data))
    # load_cave(lines(puzzle.input_data))

    print("Before any steps:")
    print_cave()

    for c in range(1, 101):
        # print(f"After step {c}")
        step()
        # print_cave()

    print(f"Total {cnt_flash} flashes")

def main_b():
    # global cave, flash, queue, sz

    # input = lines(example_data)
    #input = lines(puzzle.input_data)
    # load_cave(lines(example_data))
    load_cave(lines(puzzle.input_data))

    print("Before any steps:")
    print_cave()

    res = False
    iStep = 0
    while not res:
        # print(f"After step {c}")
        iStep += 1
        res = step()
        # print_cave()

    print(f"All octopusses flashed during step {iStep}")


if __name__ == '__main__':
    init()
    writebar(puzzle.day, 'b')
    # main_a()
    main_b()
