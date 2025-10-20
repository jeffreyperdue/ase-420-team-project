"""
Unit tests for the Row class edge cases.

To run these tests from the repository root:
  python -m unittest tests/test_row_edge_cases.py         # Simple run
  python -m unittest -v tests/test_row_edge_cases.py      # Verbose output
    
To run a specific test:
  python -m unittest tests.test_row_edge_cases.TestRowEdgeCases.test_init_invalid_width_raises
"""

import os
import sys
import unittest

# Add repo root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
  sys.path.insert(0, repo_root)

from src.game.row import Row


class TestRowEdgeCases(unittest.TestCase):
  def test_init_invalid_width_raises(self):
    with self.assertRaises(ValueError):
      Row(0)

  def test_get_bit_index_out_of_range_raises(self):
    r = Row(3)
    with self.assertRaises(IndexError):
      r.get_bit(3)

  def test_set_bit_index_out_of_range_raises(self):
    r = Row(3)
    with self.assertRaises(IndexError):
      r.set_bit(-1, 'c')

  def test_get_color_missing_returns_none(self):
    r = Row(3)
    self.assertIsNone(r.get_color(1))


if __name__ == '__main__':
  unittest.main()
