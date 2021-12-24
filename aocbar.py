import sys


def writebar(day, step):
    try:
        day = int(day)
        if day < 1 or day > 25:
            raise ValueError()
    except ValueError:
        print(f"Invalid day: {day}")
        exit(1)

    if step not in ('a', 'b'):
        print(f"Invalid step: {step}, must be 'a' or 'b'")
        exit(1)

    with open('aocbar.txt', 'w') as f:
        line = '#' * (day - 1)
        if step == 'a':
            line += '-'
        else:
            line += '='

        while len(line) < 25:
            line += '.'

        print('ADV3NT OF C0DE 2021 [' + line + ']', file=f)

if __name__ == '__main__':
    # main(sys.argv[1:])
    writebar(2, 'a')
