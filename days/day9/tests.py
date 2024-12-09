import os
import unittest

from utils.io import readfile
from .solution import solve_part_one, solve_part_two, hashsum


class Tests(unittest.TestCase):
    def _assertValue(self, solution, result):
        input = readfile(os.path.join(os.path.dirname(__file__), "input_test.txt"))
        self.assertEqual(solution(input), result)

    def test_part_one(self):
        self._assertValue(solve_part_one, 1928)

    def test_part_two(self):
        self._assertValue(solve_part_two, 0)

    def test_hashsum_without_space(self):
        # 1234 = 1 * 0 + 2 * 1 + 3 * 2 + 4 * 3
        self.assertEqual(hashsum("1010101"), 20)

if __name__ == '__main__':
    unittest.main()
