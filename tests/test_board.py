"""
Unit tests for the Board class.

To run these tests from the repository root:
    python -m unittest tests/test_board.py         # Simple run
    python -m unittest -v tests/test_board.py      # Verbose output
    
To run a specific test:
    python -m unittest tests.test_board.TestBoard.test_clear_full_lines_one_full_line
"""

import os
import sys
import unittest

# Add repository root to path for imports
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.board import Board
from src.constants import HEIGHT, WIDTH


class TestBoard(unittest.TestCase):
    def setUp(self):
        """Create a fresh board before each test."""
        # Board currently initializes with HEIGHT x WIDTH from src.constants
        self.board = Board()

    def test_init_dimensions_and_empty(self):
        """Board initializes to configured HEIGHT and WIDTH and is empty."""
        self.assertEqual(self.board.get_height(), HEIGHT)
        self.assertEqual(self.board.get_width(), WIDTH)

        # All cells should be empty (False)
        for i in range(self.board.get_height()):
            for j in range(self.board.get_width()):
                self.assertFalse(self.board.get_cell(i, j))

    def test_clear_and_set_get_cell(self):
        """Test set_cell, get_cell and clear behavior."""
        h = self.board.get_height()
        w = self.board.get_width()

        # Set a few cells and verify occupancy
        self.board.set_cell(0, 0, 1)
        self.board.set_cell(1, 1, 2)
        self.board.set_cell(2, 2, 3)

        self.assertTrue(self.board.get_cell(0, 0))
        self.assertTrue(self.board.get_cell(1, 1))
        self.assertTrue(self.board.get_cell(2, 2))

        # Clear and verify all cells are empty
        self.board.clear()
        for i in range(h):
            for j in range(w):
                self.assertFalse(self.board.get_cell(i, j))

    def test_clear_full_lines_single(self):
        """Fill a single row completely and ensure clear_full_lines removes it."""
        h = self.board.get_height()
        w = self.board.get_width()

        # Ensure board is empty
        self.assertEqual(sum(1 for i in range(h) if any(self.board.get_cell(i, j) for j in range(w))), 0)

        # Fill the bottom row (row index h-1)
        for col in range(w):
            self.board.set_cell(h - 1, col, 1)

        # Verify bottom row is occupied
        self.assertTrue(all(self.board.get_cell(h - 1, col) for col in range(w)))

        # Clear full lines and verify number of occupied rows goes back to 0
        self.board.clear_full_lines()
        self.assertEqual(sum(1 for i in range(h) if any(self.board.get_cell(i, j) for j in range(w))), 0)

    def test_clear_full_lines_multiple(self):
        """Fill multiple rows and ensure they are cleared."""
        h = self.board.get_height()
        w = self.board.get_width()

        # Fill two bottom rows
        for row in (h - 1, h - 2):
            for col in range(w):
                self.board.set_cell(row, col, 1)

        # Verify rows are occupied
        self.assertTrue(all(self.board.get_cell(h - 1, col) for col in range(w)))
        self.assertTrue(all(self.board.get_cell(h - 2, col) for col in range(w)))

        # Clear full lines
        self.board.clear_full_lines()
        self.assertEqual(sum(1 for i in range(h) if any(self.board.get_cell(i, j) for j in range(w))), 0)


if __name__ == '__main__':
    unittest.main()