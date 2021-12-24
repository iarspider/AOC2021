import itertools
from functools import reduce

from aocd.models import Puzzle
from aocd.transforms import lines

from aocbar import writebar

puzzle = Puzzle(year=2021, day=8)

example_data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


def main_a():
    # input = lines(example_data)
    input = lines(puzzle.input_data)

    cnt = 0
    for line in input:
        _, num = line.split('|')
        digits = num.split(' ')
        for dig in digits:
            if len(dig) in (2, 3, 4, 7):
                print(dig, end=' ')
                cnt += 1

        print()

    print(cnt)


def main_b():
    # input = lines(example_data)
    # input = ['acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf']
    input = lines(puzzle.input_data)

    digits_a = [frozenset('abcefg'), frozenset('cf'), frozenset('acdeg'),
               frozenset('acdfg'), frozenset('bcdf'),
               frozenset('abdfg'), frozenset('abdefg'), frozenset('acf'),
               frozenset('abcdefg'), frozenset('abcdfg')]

    digits_d = dict(zip(digits_a, range(10)))

    summ = 0

    for line in input:
        words, num = line.split('|')
        words = [set(w) for w in words.split(' ') if w]
        digits = [frozenset(n) for n in num.split(' ') if n]

        words = sorted(words, key=lambda x: len(x))
        # print(words)

        # First, figure out c/f
        cf = []
        for w in words:
            if len(w) == 2:
                cf = list(w)
                break

        # print('c is', '/'.join(cf))
        # print('f is', '/'.join(cf)[::-1])

        # Next, figure out a
        a = []
        for w in words:
            if len(w) == 3:
                a = list(w - set(cf))
                break

        # print('a is', a)

        # Figure out b,d
        bd = []
        for w in words:
            if len(w) == 4:
                bd = list(w ^ set(cf))
                break

        # print('b is', '/'.join(bd))
        # print('d is', '/'.join(bd)[::-1])

        # figure out d and g, and b as well
        fives = []
        for w in words:
            if len(w) == 5:
                fives.append(w)

        adg = reduce(lambda a, b: a & b, fives)
        # print('adg is', list(adg))
        dg = adg.difference(a)
        # print('dg is', list(dg))
        g = list(dg.difference(bd))
        # print('g is', g)
        d = list(dg.difference(g))
        # print('d is', d)
        b = list(set(bd).difference(d))
        # print('b is', b)

        # Figure out f, c
        f = []
        for w in fives:
            if len(w.difference(a, b, d, g)) == 1:
                f = list(w.difference(a, b, d, g))
                # print('f is', f)

        c = list(set(cf).difference(f))
        # print('c is', c)

        # Figure out e
        e = list(set('abcdefg').difference(a, b, c, d, f, g))
        # print('e is', e)

        # Now, build mapping
        # print('Final mapping:', ''.join(a+b+c+d+e+f+g))
        mapping = str.maketrans(''.join(a+b+c+d+e+f+g), 'abcdefg')

        res = 0
        for dig in digits:
            # print('input', dig)
            # print('mapped', ''.join(dig).translate(mapping))
            dig = frozenset(''.join(dig).translate(mapping))
            val = digits_d[dig]
            res = res*10 + val

        summ += res

    print(summ)


if __name__ == '__main__':
    writebar(puzzle.day, 'b')
    # main_a()
    main_b()
