import pygame
from src.constants import COLORS, CELL_SIZE, WHITE, GRAY, BLACK, NEXT_PAGE_PREVIEW_RECT, SCREEN_SIZE
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
        
        pygame.draw.rect(self.screen, BLACK, NEXT_PAGE_PREVIEW_RECT, 1)
        font = pygame.font.SysFont('Arial', 20)

        text_surface = font.render('Next Piece', True, BLACK)

        self.screen.blit(text_surface, (315, 200))

        # Drawing piece into box holding the next piece
        self.draw_next_piece(next_piece)

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

    def draw_next_piece(self, piece):
        color = COLORS[piece.color]
        shape = SHAPES[piece.type][piece.rotation]

        cols = [grid_position % 4 for grid_position in shape]
        rows = [grid_position // 4 for grid_position in shape]
        
        min_col, max_col = min(cols), max(cols)
        min_row, max_row = min(rows), max(rows)
        
        piece_width = max_col - min_col + 1
        piece_height = max_row - min_row + 1
        
        preview_center_x = NEXT_PAGE_PREVIEW_RECT[0] + NEXT_PAGE_PREVIEW_RECT[2] // 2
        preview_center_y = NEXT_PAGE_PREVIEW_RECT[1] + NEXT_PAGE_PREVIEW_RECT[3] // 2
        
        offset_x = (4 - piece_width) / 2 - min_col
        offset_y = (4 - piece_height) / 2 - min_row

        for grid_position in shape:
            col = (grid_position % 4) + offset_x
            row = (grid_position // 4) + offset_y
            
            rect = [
                preview_center_x - (2 * CELL_SIZE) + (col * CELL_SIZE),
                preview_center_y - (2 * CELL_SIZE) + (row * CELL_SIZE),
                CELL_SIZE - 1,
                CELL_SIZE - 1
            ]

            pygame.draw.rect(self.screen, color, rect)

    def draw_pause_screen(self):
        """Draw the pause screen overlay"""
        overlay = pygame.Surface(SCREEN_SIZE)
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.SysFont('Arial', 48, bold=True)
        font_small = pygame.font.SysFont('Arial', 24)
        
        center_x = SCREEN_SIZE[0] // 2
        center_y = SCREEN_SIZE[1] // 2
        
        paused_text = font_large.render('PAUSED', True, WHITE)
        paused_rect = paused_text.get_rect(center=(center_x, center_y - 40))
        self.screen.blit(paused_text, paused_rect)
        
        resume_text = font_small.render('Press P, ESC, or Click to Resume', True, WHITE)
        resume_rect = resume_text.get_rect(center=(center_x, center_y + 20))
        self.screen.blit(resume_text, resume_rect)