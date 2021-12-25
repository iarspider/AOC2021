import itertools
import os
from collections import Counter

from aocd.models import Puzzle
from aocd.transforms import lines
from colorama import init

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))

rolls: Counter


def get_rolls(sides: int):
    global rolls
    x = list(itertools.product(*itertools.repeat(range(1, sides + 1), 3)))
    rolls = Counter([sum(_) for _ in x])


dummystats = {1: 0, 2: 0}


def dummy_b(p1: int, p2: int, sc1: int, sc2: int, nn1: int, nn2: int):
    for o1, n1 in rolls.items():
        p1_ = p1 + o1
        while p1_ > 10:
            p1_ -= 10

        sc1_ = sc1 + p1_
        nn1_ = nn1 * n1
        if sc1_ >= 21:
            dummystats[1] += nn1_
            continue

        for o2, n2 in rolls.items():
            p2_ = p2 + o2
            while p2_ > 10:
                p2 -= 10
            sc2_ = sc2 + p2_
            nn2_ = nn2 * n2
            if sc2 >= 21:
                dummystats[2] += nn2_
                continue

            dummy_b(p1_, p2_, sc1_, sc2_, nn1_, nn2_)


def main_b():
    # writebar(puzzle.day, 'b')
    input = lines(puzzle.example_data)
    # input = lines(puzzle.input_data)
    p1 = int(input[0].rsplit()[-1])
    p2 = int(input[1].rsplit()[-1])

    get_rolls(3)
    dummy_b(p1, p2, 0, 0, 1, 1)
    print(dummystats)


# Result:  {1: 2508094104341,   2: 1720527181002}
# Example: {1: 444356092776315, 2: 341960390180808}

if __name__ == '__main__':
    init()
    get_rolls(3)
    # main_a()
    main_b()