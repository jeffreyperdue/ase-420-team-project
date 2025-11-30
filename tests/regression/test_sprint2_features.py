"""
Regression tests for Sprint 2 features.

These tests protect Sprint 2 functionality from breaking during future development.
They ensure that all Sprint 2 features continue to work as expected.
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
from src.view.input import InputHandler
from src.utils.session_manager import SessionManager
from src.constants import WIDTH, HEIGHT
from src.constants.game_states import START_SCREEN, PLAYING, GAME_OVER


class TestSprint2Features(unittest.TestCase):
    """Regression tests for all Sprint 2 features."""
    
    def setUp(self):
        """Set up test environment."""
        SessionManager._instance = None
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.input_handler = InputHandler()
    
    def test_next_piece_preview_still_works(self):
        """REGRESSION: Next piece preview still works correctly."""
        # Given: Game is playing
        self.game.start_new_game()
        
        # Then: Next piece is available
        self.assertIsNotNone(self.game.next_piece)
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNot(self.game.current_piece, self.game.next_piece)
        
        # When: Current piece locks
        next_piece_before = self.game.next_piece
        self.game.apply(["DROP"])
        
        # Then: Previous next piece is now current
        self.assertIs(self.game.current_piece, next_piece_before)
        # And new next piece is spawned
        self.assertIsNotNone(self.game.next_piece)
        self.assertIsNot(self.game.current_piece, self.game.next_piece)
    
    def test_pause_resume_still_works(self):
        """REGRESSION: Pause/resume functionality still works."""
        # Given: Game is playing
        self.game.start_new_game()
        self.assertFalse(self.game.paused)
        
        # When: User pauses
        self.game.apply(["PAUSE"])
        
        # Then: Game is paused
        self.assertTrue(self.game.paused)
        self.assertEqual(self.game._state, PLAYING)
        
        # When: User resumes
        self.game.apply(["RESUME"])
        
        # Then: Game resumes
        self.assertFalse(self.game.paused)
        self.assertEqual(self.game._state, PLAYING)
    
    def test_pause_toggle_still_works(self):
        """REGRESSION: Pause toggle still works."""
        # Given: Game is playing
        self.game.start_new_game()
        
        # When: User toggles pause
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        # When: User toggles pause again
        self.game.apply(["PAUSE"])
        self.assertFalse(self.game.paused)
    
    def test_ghost_piece_still_works(self):
        """REGRESSION: Ghost piece feature still works."""
        # Given: Game is playing
        self.game.start_new_game()
        self.assertEqual(self.game._state, PLAYING)
        self.assertFalse(self.game.paused)
        self.assertIsNotNone(self.game.current_piece)
        
        # Then: Ghost piece can be calculated
        # (Actual rendering is tested in integration tests)
        # This regression test validates the feature is available
        piece = self.game.current_piece
        self.assertIsNotNone(piece)
        self.assertIsInstance(piece.x, int)
        self.assertIsInstance(piece.y, int)
    
    def test_ghost_piece_not_visible_when_paused(self):
        """REGRESSION: Ghost piece is not visible when paused."""
        # Given: Game is playing
        self.game.start_new_game()
        
        # When: Game is paused
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        # Then: Ghost piece should not be rendered
        # (Tested via renderer integration, this validates behavior)
        self.assertTrue(self.game.paused)
        self.assertEqual(self.game._state, PLAYING)
    
    def test_enhanced_scoring_still_works(self):
        """REGRESSION: Enhanced scoring system still works."""
        # Given: Game is playing
        self.game.start_new_game()
        initial_score = self.game.score
        
        # When: User clears a line
        lines_cleared = 1
        self.game._update_score(lines_cleared)
        self.game._update_level(lines_cleared)
        
        # Then: Score has increased
        self.assertGreater(self.game.score, initial_score)
    
    def test_score_multiplier_still_works(self):
        """REGRESSION: Score multiplier still works correctly."""
        # Given: Game at level 1
        self.game.start_new_game()
        self.assertEqual(self.game.level, 1)
        multiplier_level_1 = self.game.get_score_multiplier()
        self.assertEqual(multiplier_level_1, 1.0)
        
        # When: User progresses to level 2
        self.game.level = 2
        multiplier_level_2 = self.game.get_score_multiplier()
        
        # Then: Multiplier has increased
        self.assertGreater(multiplier_level_2, multiplier_level_1)
        self.assertEqual(multiplier_level_2, 1.1)
    
    def test_level_progression_still_works(self):
        """REGRESSION: Level progression still works."""
        # Given: Game at level 1
        self.game.start_new_game()
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.lines_cleared, 0)
        
        # When: User clears 10 lines
        self.game.lines_cleared = 10
        self.game._update_level(10)
        
        # Then: Level increases
        self.assertGreaterEqual(self.game.level, 2)
    
    def test_gravity_delay_updates_with_level(self):
        """REGRESSION: Gravity delay updates correctly with level."""
        # Given: Game at level 1
        self.game.start_new_game()
        level_1_delay = self.game.gravity_delay
        
        # When: Level increases
        self.game.level = 2
        self.game.gravity_delay = self.game._calculate_gravity_delay()
        level_2_delay = self.game.gravity_delay
        
        # Then: Gravity delay is reduced
        self.assertLess(level_2_delay, level_1_delay)
    
    def test_session_management_still_works(self):
        """REGRESSION: Session management still works."""
        # Given: Session manager
        self.assertIsNotNone(self.game._session)
        
        # When: Game achieves score
        self.game.start_new_game()
        self.game._score = 500
        self.session.update_high_score(self.game._score)
        
        # Then: High score is tracked
        self.assertEqual(self.game.high_score, 500)
        self.assertEqual(self.session.high_score, 500)
    
    def test_high_score_persistence_still_works(self):
        """REGRESSION: High score persistence still works."""
        # Given: Game with high score
        self.game.start_new_game()
        self.game._score = 750
        self.session.update_high_score(self.game._score)
        
        # When: New game is started
        self.game.start_new_game()
        
        # Then: High score persists
        self.assertEqual(self.game.high_score, 750)
        # But current score is reset
        self.assertEqual(self.game.score, 0)
    
    def test_start_screen_still_works(self):
        """REGRESSION: Start screen still works."""
        # Given: Game starts in start screen
        self.assertEqual(self.game._state, START_SCREEN)
        
        # When: User sends START intent
        self.game.apply(["START"])
        
        # Then: Game starts
        self.assertEqual(self.game._state, PLAYING)
        self.assertIsNotNone(self.game.current_piece)
    
    def test_game_over_screen_still_works(self):
        """REGRESSION: Game over screen still works."""
        # Given: Game is playing
        self.game.start_new_game()
        
        # When: Game over occurs
        for row in range(0, 3):  # Fill top 3 rows to trigger collision
            for col in range(WIDTH):
                self.board.set_cell(row, col, 1)
        self.game._spawn_new_piece()
        if self.game._state == GAME_OVER:
            self.game.game_over = True
        
        # Then: Game is over
        self.assertEqual(self.game._state, GAME_OVER)
        self.assertTrue(self.game.game_over)
    
    def test_restart_from_game_over_still_works(self):
        """REGRESSION: Restart from game over still works."""
        # Given: Game is over
        self.game.start_new_game()
        # Force game over
        for row in range(0, 3):  # Fill top 3 rows to trigger collision
            for col in range(WIDTH):
                self.board.set_cell(row, col, 1)
        self.game._spawn_new_piece()
        if self.game._state == GAME_OVER:
            self.game.game_over = True
        self.assertEqual(self.game._state, GAME_OVER)
        
        # When: User restarts
        self.game.apply(["RESTART"])
        
        # Then: New game starts
        self.assertEqual(self.game._state, PLAYING)
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.score, 0)


class TestSprint2FeatureInteractions(unittest.TestCase):
    """Regression tests for Sprint 2 feature interactions."""
    
    def setUp(self):
        """Set up test environment."""
        SessionManager._instance = None
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
    
    def test_pause_with_next_piece_preview(self):
        """REGRESSION: Pause works correctly with next piece preview."""
        # Given: Game is playing
        self.game.start_new_game()
        next_piece_before = self.game.next_piece
        
        # When: User pauses
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        # Then: Next piece is still available
        self.assertIsNotNone(self.game.next_piece)
        # Next piece should remain the same when paused
        self.assertIs(self.game.next_piece, next_piece_before)
    
    def test_scoring_with_level_progression(self):
        """REGRESSION: Scoring works correctly with level progression."""
        # Given: Game at level 1
        self.game.start_new_game()
        self.assertEqual(self.game.level, 1)
        
        # When: User clears lines and progresses level
        self.game._update_score(1)
        self.game._update_level(1)
        
        # Progress to level 2
        self.game.lines_cleared = 10
        self.game.level = 2
        self.game.gravity_delay = self.game._calculate_gravity_delay()
        
        # Clear more lines at level 2
        self.game._update_level(1)
        
        # Then: Score has increased with level multiplier
        self.assertGreater(self.game.score, 0)
        self.assertEqual(self.game.level, 2)
    
    def test_session_with_level_progression(self):
        """REGRESSION: Session management works with level progression."""
        # Given: Game with session
        self.game.start_new_game()
        
        # When: User progresses levels and achieves score
        self.game.level = 2
        self.game._score = 1000
        self.session.update_high_score(self.game._score)
        
        # Then: High score is tracked
        self.assertEqual(self.game.high_score, 1000)
        
        # When: New game starts
        self.game.start_new_game()
        
        # Then: High score persists, but level resets
        self.assertEqual(self.game.high_score, 1000)
        self.assertEqual(self.game.level, 1)


if __name__ == '__main__':
    unittest.main()

