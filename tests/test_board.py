"""
Unit tests for the Board class.

To run these tests from the repository root:
    python -m unittest tests/test_board.py         # Simple run
    python -m unittest -v tests/test_board.py      # Verbose output
    
To run a specific test:
    python -m unittest tests.test_board.TestBoard.test_clear_full_lines_one_full_line
"""

import unittest
import os
import sys

# Add repository root to path for imports
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        """Create a fresh board before each test."""
        self.board = Board(4, 3)  # Small board for testing (4 rows, 3 columns)

    def test_init_valid(self):
        """Test board initialization with valid dimensions."""
        board = Board(5, 4)
        self.assertEqual(board.height, 5)
        self.assertEqual(board.width, 4)
        # Check all cells are initialized to 0
        for i in range(5):
            for j in range(4):
                self.assertEqual(board.cell(i, j), 0)

    def test_init_invalid_type(self):
        """Test board initialization with invalid types."""
        with self.assertRaises(TypeError):
            Board("4", 3)  # height must be int
        with self.assertRaises(TypeError):
            Board(4, "3")  # width must be int

    def test_init_invalid_value(self):
        """Test board initialization with invalid values."""
        with self.assertRaises(ValueError):
            Board(0, 3)  # height must be positive
        with self.assertRaises(ValueError):
            Board(4, 0)  # width must be positive
        with self.assertRaises(ValueError):
            Board(-1, 3)  # height must be positive
        with self.assertRaises(ValueError):
            Board(4, -1)  # width must be positive

    def test_clear(self):
        """Test board clearing."""
        # Fill some cells
        self.board.set_cell(0, 0, 1)
        self.board.set_cell(1, 1, 2)
        self.board.set_cell(2, 2, 3)
        
        # Clear the board
        self.board.clear()
        
        # Verify all cells are 0
        for i in range(self.board.height):
            for j in range(self.board.width):
                self.assertEqual(self.board.cell(i, j), 0)

    def test_cell_and_set_cell(self):
        """Test getting and setting cell values."""
        # Test setting and reading back values
        self.board.set_cell(0, 0, 1)
        self.board.set_cell(1, 1, 2)
        self.board.set_cell(2, 2, 3)
        
        self.assertEqual(self.board.cell(0, 0), 1)
        self.assertEqual(self.board.cell(1, 1), 2)
        self.assertEqual(self.board.cell(2, 2), 3)
        
        # Test that unset cells are still 0
        self.assertEqual(self.board.cell(0, 1), 0)
        self.assertEqual(self.board.cell(1, 0), 0)

if __name__ == '__main__':
    unittest.main()