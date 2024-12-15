import itertools
import queue
import re
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from functools import reduce

from time import sleep

from rich import print
from rich.console import Console
from rich.text import Text

from PIL.ImageChops import screen
from asciimatics.screen import Screen

import click

from utils.io import readfile


@click.command()
@click.option('--part',
              default='both',
              type=click.Choice(['one', 'two', 'both'], case_sensitive=False))
@click.option('--no_wide', is_flag=True)
@click.argument('pzl', type=click.Path())
def run_day(part, no_wide, pzl):
    input = readfile(pzl)

    if part in ('one', 'both'):
        print("Result part one: " + str(solve_part_one(input)) + "\n")

    if part in ('two', 'both'):
        print("Result part two: " + str(solve_part_two(input, no_wide)) + "\n")


def dir_by_cmd(cmd):
    return {
        '^': (-1, 0),
        '>': (0, 1),
        '<': (0, -1),
        'v': (1, 0),
    }[cmd]


def solve_part_one(input: list[str]) -> int:
    board, cmds = parse_input(input)
    r = find_robot(board)

    debug = False

    print_board(board, f"Initial state, robot={r}")
    for cmd in itertools.chain.from_iterable(cmds):
        dy, dx = dir_by_cmd(cmd)
        ry, rx = r

        y, x = ry + dy, rx + dx

        if board[y][x] == '#':
            debug and print_board(board, f"Cmd={cmd}, dir={(dy, dx)}, robot={r}")
            continue

        if board[y][x] == '.':
            board[ry][rx] = '.'
            board[y][x] = '@'
            r = (y, x)
            debug and print_board(board, f"Cmd={cmd}, dir={(dy, dx)}, robot={r}")
            continue

        # find space
        sy, sx = y, x
        while board[sy][sx] != '#' and board[sy][sx] != '.':
            sy, sx = sy + dy, sx + dx

        if board[sy][sx] == '#':
            continue

        prev = '@'
        board[ry][rx] = '.'
        cy, cx = ry, rx
        while cy != sy or cx != sx:
            cy, cx = cy + dy, cx + dx
            tmp = board[cy][cx]
            board[cy][cx] = prev
            prev = tmp

        r = (y, x)

        debug and print_board(board, f"Cmd={cmd}, dir={(dy, dx)}, robot={r}")

    not debug and print_board(board, f"Final state, robot={r}")

    total = 0
    for y, line in enumerate(board):
        for x, v in enumerate(line):
            if v == 'O':
                total += 100 * y + x

    return total


def solve_part_two(input: list[str], no_wide=False):
    board, cmds = parse_input(input)
    if not no_wide:
        board = wide_board(board)
    r = find_robot(board)

    debug = False

    print_board(board, f"Initial state, robot={r}")
    for cmd in itertools.chain.from_iterable(cmds):
        debug and print(f"Cmd={cmd}")

        dy, dx = dir_by_cmd(cmd)
        ry, rx = r

        y, x = ry + dy, rx + dx
        if board[y][x] == '#':
            # debug and print_board(board, f"Cmd={cmd}, dir={(dy, dx)}, robot={r}")
            continue

        if board[y][x] == '.':
            board[ry][rx] = '.'
            board[y][x] = '@'
            r = (y, x)
            # debug and print_board(board, f"Cmd={cmd}, dir={(dy, dx)}, robot={r}")
            continue

        debug and print_board(board, f"State before")

        if cmd in ['<', '>']:
            # find space
            sy, sx = y, x
            while board[sy][sx] != '#' and board[sy][sx] != '.':
                sy, sx = sy + dy, sx + dx

            if board[sy][sx] == '#':
                continue

            prev = '@'
            board[ry][rx] = '.'
            cy, cx = ry, rx
            while cy != sy or cx != sx:
                cy, cx = cy + dy, cx + dx
                tmp = board[cy][cx]
                board[cy][cx] = prev
                prev = tmp

            r = (y, x)
            debug and print_board(board, f"Cmd={cmd}, dir={(dy, dx)}, robot={r}")
            continue

        can_move = try_move_boxes(board, (y, x), (dy, dx))
        if can_move:
            board[ry][rx] = '.'
            board[y][x] = '@'
            r = (y, x)

        debug and print_board(board, f"Cmd={cmd}, dir={(dy, dx)}, robot={r}, moved={can_move}")

    not debug and print_board(board, f"Final state, robot={r}")

    total = 0
    for y, line in enumerate(board):
        for x, v in enumerate(line):
            if v == '[':
                total += 100 * y + x

    return total


def try_move_boxes(board, point, dir) -> bool:
    def get_box(y, x):
        if board[y][x] == '[':
            return {(y, x), (y, x + 1)}
        else:
            return {(y, x), (y, x - 1)}

    y, x = point
    dy, dx = dir

    stack = deque()
    stack.append(get_box(y, x))
    while True:
        boxes = stack.pop()

        new_boxes = set()
        for by, bx in boxes:
            y, x = by + dy, bx + dx
            if board[y][x] == '#':
                return False

            if board[y][x] != '.':
                new_boxes.update(get_box(y, x))

        stack.append(boxes)
        if len(new_boxes) > 0:
            stack.append(new_boxes)
        else:
            break

    while len(stack) > 0:
        boxes = stack.pop()

        for (by, bx) in boxes:
            ny, nx = by + dy, bx + dx

            board[ny][nx] = board[by][bx]
            board[by][bx] = '.'

    return True


def print_board(b, header=None):
    text = Text()
    if header:
        text.append(header + text.end, style="green")

    for y, line in enumerate(b):
        for x, v in enumerate(line):
            color = "white"
            if v == '@':
                color = "yellow"
            if v == 'O':
                color = "blue"

            text.append(v, style=color)
        text.append(text.end)

    console = Console()
    console.print(text)


def find_robot(board):
    for y, line in enumerate(board):
        for x, v in enumerate(line):
            if v == '@':
                return y, x


def wide_board(board):
    new_board = list()

    for y, line in enumerate(board):
        new_line = list()
        for x, v in enumerate(line):
            if v == 'O':
                new_line += ['[', ']']
            elif v == '#':
                new_line += ['#', '#']
            elif v == '@':
                new_line += ['@', '.']
            else:
                new_line += ['.', '.']
        new_board.append(new_line)

    return new_board


def parse_input(input: list[str]) -> (list[list], list[list]):
    board = list()
    cmds = list()

    find_cmds = False
    for line in input:
        if line.strip() == '':
            find_cmds = True
            continue

        if not find_cmds:
            board.append(list(line))
        else:
            cmds.append(list(line))

    return board, cmds
