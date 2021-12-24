import os
from collections import Counter

from aocd.models import Puzzle
from aocd.transforms import lines, numbers

from colorama import init
from termcolor import colored

from aocbar import writebar

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))

dots = []

folds = []

max_x = 0
max_y = 0


def read_dots(input):
    line = input.pop(0)
    while line:
        dots.append(tuple(int(x) for x in line.split(',')))
        line = input.pop(0)

    return input


def read_folds(input):
    for line in input:
        _, _, fold = line.split()
        folds.append(fold.split('='))
        folds[-1][-1] = int(folds[-1][-1])


def do_fold_up(y):
    global dots, max_y

    for i, dot in enumerate(dots):
        if dot[1] > y:
            # print(f"Folding {dot} to ", end='')
            dots[i] = (dot[0], max_y - dot[1])
            # print(f"{dots[i]}")

    max_y = y - 1


def do_fold_left(x):
    global dots, max_x

    for i, dot in enumerate(dots):
        if dot[0] > x:
            # print(f"Folding {dot} to ", end='')
            dots[i] = (max_x - dot[0], dot[1])
            # print(f"{dots[i]}")

    max_x = x - 1


def do_fold(fold):
    if fold[0] == 'x':
        do_fold_left(fold[1])
    else:
        do_fold_up(fold[1])


def main_a():
    global max_x, max_y
    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)

    input = read_dots(input)
    max_x = max(x[0] for x in dots)
    max_y = max(x[1] for x in dots)

    read_folds(input)
    for fold in folds:
        sz = fold[1] * 2
        if fold[0] == 'x':
            max_x = max(max_x, sz)
        else:
            max_y = max(max_y, sz)

    # print(f'{max_x=}, {max_y=}')

    # print_dots(folds[0])
    do_fold(folds[0])
    # print()
    # print_dots()
    # do_fold(folds[1])
    # print()
    # print_dots()

    c = Counter(dots)
    print('Visible dots:', len(c))


def main_b():
    global max_x, max_y
    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)

    input = read_dots(input)
    max_x = max(x[0] for x in dots)
    max_y = max(x[1] for x in dots)

    read_folds(input)
    for fold in folds:
        sz = fold[1] * 2
        if fold[0] == 'x':
            max_x = max(max_x, sz)
        else:
            max_y = max(max_y, sz)

    # print(f'{max_x=}, {max_y=}')

    # print_dots(folds[0])
    for fold in folds:
        do_fold(fold)
    # print()
    # print_dots()
    # do_fold(folds[1])
    # print()
    # print_dots()

    # c = Counter(dots)
    # print('Visible dots:', len(c))

    print_dots()


def print_dots(fold=None):
    fold_dots = []

    if fold is not None:
        if fold[0] == 'y':
            for j in range(max_x + 1):
                fold_dots.append((j, fold[1]))
        else:
            for i in range(max_y + 1):
                fold_dots.append((fold[1], i))

    for i in range(max_y + 1):
        for j in range(max_x + 1):
            if (j, i) in dots:
                print('#', end='')
                if (j, i) in fold_dots:
                    raise RuntimeError(f'ERROR: folding line {fold} contains dot {(j, i)}!')
            else:
                if (j, i) in fold_dots:
                    print('-', end='')
                else:
                    print(' ', end='')

        print()


if __name__ == '__main__':
    init()
    writebar(puzzle.day, 'b')
    # main_a()
    main_b()
