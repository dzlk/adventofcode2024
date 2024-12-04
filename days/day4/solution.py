import re
from collections import Counter
from dataclasses import dataclass
from functools import reduce
from itertools import count
from time import sleep
from typing import List, Tuple

import click
from random import randint

from PIL.ImageChops import screen
from asciimatics.screen import Screen

from utils.io import readfile


@click.command()
@click.argument('pzl', type=click.Path())
def run_day4(pzl):
    input = readfile(pzl)
    print("Result part one: " + str(solve_part_one(input)) + "\n")
    print("Result part two: " + str(solve_part_two(input)) + "\n")


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class Board:
    words: List[List[str]]
    width: int
    height: int

    def check_point(self, point):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def word(self, x, y) -> str:
        return self.words[y][x]

    def word_p(self, p: Point) -> str:
        return self.word(p.x, p.y) if self.check_point(p) else ''

    def iterate(self):
        for y in range(self.height):
            for x in range(self.width):
                yield x, y


def create_data_from_input(input: List[str]) -> Board:
    board = Board(words=[], width=0, height=0)

    for line in input:
        board.words.append(list(line))

    board.width = len(board.words[0])
    board.height = len(board.words)
    return board


@dataclass
class State:
    board: Board
    xy: set[Point]

    count: int

    def found(self):
        self.count += 1


def solve_part_one(input: list[str]) -> int:
    state = State(
        board=create_data_from_input(input),
        xy=set(),
        count=0,
    )

    directions = [
        (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)
    ]

    def check_xmas(p: Point, sign_x, sign_y) -> bool:
        board = state.board

        p1 = Point(p.x + 1 * sign_x, p.y + 1 * sign_y)
        p2 = Point(p.x + 2 * sign_x, p.y + 2 * sign_y)
        p3 = Point(p.x + 3 * sign_x, p.y + 3 * sign_y)

        if (board.word_p(p1) == 'M' and
                board.word_p(p2) == 'A' and
                board.word_p(p3) == 'S'):
            state.xy.update([p, p1, p2, p3])

            return True
        return False

    def create_screen(screen):
        for x, y in state.board.iterate():
            p = Point(x, y)

            if state.board.word_p(p) == 'X':
                for d in directions:
                    if check_xmas(p, d[0], d[1]):
                        state.found()

            # print_data(screen, state, p)

            ev = screen.get_key()
            if ev in (ord('Q'), ord('q')):
                return

        # sleep(1000)

    Screen.wrapper(create_screen)

    return state.count


def solve_part_two(input: list[str]):
    state = State(
        board=create_data_from_input(input),
        xy=set(),
        count=0,
    )

    def check_xmas(p: Point) -> bool:
        board = state.board

        p1 = Point(p.x - 1, p.y - 1)
        p2 = Point(p.x + 1, p.y + 1)
        w12 = board.word_p(p1) + board.word_p(p2)

        p3 = Point(p.x + 1, p.y - 1)
        p4 = Point(p.x - 1, p.y + 1)
        w34 = board.word_p(p3) + board.word_p(p4)

        if (w12 == 'MS' or w12 == 'SM') and (w34 == 'MS' or w34 == 'SM'):
            state.xy.update([p, p1, p2, p3, p4])
            return True

        return False

    def create_screen(screen):
        for x, y in state.board.iterate():
            p = Point(x, y)

            if state.board.word_p(p) == 'A':
                if check_xmas(p):
                    state.found()

            # print_data(screen, state, p)

            ev = screen.get_key()
            if ev in (ord('Q'), ord('q')):
                return

        # sleep(1000)

    Screen.wrapper(create_screen)

    return state.count


def print_data(screen, state, pos: Point):
    for x, y in state.board.iterate():
        point = Point(x, y)
        color = 7
        if point == pos:
            color = 6
        elif point in state.xy:
            color = 4

        screen.print_at(state.board.word(x, y), x, y + 2, colour=color)

        # if x == 0:
        #     screen.refresh()
        # screen.refresh()

    screen.print_at(f"Count: {state.count}", 0, 0, colour=7)
    screen.refresh()
