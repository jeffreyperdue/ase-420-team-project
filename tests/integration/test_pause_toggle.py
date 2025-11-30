import os
import sys
import unittest
from unittest.mock import MagicMock
import pygame

# Add repository root to path for imports
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


class TestPauseToggle(unittest.TestCase):
    def setUp(self):
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        self.session = SessionManager()
        self.game = Game(self.board, spawn_piece, self.session)
        self.game.start_new_game()  # Start game so pause works
        self.input_handler = InputHandler()

    def test_pause_with_p_key(self):
        """Pressing 'p' toggles pause on and off."""
        self.assertFalse(self.game.paused)
        events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_p)]
        intents = self.input_handler.get_intents(events)
        self.game.apply(intents)
        self.assertTrue(self.game.paused)
        events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_p)]
        intents = self.input_handler.get_intents(events)
        self.game.apply(intents)
        self.assertFalse(self.game.paused)

    def test_escape_acts_as_quit_and_pause(self):
        """ESC emits QUIT + PAUSE and toggles paused state."""
        events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)]
        intents = self.input_handler.get_intents(events)
        self.assertIn("QUIT", intents)
        self.assertIn("PAUSE", intents)
        self.game.apply(intents)
        self.assertTrue(self.game.paused)
        intents = self.input_handler.get_intents(events)
        self.game.apply(intents)
        self.assertFalse(self.game.paused)

    def test_click_unpauses(self):
        """Mouse click resumes from paused state."""
        events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_p)]
        intents = self.input_handler.get_intents(events)
        self.game.apply(intents)
        self.assertTrue(self.game.paused)
        click_events = [MagicMock(type=pygame.MOUSEBUTTONDOWN)]
        intents = self.input_handler.get_intents(click_events)
        self.game.apply(intents)
        self.assertFalse(self.game.paused)


if __name__ == '__main__':
    unittest.main()
