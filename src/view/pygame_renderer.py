import pygame
from src.constants import WHITE, GRAY, COLORS, CELL_SIZE

class PygameRenderer:
    def __init__(self, screen, board_origin=(100, 60)):
        self.screen = screen
        self.board_x, self.board_y = board_origin

    def draw_board(self, board):
        self.screen.fill(WHITE)

        for row in range(board.height):
            for col in range(board.width):
                rect = [
                    self.board_x + CELL_SIZE * col,
                    self.board_y + CELL_SIZE * row,
                    CELL_SIZE,
                    CELL_SIZE
                ]
                # draw grid outline
                pygame.draw.rect(self.screen, GRAY, rect, 1)

                # draw filled cells
                cell_value = board.grid[row][col]
                if cell_value > 0:
                    pygame.draw.rect(
                        self.screen,
                        COLORS[cell_value],
                        [rect[0] + 1, rect[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2]
                    )

    def draw_piece(self, piece):
        color = COLORS[piece.color]
        for (dx, dy) in piece.cells:
            rect = [
                self.board_x + CELL_SIZE * (piece.x + dx),
                self.board_y + CELL_SIZE * (piece.y + dy),
                CELL_SIZE - 2,
                CELL_SIZE - 2
            ]
            pygame.draw.rect(self.screen, color, rect)
