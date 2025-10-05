import os
import sys
import unittest
from unittest.mock import patch

# Add repo root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.piece import Piece

class TestPiece(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()