from aocd.models import Puzzle
from aocd.transforms import lines, numbers
from aocbar import writebar

puzzle = Puzzle(year=2021, day=2)


def main():
    vpos = 0
    hpos = 0
    aim = 0

    input = lines(puzzle.input_data)
    # input = lines(puzzle.example_data)
    for line in input:
        verb, number = line.strip().split()
        try:
            number = int(number)
        except ValueError:
            print(f"Invalid number {number}")
            exit(1)

        if verb == 'forward':
            hpos += number
            vpos += aim * number
        elif verb == 'up':
            aim -= number
        elif verb == 'down':
            aim += number
        else:
            print(f'Invalid verb {verb}')
            exit(1)

    print(vpos * hpos)


if __name__ == '__main__':
    writebar(2, 'b')
    main()
