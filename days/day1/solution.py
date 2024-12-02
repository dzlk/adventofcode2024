from collections import Counter
from typing import List

import click

from utils.io import readfile


@click.command()
@click.argument('pzl', type=click.Path())
def run_day1(pzl):
    input = readfile(pzl)
    print("Result part one: " + str(solve_part_one(input)) + "\n")
    print("Result part two: " + str(solve_part_two(input)) + "\n")


def solve_part_one(input: list[str]):
    left: list[int] = []
    right: list[int] = []
    for ps in input:
        l, r = [int(x) for x in ps.split()]

        left.append(l)
        right.append(r)

    left.sort()
    right.sort()

    result = 0
    for i in range(len(left)):
        result += abs(left[i] - right[i])

    return result


def solve_part_two(input: list[str]):
    left: list[int] = []
    right: Counter[int] = Counter()

    for ps in input:
        l, r = [int(x) for x in ps.split()]

        left.append(l)
        right[r] += 1

    result = 0
    for x in left:
        result += x * right[x]

    return result

