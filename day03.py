import copy
from collections import defaultdict

from aocd.models import Puzzle
from aocd.transforms import lines, numbers
from aocbar import writebar

puzzle = Puzzle(year=2021, day=3)


def main_a():
    gam_rate = ''
    eps_rate = ''

    sum = []
    append = True

    input = lines(puzzle.input_data)
    # input = lines(puzzle.example_data)

    for line in input:
        for i, bit in enumerate(line):
            if append:
                sum.append(int(bit) * 2 - 1)
            else:
                sum[i] += int(bit) * 2 - 1

        append = False

    for bit in sum:
        bit = bit / abs(bit)
        gam_rate += str(int((1 + bit) // 2))
        eps_rate += str(int((1 - bit) // 2))

    gamma = int(gam_rate, 2)
    epsilon = int(eps_rate, 2)

    print(gamma * epsilon)


def main_b():
    def find_common(input, i, most=True):
        sum = 0
        for line in input:
            bit = line[i]
            sum += int(bit) * 2 - 1

        if sum == 0:
            sum = 1
        bit = sum / abs(sum)
        
        return str(int((1 + bit) // 2)) if most else str(int((1 - bit) // 2))

    def filter_input(input, prefix):
        return [x for x in input if x.startswith(prefix)]

    filtered_data = defaultdict(list)

    input_most = lines(puzzle.input_data)
    # input_most = lines(puzzle.example_data)
    input_least = copy.copy(input_most)
    
    line_len = len(input_most[0])

    prefix_least = ''
    prefix_most = ''
    
    do_most = True
    do_least = True

    for i in range(line_len):
        print(f"Considering bit at pos {i}")
        if do_most:
            mc = find_common(input_most, i, True)
            prefix_most += mc
            input_most = filter_input(input_most, prefix_most)
            print(f'\t{prefix_most=}')
            print(f'\t{input_most=}')
            if len(input_most) == 1:
                prefix_most = input_most[0]
                do_most = False

        print('***')
        if do_least:
            lc = find_common(input_least, i, False)
            prefix_least += lc
            input_least = filter_input(input_least, prefix_least)
            print(f'\t{prefix_least=}')
            print(f'\t{input_least=}')
            if len(input_least) == 1:
                prefix_least = input_least[0]
                do_least = False

    if do_most:
        print("ERROR: did not find most common!")
        exit(1)

    if do_least:
        print("ERROR: did not find least common!")
        exit(1)

    print(f"{prefix_most=}, {prefix_least=}")
    most = int(prefix_most, 2)
    least = int(prefix_least, 2)

    ret = most*least
    print(f"{most=}, {least=}; {ret=}")

if __name__ == '__main__':
    writebar(3, 'b')
    # print(len(lines(puzzle.input_data)))
    # print(len(lines(puzzle.input_data)[0]))
    main_b()
