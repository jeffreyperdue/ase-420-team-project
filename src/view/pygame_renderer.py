import pygame
from src.constants import COLORS, CELL_SIZE, RED, WHITE, GRAY, BLACK, NEXT_PAGE_PREVIEW_RECT, SCREEN_SIZE
from src.figures import SHAPES
from src.ui.button_manager import ButtonManager
from src.ui.start_screen_layout_utils import center_popup, content_area
from src.ui.start_screen_render_utils import draw_overlay, draw_popup_background, draw_wrapped_label

class PygameRenderer:
    def __init__(self, screen, board_origin=(70, 60), next_piece_preview_origin=(110, 60)):
        self.screen = screen
        self.board_x, self.board_y = board_origin
        self.next_piece_preview_x, self.next_piece_preview_y = next_piece_preview_origin
        self.arrow_keys_img = pygame.image.load("src/view/img/arrow-keys.png").convert_alpha()
        self.arrow_keys_img = self._scale_by_height(self.arrow_keys_img, 80)
        self.spacebar_key_img = pygame.image.load("src/view/img/spacebar-key.png").convert()
        self.spacebar_key_img = self._scale_by_height(self.spacebar_key_img, 30)
        self.button_manager = ButtonManager()

    def _scale_by_height(self, image, target_height):
        original_width, original_height = image.get_size()
        scale_factor = target_height / original_height
        scaled_width = int(original_width * scale_factor)
        scaled_image = pygame.transform.smoothscale(image, (scaled_width, target_height))
        return scaled_image

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

    def draw_start_screen(self):
        """Draw the start screen."""
        draw_overlay(self.screen, BLACK)
        
        # Create start screen popup
        popup_width = 400
        popup_height = 520
        popup_x, popup_y = center_popup(self.screen.get_width(), self.screen.get_height(), popup_width, popup_height)
        
        padding = 30
        content_x, content_y, content_width, content_height = content_area(popup_x, popup_y, popup_width, popup_height, padding)

        draw_popup_background(self.screen, WHITE, popup_x, popup_y, popup_width, popup_height)
        
        # Title
        title_font = pygame.font.Font(None, 60)
        title_text = title_font.render("Tetris", True, BLACK)
        title_rect = title_text.get_rect(centerx=popup_x + popup_width // 2, y=content_y)
        self.screen.blit(title_text, title_rect)

        spacing_below_title = 100
        
        # Controls section
        controls_font = pygame.font.SysFont('Arial', 16, bold=False)
        
        # Draw arrow keys image
        arrow_img_x = content_x + (content_width - self.arrow_keys_img.get_width()) // 2
        arrow_img_y = content_y + spacing_below_title
        self.screen.blit(self.arrow_keys_img, (arrow_img_x, arrow_img_y))

        # Get arrow image dimensions and center
        arrow_width = self.arrow_keys_img.get_width()
        arrow_height = self.arrow_keys_img.get_height()
        arrow_center_x = arrow_img_x + arrow_width // 2
        arrow_center_y = arrow_img_y + arrow_height // 2

        # ROTATE (label)
        rotate_label = controls_font.render("Rotate", True, BLACK)
        rotate_rect = rotate_label.get_rect(center=(arrow_center_x, arrow_img_y - 18))
        self.screen.blit(rotate_label, rotate_rect)

        # MOVE LEFT (label)
        draw_wrapped_label(self.screen, controls_font, arrow_img_x - 25, arrow_center_y + 20, "Move", "Left", BLACK)

        # MOVE RIGHT (label)
        draw_wrapped_label(self.screen, controls_font, arrow_img_x + arrow_width + 25, arrow_center_y + 20, "Move", "Right", BLACK)

        # SOFT DROP (label)
        drop_bottom = draw_wrapped_label(self.screen, controls_font, arrow_center_x, arrow_img_y + arrow_height + 25, "Soft", "Drop", BLACK)
        
        # Draw spacebar image directly below
        spacebar_img_x = content_x + (content_width - self.spacebar_key_img.get_width()) // 2
        spacebar_img_y = drop_bottom + 30
        self.screen.blit(self.spacebar_key_img, (spacebar_img_x, spacebar_img_y))

        # Draw spacebar label (below spacebar)
        spacebar_width = self.spacebar_key_img.get_width()
        space_label = controls_font.render("Space Bar: Hard Drop", True, BLACK)
        space_rect = space_label.get_rect(center=(spacebar_img_x + spacebar_width // 2, spacebar_img_y + self.spacebar_key_img.get_height() + 20))
        self.screen.blit(space_label, space_rect)

        spacing_above_buttons = 30

        # Buttons
        button_width = 200
        button_height = 40
        button_x = content_x + (content_width - button_width) // 2
        
        start_y = space_rect.bottom + spacing_above_buttons
        exit_y = start_y + button_height + 10

        # Add buttons to manager (only once)
        if not self.button_manager.buttons:
            self.button_manager.add_button(
                rect=(button_x, start_y, button_width, button_height),
                label="Start Game",
                action="START",
                color=(0, 200, 0),
                text_color=WHITE
            )
            self.button_manager.add_button(
                rect=(button_x, exit_y, button_width, button_height),
                label="Exit",
                action="EXIT",
                color=(200, 0, 0),
                text_color=WHITE
            )

        # Draw buttons
        buttons_font = pygame.font.SysFont('Arial', 18, bold=True)

        self.button_manager.draw(self.screen, buttons_font)
        self.button_manager.set_cursor()

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

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

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