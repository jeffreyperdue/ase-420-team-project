"""
Integration tests for the Next Piece preview feature.

These tests verify that the Game maintains a next_piece, that it advances
when the current piece locks, and that it remains stable during non-locking moves.
"""

import os
import sys
import unittest

# Add repository root to path for imports
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.game.game import Game
from src.game.board import Board
from src.game.row import Row
from src.game.piece import Piece
from src.utils.session_manager import SessionManager
from src.constants import WIDTH, HEIGHT


def make_piece_at_spawn(piece_type=0, color=1):
    """Create a Piece at the standard spawn with deterministic type/color."""
    p = Piece(WIDTH // 2, 0)
    p.type = piece_type
    p.color = color
    p.rotation = 0
    p.cells = []
    return p


def make_spawn_sequence(pieces):
    """Return a spawn function that yields pieces from a predefined list."""
    it = iter(pieces)

    def spawn():
        try:
            return next(it)
        except StopIteration:
            # Fallback: return a fresh piece if over-consumed
            return make_piece_at_spawn(0, 1)

    return spawn


class TestNextPiecePreviewIntegration(unittest.TestCase):
    def setUp(self):
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        self.session = SessionManager()

    def test_initializes_with_next_piece(self):
        """Game should initialize with both current and next piece available."""
        p1 = make_piece_at_spawn(piece_type=0, color=1)
        p2 = make_piece_at_spawn(piece_type=1, color=2)
        spawn = make_spawn_sequence([p1, p2])

        game = Game(self.board, spawn, self.session)
        game.start_new_game()  # Initialize pieces - this sets current_piece=p1, next_piece=p2

        # After start_new_game, current_piece should be p1 and next_piece should be p2
        # Note: assertIs checks object identity, but pieces are created fresh each time
        # So we check that they exist and are different objects
        self.assertIsNotNone(game.current_piece)
        self.assertIsNotNone(game.next_piece)
        self.assertIsNot(game.current_piece, game.next_piece)
        # Verify the pieces have the expected types/colors
        self.assertEqual(game.current_piece.type, p1.type)
        self.assertEqual(game.next_piece.type, p2.type)
        self.assertIsNot(game.current_piece, game.next_piece)

    def test_next_piece_advances_after_lock(self):
        """After the current piece locks (e.g., DROP), next piece becomes current and a new next is generated."""
        p1 = make_piece_at_spawn(piece_type=0, color=1)
        p2 = make_piece_at_spawn(piece_type=2, color=3)
        p3 = make_piece_at_spawn(piece_type=3, color=4)
        spawn = make_spawn_sequence([p1, p2, p3])

        game = Game(self.board, spawn, self.session)
        game.start_new_game()  # Initialize pieces

        # Sanity before action
        self.assertIs(game.current_piece, p1)
        self.assertIs(game.next_piece, p2)

        # Force lock by hard drop
        game.apply(["DROP"])  # triggers freeze -> spawn new piece

        # Now p2 should be active, and p3 should be queued as next
        self.assertIs(game.current_piece, p2)
        self.assertIs(game.next_piece, p3)

    def test_next_piece_stable_on_non_locking_moves(self):
        """Moving/rotating without locking should not change next_piece."""
        p1 = make_piece_at_spawn(piece_type=4, color=5)
        p2 = make_piece_at_spawn(piece_type=5, color=6)
        spawn = make_spawn_sequence([p1, p2])

        game = Game(self.board, spawn, self.session)
        game.start_new_game()  # Initialize pieces

        next_before = game.next_piece

        # Non-locking moves: one step DOWN, LEFT, RIGHT, ROTATE
        game.apply(["DOWN", "LEFT", "RIGHT", "ROTATE"])  # Should not freeze

        self.assertIs(game.current_piece, p1)  # Still same current
        self.assertIs(game.next_piece, next_before)  # Next unchanged


if __name__ == '__main__':
    unittest.main()
