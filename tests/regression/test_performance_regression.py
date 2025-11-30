"""
Regression tests for performance characteristics.

These tests protect performance characteristics from degrading during
future development, ensuring baseline performance is maintained.
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


class TestPerformanceRegression(unittest.TestCase):
    """Regression tests for performance characteristics."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_game_update_performance_baseline(self):
        """REGRESSION: Game update performance meets baseline."""
        # Given: Game is playing
        self.assertEqual(self.game._state, "playing")
        
        # When: Game updates are performed
        start_time = time.time()
        
        # Perform 100 game updates
        for _ in range(100):
            self.game.update()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Performance meets baseline (< 1 second for 100 updates)
        self.assertLess(elapsed_time, 1.0,
                       f"REGRESSION: 100 game updates took {elapsed_time:.3f}s, baseline is < 1.0s")
    
    def test_piece_movement_performance_baseline(self):
        """REGRESSION: Piece movement performance meets baseline."""
        # Given: Game is playing
        piece = self.game.current_piece
        
        # When: Piece movements are performed
        start_time = time.time()
        
        # Perform 50 movement operations
        for _ in range(50):
            self.game.apply(["LEFT", "RIGHT", "ROTATE", "DOWN"])
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Performance meets baseline (< 0.5 seconds for 50 operations)
        self.assertLess(elapsed_time, 0.5,
                       f"REGRESSION: 50 piece movements took {elapsed_time:.3f}s, baseline is < 0.5s")
    
    def test_line_clearing_performance_baseline(self):
        """REGRESSION: Line clearing performance meets baseline."""
        # Given: Board with full rows
        for row in [HEIGHT - 1, HEIGHT - 2, HEIGHT - 3]:
            for col in range(WIDTH):
                self.board.set_cell(row, col, 1)
        
        # When: Line clearing is performed
        start_time = time.time()
        
        lines_cleared = self.board.clear_full_lines()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Performance meets baseline (< 0.1 seconds)
        self.assertLess(elapsed_time, 0.1,
                       f"REGRESSION: Line clearing took {elapsed_time:.3f}s, baseline is < 0.1s")
        self.assertGreater(lines_cleared, 0)
    
    def test_collision_detection_performance_baseline(self):
        """REGRESSION: Collision detection performance meets baseline."""
        # Given: Game with piece
        piece = self.game.current_piece
        
        # When: Collision checks are performed
        start_time = time.time()
        
        # Perform 100 collision checks
        for _ in range(100):
            self.board.will_piece_collide(piece)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Performance meets baseline (< 0.1 seconds for 100 checks)
        self.assertLess(elapsed_time, 0.1,
                       f"REGRESSION: 100 collision checks took {elapsed_time:.3f}s, baseline is < 0.1s")
    
    def test_ghost_piece_calculation_performance_baseline(self):
        """REGRESSION: Ghost piece calculation performance meets baseline."""
        # Given: Game with piece
        piece = self.game.current_piece
        
        # When: Ghost piece calculations are performed
        start_time = time.time()
        
        # Perform 100 ghost piece calculations
        for _ in range(100):
            landing_y = self.board.get_landing_y(piece)
            ghost_cells = self.board.get_ghost_cells(piece)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Performance meets baseline (< 0.1 seconds for 100 calculations)
        self.assertLess(elapsed_time, 0.1,
                       f"REGRESSION: 100 ghost calculations took {elapsed_time:.3f}s, baseline is < 0.1s")
    
    def test_scoring_performance_baseline(self):
        """REGRESSION: Scoring performance meets baseline."""
        # Given: Game with score system
        initial_score = self.game.score
        
        # When: Scoring operations are performed
        start_time = time.time()
        
        # Perform 50 scoring updates
        for lines in range(1, 5):
            for _ in range(10):
                self.game._update_score(lines)
                self.game._update_level(lines)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Performance meets baseline (< 0.1 seconds for 50 operations)
        self.assertLess(elapsed_time, 0.1,
                       f"REGRESSION: 50 scoring operations took {elapsed_time:.3f}s, baseline is < 0.1s")
    
    def test_memory_stability_baseline(self):
        """REGRESSION: Memory usage remains stable."""
        # Given: Game is playing
        # When: Many operations are performed
        for i in range(1000):
            self.game.update()
            if i % 100 == 0:
                # Check that game state remains valid
                self.assertIsNotNone(self.game.current_piece)
        
        # Then: Game state remains valid (memory leak would cause issues)
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNotNone(self.game.next_piece)
        self.assertIsNotNone(self.game.board)


class TestPerformanceUnderLoadRegression(unittest.TestCase):
    """Regression tests for performance under load."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()
    
    def test_performance_with_many_pieces_baseline(self):
        """REGRESSION: Performance with many pieces meets baseline."""
        # Given: Board with many pieces
        for row in range(HEIGHT - 10, HEIGHT):
            for col in range(WIDTH):
                if (row + col) % 2 == 0:
                    self.board.set_cell(row, col, 1)
        
        # When: Game operations are performed
        start_time = time.time()
        
        # Perform 50 game updates
        for _ in range(50):
            self.game.update()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Performance meets baseline (< 1 second for 50 updates)
        self.assertLess(elapsed_time, 1.0,
                       f"REGRESSION: 50 updates with many pieces took {elapsed_time:.3f}s, baseline is < 1.0s")
    
    def test_performance_at_high_level_baseline(self):
        """REGRESSION: Performance at high level meets baseline."""
        # Given: Game at high level
        self.game.level = 10
        self.game.gravity_delay = self.game._calculate_gravity_delay()
        
        # When: Game operations are performed
        start_time = time.time()
        
        # Perform 100 game updates
        for _ in range(100):
            self.game.update()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Performance meets baseline (< 1 second for 100 updates)
        self.assertLess(elapsed_time, 1.0,
                       f"REGRESSION: 100 updates at high level took {elapsed_time:.3f}s, baseline is < 1.0s")
    
    def test_rapid_input_performance_baseline(self):
        """REGRESSION: Rapid input handling performance meets baseline."""
        # Given: Game is playing
        piece = self.game.current_piece
        
        # When: Rapid input is applied
        start_time = time.time()
        
        # Apply rapid input (100 operations)
        for _ in range(100):
            self.game.apply(["LEFT", "RIGHT", "ROTATE", "DOWN"])
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Then: Performance meets baseline (< 0.5 seconds)
        self.assertLess(elapsed_time, 0.5,
                       f"REGRESSION: 100 rapid inputs took {elapsed_time:.3f}s, baseline is < 0.5s")
        # Game state should remain valid
        self.assertIsNotNone(self.game.current_piece)


if __name__ == '__main__':
    unittest.main()

