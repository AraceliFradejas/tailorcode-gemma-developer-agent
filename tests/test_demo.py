"""Verify observable behavior and actual checks behind the portfolio demo."""
import unittest
from demo.engine import compare, run_checks


class DemoTests(unittest.TestCase):
    def test_interactive_values_preserve_the_reported_rule(self):
        self.assertEqual(compare(0, 20), (20, 0))
        self.assertEqual(compare(None, 20), (20, 20))
        self.assertEqual(compare(-3, 20), (-3, -3))
        self.assertEqual(compare(12.5, 20), (12.5, 12.5))

    def test_button_checks_actual_original_and_corrected_code(self):
        result = run_checks()
        self.assertNotEqual(result['before']['exit_code'], 0)
        self.assertIn('AssertionError', result['before']['output'])
        self.assertEqual(result['after']['exit_code'], 0)
        self.assertIn('Ran 3 tests', result['after']['output'])
        self.assertIn('OK', result['after']['output'])


if __name__ == '__main__':
    unittest.main()
