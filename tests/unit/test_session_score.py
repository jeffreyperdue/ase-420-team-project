"""Unit tests for session-level high score tracking."""
import os
import sys
import unittest

# Ensure repo root in path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.utils.session_manager import SessionManager
from src.game.game import Game
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row
from src.constants import WIDTH, HEIGHT


def simple_spawn():
    """Helper to spawn pieces in predictable positions."""
    return Piece(3, 0)


class TestSessionScore(unittest.TestCase):
    def setUp(self):
        """Create a clean set of components for each test."""
        self.session = SessionManager()  # Get singleton instance
        self.session._high_score = 0  # Reset high score for clean test state
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        self.game = Game(self.board, simple_spawn, self.session)

    def test_session_manager_singleton(self):
        """Test SessionManager maintains single state across instances."""
        # Create multiple instances - should all be same object
        manager1 = SessionManager()
        manager2 = SessionManager()
        self.assertIs(manager1, manager2, "SessionManager instances should be identical")
        
        # Update through one instance, check in other
        manager1._high_score = 1000
        self.assertEqual(manager2.high_score, 1000,
                       "High score changes should be visible to all instances")

    def test_high_score_persistence(self):
        """Test high score persists when starting new games."""
        # Play first game
        self.game._update_score(4)  # 800 points
        self.session.update_high_score(self.game.score)  # Update high score
        self.assertEqual(self.game.score, 800)
        self.assertEqual(self.session.high_score, 800)
        
        # Start new game - score resets, high score remains
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        self.game = Game(self.board, simple_spawn, self.session)
        self.assertEqual(self.game.score, 0, "New game should start at 0")
        self.assertEqual(self.session.high_score, 800,
                       "High score should persist across games")

    def test_high_score_updates_only_when_exceeded(self):
        """Test high score only updates when current score is higher."""
        # First game sets initial high score
        self.game._update_score(4)  # 800 points
        self.session.update_high_score(self.game.score)  # Update high score
        self.assertEqual(self.session.high_score, 800)
        
        # Start new game
        self.board = Board(lambda: Row(WIDTH))
        self.game = Game(self.board, simple_spawn, self.session)
        
        # Lower scores shouldn't affect high score
        self.game._update_score(1)  # 100 points
        self.assertEqual(self.session.high_score, 800,
                       "High score shouldn't decrease")
        
        # Higher scores should update it
        self.game._update_score(4)  # +800 = 900 total
        self.session.update_high_score(self.game.score)  # Update high score
        self.assertEqual(self.session.high_score, 900,
                       "High score should update when exceeded")

    def test_high_score_game_over_interaction(self):
        """Test game over doesn't affect high score tracking."""
        # Get some points then end game
        self.game._update_score(4)  # 800 points
        self.session.update_high_score(self.game.score)  # Update high score
        self.game.game_over = True
        
        # High score should be set
        self.assertEqual(self.session.high_score, 800)
        
        # New game should still see that high score
        self.board = Board(lambda: Row(WIDTH))
        self.game = Game(self.board, simple_spawn, self.session)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.session.high_score, 800)

    def test_high_score_multiple_games(self):
        """Test high score tracking across multiple game sessions."""
        # Game 1: Score 800
        self.game._update_score(4)
        self.session.update_high_score(self.game.score)  # Update high score
        self.assertEqual(self.session.high_score, 800)
        
        # Game 2: Score 300 (shouldn't affect high score)
        self.board = Board(lambda: Row(WIDTH))
        self.game = Game(self.board, simple_spawn, self.session)
        self.game._update_score(2)  # 300 points
        self.assertEqual(self.session.high_score, 800)
        
        # Game 3: Score 1000 (should become new high score)
        self.board = Board(lambda: Row(WIDTH))
        self.game = Game(self.board, simple_spawn, self.session)
        self.game._update_score(4)  # 800 points
        self.game._update_score(2)  # +300 = 1100 total
        self.session.update_high_score(self.game.score)  # Update high score
        self.assertEqual(self.session.high_score, 1100)
        
        # Game 4: Game over shouldn't reset high score
        self.board = Board(lambda: Row(WIDTH))
        self.game = Game(self.board, simple_spawn, self.session)
        self.game.game_over = True
        self.assertEqual(self.session.high_score, 1100)

    def test_session_manager_edge_cases(self):
        """Test edge cases in session manager behavior."""
        # High score should never go negative
        self.session._high_score = -100  # Try to break it
        self.session.update_high_score(0)  # Should fix to 0
        self.assertEqual(self.session.high_score, 0,
                       "High score should never be negative")
        
        # Very large scores should work
        huge_score = 1_000_000
        self.session.update_high_score(huge_score)
        self.assertEqual(self.session.high_score, huge_score,
                       "Should handle very large scores")
        
        # Zero is a valid score
        self.session.update_high_score(0)
        self.assertEqual(self.session.high_score, huge_score,
                       "Zero score shouldn't affect higher high score")


if __name__ == '__main__':
    unittest.main()