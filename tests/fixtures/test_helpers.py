"""
Test helper utilities for the Tetris testing suite.

This module provides utility functions and classes that can be used across
different test modules to reduce code duplication and improve test maintainability.
"""

import os
import sys
from unittest.mock import patch, MagicMock

# Add repository root to path for imports
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.game import Game
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row
from src.utils.session_manager import SessionManager
from src.constants import WIDTH, HEIGHT


class GameTestHelper:
    """Helper class for common test operations."""
    
    @staticmethod
    def create_board_with_pieces(board, positions):
        """
        Helper to create specific board states for testing.
        
        Args:
            board: Board instance to modify
            positions: List of (row, col, color) tuples
            
        Returns:
            Modified board instance
        """
        for row, col, color in positions:
            if 0 <= row < board.height and 0 <= col < board.width:
                board.set_cell(row, col, color)
        return board
    
    @staticmethod
    def simulate_game_session(game, duration_frames=1000):
        """
        Helper to simulate a complete game session.
        
        Args:
            game: Game instance to simulate
            duration_frames: Maximum number of frames to simulate
            
        Returns:
            Number of moves played
        """
        moves_played = 0
        max_moves = duration_frames
        
        while not game.done and moves_played < max_moves:
            # Simulate typical user input
            game.apply(["RIGHT", "DOWN", "ROTATE"])
            game.update()
            moves_played += 1
        
        return moves_played
    
    @staticmethod
    def capture_game_state(game):
        """
        Helper to capture complete game state for assertions.
        
        Args:
            game: Game instance to capture state from
            
        Returns:
            Dictionary containing game state
        """
        return {
            'done': game.done,
            'current_piece': game.current_piece,
            'gravity_timer': game.gravity_timer,
            'gravity_delay': game.gravity_delay,
            'board_height': game.board.height,
            'board_width': game.board.width
        }
    
    @staticmethod
    def create_piece_at_position(x, y, piece_type=0, color=1):
        """
        Helper to create a piece at a specific position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            piece_type: Type of piece (0-6)
            color: Color of piece (1-7)
            
        Returns:
            Piece instance at specified position
        """
        with patch('src.game.piece.random.randint') as mock_randint:
            mock_randint.side_effect = [piece_type, color]
            return Piece(x, y)
    
    @staticmethod
    def create_full_row_board(row_index, width=WIDTH):
        """
        Helper to create a board with a full row.
        
        Args:
            row_index: Index of the row to fill
            width: Width of the row
            
        Returns:
            Board with specified row filled
        """
        board = Board(lambda: Row(width), height=HEIGHT, width=width)
        
        for col in range(width):
            board.set_cell(row_index, col, 1)
        
        return board
    
    @staticmethod
    def create_game_over_board():
        """
        Helper to create a board in game over condition.
        
        Returns:
            Board with pieces at the top
        """
        board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        
        # Fill top few rows to create game over condition
        for row in range(HEIGHT - 2, HEIGHT):
            for col in range(WIDTH):
                board.set_cell(row, col, 1)
        
        return board
    
    @staticmethod
    def count_full_rows(board):
        """
        Helper to count full rows on a board.
        
        Args:
            board: Board instance to check
            
        Returns:
            Number of full rows
        """
        full_rows = 0
        
        for row in range(board.height):
            if all(board.get_cell(row, col) for col in range(board.width)):
                full_rows += 1
        
        return full_rows
    
    @staticmethod
    def verify_piece_placement(board, piece):
        """
        Helper to verify that a piece is properly placed on the board.
        
        Args:
            board: Board instance
            piece: Piece instance
            
        Returns:
            True if piece is properly placed, False otherwise
        """
        from src.figures import SHAPES
        
        shape = SHAPES[piece.type][piece.rotation]
        
        for grid_position in shape:
            coords = board.grid_position_to_coords(grid_position, piece.x, piece.y)
            col, row = coords
            
            if 0 <= row < board.height and 0 <= col < board.width:
                if not board.get_cell(row, col):
                    return False
        
        return True


class MockInputHelper:
    """Helper class for creating mock input events."""
    
    @staticmethod
    def create_key_event(key_code):
        """
        Create a mock pygame key event.
        
        Args:
            key_code: pygame key constant
            
        Returns:
            Mock pygame event
        """
        return MagicMock(type=1000, key=key_code)
    
    @staticmethod
    def create_keyboard_sequence(keys):
        """
        Create a sequence of mock keyboard events.
        
        Args:
            keys: List of pygame key constants
            
        Returns:
            List of mock pygame events
        """
        return [MockInputHelper.create_key_event(key) for key in keys]
    
    @staticmethod
    def create_rapid_input_sequence(key, count=10):
        """
        Create rapid input sequence for testing.
        
        Args:
            key: pygame key constant
            count: Number of rapid inputs
            
        Returns:
            List of mock pygame events
        """
        return [MockInputHelper.create_key_event(key) for _ in range(count)]


class PerformanceTestHelper:
    """Helper class for performance testing."""
    
    @staticmethod
    def measure_execution_time(func, *args, **kwargs):
        """
        Measure execution time of a function.
        
        Args:
            func: Function to measure
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Tuple of (result, execution_time)
        """
        import time
        
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        return result, execution_time
    
    @staticmethod
    def benchmark_game_operations(game, operations_count=1000):
        """
        Benchmark game operations for performance testing.
        
        Args:
            game: Game instance to benchmark
            operations_count: Number of operations to perform
            
        Returns:
            Dictionary with performance metrics
        """
        import time
        
        start_time = time.time()
        
        for _ in range(operations_count):
            game.apply(["RIGHT", "LEFT", "ROTATE", "DOWN"])
            game.update()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return {
            'operations_count': operations_count,
            'execution_time': execution_time,
            'operations_per_second': operations_count / execution_time,
            'average_operation_time': execution_time / operations_count
        }


class TestDataGenerator:
    """Helper class for generating test data."""
    
    @staticmethod
    def generate_board_positions(count=10):
        """
        Generate random board positions for testing.
        
        Args:
            count: Number of positions to generate
            
        Returns:
            List of (row, col, color) tuples
        """
        import random
        
        positions = []
        for _ in range(count):
            row = random.randint(0, HEIGHT - 1)
            col = random.randint(0, WIDTH - 1)
            color = random.randint(1, 7)
            positions.append((row, col, color))
        
        return positions
    
    @staticmethod
    def generate_piece_sequence(count=20):
        """
        Generate a sequence of piece types for testing.
        
        Args:
            count: Number of pieces to generate
            
        Returns:
            List of piece type indices
        """
        import random
        
        return [random.randint(0, 6) for _ in range(count)]
    
    @staticmethod
    def generate_input_sequence(length=50):
        """
        Generate a random input sequence for testing.
        
        Args:
            length: Length of input sequence
            
        Returns:
            List of input strings
        """
        import random
        
        inputs = ["LEFT", "RIGHT", "DOWN", "ROTATE", "DROP"]
        return [random.choice(inputs) for _ in range(length)]


class AssertionHelper:
    """Helper class for common test assertions."""
    
    @staticmethod
    def assert_piece_within_bounds(piece, board):
        """
        Assert that a piece is within board bounds.
        
        Args:
            piece: Piece instance
            board: Board instance
        """
        assert piece.x >= 0, f"Piece x coordinate {piece.x} is below 0"
        assert piece.x < board.width, f"Piece x coordinate {piece.x} exceeds board width {board.width}"
        assert piece.y >= 0, f"Piece y coordinate {piece.y} is below 0"
        assert piece.y < board.height, f"Piece y coordinate {piece.y} exceeds board height {board.height}"
    
    @staticmethod
    def assert_game_state_valid(game):
        """
        Assert that a game is in a valid state.
        
        Args:
            game: Game instance
        """
        assert game is not None, "Game instance is None"
        assert game.board is not None, "Game board is None"
        assert game.current_piece is not None, "Game current piece is None"
        assert isinstance(game.done, bool), f"Game done flag is not boolean: {type(game.done)}"
        assert game.gravity_timer >= 0, f"Gravity timer is negative: {game.gravity_timer}"
        assert game.gravity_delay > 0, f"Gravity delay is not positive: {game.gravity_delay}"
    
    @staticmethod
    def assert_board_dimensions_valid(board):
        """
        Assert that board dimensions are valid.
        
        Args:
            board: Board instance
        """
        assert board.height > 0, f"Board height is not positive: {board.height}"
        assert board.width > 0, f"Board width is not positive: {board.width}"
        assert board.height == HEIGHT, f"Board height {board.height} doesn't match expected {HEIGHT}"
        assert board.width == WIDTH, f"Board width {board.width} doesn't match expected {WIDTH}"


# Convenience functions for common test operations
def create_test_board(positions=None):
    """Create a test board with optional piece positions."""
    board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
    
    if positions:
        GameTestHelper.create_board_with_pieces(board, positions)
    
    return board


def create_test_game(board=None):
    """Create a test game with optional board."""
    if board is None:
        board = create_test_board()
    
    def spawn_piece():
        return Piece(WIDTH // 2, 0)
    
    session = SessionManager()
    return Game(board, spawn_piece, session)


def create_test_piece(x=None, y=None, piece_type=0, color=1):
    """Create a test piece at specified position."""
    if x is None:
        x = WIDTH // 2
    if y is None:
        y = 0
    
    return GameTestHelper.create_piece_at_position(x, y, piece_type, color)


def simulate_user_input(game, input_sequence):
    """Simulate a sequence of user inputs on a game."""
    for input_action in input_sequence:
        game.apply([input_action])
        game.update()
