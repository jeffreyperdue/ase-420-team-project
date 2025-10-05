"""
Unit tests for the core Board class functionality.

To run these tests from the repository root:
    python -m unittest tests/test_board_core.py         # Simple run
    python -m unittest -v tests/test_board_core.py      # Verbose output
    
To run a specific test:
    python -m unittest tests.test_board_core.TestBoardCore.test_init_with_factory_sets_dimensions
"""

import os
import sys
import unittest

# Add repository root to path for imports
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.board import Board
import src.constants as constants


def simple_row_factory():
    from src.game.row import Row
    return Row(4)


class TestBoardCore(unittest.TestCase):
    """Comprehensive board unit tests."""

    # Small, focused core tests for quick smoke checks.
    def test_init_with_factory_sets_dimensions(self):
        b = Board(simple_row_factory, height=4, width=4)
        self.assertEqual(b.height, 4)
        self.assertEqual(b.width, 4)

    def test_set_get_cell_single(self):
        b = Board(simple_row_factory, height=3, width=3)
        b.set_cell(0, 0, 'c')
        self.assertTrue(b.get_cell(0, 0))

    def test_clear_resets_rows(self):
        b = Board(simple_row_factory, height=3, width=3)
        b.set_cell(2, 2, 1)
        b.clear()
        self.assertFalse(b.get_cell(2, 2))
    
    # Full board tests
    def setUp(self):
        # Use a simple row factory compatible with the current Board constructor
        from src.game.row import Row
        self.board = Board(lambda: Row(constants.WIDTH), height=constants.HEIGHT, width=constants.WIDTH)

    def test_init_dimensions_and_empty(self):
        """Board initializes to configured HEIGHT and WIDTH and is empty."""
        self.assertEqual(self.board.height, constants.HEIGHT)
        self.assertEqual(self.board.width, constants.WIDTH)

        # All cells should be empty (False)
        for i in range(self.board.height):
            for j in range(self.board.width):
                self.assertFalse(self.board.get_cell(i, j))

    def test_set_and_get_cell(self):
        """Test that set_cell and get_cell correctly mark cells as occupied."""
        self.board.set_cell(0, 0, 1)
        self.board.set_cell(1, 1, 2)
        self.board.set_cell(2, 2, 3)

        self.assertTrue(self.board.get_cell(0, 0))
        self.assertTrue(self.board.get_cell(1, 1))
        self.assertTrue(self.board.get_cell(2, 2))

    def test_clear_resets_board(self):
        """Test that clear() empties all cells on the board."""
        h = self.board.height
        w = self.board.width

        # Pre-fill some cells
        self.board.set_cell(0, 0, 1)
        self.board.set_cell(h - 1, w - 1, 2)
        self.board.set_cell(2, 2, 3)

        self.assertTrue(self.board.get_cell(0, 0))
        self.assertTrue(self.board.get_cell(h - 1, w - 1))
        self.assertTrue(self.board.get_cell(2, 2))

        self.board.clear()

        for i in range(h):
            for j in range(w):
                self.assertFalse(self.board.get_cell(i, j))

    def test_clear_full_lines_single(self):
        """Fill a single row completely and ensure clear_full_lines removes it."""
        h = self.board.height
        w = self.board.width

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
        h = self.board.height
        w = self.board.width

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