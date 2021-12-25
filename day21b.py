import itertools
from collections import Counter

rolls: Counter
dummystats = {1: 0, 2: 0}


# Get possible outcomes (sums and number of combinations) from rolling 3d3
def get_rolls(sides: int):
    global rolls
    x = list(itertools.product(*itertools.repeat(range(1, sides + 1), 3)))
    rolls = Counter([sum(_) for _ in x])


# p1, p2: player positions
# sc1, sc2: player scores
# nn: number of universes at the start of the round
def dummy_b(p1: int, p2: int, sc1: int, sc2: int, nn: int):
    # Player 1 rolls
    for o1, n1 in rolls.items():
        # o1: sum of 3d3, n1: number of combinations
        # Calculate new position of Player 1
        p1_ = p1 + o1
        # The board is circular, so 11 -> 1, 12->2, etc
        while p1_ > 10:
            p1_ -= 10

        # Calculate new score
        sc1_ = sc1 + p1_
        # Calculate new number of universes
        nn1_ = nn * n1
        # Did P1 win?
        if sc1_ >= 21:
            dummystats[1] += nn1_
            continue

        # P1 did not win, proceed to P2
        for o2, n2 in rolls.items():
            p2_ = p2 + o2
            while p2_ > 10:
                p2 -= 10
            sc2_ = sc2 + p2_
            nn2_ = nn1_ * n2
            # Did P2 win?
            if sc2 >= 21:
                dummystats[2] += nn2_
                continue

            # Neither P1 nor P2 won, let's roll again
            dummy_b(p1_, p2_, sc1_, sc2_, nn2_)


def main_b():
    get_rolls(3)
    dummy_b(4, 8, 0, 0, 1)
    print(dummystats)


# Result:  {1: 2508094104341,   2: 1720527181002}
# Example: {1: 444356092776315, 2: 341960390180808}

if __name__ == '__main__':
    get_rolls(3)
    # main_a()
    main_b()
