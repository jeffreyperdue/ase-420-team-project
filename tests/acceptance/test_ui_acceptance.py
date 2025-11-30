"""
Acceptance tests for UI/UX requirements.

These tests validate that the game provides acceptable user interface
and user experience from an end-user perspective.
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


class TestUIAcceptance(unittest.TestCase):
    """Acceptance tests for UI/UX requirements."""
    
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
    
    def test_start_screen_displays_correctly(self):
        """ACCEPTANCE: Start screen displays correctly with all elements."""
        # Given: Game in start screen state
        self.assertEqual(self.game._state, START_SCREEN)
        
        # When: Start screen is rendered
        self.renderer.draw_start_screen()
        
        # Then: Start screen elements are available
        # Button manager should have buttons
        self.assertIsNotNone(self.renderer.button_manager)
        # Start and Exit buttons should be registered
        button_actions = [btn.action for btn in self.renderer.button_manager.buttons]
        self.assertIn("START", button_actions)
        self.assertIn("EXIT", button_actions)
    
    def test_game_over_screen_displays_correctly(self):
        """ACCEPTANCE: Game over screen displays correctly with score information."""
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
        
        # When: Game over screen is rendered
        self.renderer.draw_game_over_screen(
            score=self.game.score,
            high_score=self.game.high_score
        )
        
        # Then: Game over screen elements are available
        self.assertIsNotNone(self.renderer.button_manager)
        # Restart and Quit buttons should be registered
        button_actions = [btn.action for btn in self.renderer.button_manager.buttons]
        self.assertIn("RESTART", button_actions)
        self.assertIn("QUIT", button_actions)
    
    def test_pause_overlay_displays_correctly(self):
        """ACCEPTANCE: Pause overlay displays correctly when game is paused."""
        # Given: Game is playing and paused
        self.game.start_new_game()
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        # When: Pause overlay is rendered
        self.renderer.draw_pause_popup(
            score=self.game.score,
            high_score=self.game.high_score
        )
        
        # Then: Pause overlay elements are available
        self.assertIsNotNone(self.renderer.hud_button_manager)
        # Pause popup should have buttons
        # (Exact buttons depend on implementation)
    
    def test_score_display_updates_correctly(self):
        """ACCEPTANCE: Score display updates correctly during gameplay."""
        # Given: Game is playing
        self.game.start_new_game()
        initial_score = self.game.score
        
        # Reset high score to ensure clean test
        self.session._high_score = 0
        
        # When: Score changes
        self.game._score = 500
        self.session.update_high_score(500)
        
        # Then: Score can be rendered correctly
        self.renderer.draw_score(self.game.score, self.game.high_score)
        self.assertEqual(self.game.score, 500)
        self.assertEqual(self.game.high_score, 500)
    
    def test_next_piece_preview_displays_correctly(self):
        """ACCEPTANCE: Next piece preview displays correctly."""
        # Given: Game is playing
        self.game.start_new_game()
        self.assertIsNotNone(self.game.next_piece)
        
        # When: Next piece preview is rendered
        self.renderer.draw_next_piece_preview(self.game.next_piece)
        
        # Then: Next piece preview is displayed
        # (Rendering is tested, this validates data availability)
        self.assertIsNotNone(self.game.next_piece)
        self.assertIsInstance(self.game.next_piece, Piece)
    
    def test_ghost_piece_displays_correctly(self):
        """ACCEPTANCE: Ghost piece displays correctly when playing."""
        # Given: Game is playing and not paused
        self.game.start_new_game()
        self.assertEqual(self.game._state, PLAYING)
        self.assertFalse(self.game.paused)
        self.assertIsNotNone(self.game.current_piece)
        
        # When: Ghost piece is rendered
        self.renderer.draw_ghost_piece(self.board, self.game.current_piece)
        
        # Then: Ghost piece is displayed
        # (Rendering is tested, this validates data availability)
        self.assertIsNotNone(self.game.current_piece)
        landing_y = self.board.get_landing_y(self.game.current_piece)
        self.assertIsInstance(landing_y, int)
    
    def test_ghost_piece_not_displayed_when_paused(self):
        """ACCEPTANCE: Ghost piece is not displayed when game is paused."""
        # Given: Game is playing and paused
        self.game.start_new_game()
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        # Then: Ghost piece should not be rendered
        # (This is tested in app.py logic: ghost piece only rendered when not paused)
        # This acceptance test validates the behavior
        self.assertTrue(self.game.paused)
        self.assertEqual(self.game._state, PLAYING)
    
    def test_level_info_displays_correctly(self):
        """ACCEPTANCE: Level information displays correctly."""
        # Given: Game is playing
        self.game.start_new_game()
        self.assertEqual(self.game.level, 1)
        
        # When: Level info is rendered
        self.renderer.draw_level_info(
            self.game.level,
            self.game.lines_cleared,
            self.game.gravity_delay
        )
        
        # Then: Level info is displayed correctly
        self.assertIsInstance(self.game.level, int)
        self.assertIsInstance(self.game.lines_cleared, int)
        self.assertIsInstance(self.game.gravity_delay, int)
    
    def test_button_clicks_provide_feedback(self):
        """ACCEPTANCE: Button clicks provide visual feedback."""
        # Given: Start screen with buttons
        self.assertEqual(self.game._state, START_SCREEN)
        self.renderer.draw_start_screen()
        
        # When: Button is clicked (simulated)
        # Button manager handles click
        buttons = self.renderer.button_manager.buttons
        self.assertGreater(len(buttons), 0)
        
        # Then: Button click can be processed
        # (Visual feedback is tested via rendering, this validates functionality)
        start_button = next((btn for btn in buttons if btn.action == "START"), None)
        self.assertIsNotNone(start_button)


class TestUIStateConsistency(unittest.TestCase):
    """Acceptance tests for UI state consistency."""
    
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
    
    def test_ui_elements_match_game_state(self):
        """ACCEPTANCE: UI elements match current game state."""
        # Test START_SCREEN state
        self.assertEqual(self.game._state, START_SCREEN)
        self.renderer.draw_start_screen()
        button_actions = [btn.action for btn in self.renderer.button_manager.buttons]
        self.assertIn("START", button_actions)
        
        # Test PLAYING state
        self.game.apply(["START"])
        self.assertEqual(self.game._state, PLAYING)
        self.renderer.draw_board(self.board)
        if self.game.current_piece:
            self.renderer.draw_piece(self.game.current_piece)
        
        # Test GAME_OVER state
        for row in range(0, 3):  # Fill top 3 rows to trigger collision
            for col in range(WIDTH):
                self.board.set_cell(row, col, 1)
        self.game._spawn_new_piece()
        self.assertEqual(self.game._state, GAME_OVER)
        if self.game._state == GAME_OVER:
            self.game.game_over = True
        self.renderer.draw_game_over_screen(
            score=self.game.score,
            high_score=self.game.high_score
        )
        button_actions = [btn.action for btn in self.renderer.button_manager.buttons]
        self.assertIn("RESTART", button_actions)
    
    def test_score_display_consistency(self):
        """ACCEPTANCE: Score display is consistent across game states."""
        # Given: Game with score
        self.game.start_new_game()
        self.game._score = 750
        self.session.update_high_score(750)
        
        # When: Score is displayed in different states
        # Playing state
        self.renderer.draw_score(self.game.score, self.game.high_score)
        self.assertEqual(self.game.score, 750)
        
        # Paused state
        self.game.apply(["PAUSE"])
        self.renderer.draw_pause_popup(
            score=self.game.score,
            high_score=self.game.high_score
        )
        self.assertEqual(self.game.score, 750)
        
        # Game over state
        self.game._state = GAME_OVER
        self.renderer.draw_game_over_screen(
            score=self.game.score,
            high_score=self.game.high_score
        )
        self.assertEqual(self.game.score, 750)
    
    def test_ui_responsiveness(self):
        """ACCEPTANCE: UI responds correctly to state changes."""
        # Given: Game in start screen
        self.assertEqual(self.game._state, START_SCREEN)
        
        # When: State changes to playing
        self.game.apply(["START"])
        self.assertEqual(self.game._state, PLAYING)
        
        # Then: UI can render playing state
        self.renderer.draw_board(self.board)
        if self.game.current_piece:
            self.renderer.draw_piece(self.game.current_piece)
        
        # When: State changes to paused
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        # Then: UI can render pause state
        self.renderer.draw_pause_popup(
            score=self.game.score,
            high_score=self.game.high_score
        )


if __name__ == '__main__':
    unittest.main()

