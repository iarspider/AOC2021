from aocd.models import Puzzle
from aocd.transforms import lines, numbers


puzzle = Puzzle(year=2021, day=1)
def main():
    input = numbers(puzzle.input_data)
    # input = numbers(puzzle.example_data)
    res = 0
    last_sum = None
    for p1, p2, p3 in zip(input, input[1:], input[2:]):
        # res += 1 if p1 < p2 else 0
        sum = p1 + p2 + p3
        if last_sum is not None:
            res += 1 if last_sum < sum else 0

        last_sum = sum

    print(res)

if __name__ == '__main__':
    main()