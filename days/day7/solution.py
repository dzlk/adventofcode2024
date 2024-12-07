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
    examples = parse_input(input)

    def is_valid(total, nums):
        if len(nums) == 0:
            return total == 0

        if total < 0:
            return False

        return is_valid(total - nums[-1], nums[:-1]) or (
                total % nums[-1] == 0 and is_valid(total // nums[-1], nums[:-1])
        )

    result = 0

    for total, nums in examples:
        totals = list()
        totals.append((total, ""))

        print(total, nums)
        print("----------")

        if is_valid(total, nums):
            print("valid")
            result += total

        print("\n")

    return result


def solve_part_two(input: list[str]):
    examples = parse_input(input)

    def is_valid(total, nums):
        if len(nums) == 0:
            return total == 0

        if total < 0:
            return False

        total_str = str(total)
        num_str = str(nums[-1])
        total_len = len(total_str)
        num_len = len(num_str)

        return is_valid(total - nums[-1], nums[:-1]) or (
                total % nums[-1] == 0 and is_valid(total // nums[-1], nums[:-1])
        ) or (
            total_len >= num_len and total_str[-num_len:] == num_str and
            is_valid(int(total_str[:-len(num_str)] or 0), nums[:-1])
        )

    result = 0

    for total, nums in examples:
        totals = list()
        totals.append((total, ""))

        print(total, nums)
        print("----------")

        if is_valid(total, nums):
            print("valid")
            result += total

        print("\n")

    return result


def parse_input(input: list[str]):
    examples = list()

    for line in input:
        total, nums = line.split(": ")
        total = int(total)

        nums = [int(n) for n in nums.split()]

        examples.append((total, nums))

    return examples
