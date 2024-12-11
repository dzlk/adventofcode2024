import queue
import re
from collections import Counter, defaultdict, deque
from functools import reduce
from string import digits

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
    nums = Counter([n for n in input[0].strip().split()])
    print(nums)


    for time in range(0, 75):
        print("--"*10)
        print("time = ", time)
        print("--"*10)
        print(nums)
        uniq_nums = [n for n, v in nums.items() if v > 0]
        values = [nums[n] for n in uniq_nums]
        print(uniq_nums)
        for i, num in enumerate(uniq_nums):
            value = values[i]
            nums[num] -= value

            if int(num) == 0:
                nums["1"] += value
                continue

            if len(num) % 2 == 0:
                x = len(num) // 2
                nums[str(int(num[0:x]))] += value
                nums[str(int(num[x:]))] += value

                continue

            nums[str(int(num)*2024)] += value

        print([n for n, v in nums.items() if v > 0])
        print(sum(nums.values()))

    return sum(nums.values())



def solve_part_two(input: list[str]):
    return 0
