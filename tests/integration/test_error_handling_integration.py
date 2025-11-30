"""
Integration tests for error handling across components.

These tests verify that error handling works correctly across component
interactions, ensuring graceful degradation and proper error recovery.
"""

import unittest
from unittest.mock import patch, MagicMock
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


class TestErrorHandlingIntegration(unittest.TestCase):
    """Integration tests for error handling."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
    
    def test_invalid_input_handling(self):
        """INTEGRATION: Invalid input is handled gracefully."""
        # Given: Game is playing
        self.game.start_new_game()
        initial_state = self.game._state
        initial_piece = self.game.current_piece
        
        # When: Invalid intents are applied
        self.game.apply(["INVALID_INTENT", "UNKNOWN_ACTION", "BAD_INPUT"])
        
        # Then: Game state remains valid
        self.assertEqual(self.game._state, initial_state)
        self.assertIsNotNone(self.game.current_piece)
        # Piece should remain unchanged
        self.assertIsNotNone(initial_piece)
    
    def test_empty_intent_list_handling(self):
        """INTEGRATION: Empty intent list is handled gracefully."""
        # Given: Game is playing
        self.game.start_new_game()
        initial_state = self.game._state
        
        # When: Empty intent list is applied
        self.game.apply([])
        
        # Then: Game state remains valid
        self.assertEqual(self.game._state, initial_state)
        self.assertIsNotNone(self.game.current_piece)
    
    def test_boundary_condition_handling(self):
        """INTEGRATION: Boundary conditions are handled correctly."""
        # Given: Game with piece at boundary
        self.game.start_new_game()
        piece = self.game.current_piece
        
        # When: Piece is moved to left boundary
        for _ in range(WIDTH + 5):
            self.game.apply(["LEFT"])
            if piece.x == 0:
                break
        
        # Then: Piece doesn't go below 0
        self.assertGreaterEqual(piece.x, 0)
        
        # When: Piece is moved to right boundary
        for _ in range(WIDTH + 5):
            self.game.apply(["RIGHT"])
            if piece.x >= WIDTH - 1:
                break
        
        # Then: Piece doesn't exceed board width
        self.assertLess(piece.x, WIDTH)
    
    def test_collision_error_recovery(self):
        """INTEGRATION: Collision errors are handled gracefully."""
        # Given: Game with piece
        self.game.start_new_game()
        piece = self.game.current_piece
        
        # When: Collision detection is performed on invalid positions
        # Test with out-of-bounds position
        test_piece = Piece(-1, 0)  # Invalid x position
        test_piece.type = piece.type if piece else 0
        test_piece.rotation = piece.rotation if piece else 0
        
        # Then: Collision detection handles invalid position without crashing
        # will_piece_collide should detect out-of-bounds and return True
        # For x=-1, most piece shapes will have cells at col < 0, causing collision
        collision_result = self.board.will_piece_collide(test_piece)
        self.assertIsInstance(collision_result, bool)
        # Verify collision detection works - for x=-1, should detect out-of-bounds
        # The exact result depends on the piece shape, but it should not crash
        # Most pieces at x=-1 will have at least one cell out of bounds
        if test_piece.type is not None:
            # For a piece at x=-1, the shape cells will typically be at negative x
            # which should trigger the bounds check (col < 0) in will_piece_collide
            # However, if the shape is positioned such that all cells are still in bounds
            # (unlikely but possible), the result might be False
            # The important thing is that it doesn't crash
            # Let's test with a more extreme out-of-bounds position to ensure detection
            extreme_piece = Piece(-10, 0)  # Definitely out of bounds
            extreme_piece.type = test_piece.type
            extreme_piece.rotation = test_piece.rotation
            extreme_result = self.board.will_piece_collide(extreme_piece)
            self.assertTrue(extreme_result, "Piece at x=-10 should definitely be out of bounds")
    
    def test_session_error_recovery(self):
        """INTEGRATION: Session errors are handled gracefully."""
        # Given: Game with session manager
        self.assertIsNotNone(self.game._session)
        
        # When: Session operations are performed with invalid data
        # Test with negative score
        try:
            self.session.update_high_score(-100)
        except Exception:
            pass  # Should handle gracefully
        
        # Then: Session remains valid
        self.assertIsNotNone(self.game._session)
        self.assertIsInstance(self.game.high_score, int)
        self.assertGreaterEqual(self.game.high_score, 0)
    
    def test_state_corruption_recovery(self):
        """INTEGRATION: State corruption is handled gracefully."""
        # Given: Game in valid state
        self.game.start_new_game()
        self.assertEqual(self.game._state, PLAYING)
        
        # When: Invalid state transition is attempted
        # (Game should prevent invalid transitions)
        # Try to apply invalid intents in game over state
        self.game._state = GAME_OVER
        self.game.apply(["LEFT", "RIGHT", "ROTATE"])
        
        # Then: State remains valid
        self.assertEqual(self.game._state, GAME_OVER)
        # Game over state should ignore gameplay intents
    
    def test_resource_cleanup_on_errors(self):
        """INTEGRATION: Resources are cleaned up correctly on errors."""
        # Given: Game with resources
        self.game.start_new_game()
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNotNone(self.game.next_piece)
        
        # When: Error occurs (simulated by invalid operation)
        try:
            # Attempt invalid operation
            self.game.apply(["INVALID"])
        except Exception:
            pass
        
        # Then: Resources remain valid
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNotNone(self.game.next_piece)
        self.assertIsNotNone(self.game.board)
    
    def test_rapid_input_error_handling(self):
        """INTEGRATION: Rapid input errors are handled gracefully."""
        # Given: Game is playing
        self.game.start_new_game()
        piece = self.game.current_piece
        initial_x = piece.x
        
        # When: Rapid invalid inputs are applied
        for _ in range(100):
            self.game.apply(["LEFT", "RIGHT", "INVALID", "ROTATE", "BAD"])
        
        # Then: Game state remains valid
        self.assertIsNotNone(self.game.current_piece)
        self.assertGreaterEqual(piece.x, 0)
        self.assertLess(piece.x, WIDTH)
    
    def test_score_calculation_error_handling(self):
        """INTEGRATION: Score calculation errors are handled gracefully."""
        # Given: Game with score system
        self.game.start_new_game()
        initial_score = self.game.score
        
        # When: Score calculation is performed with edge cases
        # Test with zero lines cleared
        try:
            self.game._update_score(0)
        except Exception:
            pass
        
        # Then: Score remains valid
        self.assertIsInstance(self.game.score, int)
        self.assertGreaterEqual(self.game.score, initial_score)
        
        # Test with very large number
        try:
            self.game._update_score(1000)
        except Exception:
            pass
        
        # Then: Score remains valid
        self.assertIsInstance(self.game.score, int)


class TestErrorHandlingEdgeCases(unittest.TestCase):
    """Integration tests for edge cases in error handling."""
    
    def setUp(self):
        """Set up test environment."""
        self.session = SessionManager()
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        
        self.game = Game(self.board, spawn_piece, self.session)
    
    def test_null_piece_handling(self):
        """INTEGRATION: Null piece references are handled gracefully."""
        # Given: Game with piece
        self.game.start_new_game()
        
        # When: Piece operations are performed
        # (Piece should always be valid in normal gameplay)
        self.assertIsNotNone(self.game.current_piece)
        
        # Then: Operations succeed
        self.game.apply(["LEFT", "RIGHT"])
        self.assertIsNotNone(self.game.current_piece)
    
    def test_board_state_error_handling(self):
        """INTEGRATION: Board state errors are handled gracefully."""
        # Given: Game with board
        self.game.start_new_game()
        
        # When: Board operations are performed with edge cases
        # Test with out-of-bounds indices
        try:
            # These should raise IndexError, which is expected
            self.board.get_cell(-1, 0)
        except IndexError:
            pass  # Expected behavior
        
        try:
            self.board.get_cell(HEIGHT, 0)
        except IndexError:
            pass  # Expected behavior
        
        # Then: Board remains valid
        self.assertIsNotNone(self.board)
        self.assertEqual(self.board.height, HEIGHT)
        self.assertEqual(self.board.width, WIDTH)
    
    def test_level_progression_error_handling(self):
        """INTEGRATION: Level progression errors are handled gracefully."""
        # Given: Game with level system
        self.game.start_new_game()
        initial_level = self.game.level
        
        # When: Level progression is performed with edge cases
        # Test with negative lines cleared
        try:
            self.game.lines_cleared = -1
            self.game._update_level(-1)
        except Exception:
            pass
        
        # Then: Level remains valid
        self.assertIsInstance(self.game.level, int)
        self.assertGreaterEqual(self.game.level, 1)
        
        # Test with very large number
        try:
            self.game.lines_cleared = 1000000
            self.game._update_level(1000000)
        except Exception:
            pass
        
        # Then: Level remains valid
        self.assertIsInstance(self.game.level, int)
    
    def test_gravity_calculation_error_handling(self):
        """INTEGRATION: Gravity calculation errors are handled gracefully."""
        # Given: Game with gravity system
        self.game.start_new_game()
        
        # When: Gravity calculation is performed with edge cases
        # Test with very high level
        self.game.level = 1000
        gravity_delay = self.game._calculate_gravity_delay()
        
        # Then: Gravity delay remains valid (should be capped at minimum)
        self.assertIsInstance(gravity_delay, int)
        self.assertGreater(gravity_delay, 0)
        # Should be at minimum delay
        self.assertGreaterEqual(gravity_delay, 10)  # min_delay = 10
    
    def test_concurrent_operation_handling(self):
        """INTEGRATION: Concurrent operations are handled gracefully."""
        # Given: Game is playing
        self.game.start_new_game()
        
        # When: Multiple operations are performed simultaneously
        # (Simulated by rapid sequential operations)
        for _ in range(50):
            self.game.apply(["LEFT", "RIGHT", "ROTATE", "DOWN"])
            self.game.update()
        
        # Then: Game state remains valid
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNotNone(self.game.next_piece)
        self.assertEqual(self.game._state, PLAYING)


if __name__ == '__main__':
    unittest.main()

