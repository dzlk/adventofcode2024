import re
from collections import Counter, defaultdict
from functools import reduce

import click

from utils.io import readfile


@click.command()
@click.argument('pzl', type=click.Path())
def run_day5(pzl):
    input = readfile(pzl)
    print("Result part one: " + str(solve_part_one(input)) + "\n")
    print("Result part two: " + str(solve_part_two(input)) + "\n")


def solve_part_one(input: list[str]) -> int:
    rules_to, rules_from, updates = parse_input(input)

    print(rules_to)
    print(rules_from)

    result = 0
    for update in updates:
        ok = check_update(update, rules_from)

        if ok:
            middle = update[len(update) // 2]
            print(f"Valid! Middle {middle}")

            result += middle

    return result


def solve_part_two(input: list[str]):
    rules_to, rules_from, updates = parse_input(input)

    print(rules_to)
    print(rules_from)

    result = 0
    for update in updates:
        ok = check_update(update, rules_from)

        if ok:
            print(f"Valid update: {update}!")
        else:
            print(f"Invalid update: {update}")

            backlinks = {page: len(rules_from[page] & set(update)) for page in update}
            print(f"Backlinks: {backlinks}")

            update_sorted = []
            queue = []
            for page in update:
                if backlinks[page] == 0:
                    queue.append(page)

            while queue:
                page = queue.pop(0)
                update_sorted.append(page)

                for page in rules_to[page] & set(update):
                    backlinks[page] -= 1

                    if backlinks[page] == 0:
                        queue.append(page)

            middle = update_sorted[len(update) // 2]
            print(f"Invalid {update} --> valid update: {update_sorted}! Middle {middle}")

            result += middle

    return result


def check_update(update, rules_from):
    for i, page_one in enumerate(update):
        for page_two in update[i:]:
            if page_two in rules_from[page_one]:
                return False

    return True

def parse_input(input: list[str]):
    rules_to = defaultdict(set)
    rules_from = defaultdict(set)

    updates = list()

    find_pair = True
    for line in input:
        if not line:
            find_pair = False
            continue

        if find_pair:
            a, b = map(int, line.split("|"))

            rules_to[a].add(b)
            rules_from[b].add(a)

        else:
            updates.append([int(p) for p in line.split(",")])

    return rules_to, rules_from, updates
