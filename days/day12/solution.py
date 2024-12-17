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
    board = parse_input(input)

    point_to_region = dict()
    region_to_point = defaultdict(set)

    price_by_perimetr = 0
    price_by_edges = 0

    r_id = 0
    visited = set()
    for y, line in enumerate(board):
        for x, v in enumerate(line):
            if v == '_':
                continue

            if (y, x) in visited:
                continue

            visited.add((y, x))

            points = find_region(board, (y, x), v)
            visited = visited.union(points)

            region_to_point[r_id] = points
            for p in points:
                point_to_region[p] = r_id

            area = len(points)
            print(f"region = {r_id}, value = {v}, area = {area}, ")

            perimetr = calc_perimetr(points)
            price = perimetr * area
            print(f"perimetr = {perimetr}, price = {price}")
            price_by_perimetr += price

            edges = calc_edges(points)
            price = edges * area
            print(f"edges = {edges}, price = {price}")
            price_by_edges += price

            # print_board(board, point_to_region, points)
            r_id += 1
            # return price


    return (price_by_perimetr, price_by_edges)


def solve_part_two(input: list[str]):
    return 0

def calc_perimetr(points):
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    borders = set()
    for ty, tx in points:
        for (dy, dx) in dirs:
            b = ty + dy / 2, tx + dx / 2
            if b in borders:
                borders.remove(b)
            else:
                borders.add(b)

    # print(f"borders={borders}")

    return len(borders)

def calc_edges(points):
    by_y = defaultdict(dict)
    by_x = defaultdict(dict)
    for ty, tx in points:
        by_y[ty][tx] = 1
        by_x[tx][ty] = 1

    def count_edge(by_y, by_x):
        y_min = min(by_y.keys())
        y_max = max(by_y.keys())

        x_max = max(by_x.keys())

        edge = 0
        line = [0 for _ in range(0, x_max + 1)]
        print(f"line={line}")
        for y in range(y_min, y_max + 2):
            curr = by_y[y] if y in by_y else dict()
            diff = list()
            for i, x in enumerate(line):
                if x == 0 and i in curr:
                    line[i] = 1
                    diff.append(i)
                    continue

                if x == 1 and i not in curr:
                    line[i] = 0
                    diff.append(-i)

            # print(line, diff)

            p = None
            for x in diff:
                if p is None:
                    edge += 1
                else:
                    if p * x < 0:
                        edge += 1
                    elif abs(x) - abs(p) > 1:
                        edge += 1

                # if p is None or x - p > 1:
                #     edge += 1
                p = x

            print(f"m={y} edge={edge}")

        return edge

    edges = count_edge(by_y, by_x)
    print(f"edge_y={edges}")

    edges += count_edge(by_x, by_y)
    print(f"edge_x={edges}")

    return edges

def find_region(board, point, target):
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]


    queue = deque([point])
    points = {point}
    while len(queue):
        (ty, tx) = queue.pop()

        for dy, dx in dirs:
            y, x = ty + dy, tx + dx

            if (y, x) in points:
                continue

            if 0 <= y < len(board) and 0 <= x < len(board[0]):
                if board[y][x] == target:
                    points.add((y, x))
                    queue.append((y, x))

    return points


def print_board(b, rm, ps):
    text = Text()
    for y, line in enumerate(b):
        for x, v in enumerate(line):
            color = ""
            if (y, x) in rm:
                color = "blue"
            if (y, x) in ps:
                color = "yellow"

            text.append(v, style=color)
        text.append(text.end)

    console = Console()
    console.print(text)

def parse_input(input: list[str]):
    board = list()

    for line in input:
        board.append(list(line))

    return board
