import pygame
from src.constants import COLORS, CELL_SIZE, WHITE, GRAY
from src.figures import SHAPES

class PygameRenderer:
    def __init__(self, screen, board_origin=(70, 60), next_piece_preview_origin=(110, 60)):
        self.screen = screen
        self.board_x, self.board_y = board_origin
        self.next_piece_preview_x, self.next_piece_preview_y = next_piece_preview_origin

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
                if board.get_cell(row, col):
                    row_obj = board.get_row_object(row)
                    color = row_obj.get_color(col)
                    if color is not None:
                        pygame.draw.rect(
                            self.screen,
                            COLORS[color],
                            [rect[0] + 1, rect[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2]
                        )

    def draw_next_piece_preview(self, next_piece):
        #TODO: May change this color to black
        pygame.draw.rect(self.screen, GRAY, [290, 200, 150, 150], 1)
        font = pygame.font.SysFont('Arial', 20)
        #TODO: Need to change this font color to black, maybe bold as well if possible?
        text_surface = font.render('Next Piece', True, GRAY)

        self.screen.blit(text_surface, (315, 200))

        pass

    def draw_piece(self, piece):
        color = COLORS[piece.color]
        shape = SHAPES[piece.type][piece.rotation]
    
        for grid_position in shape:
            # Convert 4x4 grid position to board coordinates
            col = piece.x + (grid_position % 4)
            row = piece.y + (grid_position // 4)
        
            rect = [
                self.board_x + CELL_SIZE * col,
                self.board_y + CELL_SIZE * row,
                CELL_SIZE - 2,
                CELL_SIZE - 2
            ]
            pygame.draw.rect(self.screen, color, rect)