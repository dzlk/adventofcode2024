import queue
import re
from collections import Counter, defaultdict, deque
from functools import reduce

from rich import print
from rich.console import Console
from rich.text import Text

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


def solve_part_one(input: list[str]) -> (int, int):
    a_cost = 3
    b_cost = 1

    total = 0

    for i in range(0, len(input), 4):
        ax, ay = parse_cmd(input[i])
        bx, by = parse_cmd(input[i+1])
        x, y = parse_cmd(input[i+2])

        x += 10000000000000
        y += 10000000000000

        b = (y * ax - x * ay) / (by * ax - bx * ay)
        a = (x - b * bx) / ax

        if int(a) != a or int(b) != b:
            print("LOSE\n")
            continue

        cost = a*a_cost + b*b_cost
        print(f"WIN: a={a}, b={b}, cost={cost}\n\n", a, b)



        total += cost


    return total


def solve_part_two(input: list[str]):
    return 0

def parse_cmd(cmd):
    # Button A: X+94, Y+34
    matches = re.findall(r'\w+: X.(\d+), Y.(\d+)', cmd)
    print(cmd, matches)

    x, y = matches.pop()
    return int(x), int(y)
