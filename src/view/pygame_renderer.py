import pygame
from src.constants import COLORS, CELL_SIZE, RED, WHITE, GRAY, BLACK, NEXT_PAGE_PREVIEW_RECT, SCREEN_SIZE
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

    def draw_score(self, score, high_score, font_size=24, color=BLACK):
        """Render the current score and high score on screen.
        Positions scores relative to the game board.

        Args:
            score (int): The current score to display.
            high_score (int): The high score to display.
            font_size (int): Size of the font.
            color (tuple): RGB color of the text.
        """
        font = pygame.font.SysFont('Arial', font_size, bold=True)
        
        # Position scores to the right of the board
        # Calculate position based on board_x and CELL_SIZE
        score_x = self.board_x + 12 * CELL_SIZE  # Position after the board width (10) plus some padding
        score_y = self.board_y  # Align with top of board
        
        # Draw current score
        score_text = font.render(f"Score: {score}", True, color)
        self.screen.blit(score_text, (score_x, score_y))
        
        # Draw high score below current score with spacing
        high_score_text = font.render(f"High Score: {high_score}", True, color)
        high_score_pos = (score_x, score_y + font_size + 5)
        self.screen.blit(high_score_text, high_score_pos)

    def draw_game_over_screen(self):
        """Draw the game over screen"""
        # Create a semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)  # Semi-transparent
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Instructions text
        font_small = pygame.font.Font(None, 24)
        instructions_text = font_small.render("Press R to Restart or ESC to Quit", True, WHITE)
        instructions_rect = instructions_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 20))
        self.screen.blit(instructions_text, instructions_rect)

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
        
        resume_text = font_small.render('Press ESC or Click to Resume', True, WHITE)
        resume_rect = resume_text.get_rect(center=(center_x, center_y + 20))
        self.screen.blit(resume_text, resume_rect)