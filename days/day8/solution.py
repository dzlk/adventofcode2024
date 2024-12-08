import re
from collections import Counter, defaultdict
from functools import reduce

import click

from utils.io import readfile


@click.command()
@click.argument('pzl', type=click.Path())
def run_day(pzl):
    input = readfile(pzl)
    print("Result part one: " + str(solve_part_one(input)) + "\n")
    print("Result part two: " + str(solve_part_two(input)) + "\n")


def solve_part_one(input: list[str]) -> int:
    board = parse_input(input)

    width = len(board[0])
    height = len(board)

    nodes = defaultdict(list)
    antinodes = set()

    def check_xy(y: int, x: int):
        return 0 <= x < width and 0 <= y < height

    for y, line in enumerate(board):
        for x, node in enumerate(line):
            if node != '.':
                nodes[node].append((y, x))

    print(nodes)

    def find_antinodes(node, point, diff, dir):
        dy, dx = diff
        fy, fx = point

        # part2
        antinodes.add(point)

        while True:
            y, x = fy + dir[0]*dy, fx + dir[1]*dx
            print(y, x)

            if not check_xy(y, x):
                return

            t = board[y][x]
            if t != node:
                antinodes.add((y, x))
                # part2
                # return

            fy, fx = y, x

    for node, points in nodes.items():
        for i, a in enumerate(points):
            for j, b in enumerate(points[i + 1:]):
                dy, dx = a[0] - b[0], a[1] - b[1]

                print(a, b, dy, dx)

                find_antinodes(node, a, (dy, dx), (1, 1))
                find_antinodes(node, b, (dy, dx), (-1, -1))

    print_board(board, antinodes)

    return len(antinodes)


def solve_part_two(input: list[str]):
    return 0


def parse_input(input: list[str]):
    board = list()

    for line in input:
        board.append(list(line))

    return board


def print_board(b, an: set):
    for y, line in enumerate(b):
        for x, node in enumerate(line):
            node = node if ((y, x) not in an) or node != '.' else '#'
            print(node, end='')
        print('')
