"""
Unit tests for the core Row class functionality.

To run these tests from the repository root:
    python -m unittest tests/test_row_core.py         # Simple run
    python -m unittest -v tests/test_row_core.py      # Verbose output
    
To run a specific test:
    python -m unittest tests.test_row_core.TestRowCore.test_init_sets_width_and_mask
"""

import os
import sys
import unittest

# Add repo root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.row import Row


class TestRowCore(unittest.TestCase):
    def test_init_sets_width_and_mask(self):
        r = Row(4)
        self.assertEqual(r.width, 4)
        self.assertEqual(r.mask, (1 << 4) - 1)

    def test_set_and_get_bit(self):
        r = Row(3)
        r.set_bit(1, 'x')
        self.assertTrue(r.get_bit(1))

    def test_get_color_after_set(self):
        r = Row(3)
        r.set_bit(2, 'blue')
        self.assertEqual(r.get_color(2), 'blue')


if __name__ == '__main__':
    unittest.main()

