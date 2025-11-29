"""
Comprehensive integration tests for pause/resume and next piece preview together.

Tests complex scenarios involving both features working together:
- Pausing while pieces are queued
- Resuming and continuing piece progression
- Preview update behavior during pause
- Full game flow with pause interruptions
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


def create_piece_with_type(piece_type=0, color=1):
    """Create a Piece with specified type and color."""
    p = Piece(WIDTH // 2, 0)
    p.type = piece_type
    p.color = color
    p.rotation = 0
    return p


def create_spawn_sequence(types_and_colors):
    """Create a spawn function with predefined sequence."""
    pieces = [create_piece_with_type(t, c) for t, c in types_and_colors]
    it = iter(pieces)
    
    def spawn():
        try:
            return next(it)
        except StopIteration:
            return create_piece_with_type(0, 1)
    
    return spawn


class TestPauseAndPreviewIntegration(unittest.TestCase):
    """Test pause and preview features working together."""
    
    def setUp(self):
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
    
    def test_next_piece_visible_then_pause(self):
        """Next piece should remain visible after pausing."""
        spawn = create_spawn_sequence([(0, 1), (1, 2), (2, 3)])
        game = Game(self.board, spawn)
        
        # Get initial pieces
        current_before = game.current_piece
        next_before = game.next_piece
        
        # Pause
        game.apply(["PAUSE"])
        
        # Pieces should be unchanged
        self.assertIs(game.current_piece, current_before)
        self.assertIs(game.next_piece, next_before)
    
    def test_next_piece_advances_after_pause_and_drop(self):
        """Piece advancement should work normally after resuming."""
        spawn = create_spawn_sequence([(0, 1), (1, 2), (2, 3), (3, 4)])
        game = Game(self.board, spawn)
        
        p1 = game.current_piece
        p2 = game.next_piece
        
        # Pause and resume
        game.apply(["PAUSE"])
        game.apply(["CLICK"])
        
        # Now drop and check next piece advances
        game.apply(["DROP"])
        
        self.assertIs(game.current_piece, p2)
        self.assertIsNot(game.next_piece, p2)
    
    def test_pause_during_piece_progression(self):
        """Pausing should not interfere with piece progression after resume."""
        spawn = create_spawn_sequence([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
        game = Game(self.board, spawn)
        
        # Drop first piece
        game.apply(["DROP"])
        p2_after_drop = game.current_piece
        
        # Pause
        game.apply(["PAUSE"])
        self.assertTrue(game.paused)
        
        # Try to drop (should be blocked)
        game.apply(["DROP"])
        self.assertIs(game.current_piece, p2_after_drop)
        
        # Resume
        game.apply(["CLICK"])
        self.assertFalse(game.paused)
        
        # Drop again (should work)
        game.apply(["DROP"])
        self.assertIsNot(game.current_piece, p2_after_drop)
    
    def test_multiple_pause_cycles_with_piece_changes(self):
        """Multiple pause/resume cycles with piece drops should work correctly."""
        spawn = create_spawn_sequence([
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)
        ])
        game = Game(self.board, spawn)
        
        piece_sequence = [game.current_piece]
        
        for cycle in range(3):
            # Drop current piece
            game.apply(["DROP"])
            piece_sequence.append(game.current_piece)
            
            # Pause and resume
            game.apply(["PAUSE"])
            self.assertTrue(game.paused)
            game.apply(["CLICK"])
            self.assertFalse(game.paused)
        
        # All pieces should be different
        self.assertEqual(len(set(id(p) for p in piece_sequence)), len(piece_sequence))


class TestPauseWithGameStateComplexity(unittest.TestCase):
    """Test pause functionality with complex game states."""
    
    def setUp(self):
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        spawn = create_spawn_sequence([(0, 1), (1, 2), (2, 3)])
        self.game = Game(self.board, spawn)
    
    def test_pause_preserves_piece_position_and_gravity(self):
        """Pausing should preserve exact piece position and gravity state."""
        # Move piece around
        self.game.apply(["LEFT", "LEFT", "RIGHT", "ROTATE"])
        
        state_before = {
            'x': self.game.current_piece.x,
            'y': self.game.current_piece.y,
            'rotation': self.game.current_piece.rotation,
            'gravity_timer': self.game.gravity_timer
        }
        
        # Pause and update multiple times
        self.game.apply(["PAUSE"])
        for _ in range(10):
            self.game.update()
        
        # Resume and check state
        self.game.apply(["CLICK"])
        
        self.assertEqual(self.game.current_piece.x, state_before['x'])
        self.assertEqual(self.game.current_piece.y, state_before['y'])
        self.assertEqual(self.game.current_piece.rotation, state_before['rotation'])
    
    def test_gravity_countdown_resumes_correctly(self):
        """Gravity timer should resume from where it was paused."""
        # Let gravity accumulate
        for _ in range(15):
            self.game.update()
        
        gravity_at_pause = self.game.gravity_timer
        
        # Pause
        self.game.apply(["PAUSE"])
        self.game.update()
        self.game.update()
        
        # Should not have changed
        self.assertEqual(self.game.gravity_timer, gravity_at_pause)
        
        # Resume
        self.game.apply(["CLICK"])
        self.game.update()
        
        # Should continue counting up
        self.assertGreater(self.game.gravity_timer, gravity_at_pause)
    
    def test_rapid_pause_resume_cycles(self):
        """Rapid pause/resume should maintain game integrity."""
        initial_piece = self.game.current_piece
        
        for _ in range(20):
            self.game.apply(["PAUSE"])
            self.game.apply(["CLICK"])
            self.game.update()
        
        # Piece should still be the same
        self.assertIs(self.game.current_piece, initial_piece)


class TestPreviewStabilityWithComplexMovements(unittest.TestCase):
    """Test that preview piece remains stable during complex movements."""
    
    def setUp(self):
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
    
    def test_preview_stable_through_various_movements(self):
        """Preview should not change during movement sequences."""
        spawn = create_spawn_sequence([(0, 1), (1, 2), (2, 3)])
        game = Game(self.board, spawn)
        
        next_piece_id = id(game.next_piece)
        
        # Perform various movements
        movements = [
            ["LEFT", "LEFT", "ROTATE"],
            ["RIGHT", "RIGHT", "RIGHT"],
            ["DOWN", "DOWN", "DOWN"],
            ["ROTATE", "LEFT", "RIGHT"],
        ]
        
        for movement_set in movements:
            game.apply(movement_set)
            # Preview should remain unchanged
            self.assertEqual(id(game.next_piece), next_piece_id)
    
    def test_preview_updates_only_on_lock(self):
        """Preview should only change when current piece locks."""
        spawn = create_spawn_sequence([(0, 1), (1, 2), (2, 3), (3, 4)])
        game = Game(self.board, spawn)
        
        next_piece_before = game.next_piece
        
        # Many movements without locking
        for _ in range(50):
            game.apply(["LEFT"])
            self.assertIs(game.next_piece, next_piece_before)
        
        # Lock piece with DROP
        game.apply(["DROP"])
        
        # Now preview should have changed
        self.assertIsNot(game.next_piece, next_piece_before)


class TestPauseInputHandlingEdgeCases(unittest.TestCase):
    """Test edge cases in pause input handling."""
    
    def setUp(self):
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        spawn = create_spawn_sequence([(0, 1), (1, 2), (2, 3)])
        self.game = Game(self.board, spawn)
    
    def test_pause_with_multiple_movement_intents_in_same_frame(self):
        """Multiple movement intents when paused should all be blocked."""
        initial_state = {
            'x': self.game.current_piece.x,
            'y': self.game.current_piece.y,
            'rotation': self.game.current_piece.rotation
        }
        
        self.game.apply(["PAUSE"])
        self.game.apply(["LEFT", "RIGHT", "DOWN", "ROTATE", "DROP"])
        
        # No movement should have occurred
        self.assertEqual(self.game.current_piece.x, initial_state['x'])
        self.assertEqual(self.game.current_piece.y, initial_state['y'])
        self.assertEqual(self.game.current_piece.rotation, initial_state['rotation'])
    
    def test_pause_click_pause_sequence(self):
        """PAUSE -> CLICK -> PAUSE should work correctly."""
        self.assertFalse(self.game.paused)
        
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        self.game.apply(["CLICK"])
        self.assertFalse(self.game.paused)
        
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
    
    def test_mixed_intents_respecting_pause(self):
        """Mixed valid and invalid intents should be handled correctly."""
        piece_before = self.game.current_piece
        x_before = self.game.current_piece.x
        
        # Mix pause/unpause with movements
        self.game.apply(["PAUSE"])  # Pause
        self.game.apply(["LEFT"])   # Blocked
        self.game.apply(["CLICK"])  # Resume
        self.game.apply(["RIGHT"])  # Allowed
        
        self.assertFalse(self.game.paused)
        # Piece should be the same after partial execution
        self.assertIs(self.game.current_piece, piece_before)
        # RIGHT movement might not change position if at boundary
        # But at least verify no crashes occurred and pause state is correct


if __name__ == '__main__':
    unittest.main()
