import builtins
import functools
import os
from collections import namedtuple
from typing import List, Mapping

from aocd.models import Puzzle
from aocd.transforms import lines, numbers

from colorama import init
from termcolor import colored
from collections import Counter

from aocbar import writebar

import itertools

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))


class DeterministicDie(object):
    def __init__(self, sides):
        self._die = itertools.cycle(range(1, sides + 1))
        self.counter = 0

    def roll(self):
        self.counter += 1
        return next(self._die)


class Player(object):
    def __init__(self, die, pos, max_score=1000):
        self.pos = pos
        self.die = die
        self.score = 0
        self.max_score = max_score

    def move(self):
        steps = sum(self.die.roll() for _ in range(3))
        self.pos += steps
        while self.pos > 10:
            self.pos -= 10

        self.score += self.pos

    def won(self):
        return self.score >= self.max_score


def main_a():
    writebar(puzzle.day, 'a')
    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)

    die = DeterministicDie(100)

    player1 = Player(die, int(input[0].rsplit()[-1]))
    player2 = Player(die, int(input[1].rsplit()[-1]))

    while True:
        player1.move()
        if player1.won():
            break
        player2.move()
        if player2.won():
            break

    if player2.won():
        print(player1.score * die.counter)
    else:
        print(player2.score * die.counter)


outcomes: Mapping[int, int]
# nTurn: int = 0
stats: Counter = Counter()
# keys = {}

print_ = builtins.print


def dummy_print(*values, sep=None, end=None, file=None, flush=None):
    return


def winOnTurn(pos: int, score: int, nTurn: int, nOutcomes: int):  # , rolls=None):
    print_('.' * (nTurn), end='')
    print_(f'winOnTurn({pos=}, {score=}, {nTurn=}, {nOutcomes=})', end='')

    if score >= 21:
        print_(f' -> {nTurn}')
        stats[nTurn] += nOutcomes
        return

    print_()

    for outcome, num in outcomes.items():
        newPos = pos + outcome
        while newPos > 10:
            newPos -= 10

        newScore = score + newPos
        print_('.' * (nTurn), end='')
        print_(f'Testing outcome {outcome} (x{num}): {newScore}')

        winOnTurn(newPos, newScore, nTurn + 1, nOutcomes * num)
    return


# Counter({7: 37322440, 8: 28186346, 6: 15358599, 9: 3837558, 5: 2573275, 4: 267290, 10: 22032, 3: 5401})
# Counter({7: 114160962, 8: 80965157, 6: 37883293, 9: 10211112, 5: 5561996, 4: 229668, 10: 68283, 3: 1402})
def main_b():
    global outcomes, stats
    writebar(puzzle.day, 'b')
    input = lines(puzzle.example_data)
    # input = lines(puzzle.input_data)
    p1 = int(input[0].rsplit()[-1]) - 1
    p2 = int(input[1].rsplit()[-1]) - 1

    outcomes = get_outcomes(3)

    winOnTurn(p1, 0, 0, 1)
    c1 = stats.copy()

    stats = Counter()
    winOnTurn(p2, 0, 0, 1)
    c2 = stats.copy()

    print(c1)
    print(c2)

    sum = 0
    for k in c1.keys():
        n = 0
        for kk in c2.keys():
            if kk >= k:
                n += c2[kk]
        n *= c1[k]
        sum += n

    print(sum)
    # #     14722393552430499
    # print(444356092776315)


def get_outcomes(sides: int) -> Mapping[int, int]:
    x = list(itertools.product(*itertools.repeat(range(1, sides + 1), 3)))
    c = Counter([sum(_) for _ in x])

    return c


def run(pos, rolls):
    score = 0
    for r in rolls:
        print(f'{score=}, {pos=}, {r=}')
        pos += r
        print(f'Now {pos=}')
        while pos > 10:
            pos -= 10

        print(f'Corrected {pos=}')
        score += pos
        print(f'Score now {score}')
    return score


if __name__ == '__main__':
    init()
    get_outcomes(3)
    # main_a()
    main_b()
