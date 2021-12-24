import itertools
import os
from math import sqrt

from aocd.models import Puzzle
from aocd.transforms import lines, numbers

from colorama import init
from termcolor import colored

from aocbar import writebar

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))

xrange = range(1000, 1000)
yrange = range(1000, 1000)


def dummy(*args, **kwargs):
    return


def shoot(vx, vy, printf=print):
    x = 0
    y = 0
    ymax = -1000
    ymin = min(yrange)
    flag = True
    hit = False
    step = 0
    while flag:
        printf(f"Before step {step}: {x} + {vx}, {y} + {vy}, {ymax=}")
        x += vx
        y += vy
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        else:
            vx = 0

        ymax = max(y, ymax)
        vy -= 1
        printf(f"After step {step}: {x} + {vx}, {y} + {vy}, {ymax=}")

        if x in xrange and y in yrange:
            printf("It's a hit!")
            hit = True
            if vy < 0:
                flag = False
        else:
            if y < ymin and vy <= 0:
                printf("Fell too low")
                flag = False

        printf('-' * 80)
        step += 1
    return hit, ymax


def get_vxmin():
    a = 1
    b = -1
    c = -2 * min(xrange)

    vx1 = (-b + sqrt(b * b - 4 * a * c)) / (2 * a)
    vx2 = (-b - sqrt(b * b - 4 * a * c)) / (2 * a)

    if vx1 == vx2:
        if vx1 >= 0:
            return int(vx1)
        else:
            raise RuntimeError(f"This should never happen: vx1 = vx2 = {vx1} < 0!")
    else:
        if vx1 < 0 < vx2:
            return int(vx2)
        elif vx1 > 0 > vx2:
            return int(vx1)
        else:
            raise RuntimeError(f"This should never happen! {vx1}, {vx2}")


def main_a():
    global xrange, yrange
    input = lines(puzzle.input_data)[0]
    input = [int(x) for x in input.replace('target area: x=', '').replace('..', ' ').replace(',', '').replace('y=',
                                                                                                              '').split()]
    print(input)
    # return

    xrange = range(input[0], input[1] + 1)
    yrange = range(input[2], input[3] + 1)

    ymaxes = []

    # print(get_vxmin())
    # return

    for vx in range(get_vxmin(), max(xrange) + 1):
        for vy in range(0, 200):
            res, ymax = shoot(vx, vy, dummy)
            if res:
                ymaxes.append(ymax)
            # # if res:
            # #     print(vx, vy, res, ymax)
            # if res and ymax == 19900:
            #     res, ymax = shoot(vx, vy, print)
            #     return
            # ymaxes.append(ymax)

    print(max(ymaxes))
    # input = lines(puzzle.input_data)


def main_b():
    # input = lines(puzzle.input_data)
    global xrange, yrange
    # input = "target area: x=20..30, y=-10..-5"
    input = lines(puzzle.input_data)[0]
    input = [int(x) for x in input.replace('target area: x=', '').replace('..', ' ').replace(',', '').replace('y=',
                                                                                                              '').split()]
    print(input)
    # return

    xrange = range(input[0], input[1] + 1)
    yrange = range(input[2], input[3] + 1)

    cnt = 0

    # print(get_vxmin())
    # return

    for vx in range(get_vxmin(), max(xrange) + 1):
        for vy in range(-200, 200): # itertools.chain(range(-300, -200), (200, 300)):
            res, ymax = shoot(vx, vy, dummy)
            if res:
                cnt += 1
            # # if res:
            # #     print(vx, vy, res, ymax)
            # if res and ymax == 19900:
            #     res, ymax = shoot(vx, vy, print)
            #     return
            # ymaxes.append(ymax)

    print(cnt)
    # input = lines(puzzle.input_data)


if __name__ == '__main__':
    init()
    writebar(puzzle.day, 'b')
    # main_a()
    main_b()
