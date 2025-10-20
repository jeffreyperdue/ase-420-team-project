"""
Pytest configuration and shared fixtures for the Tetris testing suite.

This file provides common test fixtures and configuration for all test modules.
It ensures consistent test setup across unit, integration, regression, and acceptance tests.

Usage:
    pytest tests/  # Runs all tests with these fixtures available
    pytest tests/integration/ -v  # Runs integration tests with fixtures
"""

import pytest
import pygame
import sys
import os
from unittest.mock import MagicMock, patch

# Add repository root to path for imports
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.game import Game
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row
from src.view.input import InputHandler
from src.constants import WIDTH, HEIGHT


@pytest.fixture
def game_board():
    """Fixture providing a standard game board for testing."""
    return Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)


@pytest.fixture
def sample_piece():
    """Fixture providing a sample piece for testing."""
    return Piece(WIDTH // 2, 0)


@pytest.fixture
def game_instance(game_board):
    """Fixture providing a complete game instance for testing."""
    def spawn_piece():
        return Piece(WIDTH // 2, 0)
    
    return Game(game_board, spawn_piece)


@pytest.fixture
def input_handler():
    """Fixture providing an input handler for testing."""
    return InputHandler()


@pytest.fixture
def mock_pygame():
    """Fixture providing mocked pygame for headless testing."""
    with patch('pygame.init'), \
         patch('pygame.display.set_mode'), \
         patch('pygame.display.set_caption'), \
         patch('pygame.display.flip'), \
         patch('pygame.event.get'), \
         patch('pygame.quit'):
        yield pygame


@pytest.fixture
def mock_keyboard_events():
    """Fixture providing mock keyboard events for testing."""
    return [
        MagicMock(type=1000, key=1073741906),  # pygame.K_UP (ROTATE)
        MagicMock(type=1000, key=1073741904),  # pygame.K_LEFT (LEFT)
        MagicMock(type=1000, key=1073741903),  # pygame.K_RIGHT (RIGHT)
        MagicMock(type=1000, key=1073741905),  # pygame.K_DOWN (DOWN)
        MagicMock(type=1000, key=32),          # pygame.K_SPACE (DROP)
        MagicMock(type=1000, key=27),          # pygame.K_ESCAPE (QUIT)
    ]


@pytest.fixture
def deterministic_piece():
    """Fixture providing deterministic piece generation for testing."""
    with patch('src.game.piece.random.randint') as mock_randint:
        mock_randint.side_effect = [0, 1]  # type=0 (I piece), color=1
        yield Piece(WIDTH // 2, 0)


@pytest.fixture
def empty_board():
    """Fixture providing an empty board for testing."""
    board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
    board.clear()
    return board


@pytest.fixture
def board_with_pieces():
    """Fixture providing a board with some pieces placed for testing."""
    board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
    
    # Place some test pieces
    board.set_cell(HEIGHT - 1, 0, 1)
    board.set_cell(HEIGHT - 1, 1, 1)
    board.set_cell(HEIGHT - 2, 0, 1)
    
    return board


@pytest.fixture
def board_with_full_row():
    """Fixture providing a board with a full row for line clearing tests."""
    board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
    
    # Fill bottom row completely
    for col in range(WIDTH):
        board.set_cell(HEIGHT - 1, col, 1)
    
    return board


@pytest.fixture
def board_near_game_over():
    """Fixture providing a board near game over condition."""
    board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
    
    # Fill board near the top
    for row in range(HEIGHT - 2, HEIGHT):
        for col in range(WIDTH):
            board.set_cell(row, col, 1)
    
    return board


@pytest.fixture
def complete_game_setup():
    """Fixture providing a complete game setup for integration testing."""
    board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
    
    def spawn_piece():
        return Piece(WIDTH // 2, 0)
    
    game = Game(board, spawn_piece)
    input_handler = InputHandler()
    
    return {
        'board': board,
        'game': game,
        'input_handler': input_handler,
        'spawn_piece': spawn_piece
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "acceptance: mark test as acceptance test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on file paths."""
    for item in items:
        # Add markers based on test file location
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "regression" in str(item.fspath):
            item.add_marker(pytest.mark.regression)
        elif "acceptance" in str(item.fspath):
            item.add_marker(pytest.mark.acceptance)
        elif "unit" in str(item.fspath) or "test_" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Mark slow tests
        if "slow" in item.name or "performance" in item.name:
            item.add_marker(pytest.mark.slow)


# Test utilities
class GameTestHelper:
    """Helper class for common test operations."""
    
    @staticmethod
    def create_board_with_pieces(board, positions):
        """Helper to create specific board states for testing."""
        for row, col, color in positions:
            board.set_cell(row, col, color)
        return board
    
    @staticmethod
    def simulate_game_session(game, duration_frames=1000):
        """Helper to simulate a complete game session."""
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
        """Helper to capture complete game state for assertions."""
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
        """Helper to create a piece at a specific position."""
        with patch('src.game.piece.random.randint') as mock_randint:
            mock_randint.side_effect = [piece_type, color]
            return Piece(x, y)


@pytest.fixture
def game_helper():
    """Fixture providing GameTestHelper for test utilities."""
    return GameTestHelper()


# Test data fixtures
@pytest.fixture
def game_scenarios():
    """Fixture providing predefined game scenarios for testing."""
    return {
        'empty_board': [],
        'single_piece': [(HEIGHT - 1, WIDTH // 2, 1)],
        'near_full_board': [(row, col, 1) for row in range(HEIGHT - 2, HEIGHT) 
                           for col in range(WIDTH)],
        'line_clear_scenario': [(HEIGHT - 1, col, 1) for col in range(WIDTH)],
        'game_over_scenario': [(row, col, 1) for row in range(HEIGHT - 1, HEIGHT) 
                              for col in range(WIDTH)]
    }


# Performance testing fixtures
@pytest.fixture
def performance_timer():
    """Fixture providing a simple performance timer for tests."""
    import time
    
    class PerformanceTimer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
        
        def elapsed(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None
    
    return PerformanceTimer()


# Mock fixtures for external dependencies
@pytest.fixture
def mock_random():
    """Fixture providing mocked random number generation."""
    with patch('random.randint') as mock_randint:
        mock_randint.side_effect = [0, 1]  # Default: type=0, color=1
        yield mock_randint


@pytest.fixture
def mock_time():
    """Fixture providing mocked time functions."""
    with patch('time.time') as mock_time_func:
        mock_time_func.side_effect = [0.0, 1.0]  # Start at 0, end at 1
        yield mock_time_func


# Test environment setup
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Automatically set up test environment for each test."""
    # Ensure pygame is initialized for tests that need it
    try:
        pygame.init()
    except:
        pass  # pygame might already be initialized
    
    yield
    
    # Cleanup after test
    try:
        pygame.quit()
    except:
        pass  # pygame might already be quit
