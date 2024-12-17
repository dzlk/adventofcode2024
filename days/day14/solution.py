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


@dataclass
class Size:
    width: int
    height: int


SIZE = Size(width=101, height=103)


@click.command()
@click.option('--part',
              default='both',
              type=click.Choice(['one', 'two', 'both'], case_sensitive=False))
@click.argument('pzl', type=click.Path())
def run_day(part, pzl):
    input = readfile(pzl)

    print(part, pzl)

    if pzl.find('test') > -1:
        SIZE.width = 11
        SIZE.height = 7

    if part in ('one', 'both'):
        print("Result part one: " + str(solve_part_one(input)) + "\n")

    if part in ('two', 'both'):
        print("Result part two: " + str(solve_part_two(input)) + "\n")


def solve_part_one(input: list[str]) -> int:
    robots = parse_input(input)
    # print_positions(robots)

    for n in range(100):
        print(f"Blink n={n + 1}")
        for r in robots:
            r.move()

        print_positions(robots)

    q1, q2, q3, q4 = 0, 0, 0, 0

    wh = SIZE.width // 2
    hh = SIZE.height // 2

    pos = Counter([r.p for r in robots])
    for (x, y), v in pos.items():
        # print(x, y, v)
        if x == wh or y == hh:
            continue

        if x < wh:
            if y < hh:
                q1 += v
            else:
                q2 += v
        else:
            if y < hh:
                q3 += v
            else:
                q4 += v

    print("q=", q1, q2, q3, q4)

    return q1 * q2 * q3 * q4


def solve_part_two(input: list[str]):
    robots = parse_input(input)

    blink_start = 7500

    for n in range(blink_start):
        print(f"Blink n={n + 1}")
        for r in robots:
            r.move()

    def create_screen(screen):
        blink_no = blink_start
        pause = False

        while blink_no < 7521:
            if not pause:
                blink_no += 1
                screen.print_at(f"Blink n={blink_no}", 0, 0, colour=7)

                if blink_no == 7520:
                    pause = True

                for r in robots:
                    r.move()

                pos = Counter([r.p for r in robots])
                for y in range(SIZE.height):
                    for x in range(SIZE.width):
                        value = "."
                        color = 0

                        if (x, y) in pos:
                            value = '#'
                            color = 2

                        if y < 70:
                            screen.print_at(y, 0, y + 3, colour=1)
                            screen.print_at(value, x + 4, y + 3, colour=color)
                        else:
                            d = SIZE.width + 10
                            screen.print_at(y, d, y % 70 + 3, colour=1)
                            screen.print_at(value, d + x + 4, y % 70 + 3, colour=color)
                screen.refresh()
                # sleep(1)

            ev = screen.get_key()
            if ev in (ord('Q'), ord('q')):
                return

            if ev in (ord('P'), ord('p')):
                pause = not pause

    Screen.wrapper(create_screen)
    # create_screen(FakeScreen())

    return n


@dataclass
class Robot:
    p: (int, int)
    v: (int, int)

    def move(self):
        x, y = self.p
        dx, dy = self.v

        x = (x + dx)
        x = SIZE.width + x if x < 0 else x % SIZE.width

        y = (y + dy)
        # print(f"y={y}, dy={dy}")
        y = SIZE.height + y if y < 0 else y % SIZE.height

        self.p = (x, y)


def print_positions(robots: list[Robot], show_count=True):
    pos = Counter([r.p for r in robots])
    text = Text()
    for y in range(SIZE.height):
        for x in range(SIZE.width):
            value = "."
            color = ""

            if (x, y) in pos:
                value = str(pos[(x, y)]) if show_count else '#'
                color = "blue"

            text.append(value, style=color)
        text.append(text.end)

    console = Console()
    console.print(text)


def parse_input(input: list[str]) -> list[Robot]:
    robots = list()

    for line in input:
        matches = re.findall(r'p=([-\d]+),([-\d]+) v=([-\d]+),([-\d]+)', line)
        print(f"line='{line}', matches={matches}")
        x, y, dx, dy = matches[0]

        robots.append(Robot(
            p=(int(x), int(y)),
            v=(int(dx), int(dy))
        ))

    return robots
