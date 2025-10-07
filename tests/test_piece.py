import os
import sys
import unittest
from unittest.mock import patch

# Add repo root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.piece import Piece
from src.game.board import Board
from src.figures import SHAPES

class TestPiece(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.board = Board()
        
    @patch('src.game.piece.random.randint')
    def test_piece_initalization(self, mock_randint): 
        # Setup the return values for random numbers: first call for shape, second for color
        mock_randint.side_effect = [2, 5]

        testPiece = Piece(5, 8)

        self.assertEqual(testPiece.x, 5)
        self.assertEqual(testPiece.y, 8)
        self.assertEqual(testPiece.type, 2)
        self.assertEqual(testPiece.color, 5)
        self.assertEqual(testPiece.rotation, 0)

    @patch('src.game.piece.random.randint')
    def test_piece_rotation(self, mock_randint):
        """Test piece rotation mechanics."""
        # Use I piece (index 0) which has 2 rotations
        mock_randint.side_effect = [0, 1]  # type=0 (I piece), color=1
        piece = Piece(3, 0)

        # Get initial shape
        initial_shape = SHAPES[piece.type][piece.rotation]
        
        # Rotate piece
        self.board.rotate(piece)
        
        # Verify rotation changed
        self.assertEqual(piece.rotation, 1)
        rotated_shape = SHAPES[piece.type][piece.rotation]
        self.assertNotEqual(initial_shape, rotated_shape)
        
        # Verify it cycles back to 0
        self.board.rotate(piece)
        self.assertEqual(piece.rotation, 0)
        self.assertEqual(SHAPES[piece.type][piece.rotation], initial_shape)

    @patch('src.game.piece.random.randint')
    def test_piece_horizontal_movement(self, mock_randint):
        """Test left/right movement."""
        mock_randint.side_effect = [0, 1]  # type=0 (I piece), color=1
        piece = Piece(3, 0)
        
        # Test moving right
        initial_x = piece.x
        self.board.go_side(1, piece)
        self.assertEqual(piece.x, initial_x + 1)
        
        # Test moving left
        self.board.go_side(-1, piece)
        self.assertEqual(piece.x, initial_x)
        
        # Test wall collision (move left until wall)
        for _ in range(10):  # More than board width
            self.board.go_side(-1, piece)
        self.assertGreaterEqual(piece.x, 0)  # Should not go past left wall

    @patch('src.game.piece.random.randint')
    def test_piece_vertical_movement(self, mock_randint):
        """Test downward movement and collision detection."""
        mock_randint.side_effect = [0, 1]  # type=0 (I piece), color=1
        piece = Piece(3, 0)
        
        # Test moving down
        initial_y = piece.y
        moved = self.board.go_down(piece)
        self.assertTrue(moved)
        self.assertEqual(piece.y, initial_y + 1)
        
        # Test bottom collision
        # Move piece to bottom
        while self.board.go_down(piece):
            pass
        final_y = piece.y
        
        # Try to move down one more time
        moved = self.board.go_down(piece)
        self.assertFalse(moved)  # Should not have moved
        self.assertEqual(piece.y, final_y)  # Y position should not have changed

    @patch('src.game.piece.random.randint')
    def test_piece_hard_drop(self, mock_randint):
        """Test hard drop (space bar) functionality."""
        mock_randint.side_effect = [0, 1]  # type=0 (I piece), color=1
        piece = Piece(3, 0)
        
        initial_y = piece.y
        self.board.go_space(piece)
        
        # Piece should be at bottom
        self.assertGreater(piece.y, initial_y)
        # Verify it can't move down further
        moved = self.board.go_down(piece)
        self.assertFalse(moved)

if __name__ == '__main__':
    unittest.main()