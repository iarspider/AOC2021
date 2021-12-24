from aocd.models import Puzzle
from aocd.transforms import lines, numbers
from aocbar import writebar

from typing import List

puzzle = Puzzle(year=2021, day=4)


class Line(object):
    def __init__(self):
        self.data = {}

    def append(self, value):
        self.data[value] = False
        if len(self.data) > 5:
            print('Error: too many values in line or column')
            exit(1)

    def mark(self, value):
        if value in self.data:
            self.data[value] = True

    def all(self):
        return all(self.data.values())


class Board(object):
    def __init__(self, grid: List[List[int]]):
        self.rows = []
        self.cols = []
        self.sum_unmarked = 0
        self.score = 0
        self.numbers = []
        self.won = False
        self.seen = False

        for i in range(5):
            self.rows.append(Line())
            self.cols.append(Line())

        for i in range(5):
            for j in range(5):
                value = grid[i][j]
                self.rows[i].append(value)
                self.cols[j].append(value)
                self.numbers.append(value)
                self.sum_unmarked += value

    def mark(self, value):
        if self.won:
            return

        if value not in self.numbers:
            return

        self.sum_unmarked -= value

        for i in range(5):
            self.rows[i].mark(value)
            self.cols[i].mark(value)
            if self.rows[i].all() or self.cols[i].all():
                self.won = True
                self.score = self.sum_unmarked * value


class IAmDone(Exception):
    pass


def main_a():
    # input = numbers(puzzle.example_data)
    input = numbers(puzzle.input_data)
    calls = input.pop(0)
    boards = []
    for i in range(0, len(input), 5):
        boards.append(Board(input[i:i + 5]))

    try:
        for call in calls:
            print(f'{call=}')
            for b in boards:
                b.mark(call)
                if b.won:
                    print(b.score)
                    raise IAmDone()
    except IAmDone:
        pass
    else:
        print("No winning boards!")
    return


def main_b():
    # input = numbers(puzzle.example_data)
    input = numbers(puzzle.input_data)
    calls = input.pop(0)
    boards = []
    for i in range(0, len(input), 5):
        boards.append(Board(input[i:i + 5]))

    last = None
    for call in calls:
        print(f'{call=}')
        for i, b in enumerate(boards):
            print(f'{i=}, {b.seen=}, {b.won=}')
            b.mark(call)
            if b.won and not b.seen:
                print("got a winner!")
                b.seen = True
                last = b

        if all(x.won for x in boards):
            break

    if last is None:
        print("Non winning boards!")
    else:
        print(last.score)
    return


if __name__ == '__main__':
    writebar(4, 'b')
    # print(len(lines(puzzle.input_data)))
    # print(len(lines(puzzle.input_data)[0]))
    # main_a()
    main_b()
