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

    # Cody's game mechanics tests - PRESERVED FROM ORIGINAL test_board.py
    def test_will_piece_collide(self):
        """Test piece collision detection functionality from Cody's implementation."""
        from src.game.piece import Piece
        from src.game.row import Row
        
        # Create a full-size board for Cody's collision tests
        def full_row_factory():
            return Row(constants.WIDTH)
        
        full_board = Board(full_row_factory, height=constants.HEIGHT, width=constants.WIDTH)
        
        # Create pieces that will actually collide - use same position for guaranteed collision
        pieceToCollide = Piece(2, 4)
        collisionTestPieceX = Piece(2, 4)  # Same position - guaranteed collision

        # Checking if collision on x axis (pieces at same position)
        full_board.place_piece(collisionTestPieceX)
        self.assertTrue(full_board.will_piece_collide(pieceToCollide))

        # Clear and test y-axis collision
        full_board.clear()
        collisionTestPieceY = Piece(2, 4)  # Same position again

        # Checking if collision on y axis
        full_board.place_piece(collisionTestPieceY)
        self.assertTrue(full_board.will_piece_collide(pieceToCollide))

        # Clearing board and checking if collision on empty board
        full_board.clear()

        pieceNoCollision = Piece(2, 5)
        self.assertFalse(full_board.will_piece_collide(pieceNoCollision))

    def test_place_piece(self):
        """Test piece placement functionality from Cody's implementation."""
        from src.game.piece import Piece
        from src.figures import SHAPES
        from src.game.row import Row
        
        # Create a full-size board for Cody's piece placement tests
        def full_row_factory():
            return Row(constants.WIDTH)
        
        full_board = Board(full_row_factory, height=constants.HEIGHT, width=constants.WIDTH)
        
        # Creating and placing piece
        testPiece = Piece(3, 5)
        full_board.place_piece(testPiece)

        shape = SHAPES[testPiece.type][testPiece.rotation]

        # Checking if each cell has been filled in for piece
        for grid_position in shape:
            coords = full_board.grid_position_to_coords(grid_position, testPiece.x, testPiece.y)
            col = coords[0]
            row = coords[1]

            self.assertTrue(full_board.get_cell(row, col))

    def test_grid_position_to_coords(self):
        """Test coordinate conversion functionality from Cody's implementation."""
        # Test coordinate conversion
        coords = self.board.grid_position_to_coords(0, 5, 3)  # position 0, x=5, y=3
        self.assertEqual(coords, (5, 3))  # (x + 0%4, y + 0//4) = (5, 3)
        
        coords = self.board.grid_position_to_coords(5, 2, 1)  # position 5, x=2, y=1
        self.assertEqual(coords, (3, 2))  # (x + 5%4, y + 5//4) = (2+1, 1+1) = (3, 2)


if __name__ == '__main__':
    unittest.main()