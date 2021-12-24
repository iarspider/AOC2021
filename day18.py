import os
import string
import math
from itertools import permutations

from aocd.models import Puzzle
from aocd.transforms import lines, numbers

from colorama import init
from termcolor import colored

from aocbar import writebar

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))


# class Pair(object):
#     def __init__(self, left, right, depth):
#         self.left: Union[int, Pair] = left
#         self.right: Union[int, Pair] = right
#         self.depth = depth
#
#     def __eq__(self, other):
#         if isinstance(other, Pair):
#             return self.left == other.left and self.right == other.right
#
#         return False
#
#     def __lt__(self, other):
#         return NotImplemented
#
#     def __gt__(self, other):
#         return NotImplemented

def add(left, right):
    return '[' + left + ',' + right + ']'


def explode(n):
    depth = 0
    last_op_sq = -1
    left_is_num = False
    right_is_num = False
    left = ''
    right = ''
    is_left = [True]
    for i, c in enumerate(n):
        if c == '[':
            depth += 1
            last_op_sq = i
            if is_left[-1]:
                left_is_num = False
            else:
                right_is_num = False

            is_left.append(True)
            left = ''
            right = ''

            continue
        elif c.isdigit():
            if is_left[-1]:
                left = left + c
                left_is_num = True
            else:
                right = right + c
                right_is_num = True
            continue
        elif c == ',':
            is_left[-1] = False
            continue
        elif c == ']':
            if depth <= 4:
                is_left.pop()
                depth -= 1
            else:
                if not (left_is_num and right_is_num):
                    is_left.pop()
                    depth -= 1
                else:
                    left = int(left)
                    right = int(right)
                    # Search left of "[" for a number
                    number_start = -1
                    number_end = -1
                    nl = ''
                    nr = ''
                    for il in range(last_op_sq, 0, -1):
                        if n[il].isdigit():
                            nl = n[il] + nl
                            if number_end == -1:
                                number_end = il + 1
                        else:
                            if number_end != -1:
                                number_start = il + 1
                                break

                    if nl:
                        nl = int(nl)
                        nl += left
                        nnl = n[:number_start] + str(nl) + n[number_end:last_op_sq]
                    else:
                        nnl = n[:last_op_sq]

                    # Search right of "]" for a number
                    number_start = -1
                    for ir in range(i, len(n)):
                        if n[ir].isdigit():
                            nr = nr + n[ir]
                            if number_start == -1:
                                number_start = ir
                        else:
                            if number_start != -1:
                                number_end = ir
                                break

                    if nr:
                        nr = int(nr)
                        nr += right
                        nnr = n[i + 1:number_start]
                        nnr = nnr + str(nr)
                        nnr = nnr + n[number_end:]
                    else:
                        nnr = n[i + 1:]

                    n = nnl + '0' + nnr
                    return (True, n)

    return (False, n)


def split(n):
    number_start = -1
    number_end = -1
    s = ''

    for i, c in enumerate(n):
        if c.isdigit():
            s = s + c
            if number_start == -1:
                number_start = i
        else:
            if number_start != -1:
                number_end = i
                if len(s) > 1:
                    break
                else:
                    number_start = -1
                    s = ''
    else:
        return (False, n)

    nl = n[:number_start]
    nr = n[number_end:]
    nc = int(s)
    left = math.floor(nc / 2)
    right = math.ceil(nc / 2)
    n = nl + '[' + str(left) + ',' + str(right) + ']' + nr
    return (True, n)


def reduce(n):
    flag = True
    while flag:
        res, n = explode(n)
        if res:
            # print("after explode: ", n)
            continue

        res, n = split(n)
        if res:
            # print("after split:   ", n)
            continue

        flag = False

    return n


def mag_r(n):
    last_op_sq = -1
    left_is_num = False
    right_is_num = False
    left = ''
    right = ''
    is_left = [True]
    for i, c in enumerate(n):
        if c == '[':
            last_op_sq = i
            if is_left[-1]:
                left_is_num = False
            else:
                right_is_num = False

            is_left.append(True)
            left = ''
            right = ''

            continue
        elif c.isdigit():
            if is_left[-1]:
                left = left + c
                left_is_num = True
            else:
                right = right + c
                right_is_num = True
            continue
        elif c == ',':
            is_left[-1] = False
            continue
        elif c == ']':
            if not (left_is_num and right_is_num):
                is_left.pop()
            else:
                left = int(left)
                right = int(right)
                nnl = n[:last_op_sq]
                nnr = n[i + 1:]

                n = nnl + str(3 * left + 2 * right) + nnr
                return (True, n)

    return (False, n)


def mag(n):
    flag = True
    # print(f"{flag=} {n=}")
    while flag:
        flag, n = mag_r(n)
        # print(f"{flag=} {n=}")

    return n


def main_a():
    # input = lines(puzzle.example_data)
    #
    # res, line = explode('[[[[[9,8],1],2],3],4]')
    # print(res, line)
    # res, line = explode('[7,[6,[5,[4,[3,2]]]]]')
    # print(res, line)
    # res, line = explode('[[6,[5,[4,[3,2]]]],1]')
    # print(res, line)
    # res, line = explode('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')
    # print(res, line)
    # res, line = explode('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
    # print(res, line)
    # res, line = split("[0, 10]")
    # print(res, line)
    # res, line = split("[0, 11]")
    # print(res, line)
    # res, line = split("[0, 12]")
    # print(res, line)
    # res = add("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]")
    # print(res)
    # res = reduce(res)
    # print(res)
    # res = mag('[9,1]')
    # print(res)
    # res = mag('[1,9]')
    # print(res)
    # res = mag('[[9,1],[1,9]]')
    # print(res)
    # res = add('[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]', '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]')
    # res = reduce(res)
    # print(res)
    # print()
    # res = add(res, '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]')
    # res = reduce(res)
    # print(res)
    # print()
    # res = add(res, '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]')
    # res = reduce(res)
    # print(res)
    # print()
    # res = add(res, '[7,[5,[[3,8],[1,4]]]]')
    # res = reduce(res)
    # print(res)
    # print()
    # res = add(res, '[[2,[2,2]],[8,[8,1]]]')
    # res = reduce(res)
    # print(res)
    # print()
    # res = add(res, '[2,9]')
    # res = reduce(res)
    # print(res)
    # print()
    # res = add(res, '[1,[[[9,3],9],[[9,0],[0,7]]]]')
    # res = reduce(res)
    # print(res)
    # print()
    # res = add(res, '[[[5,[7,4]],7],1]')
    # res = reduce(res)
    # print(res)
    # print()
    # res = add(res, '[[[[4,2],2],6],[8,7]]')
    # res = reduce(res)
    # print(res)
    # print()
    #
    # res = mag('[[1,2],[[3,4],5]]')
    # print(res)
    # res = mag('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
    # print(res)
    # res = mag('[[[[1,1],[2,2]],[3,3]],[4,4]]')
    # print(res)
    # res = mag('[[[[3,0],[5,3]],[4,4]],[5,5]]')
    # print(res)
    # res = mag('[[[[5,0],[7,4]],[5,5]],[6,6]]')
    # print(res)
    # res = mag('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]')
    # print(res)

    #     input = lines("""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    # [[[5,[2,8]],4],[5,[[9,9],0]]]
    # [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    # [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    # [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    # [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    # [[[[5,4],[7,7]],8],[[8,3],8]]
    # [[9,3],[[9,9],[6,[4,9]]]]
    # [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    # [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""")
    input = lines(puzzle.input_data)
    res = input[0]
    for part in input[1:]:
        res = add(res, part)
        res = reduce(res)

    print(res)
    print(mag(res))


def main_b():
    input = lines("""[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""")
    input = lines(puzzle.input_data)

    max_mag = 0
    comb = None

    for a, b in permutations(input, 2):
        res = add(a, b)
        res = reduce(res)
        resm = int(mag(res))
        if resm > max_mag:
            max_mag = resm
            comb = (a, b)

    a, b = comb
    print(f"{max_mag=}")
    print(f"{a=} + {b=}")
    res = add(a, b)
    res = reduce(res)
    print(f"{res=}")


if __name__ == '__main__':
    init()
    writebar(puzzle.day, 'b')
    # main_a()
    main_b()
