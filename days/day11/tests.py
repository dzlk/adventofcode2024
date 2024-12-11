import os
import unittest

from utils.io import readfile
from .solution import solve_part_one, solve_part_two


class Tests(unittest.TestCase):
    def _assertValue(self, solution, result):
        input = readfile(os.path.join(os.path.dirname(__file__), "input_test.txt"))
        self.assertEqual(solution(input), result)

    def test_part_one(self):
        self._assertValue(solve_part_one, 55312)

    def test_part_two(self):
        self._assertValue(solve_part_two, 0)

if __name__ == '__main__':
    unittest.main()
