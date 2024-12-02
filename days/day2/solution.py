from collections import Counter
from typing import List

import click

from utils.io import readfile


@click.command()
@click.argument('pzl', type=click.Path())
def run_day2(pzl):
    input = readfile(pzl)
    print("Result part one: " + str(solve_part_one(input)) + "\n")
    print("Result part two: " + str(solve_part_two(input)) + "\n")


def get_sign(num: int) -> int:
    return 1 if num > 0 else -1


def check_report(levels, tolerance=False) -> bool:
    prev = None
    sign = None

    for index, curr in enumerate(levels):
        if index == 0:
            prev = curr
            continue

        diff = prev - curr
        diff_sign = get_sign(diff)

        diff_violate = diff == 0 or abs(diff) > 3
        sign_violate = sign is not None and sign != diff_sign

        if diff_violate or sign_violate:
            if tolerance:
                if index == 1:
                    prev_drop = levels[index:]
                    curr_drop = levels[0:index] + levels[index + 1:]
                    return check_report(prev_drop) or check_report(curr_drop)
                if index == 2:
                    first_drop = levels[1:]
                    prev_drop = levels[0:index - 1] + levels[index:]
                    curr_drop = levels[0:index] + levels[index + 1:]
                    return (check_report(first_drop) or
                            check_report(prev_drop) or check_report(curr_drop))
                else:
                    tolerance = False
                    continue

            return False

        if sign is None:
            sign = diff_sign

        prev = curr

    return True


def solve_part_one(input: list[str]) -> int:
    result = 0

    for r in input:
        levels = [int(l) for l in r.split()]
        result += 1 if check_report(levels) else 0

    return result


def solve_part_two(input: list[str]):
    result = 0

    for r in input:
        levels = [int(l) for l in r.split()]
        if check_report(levels):
            result += 1
        elif check_report(levels, True):
            print(levels)
            result += 1

    return result
