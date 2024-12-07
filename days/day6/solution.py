import re
from collections import Counter, defaultdict
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
def run_day6(pzl):
    input = readfile(pzl)
    print("Result part one: " + str(solve_part_one(input)) + "\n")
    print("Result part two: " + str(solve_part_two(input)) + "\n")


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class FakeScreen:
    @staticmethod
    def print_at(value, x, y, colour):
        return

    @staticmethod
    def refresh():
        return

    @staticmethod
    def get_key():
        return

@dataclass
class Board:
    values: list[list[str]]
    width: int
    height: int

    guard_pos: Point
    guard_visited: set[Point]
    guard_path: set[tuple[Point, str]]

    loops: set[Point]

    def check_point(self, point):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def update_value(self, point, value: str):
        self.values[point.y][point.x] = value

    def value(self, p: Point) -> str:
        return self.values[p.y][p.x] if self.check_point(p) else ''

    def guard_move(self) -> bool:
        guard_value = self.value(self.guard_pos)

        offset = self.get_guard_offset()

        next_point = Point(self.guard_pos.x + offset.x, self.guard_pos.y + offset.y)
        next_value = self.value(next_point)

        if next_value == '#':
            return False

        # move guard
        self.guard_set_position(next_point, guard_value)

        return True

    def guard_set_position(self, next_point: Point, guard_value: str):
        self.update_value(self.guard_pos, '.')

        self.guard_pos = next_point
        self.update_value(next_point, guard_value)

        self.guard_visited.add(next_point)
        self.guard_path.add((next_point, guard_value))

    def guard_on_edge(self) -> bool:
        return self.point_on_edge(self.guard_pos)

    def point_on_edge(self, pos: Point) -> bool:
        return pos.x == 0 or pos.y == 0 or pos.x == self.width - 1 or pos.y == self.height - 1

    def get_guard_rotate_value(self) -> str:
        guard_value = self.value(self.guard_pos)

        return {
            '>': 'v',
            'v': '<',
            '<': '^',
            '^': '>'
        }[guard_value]

    @staticmethod
    def get_rotate_value(direction) -> str:
        return {
            '>': 'v',
            'v': '<',
            '<': '^',
            '^': '>'
        }[direction]

    def get_guard_offset(self):
        guard_value = self.value(self.guard_pos)
        return self.get_offset(guard_value)

    @staticmethod
    def get_offset(direction):
        return {
            '>': Point(1, 0),
            '<': Point(-1, 0),
            '^': Point(0, -1),
            'v': Point(0, 1)
        }[direction]

    def guard_rotate(self):
        next_direction = self.get_guard_rotate_value()
        self.update_value(self.guard_pos, next_direction)

        self.guard_path.add((self.guard_pos, next_direction))

    def check_loop(self, screen):
        pos = self.guard_pos

        offset = self.get_guard_offset()
        loop_point = Point(pos.x + offset.x, pos.y + offset.y)

        visited: set[tuple[Point, str]] = set()

        rotated = self.get_guard_rotate_value()
        visited.add((pos, rotated))

        while True:
            if self.point_on_edge(pos):
                return

            if (pos, rotated) in self.guard_path:
                self.loops.add(loop_point)
                return

            offset = self.get_offset(rotated)
            next_pos = Point(pos.x + offset.x, pos.y + offset.y)

            if self.value(next_pos) == '#':
                rotated = self.get_rotate_value(rotated)
            else:
                pos = next_pos

                if (pos, rotated) in visited:
                    return
                else:
                    visited.add((pos, rotated))

            screen.print_at(self.value(pos), pos.x, pos.y + 3, colour=2)
            screen.print_at(self.value(next_pos), next_pos.x, next_pos.y + 3, colour=4)
            screen.refresh()
            # sleep(1 / 100)
            # print(x, rotated, pos)

    def iterate(self):
        for y in range(self.height):
            for x in range(self.width):
                yield Point(x, y)


def create_board_from_input(input: List[str]) -> Board:
    board = Board(values=[], width=0, height=0,
                  guard_pos=Point(0, 0), guard_visited=set(),
                  guard_path=set(), loops=set())

    for y, line in enumerate(input):
        board.values.append(list(line))

        x = line.find("^")  # in my input
        if x > -1:
            board.guard_set_position(Point(x, y), "^")

    board.width = len(board.values[0])
    board.height = len(board.values)
    return board


@dataclass
class State:
    board: Board


def solve_part_one(input: list[str]) -> (int, int):
    board = create_board_from_input(input)

    def create_screen(screen):
        moving = True
        pause = False
        while moving:
            if not pause:
                if board.guard_move():
                    moving = not board.guard_on_edge()

                    if moving:
                        board.check_loop(screen)
                    else:
                        pause = True
                else:
                    board.guard_rotate()

            print_data(screen, board)
            # sleep(1)

            ev = screen.get_key()
            if ev in (ord('Q'), ord('q')):
                return

            if ev in (ord('P'), ord('p')):
                pause = not pause

    # Screen.wrapper(create_screen)
    create_screen(FakeScreen())

    return len(board.guard_visited), len(board.loops)


def solve_part_two(input: list[str]):
    pass

def print_data(screen, board):
    if screen.__class__.__name__ == 'FakeScreen':
        return

    for point in board.iterate():
        value = board.value(point)
        color = 7
        if value == '#':
            color = 6

        if point == board.guard_pos:
            color = 1
        elif value == 'o':
            color = 5
        elif point in board.guard_visited:
            value = '∘'
            color = 0

        screen.print_at(value, point.x, point.y + 3, colour=color)

        # if point.x == 0:
        #     screen.refresh()
        # screen.refresh()

    screen.print_at(f"Count: {len(board.guard_visited)}", 0, 1, colour=7)
    screen.print_at(f"Loops: {len(board.loops)}", 0, 2, colour=7)
    screen.refresh()
