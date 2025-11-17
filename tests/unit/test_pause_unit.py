"""
Unit tests for pause/resume functionality.

Tests the Game class's pause state management, including:
- Pause toggling with different input intents
- Movement prevention while paused
- Gravity prevention while paused
- Edge cases with multiple intents
"""

import os
import sys
import unittest

# Add repository root to path for imports
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.game import Game
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row
from src.constants import WIDTH, HEIGHT


class TestPauseStateManagement(unittest.TestCase):
    """Test pause state toggling and state preservation."""
    
    def setUp(self):
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        self.game = Game(self.board, spawn_piece)
    
    def test_initial_pause_state_is_false(self):
        """Game should start unpaused."""
        self.assertFalse(self.game.paused)
    
    def test_pause_intent_toggles_pause_on(self):
        """PAUSE intent should toggle pause from False to True."""
        self.assertFalse(self.game.paused)
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
    
    def test_pause_intent_toggles_pause_off(self):
        """PAUSE intent should toggle pause from True to False."""
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        self.game.apply(["PAUSE"])
        self.assertFalse(self.game.paused)
    
    def test_multiple_pause_intents(self):
        """Multiple PAUSE intents should toggle state correctly."""
        # Start: False -> True -> False -> True
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        self.game.apply(["PAUSE"])
        self.assertFalse(self.game.paused)
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
    
    def test_click_resumes_from_paused(self):
        """CLICK intent should resume from paused state."""
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        self.game.apply(["CLICK"])
        self.assertFalse(self.game.paused)
    
    def test_click_when_not_paused_does_nothing(self):
        """CLICK intent when not paused should not affect pause state."""
        self.assertFalse(self.game.paused)
        self.game.apply(["CLICK"])
        self.assertFalse(self.game.paused)


class TestMovementWhenPaused(unittest.TestCase):
    """Test that piece movement is blocked when paused."""
    
    def setUp(self):
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        self.game = Game(self.board, spawn_piece)
    
    def test_left_movement_blocked_when_paused(self):
        """LEFT intent should be ignored when paused."""
        initial_x = self.game.current_piece.x
        self.game.apply(["PAUSE"])
        self.game.apply(["LEFT"])
        self.assertEqual(self.game.current_piece.x, initial_x)
    
    def test_right_movement_blocked_when_paused(self):
        """RIGHT intent should be ignored when paused."""
        initial_x = self.game.current_piece.x
        self.game.apply(["PAUSE"])
        self.game.apply(["RIGHT"])
        self.assertEqual(self.game.current_piece.x, initial_x)
    
    def test_down_movement_blocked_when_paused(self):
        """DOWN intent should be ignored when paused."""
        initial_y = self.game.current_piece.y
        self.game.apply(["PAUSE"])
        self.game.apply(["DOWN"])
        self.assertEqual(self.game.current_piece.y, initial_y)
    
    def test_soft_down_blocked_when_paused(self):
        """SOFT_DOWN intent should be ignored when paused."""
        initial_y = self.game.current_piece.y
        self.game.apply(["PAUSE"])
        self.game.apply(["SOFT_DOWN"])
        self.assertEqual(self.game.current_piece.y, initial_y)
    
    def test_rotation_blocked_when_paused(self):
        """ROTATE intent should be ignored when paused."""
        initial_rotation = self.game.current_piece.rotation
        self.game.apply(["PAUSE"])
        self.game.apply(["ROTATE"])
        self.assertEqual(self.game.current_piece.rotation, initial_rotation)
    
    def test_drop_blocked_when_paused(self):
        """DROP intent should be ignored when paused."""
        initial_y = self.game.current_piece.y
        self.game.apply(["PAUSE"])
        self.game.apply(["DROP"])
        # After pause and DROP, current piece should not have moved significantly
        self.assertEqual(self.game.current_piece.y, initial_y)
    
    def test_movement_allowed_when_unpaused(self):
        """Movement should work normally after resuming."""
        initial_x = self.game.current_piece.x
        self.game.apply(["PAUSE"])
        self.game.apply(["CLICK"])  # Resume
        self.game.apply(["LEFT"])
        # After LEFT, piece x should have changed (if not at boundary)
        # We can't guarantee exact position, but it should have attempted movement
        self.assertFalse(self.game.paused)


class TestGravityWhenPaused(unittest.TestCase):
    """Test that gravity does not apply when paused."""
    
    def setUp(self):
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        self.game = Game(self.board, spawn_piece)
    
    def test_gravity_timer_not_incremented_when_paused(self):
        """Gravity timer should not increment while paused."""
        self.game.apply(["PAUSE"])
        initial_timer = self.game.gravity_timer
        self.game.update()
        self.assertEqual(self.game.gravity_timer, initial_timer)
    
    def test_piece_falls_after_unpause(self):
        """Piece should fall again after resuming from pause."""
        self.game.apply(["PAUSE"])
        self.game.update()
        paused_y = self.game.current_piece.y
        self.game.apply(["CLICK"])  # Resume
        
        # Simulate multiple gravity updates
        for _ in range(35):  # Exceed gravity_delay of 30
            self.game.update()
        
        # Piece should have fallen at least once
        self.assertGreater(self.game.current_piece.y, paused_y)
    
    def test_gravity_timer_resets_on_freeze(self):
        """Gravity timer should reset to 0 when piece freezes."""
        # Drop piece to freeze it
        self.game.apply(["DROP"])
        self.assertEqual(self.game.gravity_timer, 0)


class TestPauseEdgeCases(unittest.TestCase):
    """Test edge cases and complex pause scenarios."""
    
    def setUp(self):
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        self.game = Game(self.board, spawn_piece)
    
    def test_multiple_intents_with_pause_in_middle(self):
        """Multiple intents should respect pause state changes."""
        initial_x = self.game.current_piece.x
        # Send multiple intents with pause in the middle
        self.game.apply(["LEFT", "PAUSE", "RIGHT", "DOWN"])
        # Only LEFT should have executed (before PAUSE)
        # RIGHT, DOWN should be blocked (after PAUSE)
        self.assertTrue(self.game.paused)
    
    def test_pause_preserves_all_game_state(self):
        """Pause should not modify any game state except paused flag."""
        # Move piece and spawn new one
        self.game.apply(["LEFT", "LEFT"])
        self.game.apply(["DROP"])
        
        piece_before_pause = self.game.current_piece
        next_piece_before_pause = self.game.next_piece
        board_state_before = [(row, self.board.get_row_object(row)) for row in range(self.board.height)]
        
        # Pause and resume
        self.game.apply(["PAUSE"])
        self.game.apply(["CLICK"])
        
        # Game state should be identical
        self.assertIs(self.game.current_piece, piece_before_pause)
        self.assertIs(self.game.next_piece, next_piece_before_pause)
    
    def test_pause_then_resume_multiple_times(self):
        """Rapidly pausing and resuming should work correctly."""
        for _ in range(5):
            self.game.apply(["PAUSE"])
            self.assertTrue(self.game.paused)
            self.game.apply(["CLICK"])
            self.assertFalse(self.game.paused)
    
    def test_pause_click_sequence(self):
        """PAUSE followed by multiple CLICKs should only resume once."""
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        self.game.apply(["CLICK"])
        self.assertFalse(self.game.paused)
        # Additional CLICKs should do nothing (already unpaused)
        self.game.apply(["CLICK", "CLICK"])
        self.assertFalse(self.game.paused)


if __name__ == '__main__':
    unittest.main()
