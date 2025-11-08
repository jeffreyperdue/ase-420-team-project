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
from src.constants import WIDTH, HEIGHT


class TestPauseToggle(unittest.TestCase):
    def setUp(self):
        self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        def spawn_piece():
            return Piece(WIDTH // 2, 0)
        self.game = Game(self.board, spawn_piece)
        self.input_handler = InputHandler()

    def test_pause_with_p_key(self):
        # Initially not paused
        self.assertFalse(self.game.paused)
        
        # Press 'p' to pause
        events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_p)]
        intents = self.input_handler.get_intents(events)
        self.game.apply(intents)
        self.assertTrue(self.game.paused)
        
        # Press 'p' again to unpause
        events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_p)]
        intents = self.input_handler.get_intents(events)
        self.game.apply(intents)
        self.assertFalse(self.game.paused)

    def test_escape_acts_as_quit_and_pause(self):
        # ESC should produce QUIT and also toggle pause intent
        events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)]
        intents = self.input_handler.get_intents(events)
        self.assertIn("QUIT", intents)
        self.assertIn("PAUSE", intents)
        
        # Apply to game toggles pause
        self.game.apply(intents)
        self.assertTrue(self.game.paused)
        
        # ESC again should unpause
        intents = self.input_handler.get_intents(events)
        self.game.apply(intents)
        self.assertFalse(self.game.paused)

    def test_click_unpauses(self):
        # Pause first
        events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_p)]
        intents = self.input_handler.get_intents(events)
        self.game.apply(intents)
        self.assertTrue(self.game.paused)
        
        # Simulate mouse click
        click_events = [MagicMock(type=pygame.MOUSEBUTTONDOWN)]
        intents = self.input_handler.get_intents(click_events)
        self.game.apply(intents)
        self.assertFalse(self.game.paused)


if __name__ == '__main__':
    unittest.main()
