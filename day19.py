import os
from itertools import permutations, combinations, tee

from aocd.models import Puzzle
from aocd.transforms import lines
from colorama import init

from aocbar import writebar
from day19math import *

import igraph

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))

matrices = []

beacons = []
dists = []

matched_beacons = []
scanner_transforms = {}

g = igraph.Graph()


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def dist(v1, v2):
    return np.sum((v1 - v2) ** 2)


def generate_distances():
    for scanner in beacons:
        dists.append([])
        for v1, v2 in combinations(scanner, 2):
            dists[-1].append((v1, v2, dist(v1, v2)))


def find_matches():
    matches = {}
    for is1, is2 in permutations(range(len(beacons)), 2):
        match = []
        for ib1, jb1, d1 in dists[is1]:
            for ib2, jb2, d2 in dists[is2]:
                if d1 == d2:
                    match.append((ib1, jb1, ib2, jb2))

        if len(match) >= 66:
            matches[(is1, is2)] = match
            print(f"Scanners {is1} and {is2} have {len(match)} matching pairs")

    return matches


def transform(v, offset, m):
    vt = m * v + offset
    return vt


def calc_scanner_transf(is1, is2, match_):
    # print(f'Trying to calculate transformation from {is2} to {is1}')
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

        # print(f" Got {cnt} matches")
        if cnt >= 12:
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

        # print(f" Got {cnt} matches")
        if cnt >= 12:
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
    if data is None:
        data = beacons[from_s]
    res = data.copy()

    path = g.get_shortest_paths(from_s, to_s)[0]
    for fs, ts in pairwise(path):
        tf = scanner_transforms[(fs, ts)]
        for i in range(len(data)):
            res[i] = transform(res[i], tf['off'], tf['rot'])

    return res


def flatten(x):
    return x.transpose().tolist()[0]


def main_a():
    global matched_beacons, g
    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)
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

    g = igraph.Graph(n=len(beacons), edges=scanner_transforms.keys(), directed=True)

    # transformed_beacons = beacons[0]
    # tf = scanner_transforms[(1, 0)]
    # for b0 in beacons[1]:
    #     bt = transform(b0, tf['off'], tf['rot'])
    #     for b1 in beacons[0]:
    #         if np.array_equal(bt, b1):
    #             bt = bt.transpose().tolist()[0]
    #             print("{0},{1},{2}".format(*bt))

    # s1 = flatten(transform_scanner(1, 0, [np.array([0, 0, 0], ndmin=2).transpose()])[0])
    # print(f'{s1=}')

    # tf4_1 = scanner_transforms[(4, 1)]
    # tf1_0 = scanner_transforms[(1, 0)]
    # for b0 in beacons[4]:
    #     bt = transform(b0, tf4_1['off'], tf4_1['rot'])
    #     for b1 in beacons[1]:
    #         if np.array_equal(bt, b1):
    #             btt = transform(bt, tf1_0['off'], tf1_0['rot'])
    #             btt = btt.transpose().tolist()[0]
    #             print("{0},{1},{2}".format(*btt))

    # s4 = flatten(transform_scanner(4, 0, [np.array([0, 0, 0], ndmin=2).transpose()])[0])
    # print(f'{s4=}')

    # s2 = flatten(transform_scanner(2, 0, [np.array([0, 0, 0], ndmin=2).transpose()])[0])
    # print(f'{s2=}')

    # s3 = flatten(transform_scanner(3, 0, [np.array([0, 0, 0], ndmin=2).transpose()])[0])
    # print(f'{s3=}')

    matched_beacons = beacons[0].copy()
    for i in range(1, len(beacons)):
        res = transform_scanner(i, 0, beacons[i])
        matched_beacons.extend(res)

    print(f"Got {len(matched_beacons)} beacons before filtering")
    filter_beacons()

    for b in matched_beacons:
        print("{0},{1},{2}".format(*flatten(b)))


def mdist(a, b):
    return np.sum(np.abs(a - b))


def main_b():
    global matched_beacons, g

    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)
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

    g = igraph.Graph(n=len(beacons), edges=scanner_transforms.keys(), directed=True)

    scanners0 = [np.matrix([0, 0, 0])]
    for i in range(1, len(beacons)):
        scanners0.append(transform_scanner(i, 0, [np.array([0, 0, 0], ndmin=2).transpose()])[0].transpose())

    # print(scanners0)
    print(max(mdist(i, j) for i, j in pairwise(scanners0)))

    for i, j in pairwise(scanners0):
        print(i, j, mdist(i, j))



if __name__ == '__main__':
    init()
    matrices = generate_matrices()
    writebar(puzzle.day, 'b')
    main_a()
    # main_b()
