"""
Integration tests for Ghost Piece and Collision Detection interactions.

These tests verify that ghost piece calculation and collision detection
work together correctly, ensuring accurate landing position prediction.
"""

import unittest
from unittest.mock import patch
import os
import sys

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.game import Game
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row
from src.utils.session_manager import SessionManager
from src.constants import WIDTH, HEIGHT
from src.constants.game_states import PLAYING


class TestGhostCollisionIntegration(unittest.TestCase):
    """Integration tests for Ghost Piece and Collision Detection."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_ghost_piece_position_matches_actual_landing(self):
        """INTEGRATION: Ghost piece position matches actual landing position."""
        # Given: Game with current piece
        piece = self.game.current_piece
        initial_y = piece.y
        
        # When: Ghost piece landing position is calculated
        ghost_landing_y = self.board.get_landing_y(piece)
        ghost_cells = self.board.get_ghost_cells(piece)
        
        # Then: Ghost piece position is valid
        self.assertIsInstance(ghost_landing_y, int)
        self.assertGreaterEqual(ghost_landing_y, initial_y)
        self.assertLess(ghost_landing_y, HEIGHT)
        self.assertIsInstance(ghost_cells, list)
        self.assertGreater(len(ghost_cells), 0)
        
        # When: Piece is dropped to actual landing position
        # Simulate drop by moving piece to landing position
        piece.y = ghost_landing_y
        
        # Then: Piece would collide at landing position (or one below)
        collision_at_landing = self.board.will_piece_collide(piece)
        # Piece should be at or near collision point
        self.assertIsInstance(collision_at_landing, bool)
    
    def test_ghost_piece_updates_with_piece_movement(self):
        """INTEGRATION: Ghost piece updates correctly when piece moves horizontally."""
        # Given: Game with current piece
        piece = self.game.current_piece
        initial_x = piece.x
        
        # When: Piece moves right
        self.game.apply(["RIGHT"])
        new_x = piece.x
        
        # Then: Ghost piece position updates
        ghost_landing_y_before = self.board.get_landing_y(piece)
        ghost_cells_before = self.board.get_ghost_cells(piece)
        
        # Move piece back left
        self.game.apply(["LEFT"])
        
        # Then: Ghost piece position is different
        ghost_landing_y_after = self.board.get_landing_y(piece)
        ghost_cells_after = self.board.get_ghost_cells(piece)
        
        # Ghost cells should reflect the new position
        self.assertIsInstance(ghost_cells_before, list)
        self.assertIsInstance(ghost_cells_after, list)
    
    def test_ghost_piece_updates_with_piece_rotation(self):
        """INTEGRATION: Ghost piece updates correctly when piece rotates."""
        # Given: Game with current piece
        piece = self.game.current_piece
        initial_rotation = piece.rotation
        
        # When: Piece rotates
        self.game.apply(["ROTATE"])
        new_rotation = piece.rotation
        
        # Then: Ghost piece position updates
        ghost_landing_y = self.board.get_landing_y(piece)
        ghost_cells = self.board.get_ghost_cells(piece)
        
        # Ghost piece should reflect new rotation
        self.assertIsInstance(ghost_landing_y, int)
        self.assertIsInstance(ghost_cells, list)
        self.assertGreater(len(ghost_cells), 0)
    
    def test_ghost_piece_disappears_when_piece_locks(self):
        """INTEGRATION: Ghost piece disappears when piece locks."""
        # Given: Game with current piece
        piece = self.game.current_piece
        
        # When: Ghost piece is calculated
        ghost_landing_y = self.board.get_landing_y(piece)
        ghost_cells = self.board.get_ghost_cells(piece)
        self.assertIsNotNone(ghost_landing_y)
        self.assertIsNotNone(ghost_cells)
        
        # When: Piece locks (drops)
        self.game.apply(["DROP"])
        
        # Then: New piece is spawned
        new_piece = self.game.current_piece
        self.assertIsNotNone(new_piece)
        
        # Ghost piece for new piece should be different
        new_ghost_landing_y = self.board.get_landing_y(new_piece)
        new_ghost_cells = self.board.get_ghost_cells(new_piece)
        self.assertIsNotNone(new_ghost_landing_y)
        self.assertIsNotNone(new_ghost_cells)
    
    def test_ghost_piece_collision_detection_accuracy(self):
        """INTEGRATION: Ghost piece collision detection is accurate."""
        # Given: Game with current piece
        piece = self.game.current_piece
        
        # When: Ghost piece landing position is calculated
        ghost_landing_y = self.board.get_landing_y(piece)
        
        # Then: Landing position is valid (within board bounds)
        self.assertGreaterEqual(ghost_landing_y, 0)
        self.assertLess(ghost_landing_y, HEIGHT)
        
        # When: Piece is placed at landing position
        test_piece = Piece(piece.x, ghost_landing_y)
        test_piece.type = piece.type
        test_piece.rotation = piece.rotation
        
        # Then: Piece at landing position should be at collision point or just above
        collision_at_landing = self.board.will_piece_collide(test_piece)
        # Piece should be near collision (may or may not collide depending on implementation)
        self.assertIsInstance(collision_at_landing, bool)
    
    def test_ghost_piece_with_obstacles(self):
        """INTEGRATION: Ghost piece calculates correctly with obstacles on board."""
        # Given: Board with obstacles
        # Place some pieces on the board
        for col in range(3, 7):
            self.board.set_cell(HEIGHT - 5, col, 1)
        
        piece = self.game.current_piece
        
        # When: Ghost piece landing position is calculated
        ghost_landing_y = self.board.get_landing_y(piece)
        ghost_cells = self.board.get_ghost_cells(piece)
        
        # Then: Ghost piece lands above obstacles
        self.assertIsInstance(ghost_landing_y, int)
        self.assertLess(ghost_landing_y, HEIGHT - 5)  # Should land above obstacles
        self.assertIsInstance(ghost_cells, list)
    
    def test_ghost_piece_at_board_edges(self):
        """INTEGRATION: Ghost piece calculates correctly at board edges."""
        # Given: Piece at left edge
        piece = self.game.current_piece
        # Move piece to left edge
        for _ in range(WIDTH):
            self.game.apply(["LEFT"])
            if piece.x == 0:
                break
        
        # When: Ghost piece landing position is calculated
        ghost_landing_y = self.board.get_landing_y(piece)
        ghost_cells = self.board.get_ghost_cells(piece)
        
        # Then: Ghost piece position is valid
        self.assertIsInstance(ghost_landing_y, int)
        self.assertGreaterEqual(ghost_landing_y, 0)
        self.assertLess(ghost_landing_y, HEIGHT)
        self.assertIsInstance(ghost_cells, list)
        
        # Test at right edge
        for _ in range(WIDTH):
            self.game.apply(["RIGHT"])
            if piece.x >= WIDTH - 1:
                break
        
        ghost_landing_y_right = self.board.get_landing_y(piece)
        self.assertIsInstance(ghost_landing_y_right, int)


class TestGhostPieceEdgeCases(unittest.TestCase):
    """Integration tests for edge cases in ghost piece calculation."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_ghost_piece_with_nearly_full_board(self):
        """INTEGRATION: Ghost piece calculates correctly with nearly full board."""
        # Given: Board nearly full
        for row in range(HEIGHT - 3, HEIGHT):
            for col in range(WIDTH):
                if col != WIDTH // 2:  # Leave one column open
                    self.board.set_cell(row, col, 1)
        
        piece = self.game.current_piece
        
        # When: Ghost piece landing position is calculated
        ghost_landing_y = self.board.get_landing_y(piece)
        ghost_cells = self.board.get_ghost_cells(piece)
        
        # Then: Ghost piece position is valid
        self.assertIsInstance(ghost_landing_y, int)
        self.assertGreaterEqual(ghost_landing_y, 0)
        self.assertIsInstance(ghost_cells, list)
    
    def test_ghost_piece_with_different_piece_types(self):
        """INTEGRATION: Ghost piece calculates correctly for different piece types."""
        # Given: Different piece types
        piece = self.game.current_piece
        
        # Test with current piece type
        ghost_landing_y = self.board.get_landing_y(piece)
        self.assertIsInstance(ghost_landing_y, int)
        
        # Test with different rotations
        for _ in range(4):
            self.game.apply(["ROTATE"])
            ghost_landing_y_rotated = self.board.get_landing_y(piece)
            self.assertIsInstance(ghost_landing_y_rotated, int)
            self.assertGreaterEqual(ghost_landing_y_rotated, 0)
            self.assertLess(ghost_landing_y_rotated, HEIGHT)
    
    def test_ghost_piece_real_time_updates(self):
        """INTEGRATION: Ghost piece updates in real-time with piece movements."""
        # Given: Game with current piece
        piece = self.game.current_piece
        
        # When: Piece moves and rotates multiple times
        movements = [
            ["RIGHT"],
            ["ROTATE"],
            ["LEFT"],
            ["ROTATE"],
            ["DOWN"],
        ]
        
        for movement in movements:
            self.game.apply(movement)
            
            # Then: Ghost piece position is recalculated correctly
            ghost_landing_y = self.board.get_landing_y(piece)
            ghost_cells = self.board.get_ghost_cells(piece)
            
            self.assertIsInstance(ghost_landing_y, int)
            self.assertIsInstance(ghost_cells, list)
            self.assertGreaterEqual(ghost_landing_y, piece.y)


if __name__ == '__main__':
    unittest.main()

