import re
from collections import Counter, defaultdict
from functools import reduce

import click

from utils.io import readfile


@click.command()
@click.option('--part',
              default='both',
              type=click.Choice(['one', 'two', 'both'], case_sensitive=False))
@click.argument('pzl', type=click.Path())
def run_day(part, pzl):
    input = readfile(pzl)

    print(part, pzl)

    if part in ('one', 'both'):
        print("Result part one: " + str(solve_part_one(input)) + "\n")

    if part in ('two', 'both'):
        print("Result part two: " + str(solve_part_two(input)) + "\n")


def solve_part_one(input: list[str]) -> int:
    bfs = input[0]
    print(bfs)
    print("0099811188827773336446555566")

    # r = 0
    # for i, x in enumerate("0099811188827773336446555566"):
    #     r += i * int(x)
    # print(r)

    return hashsum(bfs)


def hashsum(bfs):
    l_idx = 0
    lid = 0

    r_idx = len(bfs) + 1
    rid = (len(bfs) - 1) // 2 + 1
    rest = 0

    result = 0
    index = 0
    for i, x in enumerate(bfs):

        x = int(x)
        if i % 2 == 0:
            l_idx = i
            if l_idx == r_idx:
                break
            # index * id + (index + 1) * id + (index + 2) * id
            # index * id + index * id + id + index * id + 2 * id
            # k * id * (index + 1)

            while x > 0:
                print("l: ", (index, lid), lid * index)
                result += lid * index
                index += 1
                x -= 1

            lid += 1
            continue

        while x > 0:
            if rest:
                result += rid * index
                print("r: ", (index, rid), rid * index)

                rest -= 1
                x -= 1
                index += 1

                continue

            r_idx -= 2
            rid -= 1
            if l_idx == r_idx:
                break

            rest = int(bfs[r_idx])
            print("rest = ", rest)

    while rest > 0:
        result += rid * index
        print("r: ", (index, rid), rid * index)

        rest -= 1
        index += 1

    return result


def solve_part_two(input: list[str]):
    bfs = input[0]

    digits = list()
    spaces = list()

    result = list()

    id = 0
    index = 0
    for i, count in enumerate(bfs):
        count = int(count)
        if i % 2 == 0:
            digits.append((index, count, id))
            for _ in range(count):
                result.append(id)
                index += 1
            id += 1
        else:
            spaces.append((index, count))
            for _ in range(count):
                result.append(None)
                index += 1

    print(result)
    print(digits)
    print(spaces)
    print("-------")

    for (index, count, id) in reversed(digits):
        print((index, count, id))
        for i, (space_index, space_count) in enumerate(spaces):
            if index < space_index:
                break

            if count <= space_count:
                for n in range(count):
                    result[space_index] = id
                    space_index += 1
                    space_count -= 1

                    result[index] = None
                    index += 1

                spaces[i] = (space_index, space_count)
                break

    hs = 0
    for i, x in enumerate(result):
        if x is not None:
            hs += i * x

    print(result)
    print(digits)
    print(spaces)


    return hs
