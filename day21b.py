import itertools
from collections import Counter

rolls: Counter
dummystats = {1: 0, 2: 0}


# Get possible outcomes (sums and number of combinations) from rolling 3d3
def get_rolls(sides: int):
    global rolls
    x = list(itertools.product(*itertools.repeat(range(1, sides + 1), 3)))
    rolls = Counter([sum(_) for _ in x])


# player1pos, player2pos: player positions
# player1score, player2score: player scores
# numUniverses: number of universes at the start of the round
def dummy_b(player1pos: int, player2pos: int, player1score: int, player2score: int, numUniverses: int):
    # Player 1 rolls
    for sumRolls1, numCombinations1 in rolls.items():
        # sumRolls1: sum of 3d3, numCombinations1: number of combinations
        # Calculate new position of Player 1
        newPlayer1pos = player1pos + sumRolls1
        # The board is circular, so 11 -> 1, 12->2, etc
        while newPlayer1pos > 10:
            newPlayer1pos -= 10

        # Calculate new score
        newPlayer1score = player1score + newPlayer1pos
        # Calculate new number of universes
        newNumUniverses = numUniverses * numCombinations1
        # Did P1 win?
        if newPlayer1score >= 21:
            dummystats[1] += newNumUniverses
            continue

        # P1 did not win, proceed to P2
        for sumRolls2, numCombinations2 in rolls.items():
            newPlayer2pos = player2pos + sumRolls2
            while newPlayer2pos > 10:
                player2pos -= 10
            sc2_ = player2score + newPlayer2pos
            newNumUniverses = newNumUniverses * numCombinations2
            # Did P2 win?
            if player2score >= 21:
                dummystats[2] += newNumUniverses
                continue

            # Neither P1 nor P2 won, let's roll again
            dummy_b(newPlayer1pos, newPlayer2pos, newPlayer1score, sc2_, newNumUniverses)


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
