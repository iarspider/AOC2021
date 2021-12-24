import os
from itertools import permutations, combinations

from aocd.models import Puzzle
from aocd.transforms import lines
from colorama import init

from aocbar import writebar
from day19math import *

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))

matrices = []

beacons = []
dists = []

matched_beacons = []
scanner_transforms = {}


def dist(v1, v2):
    return np.sum((v1 - v2) ** 2)


def generate_distances():
    for scanner in beacons:
        dists.append([])
        for v1, v2 in combinations(scanner, 2):
            dists[-1].append((v1, v2, dist(v1, v2)))


def find_matches():
    matches = {}
    for is1, is2 in combinations(range(len(beacons)), 2):
        match = []
        for ib1, jb1, d1 in dists[is1]:
            for ib2, jb2, d2 in dists[is2]:
                if d1 == d2:
                    match.append((ib1, jb1, ib2, jb2))

        if len(match) >= 66:
            matches[(is1, is2)] = match
            # print(f"Scanners {is1} and {is2} have {len(match)} matching pairs")

    return matches


def transform(v, offset, m):
    vt = m * v + offset
    return vt


def calc_scanner_transf(is1, is2, match_):
    print(f'Trying to calculate transformation from {is2} to {is1}')
    match0 = match_[0]
    match1 = match_[1:]
    ib1, jb1, ib2, jb2 = match0

    # print('Assuming ib2->ib1 and jb2->jb1 in the 1st pair')

    transformation = {'off': None, 'rot': None, 'cnt': 0}

    for im, m in enumerate(matrices):
        # print(f'Trying matrix {im + 1} / {len(matrices)}...', end='')
        off = ib1 - transform(ib2, [[0], [0], [0]], m)

        b1 = ib1
        b2 = transform(ib2, off, m)
        if not np.array_equal(b1, b2):
            raise RuntimeError()

        cnt = 0

        for b2 in beacons[is2]:
            bt = transform(b2, off, m)
            for b1 in beacons[is1]:
                if np.array_equal(bt, b1):
                    cnt += 1

        if cnt >= 12:
            print(f" Got {cnt} matches")
            found = True
            if transformation['cnt'] < cnt:
                transformation['off'] = off
                transformation['rot'] = m
                transformation['cnt'] = cnt

    if transformation['cnt'] > 0:
        del transformation['cnt']
        scanner_transforms[(is2, is1)] = transformation
        return True

    # print('Assuming ib2->jb1 and jb2->ib1 in the 1st pair')

    for im, m in enumerate(matrices):
        # print(f'Trying matrix {im + 1} / {len(matrices)}...', end='')
        off = jb1 - transform(ib2, [[0], [0], [0]], m)

        b1 = jb1
        b2 = transform(ib2, off, m)
        if not np.array_equal(b1, b2):
            raise RuntimeError()

        cnt = 0

        for b2 in beacons[is2]:
            bt = transform(b2, off, m)
            for b1 in beacons[is1]:
                if np.array_equal(bt, b1):
                    cnt += 1

        if cnt >= 12:
            print(f" Got {cnt} matches")
            found = True
            if transformation['cnt'] < cnt:
                transformation['off'] = off
                transformation['rot'] = m
                transformation['cnt'] = cnt

        if transformation['cnt'] > 0:
            del transformation['cnt']
            scanner_transforms[(is2, is1)] = transformation
            return True

        print("No transformation found")
        return False


def filter_beacons():
    global matched_beacons

    filtered_beacons = []
    for mb in matched_beacons:
        for fb in filtered_beacons:
            if np.array_equal(mb, fb):
                break
        else:
            filtered_beacons.append(mb)

    matched_beacons = filtered_beacons.copy()
    print(f"After filtering, got {len(matched_beacons)} beacons")


def transform_scanner(from_s, to_s, data=None):
    res = []
    tr = scanner_transforms.get((from_s, to_s), None)
    if tr is None:
        return None

    data = data or beacons[from_s]
    for b in data:
        res.append(transform(b, tr['off'], tr['rot']))

    return res


def main_a():
    global matched_beacons
    input = lines(puzzle.example_data)
    # input = lines(puzzle.input_data)
    for line in input:
        if line.startswith('---'):
            beacons.append([])
        elif (not line):
            continue
        else:
            beacons[-1].append(np.array([int(x) for x in line.split(',')], ndmin=2, dtype=np.int32).transpose())

    for i in range(len(beacons)):
        scanner_transforms[(i, i)] = {'rot': np.identity(3), 'off': [0, 0, 0]}

    generate_distances()
    matches = find_matches()

    for k, v in matches.items():
        calc_scanner_transf(k[0], k[1], v)
    #
    # transformed_beacons = transform_scanner(4, 1)
    # tf = scanner_transforms[(1, 0)]
    # for b0 in beacons[1]:
    #     for b1 in transformed_beacons:
    #         if np.array_equal(b0, b1):
    #             # print(f'{b0=}')
    #             # print(f'{b1=}')
    #             b = transform(b0, tf['off'], tf['rot']).transpose().tolist()[0]
    #             # print(f'{b=}')
    #             # b0.transpose()[0]
    #             print("{0},{1},{2}".format(*b))
    #
    # print('offset', (scanner_transforms[(4, 1)]['off'] + scanner_transforms[(1, 0)]['off']).transpose())
    # tr41 = scanner_transforms[(4, 1)]
    # tr10 = scanner_transforms[(1, 0)]
    #
    # s4in1 = transform([[0], [0], [0]], tr41['off'], tr41['rot'])
    # s1in0 = transform(s4in1, tr10['off'], tr10['rot'])
    #
    # print(s1in0)

    transformed_beacons = {}
    for i in range(0, len(beacons)):
        transformed_beacons[i] = beacons[i].copy()

    for i in range(len(beacons) - 1, -1, -1):
        for j in range(0, i):
            transformation = scanner_transforms.get((i, j))
            if transformation is not None:
                print(f"Will transform {len(transformed_beacons[i])} from {i} to {j} (already has "
                      f"{len(transformed_beacons[j])} beacons)")
                for b in transformed_beacons[i]:
                    bb = transform(b, transformation['off'], transformation['rot'])
                    transformed_beacons[j].append(bb)
                break
            else:
                print(f"No transformation found {i} -> {j}")

    matched_beacons = transformed_beacons[0]
    print(f"Got {len(matched_beacons)} beacons before filtering")
    filter_beacons()


def main_b():
    input = lines(puzzle.example_data)
    # input = lines(puzzle.input_data)


if __name__ == '__main__':
    init()
    matrices = generate_matrices()
    writebar(puzzle.day, 'a')
    main_a()
    # main_b()
