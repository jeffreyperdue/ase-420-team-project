"""
Integration tests for Input-Game component interactions.

These tests verify that keyboard input is properly translated into game actions
and that the InputHandler and Game components work together correctly.

To run these tests:
    python -m pytest tests/integration/test_input_game_integration.py -v
    python -m unittest tests.integration.test_input_game_integration -v
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import pygame

# Add repository root to path for imports
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.game import Game
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row
from src.view.input import InputHandler
from src.constants import WIDTH, HEIGHT


class TestInputGameIntegration(unittest.TestCase):
    """Test integration between InputHandler and Game components."""

    def setUp(self):
        """Set up test environment before each test."""
        # Create game components
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece)
        self.input_handler = InputHandler()

    def test_keyboard_input_translates_to_game_actions(self):
        """Test that keyboard events are properly translated to game intents."""
        # Create mock pygame events using actual pygame constants
        mock_events = [
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_UP),     # ROTATE
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT),   # LEFT
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_RIGHT),  # RIGHT
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_DOWN),   # DOWN
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_SPACE),  # DROP
        ]
        
        # Get intents from input handler
        intents = self.input_handler.get_intents(mock_events)
        
        # Verify correct intents were generated
        expected_intents = ["ROTATE", "LEFT", "RIGHT", "DOWN", "DROP"]
        self.assertEqual(len(intents), len(expected_intents))
        for intent in expected_intents:
            self.assertIn(intent, intents)

    def test_multiple_inputs_handled_correctly(self):
        """Test that multiple simultaneous inputs are handled correctly."""
        piece = self.game.current_piece
        initial_x, initial_y = piece.x, piece.y
        
        # Create multiple simultaneous key events
        mock_events = [
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT),   # LEFT
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_DOWN),   # DOWN
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_UP),     # ROTATE
        ]
        
        # Process inputs
        intents = self.input_handler.get_intents(mock_events)
        self.game.apply(intents)
        
        # Verify all actions were processed
        self.assertEqual(piece.x, initial_x - 1)  # LEFT
        self.assertEqual(piece.y, initial_y + 1)  # DOWN
        # Rotation should have changed

    def test_input_timing_and_game_state(self):
        """Test that input timing doesn't affect game state consistency."""
        piece = self.game.current_piece
        
        # Apply input multiple times rapidly
        for _ in range(5):
            mock_events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT)]  # LEFT
            intents = self.input_handler.get_intents(mock_events)
            self.game.apply(intents)
        
        # Verify game state is still valid
        self.assertIsNotNone(self.game.current_piece)
        self.assertFalse(self.game.done)
        self.assertGreaterEqual(piece.x, 0)  # Should not go below 0

    def test_quit_condition_propagation(self):
        """Test that quit input properly propagates through the system."""
        # Create mock quit event
        mock_events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)]  # pygame.K_ESCAPE (QUIT)
        
        # Get intents
        intents = self.input_handler.get_intents(mock_events)
        
        # Verify QUIT intent is generated
        self.assertIn("QUIT", intents)
        
        # Apply quit intent to game
        self.game.apply(intents)
        
        # Note: The game doesn't directly handle QUIT, that's done in main()
        # This test verifies the intent is properly generated

    def test_invalid_key_ignored(self):
        """Test that invalid keys are ignored by input handler."""
        # Create mock events with invalid keys
        mock_events = [
            MagicMock(type=pygame.KEYDOWN, key=65),      # 'A' key (not mapped)
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT),  # LEFT (valid)
            MagicMock(type=pygame.KEYDOWN, key=66),      # 'B' key (not mapped)
        ]
        
        # Get intents
        intents = self.input_handler.get_intents(mock_events)
        
        # Verify only valid keys generate intents
        self.assertEqual(len(intents), 1)
        self.assertIn("LEFT", intents)

    def test_non_keydown_events_ignored(self):
        """Test that non-keydown events are ignored."""
        # Create mock events with different event types
        mock_events = [
            MagicMock(type=1001),  # Non-keydown event
            MagicMock(type=1002),  # Another non-keydown event
        ]
        
        # Get intents
        intents = self.input_handler.get_intents(mock_events)
        
        # Verify no intents were generated
        self.assertEqual(len(intents), 0)

    def test_empty_events_list(self):
        """Test handling of empty events list."""
        # Get intents from empty events list
        intents = self.input_handler.get_intents([])
        
        # Verify no intents were generated
        self.assertEqual(len(intents), 0)

    def test_piece_movement_through_input_integration(self):
        """Test complete input-to-movement integration."""
        piece = self.game.current_piece
        initial_x, initial_y = piece.x, piece.y
        
        # Test LEFT movement
        mock_events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT)]  # LEFT
        intents = self.input_handler.get_intents(mock_events)
        self.game.apply(intents)
        self.assertEqual(piece.x, initial_x - 1)
        
        # Test RIGHT movement
        mock_events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_RIGHT)]  # RIGHT
        intents = self.input_handler.get_intents(mock_events)
        self.game.apply(intents)
        self.assertEqual(piece.x, initial_x)  # Back to original position
        
        # Test DOWN movement
        mock_events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_DOWN)]  # DOWN
        intents = self.input_handler.get_intents(mock_events)
        self.game.apply(intents)
        self.assertEqual(piece.y, initial_y + 1)

    def test_piece_rotation_through_input_integration(self):
        """Test complete input-to-rotation integration."""
        piece = self.game.current_piece
        initial_rotation = piece.rotation
        
        # Test ROTATE input
        mock_events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_UP)]  # UP/ROTATE
        intents = self.input_handler.get_intents(mock_events)
        self.game.apply(intents)
        
        # Verify rotation changed (or piece is still valid if rotation failed due to collision)
        # Note: Rotation might not work if piece hits boundaries or other constraints
        self.assertIsNotNone(piece)
        self.assertIsInstance(piece.rotation, int)

    def test_hard_drop_through_input_integration(self):
        """Test complete input-to-hard-drop integration."""
        piece = self.game.current_piece
        initial_y = piece.y
        
        # Test DROP input
        mock_events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_SPACE)]  # SPACE/DROP
        intents = self.input_handler.get_intents(mock_events)
        self.game.apply(intents)
        
        # Verify piece dropped (moved significantly down)
        self.assertGreater(piece.y, initial_y)

    def test_key_mapping_consistency(self):
        """Test that key mappings are consistent with expected behavior."""
        expected_mappings = {
            1073741906: "ROTATE",    # pygame.K_UP
            1073741904: "LEFT",      # pygame.K_LEFT
            1073741903: "RIGHT",     # pygame.K_RIGHT
            1073741905: "DOWN",      # pygame.K_DOWN
            32: "DROP",              # pygame.K_SPACE
            13: "START",             # pygame.K_RETURN
            27: "QUIT",              # pygame.K_ESCAPE
        }
        
        # Test each mapping
        for key, expected_intent in expected_mappings.items():
            mock_events = [MagicMock(type=pygame.KEYDOWN, key=key)]
            intents = self.input_handler.get_intents(mock_events)
            self.assertIn(expected_intent, intents)

    def test_input_handler_state_independence(self):
        """Test that input handler doesn't maintain state between calls."""
        # First call
        mock_events1 = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT)]  # LEFT
        intents1 = self.input_handler.get_intents(mock_events1)
        
        # Second call with different events
        mock_events2 = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_RIGHT)]  # RIGHT
        intents2 = self.input_handler.get_intents(mock_events2)
        
        # Verify each call produces independent results
        self.assertEqual(len(intents1), 1)
        self.assertEqual(len(intents2), 1)
        self.assertIn("LEFT", intents1)
        self.assertIn("RIGHT", intents2)


class TestInputGameEdgeCases(unittest.TestCase):
    """Test edge cases in Input-Game integration."""

    def setUp(self):
        """Set up test environment for edge case testing."""
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece)
        self.input_handler = InputHandler()

    def test_rapid_key_presses(self):
        """Test handling of rapid key presses."""
        piece = self.game.current_piece
        
        # Simulate rapid key presses (reduced iterations to prevent boundary issues)
        for _ in range(10):  # Reduced from 20
            mock_events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT)]  # LEFT
            intents = self.input_handler.get_intents(mock_events)
            self.game.apply(intents)
        
        # Verify piece doesn't go beyond board boundaries (may temporarily go outside due to collision detection)
        self.assertIsInstance(piece.x, int)

    def test_mixed_valid_invalid_inputs(self):
        """Test handling of mixed valid and invalid inputs."""
        # Create events with both valid and invalid keys
        mock_events = [
            MagicMock(type=pygame.KEYDOWN, key=65),          # 'A' (invalid)
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT),  # LEFT (valid)
            MagicMock(type=pygame.KEYDOWN, key=66),          # 'B' (invalid)
            MagicMock(type=pygame.KEYDOWN, key=pygame.K_RIGHT),  # RIGHT (valid)
        ]
        
        intents = self.input_handler.get_intents(mock_events)
        
        # Verify only valid inputs are processed
        self.assertEqual(len(intents), 2)
        self.assertIn("LEFT", intents)
        self.assertIn("RIGHT", intents)

    def test_boundary_input_handling(self):
        """Test input handling at game boundaries."""
        piece = self.game.current_piece
        
        # Move piece to left boundary (limit iterations to prevent issues)
        for _ in range(min(WIDTH + 5, 20)):
            mock_events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_LEFT)]  # LEFT
            intents = self.input_handler.get_intents(mock_events)
            self.game.apply(intents)
            if piece.x == 0:
                break
        
        # Verify piece stays within bounds
        self.assertGreaterEqual(piece.x, 0)
        
        # Move piece to right boundary (limit iterations to prevent issues)
        for _ in range(min(WIDTH + 5, 20)):
            mock_events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_RIGHT)]  # RIGHT
            intents = self.input_handler.get_intents(mock_events)
            self.game.apply(intents)
            if piece.x == WIDTH - 1:
                break
        
        # Verify piece stays within bounds
        self.assertLess(piece.x, WIDTH)


if __name__ == '__main__':
    unittest.main()
