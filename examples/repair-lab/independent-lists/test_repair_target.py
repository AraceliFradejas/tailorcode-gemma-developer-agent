import unittest
from repair_target import add_label

class LabelTests(unittest.TestCase):
    def test_default_calls_are_independent(self):
        first = add_label('python')
        second = add_label('tests')
        self.assertEqual(first, ['python'])
        self.assertEqual(second, ['tests'])
        self.assertIsNot(first, second)

    def test_supplied_list_is_preserved(self):
        labels = ['ai']
        self.assertIs(add_label('python', labels), labels)
        self.assertEqual(labels, ['ai', 'python'])

    def test_empty_supplied_list_is_not_replaced(self):
        labels = []
        self.assertIs(add_label('ai', labels), labels)

if __name__ == '__main__':
    unittest.main()
