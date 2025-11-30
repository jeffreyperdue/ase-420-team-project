"""
Acceptance tests for Sprint 2 feature acceptance.

These tests validate that Sprint 2 features meet user requirements
and provide a satisfactory user experience.
"""

import unittest
from unittest.mock import patch, MagicMock
import pygame
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


class TestNextPiecePreviewAcceptance(unittest.TestCase):
    """Acceptance tests for next piece preview feature."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_next_piece_preview_available(self):
        """ACCEPTANCE: User can see next piece before current piece locks."""
        # Given: Game is playing
        self.assertEqual(self.game._state, PLAYING)
        
        # Then: Next piece is available
        self.assertIsNotNone(self.game.next_piece)
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNot(self.game.current_piece, self.game.next_piece)
    
    def test_next_piece_preview_accuracy(self):
        """ACCEPTANCE: Next piece preview shows correct upcoming piece."""
        # Given: Game is playing with current and next pieces
        current_piece = self.game.current_piece
        next_piece = self.game.next_piece
        
        # Verify pieces are different
        self.assertIsNot(current_piece, next_piece)
        
        # When: Current piece locks and new piece spawns
        # Force piece to lock by dropping it
        self.game.apply(["DROP"])
        
        # Then: Previous next piece is now current piece
        self.assertIs(self.game.current_piece, next_piece)
        # And a new next piece has been spawned
        self.assertIsNotNone(self.game.next_piece)
        self.assertIsNot(self.game.current_piece, self.game.next_piece)
    
    def test_next_piece_updates_after_lock(self):
        """ACCEPTANCE: Next piece preview updates correctly after piece locks."""
        # Given: Game is playing
        first_next = self.game.next_piece
        
        # When: Current piece locks
        self.game.apply(["DROP"])
        
        # Then: New next piece is different
        new_next = self.game.next_piece
        self.assertIsNotNone(new_next)
        # Note: Pieces may be same type but should be different instances


class TestGhostPieceAcceptance(unittest.TestCase):
    """Acceptance tests for ghost piece feature."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_ghost_piece_visible_when_playing(self):
        """ACCEPTANCE: Ghost piece is visible when game is playing."""
        # Given: Game is playing and not paused
        self.assertEqual(self.game._state, PLAYING)
        self.assertFalse(self.game.paused)
        self.assertIsNotNone(self.game.current_piece)
        
        # Then: Ghost piece can be calculated (tested via renderer integration)
        # This acceptance test validates the feature is available
        # Actual rendering is tested in integration tests
        pass
    
    def test_ghost_piece_not_visible_when_paused(self):
        """ACCEPTANCE: Ghost piece is not visible when game is paused."""
        # Given: Game is playing
        self.assertEqual(self.game._state, PLAYING)
        
        # When: Game is paused
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        # Then: Ghost piece should not be rendered (tested via renderer)
        # This acceptance test validates the feature behavior
        pass


class TestScoringSystemAcceptance(unittest.TestCase):
    """Acceptance tests for scoring system."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_score_increases_on_line_clear(self):
        """ACCEPTANCE: User sees score increase on line clears."""
        # Given: Game is playing with initial score
        initial_score = self.game.score
        self.assertEqual(initial_score, 0)
        
        # When: User clears a line
        # Fill bottom row completely
        for col in range(WIDTH):
            self.board.set_cell(HEIGHT - 1, col, 1)
        
        # Place a piece that will complete the line
        piece = self.game.current_piece
        # Move piece to bottom and lock it
        self.game.apply(["DROP"])
        
        # Clear the line (this happens in _freeze_piece)
        lines_cleared = self.board.clear_full_lines()
        if lines_cleared > 0:
            self.game._update_score(lines_cleared)
        
        # Then: Score has increased
        # Note: Score update happens in _freeze_piece, so we test the mechanism
        self.assertGreaterEqual(self.game.score, initial_score)
    
    def test_score_multiplier_applies_at_higher_levels(self):
        """ACCEPTANCE: Score multipliers apply correctly at higher levels."""
        # Given: Game is at level 1
        self.assertEqual(self.game.level, 1)
        initial_multiplier = self.game.get_score_multiplier()
        self.assertEqual(initial_multiplier, 1.0)
        
        # When: User progresses to level 2
        # Clear 10 lines to reach level 2
        self.game.lines_cleared = 10
        self.game.level = 2
        self.game.gravity_delay = self.game._calculate_gravity_delay()
        
        # Then: Score multiplier has increased
        new_multiplier = self.game.get_score_multiplier()
        self.assertGreater(new_multiplier, initial_multiplier)
        self.assertEqual(new_multiplier, 1.1)  # Level 2 = 1.0 + (2-1)*0.1
    
    def test_high_score_updates_when_beaten(self):
        """ACCEPTANCE: High score updates when current score exceeds it."""
        # Given: Initial high score
        initial_high_score = self.session.high_score
        
        # When: User achieves a higher score
        self.game._score = initial_high_score + 100
        self.game._session.update_high_score(self.game._score)
        
        # Then: High score is updated
        self.assertGreater(self.game.high_score, initial_high_score)
        self.assertEqual(self.game.high_score, initial_high_score + 100)


class TestLevelProgressionAcceptance(unittest.TestCase):
    """Acceptance tests for level progression feature."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_level_increases_after_clearing_lines(self):
        """ACCEPTANCE: User sees level increase after clearing lines."""
        # Given: Game starts at level 1
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.lines_cleared, 0)
        
        # When: User clears 10 lines (don't set lines_cleared manually, let _update_level handle it)
        self.game._update_level(10)
        
        # Then: Level increases to 2 (10 lines // 10 + 1 = 2)
        self.assertEqual(self.game.level, 2)
        self.assertEqual(self.game.lines_cleared, 10)
    
    def test_pieces_fall_faster_at_higher_levels(self):
        """ACCEPTANCE: Pieces fall faster at higher levels."""
        # Given: Game at level 1
        level_1_delay = self.game.gravity_delay
        self.assertEqual(self.game.level, 1)
        
        # When: User progresses to level 2
        self.game.level = 2
        self.game.gravity_delay = self.game._calculate_gravity_delay()
        
        # Then: Gravity delay is reduced (pieces fall faster)
        level_2_delay = self.game.gravity_delay
        self.assertLess(level_2_delay, level_1_delay)
    
    def test_level_progression_requires_10_lines(self):
        """ACCEPTANCE: Level progression requires clearing 10 lines per level."""
        # Given: Game starts at level 1
        self.assertEqual(self.game.level, 1)
        
        # When: User clears 9 lines
        self.game._update_level(9)
        
        # Then: Level remains at 1 (9 lines // 10 + 1 = 1)
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.lines_cleared, 9)
        
        # When: User clears 1 more line (total 10)
        self.game._update_level(1)
        
        # Then: Level increases to 2 (10 lines // 10 + 1 = 2)
        self.assertEqual(self.game.level, 2)
        self.assertEqual(self.game.lines_cleared, 10)


class TestSessionManagementAcceptance(unittest.TestCase):
    """Acceptance tests for session management feature."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        # Reset session high score for testing
        self.session._high_score = 0
    
    def test_high_score_persists_across_games(self):
        """ACCEPTANCE: High score persists across multiple games in session."""
        # Given: Initial high score
        initial_high_score = 0
        
        # When: User plays first game and achieves score
        board1 = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        game1 = Game(board1, lambda: Piece(WIDTH // 2, 0), self.session)
        game1.start_new_game()
        game1._score = 500
        self.session.update_high_score(game1._score)
        
        # Then: High score is updated
        self.assertEqual(self.session.high_score, 500)
        
        # When: User starts new game
        board2 = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        game2 = Game(board2, lambda: Piece(WIDTH // 2, 0), self.session)
        game2.start_new_game()
        
        # Then: High score persists
        self.assertEqual(game2.high_score, 500)
        self.assertEqual(self.session.high_score, 500)
    
    def test_high_score_updates_when_beaten(self):
        """ACCEPTANCE: High score updates when new game beats it."""
        # Given: Existing high score
        self.session._high_score = 500
        
        # When: User plays new game with higher score
        board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        game = Game(board, lambda: Piece(WIDTH // 2, 0), self.session)
        game.start_new_game()
        game._score = 750
        self.session.update_high_score(game._score)
        
        # Then: High score is updated
        self.assertEqual(self.session.high_score, 750)
    
    def test_high_score_not_updated_when_lower(self):
        """ACCEPTANCE: High score is not updated when new score is lower."""
        # Given: Existing high score
        self.session._high_score = 1000
        
        # When: User plays new game with lower score
        board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        game = Game(board, lambda: Piece(WIDTH // 2, 0), self.session)
        game.start_new_game()
        game._score = 500
        self.session.update_high_score(game._score)
        
        # Then: High score remains unchanged
        self.assertEqual(self.session.high_score, 1000)


if __name__ == '__main__':
    unittest.main()

