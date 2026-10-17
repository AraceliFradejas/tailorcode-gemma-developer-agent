"""Verify observable behavior and actual checks behind the portfolio demo."""
import unittest
from demo.engine import basket_trace, compare, run_checks


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

    def test_new_baskets_are_independent_after_fix(self):
        trace = basket_trace('Manzanas', 'Pan')
        self.assertEqual(trace['before']['first_after_own_purchase'], ['Manzanas'])
        self.assertEqual(trace['before']['first_final'], ['Manzanas', 'Pan'])
        self.assertTrue(trace['before']['same_basket'])
        self.assertEqual(trace['after']['first_final'], ['Manzanas'])
        self.assertEqual(trace['after']['second_final'], ['Pan'])
        self.assertFalse(trace['after']['same_basket'])
        again = basket_trace('Leche', 'Huevos')
        self.assertEqual(again['before']['first_final'], ['Leche', 'Huevos'])
        self.assertEqual(again['after']['second_final'], ['Huevos'])

    def test_basket_acceptance_checks_fail_then_pass(self):
        result = run_checks('independent-lists')
        self.assertNotEqual(result['before']['exit_code'], 0)
        self.assertIn('AssertionError', result['before']['output'])
        self.assertEqual(result['after']['exit_code'], 0)
        self.assertIn('Ran 3 tests', result['after']['output'])


if __name__ == '__main__':
    unittest.main()
