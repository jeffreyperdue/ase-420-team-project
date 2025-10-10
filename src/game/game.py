import pygame
import os
import sys
# Ensure repository root is on sys.path so imports work when running from starter_code
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.constants import SCREEN_SIZE, FPS
from src.view.pygame_renderer import PygameRenderer
from src.view.input import InputHandler
class Game:
    def __init__(self, board, piece_generator):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Tetris (Team Project)")
        self.clock = pygame.time.Clock()

        self.board = board
        self.piece_generator = piece_generator
        self.active_piece = piece_generator.spawn()
        self.renderer = PygameRenderer(self.screen)
        self.input_handler = InputHandler()

        self.done = False

    def run(self):
        while not self.done:
            events = pygame.event.get()

            # Quit check
            for event in events:
                if event.type == pygame.QUIT:
                    self.done = True

            # turn raw pygame events → intents
            intents = self.input_handler.get_intents(events)

            # Debug: log intents to console
            if intents:
                print("Intents:", intents)

            # TODO: gravity / movement updates

            # --- Rendering ---
            self.renderer.draw_board(self.board)
            self.renderer.draw_piece(self.active_piece)

            # update the screen
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
