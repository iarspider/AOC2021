from aocd.models import Puzzle
from aocd.transforms import lines, numbers
from aocbar import writebar

from collections import Counter

puzzle = Puzzle(year=2021, day=5)


class IAmDone(Exception):
    pass


class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        y = self.y
        while y > 1:
            y /= 10

        return hash(self.x + y)


class Line(object):
    def __init__(self, x1, y1, x2, y2, filter=False):
        p1 = x1
        p2 = x2
        self.valid = True

        if filter and (x1 != x2 and y1 != y2):
            # print(f"Invalid line {x1}, {y1} -> {x2}, {y2}")
            self.valid = False

        try:
            self.a = (y2 - y1) // (x2 - x1)
            self.b = y1 - self.a * x1
            self.vert = False
        except ZeroDivisionError:
            self.a = x1
            self.b = None
            p1 = y1
            p2 = y2
            self.vert = True

        if p1 < p2:
            self.range = range(p1, p2 + 1)
        else:
            self.range = range(p1, p2 - 1, -1)

    def __repr__(self):
        if not self.valid:
            return 'Invalid line'
        else:
            if self.vert:
                return f'Vertical line at {self.a}: {list(self.range)}'
            else:
                return f'Line {self.a}*x+{self.b}: {list(self.range)}'

    def __iter__(self):
        if self.vert:
            for y in self.range:
                yield Coordinate(self.a, y)
        else:
            for x in self.range:
                yield Coordinate(x, self.a * x + self.b)


def print_map(map):
    smap = []
    for i in range(10):
        smap.append(list('.' * 10))

    for pos, c in map.items():
        smap[pos.y][pos.x] = str(c)

    print('\n'.join(''.join(foo) for foo in smap))


def main_a():
    # input = numbers(puzzle.example_data)
    input = numbers(puzzle.input_data)
    map = Counter()
    for line in input:
        this_line = Line(*line, filter=True)
        if this_line.valid:
            # print(line)
            # print(this_line)
            map.update(this_line)

    # print(map)
    # print_map(map)
    count = 0
    for c in map.values():
        if c > 1:
            count += 1

    print(count)

def main_b():
    # input = numbers(puzzle.example_data)
    input = numbers(puzzle.input_data)
    map = Counter()
    for line in input:
        this_line = Line(*line, filter=False)
        if this_line.valid:
            # print(line)
            # print(this_line)
            map.update(this_line)

    # print(map)
    # print_map(map)
    count = 0
    for c in map.values():
        if c > 1:
            count += 1

    print(count)


if __name__ == '__main__':
    writebar(5, 'b')
    # print(len(lines(puzzle.input_data)))
    # print(len(lines(puzzle.input_data)[0]))
    # main_a()
    main_b()
