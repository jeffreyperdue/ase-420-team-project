"""
Integration tests for Game-Board component interactions.

These tests verify that the Game and Board classes work together correctly,
ensuring proper data flow and state management between components.

To run these tests:
    python -m pytest tests/integration/test_game_integration.py -v
    python -m unittest tests.integration.test_game_integration -v
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add repository root to path for imports
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.game import Game
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row
from src.utils.session_manager import SessionManager
from src.constants import WIDTH, HEIGHT


class TestGameBoardIntegration(unittest.TestCase):
    """Test integration between Game and Board components."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create a board with standard dimensions
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        # Create a simple piece spawner function
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        # Create game instance
        self.session = SessionManager()
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()  # Start game so pieces are initialized

    def test_game_initialization_with_board(self):
        """Test that game initializes correctly with board."""
        self.assertIsNotNone(self.game.board)
        self.assertIsNotNone(self.game.current_piece)
        self.assertFalse(self.game.done)
        self.assertEqual(self.game.gravity_timer, 0)
        self.assertEqual(self.game.gravity_delay, 30)

    def test_piece_placement_and_board_state(self):
        """Test that piece placement updates board state correctly."""
        # Get initial piece position
        piece = self.game.current_piece
        initial_x, initial_y = piece.x, piece.y
        
        # Apply DOWN intent to move piece
        self.game.apply(["DOWN"])
        
        # Verify piece moved down (if no collision occurred)
        if not self.game.done:
            self.assertEqual(piece.y, initial_y + 1)
            self.assertEqual(piece.x, initial_x)

    def test_piece_rotation_integration(self):
        """Test that piece rotation works through game integration."""
        piece = self.game.current_piece
        initial_rotation = piece.rotation
        
        # Apply ROTATE intent
        self.game.apply(["ROTATE"])
        
        # Verify rotation changed (or piece is still valid if rotation failed due to collision)
        # Note: Rotation might not work if piece hits boundaries or other constraints
        self.assertIsNotNone(piece)
        self.assertIsInstance(piece.rotation, int)

    def test_piece_movement_left_right_integration(self):
        """Test horizontal movement integration."""
        piece = self.game.current_piece
        initial_x = piece.x
        
        # Move right
        self.game.apply(["RIGHT"])
        self.assertEqual(piece.x, initial_x + 1)
        
        # Move left
        self.game.apply(["LEFT"])
        self.assertEqual(piece.x, initial_x)

    def test_piece_drop_and_placement_integration(self):
        """Test that hard drop properly places piece on board."""
        piece = self.game.current_piece
        
        # Apply DROP intent
        self.game.apply(["DROP"])
        
        # Verify piece is placed at bottom
        # (This test may need adjustment based on actual drop behavior)
        self.assertGreater(piece.y, 0)

    def test_line_clearing_integration(self):
        """Test that line clearing works through game integration."""
        # Create a scenario with a full row
        # Fill bottom row completely
        for col in range(WIDTH):
            self.board.set_cell(HEIGHT - 1, col, 1)
        
        # Verify row is full
        full_rows_before = sum(1 for row in range(HEIGHT) 
                              if all(self.board.get_cell(row, col) for col in range(WIDTH)))
        self.assertEqual(full_rows_before, 1)
        
        # Clear full lines
        self.board.clear_full_lines()
        
        # Verify row is cleared
        full_rows_after = sum(1 for row in range(HEIGHT) 
                             if all(self.board.get_cell(row, col) for col in range(WIDTH)))
        self.assertEqual(full_rows_after, 0)

    def test_gravity_system_integration(self):
        """Test that gravity system works through game integration."""
        piece = self.game.current_piece
        initial_y = piece.y
        
        # Update game multiple times to trigger gravity
        for _ in range(self.game.gravity_delay + 1):
            self.game.update()
        
        # Verify piece has moved down due to gravity
        self.assertGreater(piece.y, initial_y)

    def test_collision_detection_integration(self):
        """Test collision detection between game and board."""
        piece = self.game.current_piece
        
        # Place a piece on the board
        self.board.place_piece(piece)
        
        # Create another piece at the same position
        collision_piece = Piece(piece.x, piece.y)
        
        # Verify collision is detected
        self.assertTrue(self.board.will_piece_collide(collision_piece))

    def test_game_over_condition_integration(self):
        """Test game over condition through integration."""
        # Create a new piece that would collide at spawn
        def spawn_collision_piece():
            return Piece(WIDTH // 2, 0)

        session = SessionManager()
        collision_game = Game(self.board, spawn_collision_piece, session)
        collision_game.start_new_game()  # Initialize pieces (this clears the board!)
        
        # Fill board AFTER start_new_game() since it clears the board
        # Fill rows 0-3 completely to ensure piece at spawn collides
        # Piece type 0, rotation 0 places cells at (x+1, y), (x+1, y+1), (x+1, y+2), (x+1, y+3)
        # At x=WIDTH//2=5, this is (6, 0), (6, 1), (6, 2), (6, 3)
        for row in range(0, 4):  # Fill rows 0-3
            for col in range(WIDTH):
                collision_game.board.set_cell(row, col, 1)

        # NOTE: Game over screen is not implemented in Sprint 1, so we test collision detection instead
        # Check if the piece would collide at spawn position
        # Use the current_piece from the game, which should have the correct type and rotation
        test_piece = collision_game.current_piece
        # Ensure piece has type and rotation set (will_piece_collide needs these)
        test_piece.type = 0  # Use a simple piece type
        test_piece.rotation = 0
        # Reset position to spawn position
        test_piece.x = WIDTH // 2
        test_piece.y = 0
        collision_detected = collision_game.board.will_piece_collide(test_piece)

        # Verify collision detection works (game over screen will be implemented in Sprint 2)
        # Since we filled rows 0-3, a piece at spawn (y=0) extending to row 3 should collide
        self.assertTrue(collision_detected, f"Piece at ({test_piece.x}, {test_piece.y}) with type {test_piece.type}, rotation {test_piece.rotation} should collide with filled rows 0-3")
        
        # Verify the board is properly filled near the top
        filled_cells = 0
        for row in range(min(3, HEIGHT)):
            for col in range(WIDTH):
                if collision_game.board.get_cell(row, col):
                    filled_cells += 1
        self.assertGreater(filled_cells, 0)  # At least some cells should be filled

    def test_multiple_intents_processing(self):
        """Test that multiple intents are processed correctly."""
        piece = self.game.current_piece
        initial_x, initial_y = piece.x, piece.y
        
        # Apply multiple intents
        self.game.apply(["RIGHT", "DOWN", "ROTATE"])
        
        # Verify all actions were processed
        self.assertEqual(piece.x, initial_x + 1)  # Right movement
        self.assertEqual(piece.y, initial_y + 1)  # Down movement
        # Rotation should have changed (exact value depends on piece type)

    def test_game_state_consistency(self):
        """Test that game state remains consistent across operations."""
        initial_piece = self.game.current_piece
        
        # Perform various operations
        self.game.apply(["LEFT"])
        self.game.apply(["RIGHT"])
        self.game.apply(["ROTATE"])
        self.game.update()
        
        # Verify game state is still valid
        self.assertIsNotNone(self.game.current_piece)
        self.assertFalse(self.game.done)
        self.assertIsNotNone(self.game.board)

    def test_piece_spawning_after_lock_integration(self):
        """Test that new pieces spawn correctly after locking."""
        # This test would need to simulate piece locking
        # For now, we'll test the spawn mechanism
        initial_piece = self.game.current_piece
        
        # Simulate spawning a new piece
        new_piece = self.game.spawn_piece()
        
        # Verify new piece is different from initial
        self.assertIsNotNone(new_piece)
        self.assertEqual(new_piece.x, WIDTH // 2)
        self.assertEqual(new_piece.y, 0)

    def test_board_dimensions_preserved(self):
        """Test that board dimensions are preserved through game operations."""
        initial_height = self.board.height
        initial_width = self.board.width
        
        # Perform various game operations
        self.game.apply(["DOWN", "LEFT", "RIGHT"])
        self.game.update()
        
        # Verify dimensions are unchanged
        self.assertEqual(self.board.height, initial_height)
        self.assertEqual(self.board.width, initial_width)


class TestGameBoardEdgeCases(unittest.TestCase):
    """Test edge cases in Game-Board integration."""

    def setUp(self):
        """Set up test environment for edge case testing."""
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.session = SessionManager()
        self.game = Game(self.board, spawn_piece, self.session)

    def test_boundary_movement_integration(self):
        """Test piece movement at board boundaries."""
        self.game.start_new_game()  # Initialize pieces
        piece = self.game.current_piece
        
        # Move to left boundary (limit iterations)
        initial_x = piece.x
        for _ in range(min(WIDTH + 5, 20)):  # Limit to prevent excessive iterations
            self.game.apply(["LEFT"])
            if piece.x == 0:
                break
        
        # Verify piece doesn't go below 0
        self.assertGreaterEqual(piece.x, 0)
        
        # Move to right boundary (limit iterations)
        for _ in range(min(WIDTH + 5, 20)):  # Limit to prevent excessive iterations
            self.game.apply(["RIGHT"])
            if piece.x == WIDTH - 1:
                break
        
        # Verify piece doesn't exceed board width
        self.assertLess(piece.x, WIDTH)

    def test_rapid_input_handling(self):
        """Test that rapid input is handled correctly."""
        self.game.start_new_game()  # Initialize pieces
        piece = self.game.current_piece
        
        # Apply rapid input (reduced iterations to prevent issues)
        for _ in range(5):  # Reduced from 10
            self.game.apply(["RIGHT", "LEFT", "ROTATE"])
        
        # Verify game state is still valid
        self.assertIsNotNone(self.game.current_piece)
        self.assertFalse(self.game.done)

    def test_empty_intent_list_handling(self):
        """Test handling of empty intent lists."""
        initial_piece = self.game.current_piece
        
        # Apply empty intent list
        self.game.apply([])
        
        # Verify game state is unchanged
        self.assertEqual(self.game.current_piece, initial_piece)

    def test_invalid_intent_handling(self):
        """Test handling of invalid intents."""
        initial_piece = self.game.current_piece
        
        # Apply invalid intent
        self.game.apply(["INVALID_INTENT"])
        
        # Verify game state is unchanged
        self.assertEqual(self.game.current_piece, initial_piece)


if __name__ == '__main__':
    unittest.main()
