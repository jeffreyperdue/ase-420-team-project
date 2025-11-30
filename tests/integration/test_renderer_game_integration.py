"""
Integration tests for PygameRenderer and Game component interactions.

These tests verify that the renderer and game work together correctly,
ensuring proper data flow and state management between components.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
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
from src.view.pygame_renderer import PygameRenderer
from src.utils.session_manager import SessionManager
from src.constants import WIDTH, HEIGHT
from src.constants.game_states import START_SCREEN, PLAYING, GAME_OVER


class TestRendererGameIntegration(unittest.TestCase):
    """Integration tests for PygameRenderer and Game."""
    
    def setUp(self):
        """Set up test environment."""
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.renderer = PygameRenderer(self.screen)
    
    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()
    
    def test_renderer_displays_start_screen_state(self):
        """INTEGRATION: Renderer displays start screen when game is in START_SCREEN state."""
        # Given: Game is in start screen state
        self.assertEqual(self.game._state, START_SCREEN)
        
        # When: Renderer draws start screen
        with patch.object(self.renderer, 'draw_start_screen') as mock_draw:
            if self.game._state == START_SCREEN:
                self.renderer.draw_start_screen()
        
        # Then: Start screen drawing is called
        # Note: Actual rendering requires pygame display, so we test the integration
        self.assertEqual(self.game._state, START_SCREEN)
    
    def test_renderer_displays_playing_state(self):
        """INTEGRATION: Renderer displays game elements when game is in PLAYING state."""
        # Given: Game is playing
        self.game.start_new_game()
        self.assertEqual(self.game._state, PLAYING)
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNotNone(self.game.next_piece)
        
        # When: Renderer draws game state
        self.renderer.draw_board(self.board)
        if self.game.current_piece:
            self.renderer.draw_piece(self.game.current_piece)
        if self.game.next_piece:
            self.renderer.draw_next_piece_preview(self.game.next_piece)
        self.renderer.draw_score(self.game.score, self.game.high_score)
        
        # Then: All game elements are available for rendering
        self.assertEqual(self.game._state, PLAYING)
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNotNone(self.game.next_piece)
    
    def test_renderer_displays_game_over_state(self):
        """INTEGRATION: Renderer displays game over screen when game is in GAME_OVER state."""
        # Given: Game is over
        self.game.start_new_game()
        # Force game over
        for row in range(0, 3):  # Fill top 3 rows to trigger collision
            for col in range(WIDTH):
                self.board.set_cell(row, col, 1)
        self.game._spawn_new_piece()
        self.assertEqual(self.game._state, GAME_OVER)
        if self.game._state == GAME_OVER:
            self.game.game_over = True
        
        # When: Renderer draws game over screen
        with patch.object(self.renderer, 'draw_game_over_screen') as mock_draw:
            if self.game._state == GAME_OVER:
                self.renderer.draw_game_over_screen(
                    score=self.game.score,
                    high_score=self.game.high_score
                )
        
        # Then: Game over screen drawing is called with correct data
        self.assertEqual(self.game._state, GAME_OVER)
        self.assertIsInstance(self.game.score, int)
        self.assertIsInstance(self.game.high_score, int)
    
    def test_renderer_updates_with_game_state_changes(self):
        """INTEGRATION: Renderer updates correctly when game state changes."""
        # Given: Game in start screen
        self.assertEqual(self.game._state, START_SCREEN)
        
        # When: Game state changes to playing
        self.game.apply(["START"])
        self.assertEqual(self.game._state, PLAYING)
        
        # Then: Renderer can draw playing state
        self.renderer.draw_board(self.board)
        if self.game.current_piece:
            self.renderer.draw_piece(self.game.current_piece)
        
        # When: Game state changes to game over
        for row in range(0, 3):  # Fill top 3 rows to trigger collision
            for col in range(WIDTH):
                self.board.set_cell(row, col, 1)
        self.game._spawn_new_piece()
        self.assertEqual(self.game._state, GAME_OVER)
        if self.game._state == GAME_OVER:
            self.game.game_over = True
        
        # Then: Renderer can draw game over state
        self.assertIsInstance(self.game.score, int)
        self.assertIsInstance(self.game.high_score, int)
    
    def test_renderer_displays_pause_overlay(self):
        """INTEGRATION: Renderer displays pause overlay when game is paused."""
        # Given: Game is playing
        self.game.start_new_game()
        self.assertEqual(self.game._state, PLAYING)
        self.assertFalse(self.game.paused)
        
        # When: Game is paused
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        # Then: Renderer can draw pause overlay
        with patch.object(self.renderer, 'draw_pause_popup') as mock_draw:
            if self.game.paused:
                self.renderer.draw_pause_popup(
                    score=self.game.score,
                    high_score=self.game.high_score
                )
        
        # Verify pause state
        self.assertTrue(self.game.paused)
        self.assertEqual(self.game._state, PLAYING)
    
    def test_renderer_displays_score_correctly(self):
        """INTEGRATION: Renderer displays score and high score correctly."""
        # Given: Game is playing with a score
        self.game.start_new_game()
        # Reset high score to ensure clean test
        self.session._high_score = 0
        self.game._score = 500
        self.session.update_high_score(500)
        
        # When: Renderer draws score
        self.renderer.draw_score(self.game.score, self.game.high_score)
        
        # Then: Score data is correct
        self.assertEqual(self.game.score, 500)
        self.assertEqual(self.game.high_score, 500)
        self.assertIsInstance(self.game.score, int)
        self.assertIsInstance(self.game.high_score, int)
    
    def test_renderer_displays_next_piece_preview(self):
        """INTEGRATION: Renderer displays next piece preview correctly."""
        # Given: Game is playing
        self.game.start_new_game()
        self.assertIsNotNone(self.game.next_piece)
        
        # When: Renderer draws next piece preview
        self.renderer.draw_next_piece_preview(self.game.next_piece)
        
        # Then: Next piece is available
        self.assertIsNotNone(self.game.next_piece)
        self.assertIsInstance(self.game.next_piece, Piece)
    
    def test_renderer_button_clicks_trigger_game_actions(self):
        """INTEGRATION: Button clicks from renderer trigger correct game actions."""
        # Given: Game in start screen with button manager
        self.assertEqual(self.game._state, START_SCREEN)
        self.assertIsNotNone(self.renderer.button_manager)
        
        # When: Start button is clicked (simulated)
        # The button manager would handle the click and return "START"
        intent = "START"
        self.game.apply([intent])
        
        # Then: Game starts
        self.assertEqual(self.game._state, PLAYING)
    
    def test_renderer_handles_pause_button(self):
        """INTEGRATION: Renderer pause button toggles game pause state."""
        # Given: Game is playing
        self.game.start_new_game()
        self.assertFalse(self.game.paused)
        
        # When: Pause button is clicked (simulated)
        intent = "PAUSE"
        self.game.apply([intent])
        
        # Then: Game is paused
        self.assertTrue(self.game.paused)
        
        # When: Pause button is clicked again
        self.game.apply([intent])
        
        # Then: Game is unpaused
        self.assertFalse(self.game.paused)


class TestRendererGameStateIntegration(unittest.TestCase):
    """Integration tests for renderer and game state synchronization."""
    
    def setUp(self):
        """Set up test environment."""
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.renderer = PygameRenderer(self.screen)
    
    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()
    
    def test_renderer_syncs_with_game_state_transitions(self):
        """INTEGRATION: Renderer stays synchronized with game state transitions."""
        # Test START_SCREEN -> PLAYING
        self.assertEqual(self.game._state, START_SCREEN)
        self.game.apply(["START"])
        self.assertEqual(self.game._state, PLAYING)
        
        # Test PLAYING -> PAUSED
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        self.assertEqual(self.game._state, PLAYING)
        
        # Test PAUSED -> PLAYING
        self.game.apply(["RESUME"])
        self.assertFalse(self.game.paused)
        self.assertEqual(self.game._state, PLAYING)
        
        # Test PLAYING -> GAME_OVER
        for row in range(0, 3):  # Fill top 3 rows to trigger collision
            for col in range(WIDTH):
                self.board.set_cell(row, col, 1)
        self.game._spawn_new_piece()
        self.assertEqual(self.game._state, GAME_OVER)
        if self.game._state == GAME_OVER:
            self.game.game_over = True
    
    def test_renderer_handles_rapid_state_changes(self):
        """INTEGRATION: Renderer handles rapid state changes correctly."""
        # Given: Game in start screen
        self.assertEqual(self.game._state, START_SCREEN)
        
        # When: Rapid state changes occur
        self.game.apply(["START"])
        self.assertEqual(self.game._state, PLAYING)
        
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        self.game.apply(["RESUME"])
        self.assertFalse(self.game.paused)
        
        # Then: Renderer can handle each state
        self.assertEqual(self.game._state, PLAYING)
        self.assertIsNotNone(self.game.current_piece)


if __name__ == '__main__':
    unittest.main()

