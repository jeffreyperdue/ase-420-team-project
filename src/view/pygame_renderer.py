import pygame
from src.constants import COLORS, CELL_SIZE, WHITE, GRAY, BLACK, RED
from src.figures import SHAPES

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
                if board.get_cell(row, col):
                    row_obj = board.get_row_object(row)
                    color = row_obj.get_color(col)
                    if color is not None:
                        pygame.draw.rect(
                            self.screen,
                            COLORS[color],
                            [rect[0] + 1, rect[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2]
                        )

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

    def draw_score(self, score, high_score, position=(20, 20), font_size=32, color=BLACK):
        """Render the current score and high score on screen.

        Args:
            score (int): The current score to display.
            high_score (int): The high score to display.
            position (tuple): (x, y) coordinates for the score text.
            font_size (int): Size of the font.
            color (tuple): RGB color of the text.
        """
        font = pygame.font.Font(None, font_size)
        score_text = font.render(f"Score: {score}", True, color)
        self.screen.blit(score_text, position)
        
        # Draw high score below current score
        high_score_pos = (position[0], position[1] + font_size + 5)
        high_score_text = font.render(f"High Score: {high_score}", True, color)
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
