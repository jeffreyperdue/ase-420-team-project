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

    def draw_level_info(self, level, lines_cleared, gravity_delay):
        """Draw level, lines cleared, and gravity info for debugging.
        
        Args:
            level (int): Current level
            lines_cleared (int): Total lines cleared
            gravity_delay (int): Current gravity delay in frames
        """
        font = pygame.font.Font(None, 24)
        
        # Level display
        level_text = font.render(f"Level: {level}", True, BLACK)
        self.screen.blit(level_text, (10, 10))
        
        # Lines cleared display
        lines_text = font.render(f"Lines: {lines_cleared}", True, BLACK)
        self.screen.blit(lines_text, (10, 35))
        
        # Gravity delay display (for debugging)
        gravity_text = font.render(f"Gravity: {gravity_delay} frames", True, BLACK)
        self.screen.blit(gravity_text, (10, 60))
        
    def draw_ghost_piece(self, board, piece):
        """
        Draw a 'ghost' outline of the piece at its landing position.
        """
        shape = SHAPES[piece.type][piece.rotation]
        land_y = board.get_landing_y(piece)

        for grid_position in shape:
            col = piece.x + (grid_position % 4)
            row = land_y + (grid_position // 4)

            rect = [
                self.board_x + CELL_SIZE * col,
                self.board_y + CELL_SIZE * row,
                CELL_SIZE - 2,
                CELL_SIZE - 2
            ]
            # Draw ghost piece with distinct visual style:
            # Semi-transparent fill with the piece's color (but very faded)
            ghost_color = COLORS[piece.color]
            # Create a very transparent version of the piece color
            ghost_surface = pygame.Surface((CELL_SIZE - 2, CELL_SIZE - 2))
            ghost_surface.set_alpha(50)  # Semi-transparent
            ghost_surface.fill(ghost_color)
            self.screen.blit(ghost_surface, (rect[0], rect[1]))
            # Then draw outline
            # Draw dashed outline to make it more distinct
            # Draw top and bottom edges
            pygame.draw.line(self.screen, ghost_color, 
                           (rect[0], rect[1]), 
                           (rect[0] + rect[2], rect[1]), 2)
            pygame.draw.line(self.screen, ghost_color, 
                           (rect[0], rect[1] + rect[3]), 
                           (rect[0] + rect[2], rect[1] + rect[3]), 2)
            # Draw left and right edges
            pygame.draw.line(self.screen, ghost_color, 
                           (rect[0], rect[1]), 
                           (rect[0], rect[1] + rect[3]), 2)
            pygame.draw.line(self.screen, ghost_color, 
                           (rect[0] + rect[2], rect[1]), 
                           (rect[0] + rect[2], rect[1] + rect[3]), 2)