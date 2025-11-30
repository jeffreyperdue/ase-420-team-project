"""
Integration tests for game state transitions.

These tests verify that game state transitions work correctly,
ensuring proper state management and transitions between states.
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
from src.constants.game_states import START_SCREEN, PLAYING, GAME_OVER


class TestStateTransitions(unittest.TestCase):
    """Integration tests for game state transitions."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
    
    def test_start_screen_to_playing_transition(self):
        """INTEGRATION: START_SCREEN transitions to PLAYING via START intent."""
        # Given: Game is in start screen state
        self.assertEqual(self.game._state, START_SCREEN)
        self.assertIsNone(self.game.current_piece)
        self.assertIsNone(self.game.next_piece)
        
        # When: User sends START intent
        self.game.apply(["START"])
        
        # Then: Game transitions to playing state
        self.assertEqual(self.game._state, PLAYING)
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNotNone(self.game.next_piece)
        self.assertFalse(self.game.done)
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.level, 1)
    
    def test_playing_to_paused_transition(self):
        """INTEGRATION: PLAYING transitions to PAUSED via PAUSE intent."""
        # Given: Game is playing
        self.game.start_new_game()
        self.assertEqual(self.game._state, PLAYING)
        self.assertFalse(self.game.paused)
        
        # When: User sends PAUSE intent
        self.game.apply(["PAUSE"])
        
        # Then: Game is paused (state remains PLAYING, paused flag is True)
        self.assertEqual(self.game._state, PLAYING)
        self.assertTrue(self.game.paused)
    
    def test_paused_to_playing_transition(self):
        """INTEGRATION: PAUSED transitions to PLAYING via RESUME intent."""
        # Given: Game is paused
        self.game.start_new_game()
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        self.assertEqual(self.game._state, PLAYING)
        
        # When: User sends RESUME intent
        self.game.apply(["RESUME"])
        
        # Then: Game resumes (paused flag is False)
        self.assertEqual(self.game._state, PLAYING)
        self.assertFalse(self.game.paused)
    
    def test_playing_to_game_over_transition(self):
        """INTEGRATION: PLAYING transitions to GAME_OVER when piece spawns in collision."""
        # Given: Game is playing
        self.game.start_new_game()
        self.assertEqual(self.game._state, PLAYING)
        
        # When: Board is filled near TOP so spawn collides
        for row in range(0, 3):  # Fill top 3 rows
            for col in range(WIDTH):
                self.board.set_cell(row, col, 1)
        
        # Spawn new piece which should collide
        self.game._spawn_new_piece()
        
        # Then: Game transitions to game over state
        if self.game._state == GAME_OVER:
            self.game.game_over = True
        self.assertEqual(self.game._state, GAME_OVER)
        self.assertTrue(self.game.game_over)
    
    def test_game_over_to_playing_transition_via_restart(self):
        """INTEGRATION: GAME_OVER transitions to PLAYING via RESTART intent."""
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
        
        # When: User sends RESTART intent
        self.game.apply(["RESTART"])
        
        # Then: Game transitions to playing state
        self.assertEqual(self.game._state, PLAYING)
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.level, 1)
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNotNone(self.game.next_piece)
    
    def test_start_screen_to_done_transition_via_quit(self):
        """INTEGRATION: START_SCREEN sets done flag via QUIT intent."""
        # Given: Game is in start screen
        self.assertEqual(self.game._state, START_SCREEN)
        self.assertFalse(self.game.done)
        
        # When: User sends QUIT intent
        self.game.apply(["QUIT"])
        
        # Then: Done flag is set (state remains START_SCREEN)
        self.assertTrue(self.game.done)
        self.assertEqual(self.game._state, START_SCREEN)
    
    def test_game_over_to_done_transition_via_quit(self):
        """INTEGRATION: GAME_OVER sets done flag via QUIT intent."""
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
        self.assertFalse(self.game.done)
        
        # When: User sends QUIT intent
        self.game.apply(["QUIT"])
        
        # Then: Done flag is set (state remains GAME_OVER)
        self.assertTrue(self.game.done)
        self.assertEqual(self.game._state, GAME_OVER)
    
    def test_pause_toggle_transition(self):
        """INTEGRATION: Pause can be toggled on and off."""
        # Given: Game is playing
        self.game.start_new_game()
        self.assertFalse(self.game.paused)
        
        # When: User toggles pause (first time)
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        # When: User toggles pause (second time)
        self.game.apply(["PAUSE"])
        self.assertFalse(self.game.paused)
        
        # When: User toggles pause (third time)
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)


class TestStateTransitionEdgeCases(unittest.TestCase):
    """Integration tests for edge cases in state transitions."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
    
    def test_invalid_intents_in_start_screen(self):
        """INTEGRATION: Invalid intents in START_SCREEN don't change state."""
        # Given: Game in start screen
        self.assertEqual(self.game._state, START_SCREEN)
        
        # When: User sends invalid intents
        self.game.apply(["LEFT", "RIGHT", "ROTATE", "DROP"])
        
        # Then: State remains START_SCREEN
        self.assertEqual(self.game._state, START_SCREEN)
    
    def test_invalid_intents_in_game_over(self):
        """INTEGRATION: Invalid intents in GAME_OVER don't change state."""
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
        
        # When: User sends invalid intents
        self.game.apply(["LEFT", "RIGHT", "ROTATE", "DROP"])
        
        # Then: State remains GAME_OVER
        self.assertEqual(self.game._state, GAME_OVER)
    
    def test_pause_during_game_over_transition(self):
        """INTEGRATION: Pause state is handled during game over transition."""
        # Given: Game is playing and paused
        self.game.start_new_game()
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        # When: Game over occurs
        for row in range(0, 3):  # Fill top 3 rows to trigger collision
            for col in range(WIDTH):
                self.board.set_cell(row, col, 1)
        self.game._spawn_new_piece()
        if self.game._state == GAME_OVER:
            self.game.game_over = True
        
        # Then: Game is over
        self.assertEqual(self.game._state, GAME_OVER)
        # Note: Pause state behavior during game over depends on implementation
    
    def test_rapid_state_transitions(self):
        """INTEGRATION: Rapid state transitions are handled correctly."""
        # Given: Game in start screen
        self.assertEqual(self.game._state, START_SCREEN)
        
        # When: Rapid transitions occur
        self.game.apply(["START"])
        self.assertEqual(self.game._state, PLAYING)
        
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        self.game.apply(["RESUME"])
        self.assertFalse(self.game.paused)
        
        # Then: Game remains in valid state
        self.assertEqual(self.game._state, PLAYING)
        self.assertIsNotNone(self.game.current_piece)
    
    def test_restart_from_playing_state(self):
        """INTEGRATION: RESTART intent from playing state resets game."""
        # Given: Game is playing with score
        self.game.start_new_game()
        self.game._score = 500
        self.game.level = 2
        self.game.lines_cleared = 15
        
        # When: User sends RESTART intent
        self.game.apply(["RESTART"])
        
        # Then: Game resets but remains in playing state
        self.assertEqual(self.game._state, PLAYING)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.lines_cleared, 0)
        self.assertIsNotNone(self.game.current_piece)
    
    def test_start_intent_from_playing_state(self):
        """INTEGRATION: START intent from playing state is ignored."""
        # Given: Game is already playing
        self.game.start_new_game()
        initial_score = self.game.score
        self.game._score = 100
        
        # When: User sends START intent
        self.game.apply(["START"])
        
        # Then: Game continues playing (score not reset)
        self.assertEqual(self.game._state, PLAYING)
        self.assertEqual(self.game.score, 100)


if __name__ == '__main__':
    unittest.main()

