import pygame
from src.constants import SCREEN_SIZE, FPS
from src.view.pygame_renderer import PygameRenderer

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

        self.done = False

    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                # input handling will live in input.py later

            # TODO: gravity / movement updates

            # --- Rendering ---
            self.renderer.draw_board(self.board)
            self.renderer.draw_piece(self.active_piece)

            # update the screen
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
