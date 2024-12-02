import os
import unittest

from utils.io import readfile
from days.day2.solution import solve_part_one, solve_part_two, check_report


class Tests(unittest.TestCase):
    def _assertValue(self, solution, result):
        input = readfile(os.path.abspath("./input_test.txt"))
        self.assertEqual(solution(input), result)

    def test_part_one(self):
        self._assertValue(solve_part_one, 2)

    def test_part_two(self):
        self._assertValue(solve_part_two, 4)

    def test_tolerance(self):
        self.assertTrue(check_report([11, 5, 12, 14], tolerance=True),
                        f"Wrong: {[11, 5, 12, 14]}")
        self.assertTrue(check_report([80, 82, 77, 75, 74, 72], tolerance=True),
                        f"Wrong: {[80, 82, 77, 75, 74, 72]}")
        self.assertFalse(check_report([1, 2, 7, 8, 9], tolerance=True),
                        f"Wrong: {[1, 2, 7, 8, 9]}")
        self.assertTrue(check_report([88, 86, 88, 89, 90, 93, 95], tolerance=True),
                        f"Wrong: {[88, 86, 88, 89, 90, 93, 95]}")



if __name__ == '__main__':
    unittest.main()
