import os
from collections import Counter

from aocd.models import Puzzle
from aocd.transforms import lines, numbers

from colorama import init
from termcolor import colored

from aocbar import writebar

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))


class Image(object):
    def __init__(self, data):
        self.offset = 3
        self.pixels = []
        self.r_max = len(data) + 2
        self.c_max = len(data[0]) + 2
        self.default = 0

        self.pixels.append([self.default] * (self.c_max))
        for ir in range(len(data)):
            self.pixels.append([self.default])
            for ic in range(len(data[ir])):
                self.pixels[-1].append({'.': 0, '#': 1}[data[ir][ic]])
            self.pixels[-1].append(self.default)

        self.pixels.append([self.default] * (self.c_max))

    def __getitem__(self, pos):
        return self.pixels[pos[0]][pos[1]]

    def __setitem__(self, pos, value):
        if (pos[0] not in self.rrange) or (pos[1] not in self.crange):
            raise IndexError()
        self.pixels[pos[0]][pos[1]] = value

    @property
    def crange(self):
        return range(1, self.c_max - 1)

    @property
    def rrange(self):
        return range(1, self.r_max - 1)

    def __str__(self):
        res = []
        for r in range(len(self.pixels)):
            res.append('')
            for c in range(len(self.pixels[r])):
                res[-1] += '#' if self.pixels[r][c] == 1 else '.'

        return '\n'.join(res)

    def fix_borders(self):
        self.pixels[0] = [self.default] * self.c_max
        self.pixels[-1] = [self.default] * self.c_max
        for r in range(1, self.r_max - 1):
            self.pixels[r][0] = self.default
            self.pixels[r][-1] = self.default

    def expand(self):
        self.c_max += 2 * self.offset
        self.r_max += 2 * self.offset

        for _ in range(self.offset):
            self.pixels.insert(0, [self.default] * self.c_max)
            self.pixels.append([self.default] * self.c_max)

        for r in range(self.offset, self.r_max - self.offset):
            for _ in range(self.offset):
                self.pixels[r].insert(0, self.default)
                self.pixels[r].append(self.default)

    def count(self, light=False):
        cc = Counter()
        for r in range(1, self.r_max - 1):
            for c in range(1, self.c_max - 1):
                cc.update([self.pixels[r][c]])
        return cc[1 if light else 0]


def enhance(program, image):
    updates = []
    # print('== BEFORE EXPAND() ==')
    # print(str(image))
    image.expand()
    # print('== AFTER EXPAND() ==')
    # print(str(image))

    for r in image.rrange:
        for c in image.crange:
            code = ''
            cur_pix = image[(r, c)]
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    code += str(image[(r + dr, c + dc)])

            val = int(code, 2)
            new_pix = {'.': 0, '#': 1}[program[val]]
            # print(f'{r=},{c=},{code=},{val=}')
            # print(f'{cur_pix} -> {new_pix}')
            if new_pix != cur_pix:
                updates.append((r, c, new_pix))

    for r, c, val in updates:
        image[(r, c)] = val

    # print('== AFTER ENHANCE ==')
    # print(str(image))

    if image.default == 0:
        image.default = 0 if program[0] == '.' else 1
    else:
        image.default = 0 if program[-1] == '.' else 1

    image.fix_borders()
    # print('== AFTER FIX_BORDERS() ==')
    # print(str(image))
    # print('== END ==')


def main_a():
    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)

    program = input.pop(0)
    # program = lines(puzzle.input_data)[0]
    input.pop(0)  # empty line
    image = Image(input)

    print(str(image))

    print("== ENHANCE 1 ==")
    enhance(program, image)
    # print(str(image))
    print("== ENHANCE 2 ==")
    enhance(program, image)
    # print(str(image))
    print("Light pixels:", image.count(light=True))


def main_b():
    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)

    program = input.pop(0)
    input.pop(0)  # empty line
    image = Image(input)

    # print(str(image))
    # print(image.default)
    for i in range(50):
        print(f"== ENHANCE {i + 1} ==")
        enhance(program, image)
        # print(str(image))
        # print(image.default)

    print("Light pixels:", image.count(light=True))


if __name__ == '__main__':
    init()
    writebar(puzzle.day, 'b')
    # main_a()
    main_b()
