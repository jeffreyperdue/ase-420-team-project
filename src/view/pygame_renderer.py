import pygame
from src.constants import COLORS, CELL_SIZE, RED, WHITE, GRAY, BLACK, NEXT_PAGE_PREVIEW_RECT
from src.figures import SHAPES
from src.ui.button_manager import ButtonManager
from src.ui.pop_up_layout_utils import center_popup, content_area
from src.ui.pop_up_render_utils import draw_overlay, draw_popup_background, draw_wrapped_label
from src.ui.pop_up import Popup

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
        """Draw the start screen using the Popup helper."""
        # Build body lines describing controls (we'll use images plus text)
        # To allow flexible height, we construct a Popup with title, images and body lines.
        body_lines = ["Use arrow keys to move and rotate.", "Space: Hard Drop"]

        # Compose images with small captions handled in body_lines for simplicity
        popup = Popup(
            title="Tetris",
            body_lines=body_lines,
            images=[self.arrow_keys_img, self.spacebar_key_img],
            buttons=[("Start Game", "START", (0, 200, 0)), ("Exit", "EXIT", (200, 0, 0))],
            width=420,
            padding=24,
        )

        popup.render(self.screen, self.button_manager)

    def draw_game_over_screen(self, score=None, high_score=None):
        """Draw the game over popup using the Popup helper.

        The popup will display the final score and session high score and
        provide two buttons: Play Again (RESTART) and Quit (QUIT).
        """
        # Compose body lines including the score info
        body_lines = ["You can try again or quit.", f"Score: {score if score is not None else 0}", f"High Score: {high_score if high_score is not None else 0}"]

        popup = Popup(
            title="GAME OVER",
            body_lines=body_lines,
            buttons=[("Play Again", "RESTART", (0, 200, 0)), ("Quit", "QUIT", (200, 0, 0))],
            width=360,
            padding=20,
        )

        popup.render(self.screen, self.button_manager)

    def draw_next_piece(self, piece):
        color = COLORS[piece.color]
        shape = SHAPES[piece.type][piece.rotation]

        for grid_position in shape:
            # Uses same logic as draw_piece function except places piece 
            # off of board and inside of next page preview
            col = 13 + (grid_position % 4)
            row = 9 + (grid_position // 4)
        
            rect = [
                self.board_x + CELL_SIZE * col,
                self.board_y + CELL_SIZE * row,
                CELL_SIZE - 1,
                CELL_SIZE - 1
            ]

            pygame.draw.rect(self.screen, color, rect)