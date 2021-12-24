import functools
from collections import defaultdict

from aocd.models import Puzzle
from aocd.transforms import lines, numbers

from aocbar import writebar
import os
import datetime

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))


class IAmDoneException(Exception):
    pass


class MyList(list):
    def __getitem__(self, y):
        if y < 0:
            raise IndexError('list index out of range')
        else:
            return list.__getitem__(self, y)


def main_a():
    # input_r = lines(puzzle.example_data)
    input_r = lines(puzzle.input_data)

    input = MyList()
    for line in input_r:
        input.append(MyList(int(x) for x in line))

    summ = 0

    for i in range(len(input)):
        for j in range(len(input[i])):
            cur_h = input[i][j]
            try:
                for d in (0, 1):
                    dd = 2 * d - 1
                    try:
                        near_h = input[i + dd][j]
                        if near_h < cur_h:
                            raise IAmDoneException()
                    except IndexError:
                        pass

                    try:
                        near_h = input[i][j + dd]
                        if near_h < cur_h:
                            raise IAmDoneException()
                    except IndexError:
                        pass
            except IAmDoneException:
                pass
            else:
                print(i, j)
                summ += cur_h + 1

    print(summ)


def main_aa():
    # input_r = lines(puzzle.example_data)
    input_r = lines(puzzle.input_data)

    szr = len(input_r)
    szc = len(input_r[0])

    input = [[9] * (szc + 2)]

    for line in input_r:
        input.append([9, *(int(x) for x in line), 9])

    input.append([9] * (szc + 2))

    summ = 0

    for i in range(1, szr + 1):
        for j in range(1, szc + 1):
            cur_h = input[i][j]
            cnt = 0
            for d in (0, 1):
                dd = 2 * d - 1
                near_h = input[i + dd][j]
                if near_h < cur_h:
                    print('one')
                    break
                cnt += (near_h == cur_h)

                near_h = input[i][j + dd]
                if near_h < cur_h:
                    print('two')
                    break
                cnt += (near_h == cur_h)
            else:
                # print(i - 1, j - 1, cur_h, input[i-1][j], input[i][j-1], input[i+1][j], input[i][j+1])
                if cnt != 4:
                    summ += cur_h + 1
                    print('({0:2d}'.format(i - 1), end=' ')
                    print('{0:2d})'.format(j - 1), end=' ')
                    print(cur_h, end=' ')
                    print('(', end='')

                    print(input[i - 1][j], input[i][j - 1], input[i + 1][j], input[i][j + 1], end='')
                    print(')')
                else:
                    print('three')
            print('---')
    print(summ)
    # 1719


#   ,
#   8
# .888;
#   8
#   :

class MyQueue(object):
    def __init__(self):
        self.lst = []

    def append(self, val):
        self.lst.append(val)
        if len(self.lst) == 4:
            self.lst.sort()
            self.lst.pop(0)


def main_b():
    def collect(x, y):
        size = 0
        cells_to_check = [(x, y)]
        while cells_to_check:
            i, j = cells_to_check.pop(0)
            cur_h = input[i][j]
            if cur_h == 9:
                continue
            size += 1

            input[i][j] = 9
            vals[cur_h].remove((i, j))

            for d in (0, 1):
                dd = 2 * d - 1
                near_h = input[i + dd][j]
                if near_h != 9 and near_h > cur_h:
                    cells_to_check.append((i + dd, j))

                near_h = input[i][j + dd]
                if near_h != 9 and near_h > cur_h:
                    cells_to_check.append((i, j + dd))

        return size

    # input_r = lines(puzzle.example_data)
    input_r = lines(puzzle.input_data)
    szr = len(input_r)
    szc = len(input_r[0])

    input = [[9] * (szc + 2)]

    for line in input_r:
        input.append([9, *(int(x) for x in line), 9])

    input.append([9] * (szc + 2))

    vals = defaultdict(list)

    d1 = datetime.datetime.now()

    for i in range(1, szr + 1):
        for j in range(1, szc + 1):
            cur_h = input[i][j]
            if cur_h < 9:
                vals[cur_h].append((i, j))

    dd = datetime.datetime.now() - d1
    print('Collecting vals took', dd)

    res = MyQueue()

    for h in range(0, 9):
        print(f'There are {len(vals[h])} cell(s) with value {h}')
        while vals[h]:
            x, y = vals[h][0]
            print(f'Rising from {x}, {y}')
            d1 = datetime.datetime.now()
            sz = collect(x, y)
            dd = datetime.datetime.now() - d1
            print(f'Done, size is {sz}, took {dd}')
            res.append(sz)
            print(res.lst)

    print('Answer is', functools.reduce(lambda a, b: a * b, res.lst))


if __name__ == '__main__':
    writebar(puzzle.day, 'b')
    # main_aa()
    main_b()
