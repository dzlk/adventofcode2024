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
    board = parse_input(input)
    print_board(board)

    zeros = find_zeros(board)

    result = 0

    for zero in zeros:
        targets = find_ways(board, zero)
        score = len(targets)
        print(f"zero {zero}: score={score}")
        result += score


    return result



def solve_part_two(input: list[str]):
    return 0

def find_ways(board, zero):
    targets = list()
    # part 1
    # targets = set()
    stack = [(zero, 0)]
    visited = {zero}
    while len(stack):
        curr, value = stack.pop()
        target = value + 1

        points = find_around(board, curr, value + 1)

        for p in points:
            # part 1
            # if p in visited:
            #     continue

            if target == 9:
                targets.append(p)
                # part 1
                # targets.add(p)
            else:
                stack.append((p, target))
        # part 1
        # visited = targets.union(points)

    return targets

def find_around(board, point, target):
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    (ty, tx) = point
    points = list()
    for dy, dx in dirs:
        y, x = ty + dy, tx + dx

        if 0 <= y < len(board) and 0 <= x < len(board[0]):
            if board[y][x] == target:
                points.append((y, x))

    return points

def find_zeros(board):
    zeros = list()

    for y, _ in enumerate(board):
        for x, _ in enumerate(board[y]):
            if board[y][x] == 0:
                zeros.append((y, x))

    return zeros

def parse_input(input: list[str]):
    board = list()

    for line in input:
        board.append([int(x) for x in list(line)])

    return board


def print_board(b):
    for y, line in enumerate(b):
        for x, node in enumerate(line):
            print(node, end='')
        print('')