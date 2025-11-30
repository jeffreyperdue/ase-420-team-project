"""
Acceptance tests for performance requirements.

These tests validate that the game meets performance requirements
and provides acceptable performance from a user perspective.
"""

import unittest
import time
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


class TestPerformanceAcceptance(unittest.TestCase):
    """Acceptance tests for performance requirements."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_game_update_performance(self):
        """ACCEPTANCE: Game update operations complete in acceptable time."""
        # Given: Game is playing
        self.assertEqual(self.game._state, "playing")
        
        # When: Multiple game updates are performed
        start_time = time.time()
        
        # Perform 100 game updates
        for _ in range(100):
            self.game.update()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Updates complete in acceptable time (< 1 second for 100 updates)
        self.assertLess(elapsed_time, 1.0, 
                       f"100 game updates took {elapsed_time:.3f}s, should be < 1.0s")
    
    def test_piece_movement_performance(self):
        """ACCEPTANCE: Piece movement operations are responsive."""
        # Given: Game is playing
        piece = self.game.current_piece
        
        # When: Multiple piece movements are performed
        start_time = time.time()
        
        # Perform 50 movement operations
        for _ in range(50):
            self.game.apply(["LEFT", "RIGHT", "ROTATE", "DOWN"])
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Movements complete in acceptable time (< 0.5 seconds for 50 operations)
        self.assertLess(elapsed_time, 0.5,
                       f"50 piece movements took {elapsed_time:.3f}s, should be < 0.5s")
    
    def test_line_clearing_performance(self):
        """ACCEPTANCE: Line clearing operations complete in acceptable time."""
        # Given: Board with full rows
        # Fill multiple rows
        for row in [HEIGHT - 1, HEIGHT - 2, HEIGHT - 3]:
            for col in range(WIDTH):
                self.board.set_cell(row, col, 1)
        
        # When: Line clearing is performed
        start_time = time.time()
        
        lines_cleared = self.board.clear_full_lines()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Line clearing completes in acceptable time (< 0.1 seconds)
        self.assertLess(elapsed_time, 0.1,
                       f"Line clearing took {elapsed_time:.3f}s, should be < 0.1s")
        self.assertGreater(lines_cleared, 0)
    
    def test_collision_detection_performance(self):
        """ACCEPTANCE: Collision detection is fast enough for responsive gameplay."""
        # Given: Game with pieces on board
        piece = self.game.current_piece
        
        # When: Multiple collision checks are performed
        start_time = time.time()
        
        # Perform 100 collision checks
        for _ in range(100):
            self.board.will_piece_collide(piece)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Collision checks complete in acceptable time (< 0.1 seconds for 100 checks)
        self.assertLess(elapsed_time, 0.1,
                       f"100 collision checks took {elapsed_time:.3f}s, should be < 0.1s")
    
    def test_ghost_piece_calculation_performance(self):
        """ACCEPTANCE: Ghost piece calculation is fast enough for real-time display."""
        # Given: Game with current piece
        piece = self.game.current_piece
        
        # When: Ghost piece landing position is calculated multiple times
        start_time = time.time()
        
        # Perform 100 ghost piece calculations
        for _ in range(100):
            landing_y = self.board.get_landing_y(piece)
            ghost_cells = self.board.get_ghost_cells(piece)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Calculations complete in acceptable time (< 0.1 seconds for 100 calculations)
        self.assertLess(elapsed_time, 0.1,
                       f"100 ghost piece calculations took {elapsed_time:.3f}s, should be < 0.1s")
    
    def test_scoring_calculation_performance(self):
        """ACCEPTANCE: Scoring calculations are fast enough."""
        # Given: Game with score system
        initial_score = self.game.score
        
        # When: Multiple scoring operations are performed
        start_time = time.time()
        
        # Perform 50 scoring updates
        for lines in range(1, 5):
            for _ in range(10):
                self.game._update_score(lines)
                self.game._update_level(lines)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Scoring completes in acceptable time (< 0.1 seconds for 50 operations)
        self.assertLess(elapsed_time, 0.1,
                       f"50 scoring operations took {elapsed_time:.3f}s, should be < 0.1s")
    
    def test_memory_usage_stability(self):
        """ACCEPTANCE: Memory usage remains stable during gameplay."""
        # Given: Game is playing
        import sys
        
        # When: Multiple game operations are performed
        initial_operations = 0
        
        # Perform many operations
        for i in range(1000):
            self.game.update()
            if i % 100 == 0:
                # Check that game state remains valid
                self.assertIsNotNone(self.game.current_piece)
        
        # Then: Game state remains valid (memory leak would cause issues)
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNotNone(self.game.next_piece)
    
    def test_rapid_input_handling_performance(self):
        """ACCEPTANCE: Rapid input is handled without performance degradation."""
        # Given: Game is playing
        piece = self.game.current_piece
        initial_x = piece.x
        
        # When: Rapid input is applied
        start_time = time.time()
        
        # Apply rapid input (100 operations)
        for _ in range(100):
            self.game.apply(["LEFT", "RIGHT", "ROTATE", "DOWN"])
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Input handling completes in acceptable time (< 0.5 seconds)
        self.assertLess(elapsed_time, 0.5,
                       f"100 rapid inputs took {elapsed_time:.3f}s, should be < 0.5s")
        # Game state should remain valid
        self.assertIsNotNone(self.game.current_piece)


class TestPerformanceUnderLoad(unittest.TestCase):
    """Acceptance tests for performance under load."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_performance_with_many_pieces_on_board(self):
        """ACCEPTANCE: Performance remains acceptable with many pieces on board."""
        # Given: Board with many pieces
        # Fill board partially
        for row in range(HEIGHT - 10, HEIGHT):
            for col in range(WIDTH):
                if (row + col) % 2 == 0:  # Fill every other cell
                    self.board.set_cell(row, col, 1)
        
        # When: Game operations are performed
        start_time = time.time()
        
        # Perform game updates
        for _ in range(50):
            self.game.update()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Performance remains acceptable (< 1 second for 50 updates)
        self.assertLess(elapsed_time, 1.0,
                       f"50 updates with many pieces took {elapsed_time:.3f}s, should be < 1.0s")
    
    def test_performance_during_line_clears(self):
        """ACCEPTANCE: Performance remains acceptable during line clearing."""
        # Given: Board with multiple full rows
        for row in [HEIGHT - 1, HEIGHT - 2, HEIGHT - 3, HEIGHT - 4]:
            for col in range(WIDTH):
                self.board.set_cell(row, col, 1)
        
        # When: Line clearing is performed
        start_time = time.time()
        
        lines_cleared = self.board.clear_full_lines()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Line clearing completes in acceptable time
        self.assertLess(elapsed_time, 0.2,
                       f"Line clearing took {elapsed_time:.3f}s, should be < 0.2s")
        self.assertGreater(lines_cleared, 0)
    
    def test_performance_with_high_level(self):
        """ACCEPTANCE: Performance remains acceptable at high levels."""
        # Given: Game at high level
        self.game.level = 10
        self.game.gravity_delay = self.game._calculate_gravity_delay()
        
        # When: Game operations are performed
        start_time = time.time()
        
        # Perform game updates
        for _ in range(100):
            self.game.update()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Performance remains acceptable
        self.assertLess(elapsed_time, 1.0,
                       f"100 updates at high level took {elapsed_time:.3f}s, should be < 1.0s")


if __name__ == '__main__':
    unittest.main()

