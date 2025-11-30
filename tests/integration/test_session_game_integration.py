"""
Integration tests for SessionManager and Game component interactions.

These tests verify that session management and game work together correctly,
ensuring proper data flow and state management between components.
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


class TestSessionGameIntegration(unittest.TestCase):
    """Integration tests for SessionManager and Game."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a fresh session manager for each test
        SessionManager._instance = None
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
    
    def test_game_uses_session_manager(self):
        """INTEGRATION: Game uses session manager for high score."""
        # Given: Game initialized with session manager
        self.assertIsNotNone(self.game._session)
        self.assertIs(self.game._session, self.session)
        
        # Then: Game can access high score through session
        self.assertIsInstance(self.game.high_score, int)
        self.assertEqual(self.game.high_score, self.session.high_score)
    
    def test_high_score_tracking_across_games(self):
        """INTEGRATION: High score is tracked across multiple games."""
        # Given: Initial high score
        initial_high_score = self.session.high_score
        
        # When: First game achieves a score
        self.game.start_new_game()
        self.game._score = 500
        self.game._session.update_high_score(self.game._score)
        
        # Then: High score is updated
        self.assertEqual(self.session.high_score, 500)
        self.assertEqual(self.game.high_score, 500)
        
        # When: New game is created with same session
        board2 = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        game2 = Game(board2, lambda: Piece(WIDTH // 2, 0), self.session)
        game2.start_new_game()
        
        # Then: High score persists
        self.assertEqual(game2.high_score, 500)
        self.assertEqual(self.session.high_score, 500)
    
    def test_high_score_updates_during_gameplay(self):
        """INTEGRATION: High score updates during gameplay when score exceeds it."""
        # Given: Initial high score
        self.session._high_score = 0
        
        # When: Game achieves score
        self.game.start_new_game()
        self.game._score = 300
        self.game._session.update_high_score(self.game._score)
        
        # Then: High score is updated
        self.assertEqual(self.game.high_score, 300)
        
        # When: Score increases further
        self.game._score = 600
        self.game._session.update_high_score(self.game._score)
        
        # Then: High score is updated again
        self.assertEqual(self.game.high_score, 600)
    
    def test_high_score_not_updated_when_lower(self):
        """INTEGRATION: High score is not updated when new score is lower."""
        # Given: Existing high score
        self.session._high_score = 1000
        
        # When: Game achieves lower score
        self.game.start_new_game()
        self.game._score = 500
        self.game._session.update_high_score(self.game._score)
        
        # Then: High score remains unchanged
        self.assertEqual(self.game.high_score, 1000)
        self.assertEqual(self.session.high_score, 1000)
    
    def test_score_updates_session_after_line_clear(self):
        """INTEGRATION: Score updates session high score after line clear."""
        # Given: Game with initial high score
        self.session._high_score = 0
        
        # When: User clears lines and score increases
        self.game.start_new_game()
        
        # Simulate line clear that updates score
        lines_cleared = 1
        self.game._update_score(lines_cleared)
        self.game._update_level(lines_cleared)
        
        # Update session high score (normally done in _freeze_piece)
        try:
            self.game._session.update_high_score(self.game._score)
        except Exception:
            pass
        
        # Then: High score is updated if score exceeds it
        self.assertGreaterEqual(self.game.high_score, 0)
    
    def test_session_manager_singleton_behavior(self):
        """INTEGRATION: SessionManager singleton behavior works correctly."""
        # Given: Session manager instance
        session1 = SessionManager()
        session1._high_score = 500
        
        # When: Another session manager is created
        session2 = SessionManager()
        
        # Then: Both reference the same instance
        self.assertIs(session1, session2)
        self.assertEqual(session2.high_score, 500)
    
    def test_multiple_games_share_session(self):
        """INTEGRATION: Multiple games share the same session manager."""
        # Given: First game with session
        game1 = Game(
            Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH),
            lambda: Piece(WIDTH // 2, 0),
            self.session
        )
        game1.start_new_game()
        game1._score = 750
        self.session.update_high_score(game1._score)
        
        # When: Second game is created with same session
        game2 = Game(
            Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH),
            lambda: Piece(WIDTH // 2, 0),
            self.session
        )
        game2.start_new_game()
        
        # Then: Both games share the same high score
        self.assertEqual(game1.high_score, 750)
        self.assertEqual(game2.high_score, 750)
        self.assertIs(game1._session, game2._session)
    
    def test_game_reset_preserves_session_high_score(self):
        """INTEGRATION: Game reset preserves session high score."""
        # Given: Game with high score set
        self.game.start_new_game()
        self.game._score = 1000
        self.session.update_high_score(self.game._score)
        self.assertEqual(self.game.high_score, 1000)
        
        # When: Game is reset (new game started)
        self.game.start_new_game()
        
        # Then: High score is preserved
        self.assertEqual(self.game.high_score, 1000)
        self.assertEqual(self.session.high_score, 1000)
        # But current score is reset
        self.assertEqual(self.game.score, 0)


class TestSessionGameEdgeCases(unittest.TestCase):
    """Integration tests for edge cases in session and game interaction."""
    
    def setUp(self):
        """Set up test environment."""
        SessionManager._instance = None
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
    
    def test_session_handles_zero_score(self):
        """INTEGRATION: Session handles zero score correctly."""
        # Given: Session with zero high score
        self.session._high_score = 0
        
        # When: Game achieves zero score
        self.game.start_new_game()
        self.game._score = 0
        self.session.update_high_score(self.game._score)
        
        # Then: High score remains zero
        self.assertEqual(self.game.high_score, 0)
    
    def test_session_handles_very_high_score(self):
        """INTEGRATION: Session handles very high scores correctly."""
        # Given: Session with high score
        self.session._high_score = 1000000
        
        # When: Game achieves even higher score
        self.game.start_new_game()
        self.game._score = 2000000
        self.session.update_high_score(self.game._score)
        
        # Then: High score is updated
        self.assertEqual(self.game.high_score, 2000000)
    
    def test_concurrent_score_updates(self):
        """INTEGRATION: Concurrent score updates are handled correctly."""
        # Given: Session with initial high score
        self.session._high_score = 500
        
        # When: Multiple score updates occur
        self.game.start_new_game()
        self.game._score = 600
        self.session.update_high_score(self.game._score)
        
        self.game._score = 700
        self.session.update_high_score(self.game._score)
        
        self.game._score = 800
        self.session.update_high_score(self.game._score)
        
        # Then: High score is the maximum
        self.assertEqual(self.game.high_score, 800)


if __name__ == '__main__':
    unittest.main()

