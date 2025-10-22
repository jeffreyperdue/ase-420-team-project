import unittest

# Ensure repo root in path (tests use repo-relative imports)
import os
import sys
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.score import points_for_clear
from src.game.game import Game
from src.game.board import Board
from src.game.row import Row
from src.game.piece import Piece
from src.constants import WIDTH


def simple_spawn():
    return Piece(3, 0)


class TestScoreUtils(unittest.TestCase):
    def test_score_table_basic(self):
        expected = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
        for lines, pts in expected.items():
            self.assertEqual(points_for_clear(lines), pts, f"lines={lines}")

    def test_game_uses_score_helper(self):
        board = Board(lambda: Row(WIDTH), height=20, width=WIDTH)
        game = Game(board, simple_spawn)
        # Sanity: game._update_score should produce identical effect as calling helper
        game._score = 0
        for lines in (0, 1, 2, 3, 4):
            before = game.score
            game._update_score(lines)
            # compute expected manually from helper
            expected = before + points_for_clear(lines)
            self.assertEqual(game.score, expected)


if __name__ == '__main__':
    unittest.main()
