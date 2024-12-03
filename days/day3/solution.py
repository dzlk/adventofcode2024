import re
from collections import Counter
from functools import reduce
from typing import List

import click

from utils.io import readfile


@click.command()
@click.argument('pzl', type=click.Path())
def run_day3(pzl):
    input = readfile(pzl)
    print("Result part one: " + str(solve_part_one(input)) + "\n")
    print("Result part two: " + str(solve_part_two(input)) + "\n")


def solve_part_one(input: list[str]) -> int:
    return reduce(lambda res, expr: res + execute_expr(expr), input, 0)


def execute_expr(expr: str) -> int:
    matches = re.findall(r'mul\((\d+),(\d+)\)', expr)
    print(expr)
    print(matches, len(matches))

    result = 0
    for x, y in matches:
        result += int(x) * int(y)

    return result


def solve_part_two(input: list[str]):
    expr = reduce(lambda res, line: res + line, input)
    return execute_expr_extra(expr)


def execute_expr_extra(expr: str) -> int:
    parts = expr.split("don't()")

    result = execute_expr(parts[0])
    for part in parts[1:]:
        result = reduce(lambda res, expr: res + execute_expr(expr),
                        part.split('do()')[1:],
                        result)
    return result
