import os
import unittest

from utils.io import readfile
from days.day1.solution import solution_part_one, solution_part_two


class Tests(unittest.TestCase):
    def _assertValue(self, solution, result):
        input = readfile(os.path.abspath("./input_test.txt"))
        self.assertEqual(solution(input), result)

    def test_part_one(self):
        self._assertValue(solution_part_one, 11)

    def test_part_two(self):
        self._assertValue(solution_part_two, 31)





if __name__ == '__main__':
    unittest.main()
