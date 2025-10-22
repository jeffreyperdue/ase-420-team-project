import os
import sys
import unittest

# Ensure repo root in path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.game import Game
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row
from src.view.pygame_renderer import PygameRenderer
from src.constants import WIDTH, HEIGHT, WHITE

import pygame


def simple_spawn():
    # place new pieces near top middle; tests will not rely on randomness
    return Piece(3, 0)


class TestScoring(unittest.TestCase):
    def test_update_score_direct(self):
        # direct mapping: 1 -> 100, 2 -> 300, 3 -> 500, 4 -> 800
        board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        game = Game(board, simple_spawn)
        self.assertEqual(game.score, 0)
        game._update_score(1)
        self.assertEqual(game.score, 100)
        game._update_score(2)
        self.assertEqual(game.score, 400)  # 100 + 300
        game._update_score(4)
        self.assertEqual(game.score, 1200)  # 400 + 800

    def test_update_score_table(self):
        board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        game = Game(board, simple_spawn)
        # expected mapping (canonical values)
        expected = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
        for lines, points in expected.items():
            # reset score before each mapping test
            game._score = 0
            game._update_score(lines)
            self.assertEqual(game.score, points, f"lines={lines} -> expected {points}")

    def test_freeze_piece_updates_for_multiple_lines(self):
        board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        game = Game(board, simple_spawn)

        # Fill the bottom two rows completely
        bottom = board.height - 1
        second = board.height - 2
        for c in range(board.width):
            board.set_cell(bottom, c, 1)
            board.set_cell(second, c, 1)

        # Call freeze which should clear rows and update score
        # Note: _freeze_piece relies on board.clear_full_lines() to set lines_cleared
        game._freeze_piece()
        # two lines -> 300 points
        self.assertEqual(game.score, 300)
        self.assertEqual(board.lines_cleared, 2)

    def test_score_accumulates_across_freezes(self):
        board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        game = Game(board, simple_spawn)

        # First clear 1 line
        bottom = board.height - 1
        for c in range(board.width):
            board.set_cell(bottom, c, 1)
        game._freeze_piece()
        self.assertEqual(game.score, 100)

        # Now clear 3 lines
        # fill three rows: bottom, second, third
        for r in (board.height - 1, board.height - 2, board.height - 3):
            for c in range(board.width):
                board.set_cell(r, c, 1)
        game._freeze_piece()
        # 100 + 500 = 600
        self.assertEqual(game.score, 600)

    def test_board_clear_lines_updates_score(self):
        board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        game = Game(board, simple_spawn)

        # fill the bottom row completely
        bottom = board.height - 1
        for c in range(board.width):
            board.set_cell(bottom, c, 1)

        # clearing should detect one line
        board.clear_full_lines()
        self.assertEqual(board.lines_cleared, 1)

        # game consumes that value in its scoring function
        game._update_score(board.lines_cleared)
        self.assertEqual(game.score, 100)


if __name__ == '__main__':
    unittest.main()
