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


# @functools.cache
def winOnTurn(pos: int, score: int, nTurn: int):  # , rolls=None):
    # global nTurn# , keys

    # if rolls is None:
    #     rolls = []

    print_('.' * (nTurn), end='')
    # print_(f'winOnTurn({pos=}, {score=}, {rolls=}), {nTurn=}', end='')
    print_(f'winOnTurn({pos=}, {score=}), {nTurn=}', end='')

    # if (pos, score, nTurn) in keys:
    #     print_()
    #     print_(f"Reached {pos=}, {score=}, {nTurn=} with different set of rolls")
    #     print_(f"Before:", keys.get((pos, score, nTurn)))
    #     print_(f"Now:   ", rolls)
    #     raise RuntimeError()
    #
    # keys[(pos, score, nTurn)] = rolls.copy()

    if score >= 21:
        print_(f' -> {nTurn}')
        stats[nTurn] += 1
        # return nTurn
        return

    print_()
    # c = Counter()

    for outcome in outcomes:
        newPos = pos + outcome
        while newPos > 10:
            newPos -= 10

        newScore = score + newPos
        print_('.' * (nTurn), end='')
        print_(f'Testing outcome {outcome}: {newScore}')

        # nTurn += 1
        # rolls.append(outcome)
        # res = winOnTurn(newPos, newScore, rolls)
        # rolls.pop()
        # res = winOnTurn(newPos, newScore)
        winOnTurn(newPos, newScore, nTurn + 1)
        # nTurn -= 1
        # print_('.' * (nTurn), end='')

        # print_(f'result: {res}', end='; ')
        # if isinstance(res, int):
        #     c.update((res,))
        # else:
        #     c = c + res
        # print_(f'counter now', c)

    # return c
    return


dummystats = {1: 0, 2: 0}


def dummy_b(p1: int, p2: int, sc1: int, sc2: int, nn1: int, nn2: int):
    for o1, n1 in outcomes.items():
        p1_ = (p1 + o1) % 10
        sc1_ = sc1 +  (p1_ + 1)
        nn1_ = nn1 * n1
        if sc1_ >= 21:
            dummystats[1] += nn1_
            continue

        for o2, n2 in outcomes.items():
            p2_ = (p2 + o2) % 10
            sc2_ = sc2 + (p2_ + 1)
            nn2_ = nn2 * n2
            if sc2 >= 21:
                dummystats[2] += nn2_
                continue

            dummy_b(p1_, p2_, sc1_, sc2_, nn1_, nn2_)


# Counter({7: 10856, 6: 9606, 8: 6345, 5: 4540, 9: 1587, 4: 1025, 3: 71, 10: 63})
# Counter({7: 14869, 6: 13472, 8: 7973, 5: 5882, 9: 1755, 4: 1001, 10: 63, 3: 34})
def main_b():
    global outcomes, stats
    writebar(puzzle.day, 'b')
    input = lines(puzzle.example_data)
    # input = lines(puzzle.input_data)
    p1 = int(input[0].rsplit()[-1]) - 1
    p2 = int(input[1].rsplit()[-1]) - 1

    # print(run(p1, [3, 3, 3, 3]))
    # print(run(p1, [3, 4, 3, 3, 4, 5]))

    outcomes = get_outcomes(3)
    print(outcomes)
    dummy_b(p1, p2, 0, 0, 1, 1)

    print(dummystats)

    # c1 = winOnTurn(p1, 0, 0)
    # winOnTurn(p1, 0, 0)
    # c1 = stats.copy()
    #
    # stats = Counter()
    # nTurn = 0
    # # c2 = winOnTurn(p2, 0, 0)
    # winOnTurn(p2, 0, 0)
    # c2 = stats.copy()
    #
    # print(c1)
    # print(c2)
    #
    # sum = 0
    # for k in c1.keys():
    #     n = 0
    #     for kk in c2.keys():
    #         if kk >= k:
    #             n += c2[kk]
    #     n *= c1[k]
    #     sum += n
    #
    # print(sum)
    # #           948180396
    # print(444356092776315)

    # Multiverse.append(Universe(pos=p1, score=0, turnN=0))
    #
    # nTurn = 0
    #
    # while any(x.score < 21 for x in Multiverse):
    #     print(f'== TURN {nTurn} ==')
    #     newUniverses: List[Universe] = []
    #     dropUnivesesIndices: List[int] = []
    #     u: Universe
    #     i: int
    #     for i, u in itertools.filterfalse(lambda x: x[1].score < 21, enumerate(Multiverse)):
    #         dropUnivesesIndices.insert(0, i)
    #         for outcome in outcomes:
    #             pos = u.pos + outcome
    #             while pos > 10:
    #                 pos -= 10
    #
    #             newUniverses.append(Universe(turnN=u.turnN + 1, score=u.score, pos=pos))
    #     for i in dropUnivesesIndices:
    #         Multiverse.pop(i)
    #
    #     Multiverse.extend(newUniverses)
    #     nTurn += 1


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
