import os
import sys
import unittest

# Add repo root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.row import Row


class TestRow(unittest.TestCase):
    def setUp(self):
        Row.set_mask(5)  # small width for tests
        self.row = Row()

    def test_mask_and_bits(self):
        # Initially empty
        for c in range(5):
            self.assertFalse(self.row.get_bit(c))

        # Set a bit and check
        self.row.set_bit(2, 'red')
        self.assertTrue(self.row.get_bit(2))
        self.assertEqual(self.row.get_color(2), 'red')

    def test_is_full_and_clear(self):
        # Set all bits
        for c in range(5):
            self.row.set_bit(c, 'blue')
        # Row should be full if mask matches
        self.assertTrue(self.row.is_full())

        # Clear and ensure empty
        self.row.clear_row()
        for c in range(5):
            self.assertFalse(self.row.get_bit(c))
            self.assertIsNone(self.row.get_color(c))


if __name__ == '__main__':
    unittest.main()