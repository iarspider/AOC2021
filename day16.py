import os
import pprint

from aocd.models import Puzzle
from aocd.transforms import lines, numbers

from colorama import init
from termcolor import colored

from aocbar import writebar

file__ = os.path.basename(__file__)
puzzle = Puzzle(year=2021, day=int(file__[3:5]))


def popN(line, N):
    if len(line) < N:
        raise RuntimeError(f"Not enough data to pop {N} bits: {line}")
    return line[:N], line[N:]


def sum_ver(packet):
    res = packet['version']
    if packet['type'] != 4:
        for subpacket in packet['packets']:
            res += sum_ver(subpacket)

    return res


def evaluate_0(packet):
    res = 0
    for subp in packet['packets']:
        res += evaluate(subp)

    return res


def evaluate_1(packet):
    res = 1
    for subp in packet['packets']:
        res *= evaluate(subp)

    return res


def evaluate_2(packet):
    res = []
    for subp in packet['packets']:
        res.append(evaluate(subp))

    return min(res)


def evaluate_3(packet):
    res = []
    for subp in packet['packets']:
        res.append(evaluate(subp))

    return max(res)


def evaluate_5(packet):
    if len(packet['packets']) != 2:
        raise RuntimeError(f"Invalid GT packet: len(packet['packets'])  != 2")

    res = [evaluate(packet['packets'][0]), evaluate(packet['packets'][1])]

    return 1 if res[0] > res[1] else 0


def evaluate_6(packet):
    if len(packet['packets']) != 2:
        raise RuntimeError(f"Invalid GT packet: len(packet['packets'])  != 2")

    res = [evaluate(packet['packets'][0]), evaluate(packet['packets'][1])]

    return 1 if res[0] < res[1] else 0


def evaluate_7(packet):
    if len(packet['packets']) != 2:
        raise RuntimeError(f"Invalid GT packet: len(packet['packets'])  != 2")

    res = [evaluate(packet['packets'][0]), evaluate(packet['packets'][1])]

    return 1 if res[0] == res[1] else 0


def evaluate_4(packet):
    return packet['value']


def evaluate(packet):
    func = globals().get('evaluate_' + str(packet['type']), None)
    if not func:
        raise RuntimeError(f"Unknow packet with type {packet['type']}")

    return func(packet)


def decode_packet(line, depth=0):
    res = {}
    ver, line = popN(line, 3)
    ver = int(ver, 2)
    res['version'] = ver
    typ, line = popN(line, 3)
    typ = int(typ, 2)
    res['type'] = typ
    # print(f"Packet version {res['version']} type {res['type']}")

    if typ == 4:
        flag = True
        buf = ""
        while (flag):
            data, line = popN(line, 5)
            flag = (data[0] == '1')
            buf += data[1:]

        val = int(buf, 2)
        res['value'] = val
        # print(f"Packet data: {val}")
        print(f"L{depth:02d} Literal packet: V {res['version']} T {res['type']} N {res['value']}")
        res = res
    else:
        len_mode, line = popN(line, 1)
        print(f"L{depth:02d} Operator packet V {res['version']} T {res['type']} I {len_mode}")
        if len_mode == '0':
            len_val, line = popN(line, 15)
            print(f"L{depth:02d} Subpackets are {len_val} (", end='')
            len_val = int(len_val, 2)
            print(f"{len_val}) bits long")
            data, line = popN(line, len_val)
            subpacket, data = decode_packet(data, depth + 1)
            print(f"L{depth:02d} Decoded subpacket, leftover bits: {data}.")
            res['packets'] = [subpacket]
            while data:
                subpacket, data = decode_packet(data, depth + 1)
                print(f"L{depth:02d} Decoded subpacket, leftover bits: {data}.")
                res['packets'].append(subpacket)
        else:
            len_val, line = popN(line, 11)
            len_val = int(len_val, 2)
            print(f"L{depth:02d} Decoding {len_val} subpackets")
            res['packets'] = []
            for i in range(len_val):
                p, line = decode_packet(line, depth + 1)
                print(f"L{depth:02d} Packet {i} has type {p['type']} and value {p.get('value', None)}")
                res['packets'].append(p)

    return res, line


def hex2bin(hexline):
    s = ''
    for c in hexline:
        binline = int(c, 16)
        binline = bin(binline)[2:]
        while len(binline) % 4 != 0:
            binline = '0' + binline

        s += binline

    return s


def main_a():
    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)
    # hexline = input[2]
    # binline = hex2bin(hexline)
    # # print(hexline)
    # # print(binline)
    # res, line = decode_packet(binline)
    # print("Done decoding, packet follows:")
    # pprint.pprint(res)
    # print()
    # print(f"Leftover bits (should be zeros): {line}")
    # print('=' * 80)

    for hexline in input:
        binline = hex2bin(hexline)
        # print(hexline)
        # print(binline)
        res, line = decode_packet(binline)
        print("Done decoding, packet follows:")
        pprint.pprint(res)
        print()
        print(f"Leftover bits (should be zeros): {line}")
        print('=' * 80)

        print('Sum is', sum_ver(res))


def main_b():
    # input = lines(puzzle.example_data)
    input = lines(puzzle.input_data)

    for hexline in input:
        binline = hex2bin(hexline)
        # print(hexline)
        # print(binline)
        res, line = decode_packet(binline)
        print("Done decoding, packet follows:")
        pprint.pprint(res)
        print()
        print(f"Leftover bits (should be zeros): {line}")
        print('=' * 80)

        print("Value is", evaluate(res))
        # print('Sum is', sum_ver(res))


if __name__ == '__main__':
    init()
    writebar(puzzle.day, 'b')
    # main_a()
    main_b()
