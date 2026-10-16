import unittest
from repair_target import even_numbers

class RangeTests(unittest.TestCase):
    def test_even_upper_bound_is_included(self):
        self.assertEqual(even_numbers(1, 4), [2, 4])

    def test_single_even_endpoint(self):
        self.assertEqual(even_numbers(2, 2), [2])

    def test_odd_upper_bound(self):
        self.assertEqual(even_numbers(0, 3), [0, 2])

    def test_negative_and_reversed_ranges(self):
        self.assertEqual(even_numbers(-4, 0), [-4, -2, 0])
        self.assertEqual(even_numbers(5, 1), [])

if __name__ == '__main__':
    unittest.main()
