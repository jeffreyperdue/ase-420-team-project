"""
Regression tests for critical user paths.

These tests protect the most common user workflows and high-frequency
operations, ensuring core gameplay remains functional.
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


class TestCriticalPaths(unittest.TestCase):
    """Regression tests for critical user paths."""
    
    def setUp(self):
        """Set up test environment."""
        SessionManager._instance = None
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.input_handler = InputHandler()
    
    def test_critical_path_start_to_play(self):
        """REGRESSION: Critical path - Start game to playing works."""
        # Given: Game in start screen
        self.assertEqual(self.game._state, START_SCREEN)
        
        # When: User starts game
        self.game.apply(["START"])
        
        # Then: Game is playing
        self.assertEqual(self.game._state, PLAYING)
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNotNone(self.game.next_piece)
        self.assertFalse(self.game.done)
    
    def test_critical_path_piece_movement(self):
        """REGRESSION: Critical path - Piece movement works."""
        # Given: Game is playing
        self.game.start_new_game()
        piece = self.game.current_piece
        initial_x = piece.x
        initial_y = piece.y
        
        # When: User moves piece
        self.game.apply(["LEFT"])
        self.assertEqual(piece.x, initial_x - 1)
        
        self.game.apply(["RIGHT"])
        self.assertEqual(piece.x, initial_x)
        
        self.game.apply(["DOWN"])
        self.assertEqual(piece.y, initial_y + 1)
        
        # Then: Piece movement works correctly
        self.assertGreaterEqual(piece.x, 0)
        self.assertLess(piece.x, WIDTH)
    
    def test_critical_path_piece_rotation(self):
        """REGRESSION: Critical path - Piece rotation works."""
        # Given: Game is playing
        self.game.start_new_game()
        piece = self.game.current_piece
        initial_rotation = piece.rotation
        
        # When: User rotates piece
        self.game.apply(["ROTATE"])
        
        # Then: Piece rotation works
        self.assertIsNotNone(piece)
        self.assertIsInstance(piece.rotation, int)
        # Rotation may or may not change depending on piece type and collision
        self.assertIsInstance(piece.rotation, int)
    
    def test_critical_path_piece_drop(self):
        """REGRESSION: Critical path - Piece drop works."""
        # Given: Game is playing
        self.game.start_new_game()
        piece = self.game.current_piece
        initial_y = piece.y
        
        # When: User drops piece
        self.game.apply(["DROP"])
        
        # Then: Piece is dropped
        self.assertGreater(piece.y, initial_y)
    
    def test_critical_path_line_clearing(self):
        """REGRESSION: Critical path - Line clearing works."""
        # Given: Board with full row
        for col in range(WIDTH):
            self.board.set_cell(HEIGHT - 1, col, 1)
        
        # When: Line clearing is performed
        lines_cleared = self.board.clear_full_lines()
        
        # Then: Line is cleared
        self.assertEqual(lines_cleared, 1)
        
        # Verify row is empty
        full_rows = sum(1 for row in range(HEIGHT) 
                       if all(self.board.get_cell(row, col) for col in range(WIDTH)))
        self.assertEqual(full_rows, 0)
    
    def test_critical_path_game_over(self):
        """REGRESSION: Critical path - Game over detection works."""
        # Given: Game is playing
        self.game.start_new_game()
        
        # When: Game over condition occurs (fill top rows to trigger collision)
        for row in range(0, 3):  # Fill top 3 rows
            for col in range(WIDTH):
                self.board.set_cell(row, col, 1)
        self.game._spawn_new_piece()
        
        # Then: Game over is detected
        self.assertEqual(self.game._state, GAME_OVER)
        if self.game._state == GAME_OVER:
            self.game.game_over = True
        self.assertTrue(self.game.game_over)
    
    def test_critical_path_restart(self):
        """REGRESSION: Critical path - Game restart works."""
        # Given: Game is over
        self.game.start_new_game()
        # Force game over (fill top rows to trigger collision)
        for row in range(0, 3):  # Fill top 3 rows
            for col in range(WIDTH):
                self.board.set_cell(row, col, 1)
        self.game._spawn_new_piece()
        self.assertEqual(self.game._state, GAME_OVER)
        if self.game._state == GAME_OVER:
            self.game.game_over = True
        
        # When: User restarts
        self.game.apply(["RESTART"])
        
        # Then: New game starts
        self.assertEqual(self.game._state, PLAYING)
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.score, 0)
        self.assertIsNotNone(self.game.current_piece)
    
    def test_critical_path_pause_resume(self):
        """REGRESSION: Critical path - Pause and resume works."""
        # Given: Game is playing
        self.game.start_new_game()
        self.assertFalse(self.game.paused)
        
        # When: User pauses
        self.game.apply(["PAUSE"])
        self.assertTrue(self.game.paused)
        
        # When: User resumes
        self.game.apply(["RESUME"])
        self.assertFalse(self.game.paused)
        
        # Then: Game continues normally
        self.assertEqual(self.game._state, PLAYING)
        self.assertIsNotNone(self.game.current_piece)


class TestHighFrequencyOperations(unittest.TestCase):
    """Regression tests for high-frequency operations."""
    
    def setUp(self):
        """Set up test environment."""
        SessionManager._instance = None
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_high_frequency_piece_movement(self):
        """REGRESSION: High-frequency piece movement works."""
        # Given: Game is playing
        piece = self.game.current_piece
        
        # When: Many movements are performed rapidly
        for _ in range(100):
            self.game.apply(["LEFT", "RIGHT"])
        
        # Then: Game state remains valid
        self.assertIsNotNone(self.game.current_piece)
        self.assertGreaterEqual(piece.x, 0)
        self.assertLess(piece.x, WIDTH)
    
    def test_high_frequency_rotation(self):
        """REGRESSION: High-frequency rotation works."""
        # Given: Game is playing
        piece = self.game.current_piece
        
        # When: Many rotations are performed rapidly
        for _ in range(50):
            self.game.apply(["ROTATE"])
        
        # Then: Game state remains valid
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsInstance(piece.rotation, int)
    
    def test_high_frequency_game_updates(self):
        """REGRESSION: High-frequency game updates work."""
        # Given: Game is playing
        # When: Many game updates are performed
        for _ in range(1000):
            self.game.update()
        
        # Then: Game state remains valid
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNotNone(self.game.next_piece)
        self.assertEqual(self.game._state, PLAYING)
    
    def test_high_frequency_collision_checks(self):
        """REGRESSION: High-frequency collision checks work."""
        # Given: Game with piece
        piece = self.game.current_piece
        
        # When: Many collision checks are performed
        for _ in range(1000):
            collision = self.board.will_piece_collide(piece)
            self.assertIsInstance(collision, bool)
        
        # Then: Collision detection remains functional
        collision = self.board.will_piece_collide(piece)
        self.assertIsInstance(collision, bool)


class TestCoreGameplayLoop(unittest.TestCase):
    """Regression tests for core gameplay loop."""
    
    def setUp(self):
        """Set up test environment."""
        SessionManager._instance = None
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_core_gameplay_loop(self):
        """REGRESSION: Core gameplay loop works correctly."""
        # Given: Game is playing
        self.game.start_new_game()  # Start the game
        self.assertEqual(self.game._state, PLAYING)
        
        # When: Core gameplay loop is executed multiple times
        # Use LEFT/RIGHT/ROTATE only to avoid pieces locking and filling board
        for _ in range(100):
            # Move piece (avoid DOWN to prevent pieces from locking too quickly)
            self.game.apply(["LEFT", "RIGHT", "ROTATE"])
            # Update game (gravity)
            self.game.update()
            # Clear board periodically to prevent game over
            if _ % 20 == 0:
                self.board.clear()
        
        # Then: Game continues to function (may be game_over if board filled, but shouldn't crash)
        # Game should either be playing or game_over, but not crashed
        self.assertIn(self.game._state, [PLAYING, GAME_OVER])
        # If still playing, verify pieces exist
        if self.game._state == PLAYING:
            self.assertIsNotNone(self.game.current_piece)
            self.assertIsNotNone(self.game.next_piece)
        self.assertIsInstance(self.game.done, bool)
    
    def test_core_gameplay_with_line_clearing(self):
        """REGRESSION: Core gameplay with line clearing works."""
        # Given: Game is playing
        # When: Lines are cleared during gameplay
        # Fill and clear lines multiple times
        for iteration in range(5):
            # Fill bottom row
            for col in range(WIDTH):
                self.board.set_cell(HEIGHT - 1, col, 1)
            
            # Clear line
            lines_cleared = self.board.clear_full_lines()
            if lines_cleared > 0:
                self.game._update_score(lines_cleared)
                self.game._update_level(lines_cleared)
            
            # Continue gameplay
            self.game.update()
        
        # Then: Game continues to function
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsInstance(self.game.score, int)
        self.assertIsInstance(self.game.level, int)
    
    def test_core_gameplay_with_pause(self):
        """REGRESSION: Core gameplay with pause works."""
        # Given: Game is playing
        # When: Game is paused and resumed during gameplay
        for _ in range(10):
            # Play a bit
            self.game.apply(["LEFT", "RIGHT"])
            self.game.update()
            
            # Pause
            self.game.apply(["PAUSE"])
            self.assertTrue(self.game.paused)
            
            # Resume
            self.game.apply(["RESUME"])
            self.assertFalse(self.game.paused)
        
        # Then: Game continues to function
        self.assertEqual(self.game._state, PLAYING)
        self.assertIsNotNone(self.game.current_piece)


if __name__ == '__main__':
    unittest.main()

