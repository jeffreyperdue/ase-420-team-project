import os
import sys
import unittest
from unittest import mock
from typing import Any

# Ensure repo root in path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.game import Game
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row
from src.utils.session_manager import SessionManager
from src.utils.score import points_for_clear
from src.view.pygame_renderer import PygameRenderer
from src.constants import WIDTH, HEIGHT, WHITE

import pygame


def simple_spawn():
    # place new pieces near top middle; tests will not rely on randomness
    return Piece(3, 0)


class TestScoring(unittest.TestCase):
    def setUp(self):
        """Create a clean board and game for each test."""
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        self.session = SessionManager()  # Get singleton instance
        self.game = Game(self.board, simple_spawn, self.session)

    def test_points_for_clear_basic(self):
        """Test the pure scoring function with valid inputs."""
        expected = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
        for lines, points in expected.items():
            self.assertEqual(points_for_clear(lines), points,
                           f"lines={lines} should score {points}")

    def test_points_for_clear_invalid_types(self):
        """Test scoring function rejects invalid types."""
        invalid_inputs: list[Any] = [
            None, 
            "3",                    # string that looks like int
            2.5,                    # float
            [],                     # empty list
            {"lines": 2},           # dict
            True,                   # bool
            (1,),                   # tuple
        ]
        for val in invalid_inputs:
            with self.assertRaises(TypeError):
                points_for_clear(val)  # type: ignore

    def test_points_for_clear_out_of_range(self):
        """Test scoring function handles out-of-range values."""
        # Values outside 0-4 should return 0
        invalid_lines = [-100, -1, 5, 10, 999, 1000000]
        for lines in invalid_lines:
            self.assertEqual(points_for_clear(lines), 0,
                           f"lines={lines} should return 0")

    def test_update_score_accumulation(self):
        """Test score accumulates correctly through multiple updates."""
        # Each update should add to existing score
        updates = [
            (1, 100),    # 100 total
            (2, 400),    # 300 more -> 400 total
            (4, 1200),   # 800 more -> 1200 total
            (0, 1200),   # +0 -> still 1200
            (3, 1700),   # +500 -> 1700 total
        ]
        for lines, expected_total in updates:
            self.game._update_score(lines)
            self.assertEqual(self.game.score, expected_total,
                           f"After {lines} lines score should be {expected_total}")

    def test_update_score_edge_cases(self):
        """Test Game._update_score handles edge cases safely."""
        edge_cases = [
            -1,         # negative
            5,          # too many lines
            100,        # way too many
            0,          # no lines (no score)
        ]
        self.game._score = 50  # start with some points
        for lines in edge_cases:
            before = self.game.score
            self.game._update_score(lines)
            # Out of range should add 0
            self.assertEqual(self.game.score, before,
                           f"Score shouldn't change for {lines} lines")

    def test_freeze_piece_updates_for_multiple_lines(self):
        board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        session = SessionManager()
        game = Game(board, simple_spawn, session)
        game.start_new_game()  # Initialize current_piece and next_piece

        # Fill the bottom two rows completely
        bottom = board.height - 1
        second = board.height - 2
        for c in range(board.width):
            board.set_cell(bottom, c, 1)
            board.set_cell(second, c, 1)

        # Call freeze which should clear rows and update score
        # Note: _freeze_piece relies on board.clear_full_lines() to set lines_cleared
        game._freeze_piece()
        # two lines -> 300 base points + 100 from _add_score (100 * 1.0 multiplier) = 400 total
        # _freeze_piece calls both _update_score (base) and _update_level which calls _add_score (with multiplier)
        self.assertEqual(game.score, 400)
        self.assertEqual(board.lines_cleared, 2)

    def test_score_accumulates_across_freezes(self):
        board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        session = SessionManager()
        game = Game(board, simple_spawn, session)
        game.start_new_game()  # Initialize current_piece and next_piece

        # First clear 1 line
        bottom = board.height - 1
        for c in range(board.width):
            board.set_cell(bottom, c, 1)
        game._freeze_piece()
        # 1 line -> 100 base points + 40 from _add_score (40 * 1.0 multiplier) = 140 total
        self.assertEqual(game.score, 140)

        # Now clear 3 lines
        # fill three rows: bottom, second, third
        for r in (board.height - 1, board.height - 2, board.height - 3):
            for c in range(board.width):
                board.set_cell(r, c, 1)
        game._freeze_piece()
        # 1 line: 100 (base) + 40 (multiplier) = 140
        # 3 lines: 500 (base) + 300 (multiplier) = 800
        # Total: 140 + 800 = 940
        self.assertEqual(game.score, 940)

    def test_board_clear_lines_updates_score(self):
        """Test that board.lines_cleared feeds into scoring correctly."""
        # fill the bottom row completely
        bottom = self.board.height - 1
        for c in range(self.board.width):
            self.board.set_cell(bottom, c, 1)

        # clearing should detect one line
        self.board.clear_full_lines()
        self.assertEqual(self.board.lines_cleared, 1)

        # game consumes that value in its scoring function
        self.game._update_score(self.board.lines_cleared)
        self.assertEqual(self.game.score, 100)

    def test_game_over_score_freezes(self):
        """Test that game-over state prevents further score changes."""
        from src.constants.game_states import GAME_OVER
        self.game._update_score(4)  # 800 points
        self.game._state = GAME_OVER  # Set state to GAME_OVER
        self.game.game_over = True  # mark game as done

        # Try to update score - should be ignored in game-over
        self.game._update_score(1)  # would be +100 if not game over
        self.assertEqual(self.game.score, 800,
                       "Score should not change after game_over=True")

        # Even clearing lines should not affect score
        self.game._update_score(4)  # would be +800
        self.assertEqual(self.game.score, 800,
                       "Score should remain frozen after game over")

    def test_score_boundary_max_lines(self):
        """Test scoring at maximum valid line count (4)."""
        # Fill bottom 4 rows to test max line clear
        for row in range(self.board.height - 4, self.board.height):
            for col in range(self.board.width):
                self.board.set_cell(row, col, 1)
        
        self.board.clear_full_lines()
        self.assertEqual(self.board.lines_cleared, 4, 
                       "Should detect exactly 4 lines")
        
        # Game should award 800 points for 4 lines
        self.game._update_score(self.board.lines_cleared)
        self.assertEqual(self.game.score, 800,
                       "Should award 800 points for 4-line clear")

if __name__ == '__main__':
    unittest.main()
