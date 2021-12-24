import os

from aocd.models import Puzzle
from aocd.transforms import lines, numbers

from colorama import init
from termcolor import colored

from aocbar import writebar

from PIL import Image, ImageDraw, ImageFont, ImageColor

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))

cave = []
queue = []
path = []

min_len = None
clen = 0

exit_ = None

delta = [[0, 1, 2, 3, 4], [1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7], [4, 5, 6, 7, 8]]


class CaveCell(object):
    def __init__(self, cost):
        self.total = 0
        self.in_cost = cost
        self.prev = None

    def check(self, other, pos):
        # print(f"check(): {self.total=}, {other.total=}, {self.in_cost=}, {self.prev=}")
        if self.prev is None or self.total > other.total + self.in_cost:
            self.total = other.total + self.in_cost
            self.prev = pos
            return True
        return False


def load_cave_a(input):
    global cave

    sz = len(input)
    szz = len(input)

    for i in range(sz + 2):
        cave.append([])
        for j in range(sz + 2):
            cave[-1].append(None)

    for i in range(0, 1):
        for j in range(0, 1):
            for ii, row in enumerate(input):
                for jj, cell in enumerate(row):
                    val = int(cell) + delta[i][j]
                    if val > 10:
                        val -= 9

                    cave[i * szz + ii + 1][j * szz + jj + 1] = CaveCell(val)


def load_cave_b(input):
    global cave

    sz = len(input) * 5
    szz = len(input)

    for i in range(sz + 2):
        cave.append([])
        for j in range(sz + 2):
            cave[-1].append(None)

    for i in range(0, 5):
        for j in range(0, 5):
            for ii, row in enumerate(input):
                for jj, cell in enumerate(row):
                    val = int(cell) + delta[i][j]
                    if val >= 10:
                        val -= 9

                    if val >= 10:
                        raise RuntimeError(f'ERROR: {i} + {ii}, {j} + {jj}, {int(cell)} + {delta[i][j]}, {val}')

                    cave[i * szz + ii + 1][j * szz + jj + 1] = CaveCell(val)


def flood():
    # cnt = 0
    # font = ImageFont.truetype("arial.ttf", 15)
    while queue:
        i, j = queue.pop(0)
        # print(f"Round {cnt}: check neighbours of", (i, j))

        for d in (0, 1):
            dd = 2 * d - 1
            if cave[i + dd][j] is not None:
                res = cave[i + dd][j].check(cave[i][j], (i, j))
                if res:
                    # print("Updated neighbour", i + dd, j)
                    queue.append((i + dd, j))
                else:
                    # print("Skipped neighbour", i + dd, j)
                    pass

            if cave[i][j + dd] is not None:
                res = cave[i][j + dd].check(cave[i][j], (i, j))
                if res:
                    # print("Updated neighbour", i, j + dd)
                    queue.append((i, j + dd))
                else:
                    # print("Skipped neighbour", i, j + dd)
                    pass
        #
        # cnt += 1
        # sz = len(cave) - 2
        # px = 50
        # img = Image.new('RGB', (px * sz, px * sz), (0, 0, 0))
        # canvas = ImageDraw.Draw(img)
        # maxx = None
        # for i in range(1, sz + 1):
        #     for j in range(1, sz + 1):
        #         if maxx is None or maxx < cave[i][j].total:
        #             maxx = cave[i][j].total
        #
        # step = maxx / 255
        # for i in range(1, sz + 1):
        #     for j in range(1, sz + 1):
        #         if cave[i][j].prev is not None:
        #             canvas.rectangle(((i - 1) * px, (j - 1) * px, i * px, j * px),
        #                              (int(round(cave[i][j].total // step)), 0, 0))
        #             canvas.text(((i - 1) * px, (j - 1) * px), str(cave[i][j].total), fill=(0, 0, 0), font=font)
        #
        # img.save(f'img/step{cnt:04d}.png')


def solve(pos):
    global clen, min_len
    print(f'Solve({pos})')
    path.append(pos)
    clen += cave[pos[0]][pos[1]].total
    if min_len is not None:
        if clen >= min_len:
            return False

    if pos == exit:
        min_len = clen
        return True

    for dd in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        i = pos[0] + dd[0]
        j = pos[1] + dd[1]
        if (i, j) in path:
            continue

        if cave[i][j] != None:
            res = solve((i, j))
            if res:
                return True

    path.pop()
    return False


def main_a():
    global exit_
    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)
    load_cave_a(input)

    exit_ = (len(cave) - 2, len(cave) - 2)

    queue.append((1, 1))
    cave[1][1].prev = (0, 0)
    flood()
    # solve((1, 1))
    print("Total is", cave[-2][-2].total)


def print_cave():
    for i in range(1, len(cave) - 1):
        print(''.join(str(x.in_cost) for x in cave[i][1:-1]))


def main_b():
    global exit_

    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)

    load_cave_b(input)
    # print_cave()
    # return

    exit_ = (len(cave) - 2, len(cave) - 2)

    queue.append((1, 1))
    cave[1][1].prev = (0, 0)
    flood()
    # solve((1, 1))
    print("Total is", cave[-2][-2].total)


if __name__ == '__main__':
    init()
    writebar(puzzle.day, 'b')
    # main_a()
    main_b()
