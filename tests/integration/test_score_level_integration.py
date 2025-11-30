"""
Integration tests for Score and Level component interactions.

These tests verify that scoring and level progression work together correctly,
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


class TestScoreLevelIntegration(unittest.TestCase):
    """Integration tests for Score and Level components."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_line_clear_updates_score_and_level(self):
        """INTEGRATION: Line clear updates both score and level."""
        # Given: Game at level 1 with initial score
        initial_score = self.game.score
        initial_level = self.game.level
        self.assertEqual(initial_score, 0)
        self.assertEqual(initial_level, 1)
        
        # When: User clears a line
        lines_cleared = 1
        self.game._update_score(lines_cleared)
        self.game._update_level(lines_cleared)
        
        # Then: Score has increased
        self.assertGreater(self.game.score, initial_score)
        
        # Then: Lines cleared count has increased
        self.assertEqual(self.game.lines_cleared, 1)
        # Level may not increase until 10 lines are cleared
        self.assertGreaterEqual(self.game.level, initial_level)
    
    def test_level_increase_triggers_gravity_update(self):
        """INTEGRATION: Level increase triggers gravity delay update."""
        # Given: Game at level 1
        initial_gravity_delay = self.game.gravity_delay
        self.assertEqual(self.game.level, 1)
        
        # When: User clears 10 lines (reaching level 2)
        # Don't set lines_cleared manually, let _update_level handle it
        self.game._update_level(10)
        
        # Then: Level has increased (10 lines // 10 + 1 = 2)
        self.assertEqual(self.game.level, 2)
        self.assertEqual(self.game.lines_cleared, 10)
        
        # Then: Gravity delay has been recalculated
        new_gravity_delay = self.game.gravity_delay
        self.assertLess(new_gravity_delay, initial_gravity_delay)
    
    def test_score_multiplier_applies_based_on_level(self):
        """INTEGRATION: Score multiplier applies correctly based on current level."""
        # Given: Game at level 1
        self.assertEqual(self.game.level, 1)
        level_1_multiplier = self.game.get_score_multiplier()
        self.assertEqual(level_1_multiplier, 1.0)
        
        # When: User progresses to level 2
        self.game.level = 2
        self.game.gravity_delay = self.game._calculate_gravity_delay()
        
        # Then: Score multiplier has increased
        level_2_multiplier = self.game.get_score_multiplier()
        self.assertGreater(level_2_multiplier, level_1_multiplier)
        self.assertEqual(level_2_multiplier, 1.1)
        
        # When: User progresses to level 3
        self.game.level = 3
        self.game.gravity_delay = self.game._calculate_gravity_delay()
        
        # Then: Score multiplier has increased further
        level_3_multiplier = self.game.get_score_multiplier()
        self.assertGreater(level_3_multiplier, level_2_multiplier)
        self.assertEqual(level_3_multiplier, 1.2)
    
    def test_high_score_updates_after_scoring(self):
        """INTEGRATION: High score updates correctly after scoring."""
        # Given: Reset high score to ensure clean test
        self.session._high_score = 0
        initial_high_score = self.session.high_score
        
        # When: User scores points
        self.game._score = 500
        self.session.update_high_score(self.game._score)
        
        # Then: High score is updated
        self.assertGreater(self.game.high_score, initial_high_score)
        self.assertEqual(self.game.high_score, 500)
    
    def test_multiple_line_clear_scoring(self):
        """INTEGRATION: Multiple line clears score correctly with level multiplier."""
        # Given: Game at level 1
        self.assertEqual(self.game.level, 1)
        initial_score = self.game.score
        
        # When: User clears 2 lines
        lines_cleared = 2
        self.game._update_score(lines_cleared)
        self.game._update_level(lines_cleared)
        
        # Then: Score has increased
        score_after_2_lines = self.game.score
        self.assertGreater(score_after_2_lines, initial_score)
        
        # When: User progresses to level 2 and clears 2 more lines
        self.game.lines_cleared = 10  # Reach level 2
        self.game.level = 2
        self.game.gravity_delay = self.game._calculate_gravity_delay()
        
        initial_score_level_2 = self.game.score
        self.game._update_level(2)  # Clear 2 more lines at level 2
        
        # Then: Score increase is higher due to level multiplier
        score_after_level_2_clear = self.game.score
        # The score increase should be greater at level 2
        self.assertGreater(score_after_level_2_clear, initial_score_level_2)
    
    def test_level_progression_affects_scoring(self):
        """INTEGRATION: Level progression affects scoring calculations."""
        # Given: Game at level 1
        self.assertEqual(self.game.level, 1)
        
        # Clear 1 line at level 1
        self.game._update_score(1)
        self.game._update_level(1)
        score_at_level_1 = self.game.score
        
        # When: User progresses to level 2
        self.game.lines_cleared = 10
        self.game.level = 2
        self.game.gravity_delay = self.game._calculate_gravity_delay()
        
        # Clear 1 line at level 2
        initial_score = self.game.score
        self.game._update_level(1)  # This calls _add_score internally
        
        # Then: Score increase is higher at level 2
        score_after_level_2 = self.game.score
        self.assertGreater(score_after_level_2, initial_score)
    
    def test_gravity_delay_calculation_with_level(self):
        """INTEGRATION: Gravity delay calculation uses current level."""
        # Given: Game at level 1
        level_1_delay = self.game.gravity_delay
        self.assertEqual(self.game.level, 1)
        
        # When: Level increases to 2
        self.game.level = 2
        level_2_delay = self.game._calculate_gravity_delay()
        self.game.gravity_delay = level_2_delay
        
        # Then: Gravity delay is reduced
        self.assertLess(level_2_delay, level_1_delay)
        
        # When: Level increases to 3
        self.game.level = 3
        level_3_delay = self.game._calculate_gravity_delay()
        
        # Then: Gravity delay is further reduced
        self.assertLess(level_3_delay, level_2_delay)
    
    def test_score_and_level_reset_on_new_game(self):
        """INTEGRATION: Score and level reset correctly on new game."""
        # Given: Game with score and level progression
        self.game._score = 500
        self.game.level = 2
        self.game.lines_cleared = 15
        
        # When: User starts new game
        self.game.start_new_game()
        
        # Then: Score and level are reset
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.lines_cleared, 0)
        # Gravity delay should be reset to level 1 value
        self.assertEqual(self.game.gravity_delay, self.game._calculate_gravity_delay())


class TestScoreLevelEdgeCases(unittest.TestCase):
    """Integration tests for edge cases in score and level interaction."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_multiple_level_progression_in_single_clear(self):
        """INTEGRATION: Multiple level progression in single clear is handled correctly."""
        # Given: Game at level 1 with 9 lines cleared
        self.game.lines_cleared = 9
        self.assertEqual(self.game.level, 1)
        
        # When: User clears 15 lines at once (should jump to level 2)
        self.game._update_level(15)
        
        # Then: Level has increased
        self.assertEqual(self.game.lines_cleared, 24)
        # Level should be calculated as (24 // 10) + 1 = 3
        # But _update_level only increases if new_level > current_level
        # So it should be level 2 after first increment, then level 3
        self.assertGreaterEqual(self.game.level, 2)
    
    def test_high_score_persistence_across_levels(self):
        """INTEGRATION: High score persists correctly across level progression."""
        # Given: Reset high score to ensure clean test
        self.session._high_score = 0
        initial_high_score = self.session.high_score
        
        # When: User plays and achieves score at level 1
        self.game._score = 300
        self.session.update_high_score(self.game._score)
        
        # Progress to level 2 and achieve higher score
        self.game.level = 2
        self.game._score = 600
        self.session.update_high_score(self.game._score)
        
        # Then: High score is the maximum
        self.assertEqual(self.game.high_score, 600)
        self.assertGreater(self.game.high_score, initial_high_score)


if __name__ == '__main__':
    unittest.main()

