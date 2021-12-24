import os

from aocd.models import Puzzle
from aocd.transforms import lines, numbers

from aocbar import writebar

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))

example_data = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]"""


def main_a():
    score = {')': 3, ']': 57, '}': 1197, '>': 25137}
    pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}
    # input = lines(example_data)
    input = lines(puzzle.input_data)
    ans = 0
    for line in input:
        stack = [line[0]]
        for c in line[1:]:
            if c in pairs.keys():
                stack.append(c)
            else:
                cc = stack.pop()
                if pairs[cc] != c:
                    ans += score[c]
                    print(line, pairs[cc], c)
                    break

    print(ans)
    # input = lines(puzzle.input_data)


def main_b():
    # input = lines(example_data)
    input = lines(puzzle.input_data)
    score = {')': 1, ']': 2, '}': 3, '>': 4}
    pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}
    anss = []
    for line in input:
        ans = 0
        stack = [line[0]]
        for c in line[1:]:
            if c in pairs.keys():
                stack.append(c)
            else:
                cc = stack.pop()
                if pairs[cc] != c:
                    break
        else:
            for c in stack[::-1]:
                ans = ans * 5 + score[pairs[c]]
            anss.append(ans)
            # print(''.join(pairs[_] for _ in stack[::-1]), ans)

    anss.sort()
    # print(anss)
    i = len(anss) // 2
    print(anss[i])


if __name__ == '__main__':
    writebar(puzzle.day, 'b')
    # main_a()
    main_b()
