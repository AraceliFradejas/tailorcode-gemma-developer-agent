import unittest
from repair_target import effective_price

class PriceTests(unittest.TestCase):
    def test_zero_is_a_valid_price(self):
        self.assertEqual(effective_price(0, 20), 0)

    def test_none_uses_fallback(self):
        self.assertEqual(effective_price(None, 20), 20)

    def test_nonzero_prices_are_preserved(self):
        for price in (12.5, -3):
            with self.subTest(price=price):
                self.assertEqual(effective_price(price, 20), price)

if __name__ == '__main__':
    unittest.main()
