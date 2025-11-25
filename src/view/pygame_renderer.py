import pygame
from src.constants import COLORS, CELL_SIZE, RED, WHITE, GRAY, BLACK, NEXT_PAGE_PREVIEW_RECT, SCREEN_SIZE
from src.figures import SHAPES
from src.ui.button_manager import ButtonManager
from src.ui.pop_up import Popup

class PygameRenderer:
    def __init__(self, screen, board_origin=(70, 60), next_piece_preview_origin=(110, 60)):
        """
        Initialize the PygameRenderer.

        Args:
            screen (pygame.Surface): The main display surface.
            board_origin (tuple): Top-left pixel coordinates for the board grid.
            next_piece_preview_origin (tuple): Top-left pixel coordinates for the next piece preview box.
        """
        self.screen = screen
        self.board_x, self.board_y = board_origin
        self.next_piece_preview_x, self.next_piece_preview_y = next_piece_preview_origin
        self.controls_img = pygame.image.load("src/view/img/controls.png").convert_alpha()
        self.controls_img = self._scale_by_height(self.controls_img, 240)
        self.button_manager = ButtonManager()
        self.hud_button_manager = ButtonManager()
        self._hud_button_font = pygame.font.SysFont('Arial', 18, bold=True)

    def _scale_by_height(self, image, target_height):
        """
        Scale an image proportionally to a target height.

        Args:
            image (pygame.Surface): The image to scale.
            target_height (int): Desired height in pixels.

        Returns:
            pygame.Surface: Scaled image surface.
        """
        original_width, original_height = image.get_size()
        scale_factor = target_height / original_height
        scaled_width = int(original_width * scale_factor)
        scaled_image = pygame.transform.smoothscale(image, (scaled_width, target_height))
        return scaled_image

    def draw_board(self, board):
        """
        Render the game board grid and filled cells.

        Args:
            board (Board): The game board object containing cell states and colors.
        """
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
        """
        Draw the preview box and label for the next piece.

        Args:
            next_piece (Piece): The upcoming piece to render in the preview box.
        """
        pygame.draw.rect(self.screen, BLACK, NEXT_PAGE_PREVIEW_RECT, 1)
        font = pygame.font.SysFont('Arial', 20)

        text_surface = font.render('Next Piece', True, BLACK)

        self.screen.blit(text_surface, (315, 200))

        # Drawing piece into box holding the next piece
        self.draw_next_piece(next_piece)

    def draw_piece(self, piece):
        """
        Render the currently falling piece on the board.

        Args:
            piece (Piece): The active piece with position, rotation, and color.
        """
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
        """
        Render the current score and high score beside the board.

        Args:
            score (int): Current score.
            high_score (int): Session high score.
            font_size (int): Font size for text.
            color (tuple): RGB color for text.
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
        """Render the start screen popup with controls image and start/exit buttons."""
        # Build body lines describing controls
        # To allow flexible height, we construct a Popup with title, images and body lines.
        body_lines = ["Press 'p' or 'ESC' at any time to pause."]

        # Compose images with small captions handled in body_lines for simplicity
        popup = Popup(
            title="Tetris",
            body_lines=body_lines,
            images=[self.controls_img],
            button_specs=[("Start Game", "START", (0, 200, 0)), ("Exit", "EXIT", (200, 0, 0))],
            popup_width=420,
            padding=24,
        )

        popup.render(self.screen, self.button_manager)

    def draw_game_over_screen(self, score=None, high_score=None):
        """
        Render the game over popup with final score, high score,and two buttons:
        Play Again (RESTART) and Quit (QUIT).

        Args:
            score (int, optional): Final score. Defaults to 0 if None.
            high_score (int, optional): Session high score. Defaults to 0 if None.
        """
        # Compose body lines including the score info
        body_lines = ["You can try again or quit.", f"Score: {score if score is not None else 0}", f"High Score: {high_score if high_score is not None else 0}"]

        popup = Popup(
            title="GAME OVER",
            body_lines=body_lines,
            button_specs=[("Play Again", "RESTART", (0, 200, 0)), ("Quit", "QUIT", (200, 0, 0))],
            popup_width=360,
            padding=20,
        )

        popup.render(self.screen, self.button_manager)

    def draw_next_piece(self, piece):
        """ Render the next piece inside the preview box.

        Args:
            piece (Piece): The upcoming piece with type, rotation, and color.
        """
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
        """Render the pause overlay with 'PAUSED' text and resume instructions."""
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

    def draw_pause_popup(self, score, high_score):
        """Render a modal pause popup with resume, restart, and exit options."""
        self.hud_button_manager.clear()

        body_lines = [
            "Game paused.",
            f"Score: {score}",
            f"High Score: {high_score}",
            "Resume to keep playing or restart to try again.",
        ]

        popup = Popup(
            title="Paused",
            body_lines=body_lines,
            button_specs=[
                ("Resume", "RESUME", (34, 139, 34)),
                ("Restart", "RESTART", (30, 144, 255)),
                ("Quit", "EXIT", (200, 0, 0)),
            ],
            popup_width=360,
            padding=24,
        )

        popup.render(self.screen, self.button_manager)

    def draw_pause_button(self):
        """Draw the in-game HUD pause button."""
        self.hud_button_manager.clear()

        button_width, button_height = 120, 40
        padding = 20
        button_rect = (
            SCREEN_SIZE[0] - button_width - padding,
            padding,
            button_width,
            button_height,
        )

        self.hud_button_manager.add_button(
            rect=button_rect,
            label="Pause",
            action="PAUSE",
            color=(30, 144, 255),
            text_color=(255, 255, 255),
        )

        self.hud_button_manager.draw(self.screen, self._hud_button_font)
        self.hud_button_manager.set_cursor()

    def clear_hud_buttons(self):
        """Clear HUD buttons to avoid stale interactions when overlays are active."""
        if self.hud_button_manager.buttons:
            self.hud_button_manager.clear()

    def clear_popup_buttons(self):
        """Clear popup buttons when returning to gameplay."""
        if self.button_manager.buttons:
            self.button_manager.clear()

    def draw_level_info(self, level, lines_cleared, gravity_delay):
        """Render level, lines cleared, and gravity info.
        
        Args:
            level (int): Current level
            lines_cleared (int): Total lines cleared
            gravity_delay (int): Current gravity delay in frames
        """
        font = pygame.font.Font(None, 24)
        
        # Level display (top-left)
        level_text = font.render(f"Level: {level}", True, BLACK)
        self.screen.blit(level_text, (10, 10))

        # Lines cleared display (under level)
        lines_text = font.render(f"Lines: {lines_cleared}", True, BLACK)
        self.screen.blit(lines_text, (10, 35))

        # Gravity delay display (top-right)
        gravity_text = font.render(f"Gravity: {gravity_delay} frames", True, BLACK)
        gravity_rect = gravity_text.get_rect()
        gravity_rect.topright = (self.screen.get_width() - 10, 10)
        self.screen.blit(gravity_text, gravity_rect)
    def draw_ghost_piece(self, board, piece):
        """
        Render a semi-transparent 'ghost' outline of the active piece
        at its projected landing position.

        The ghost piece shows players where the current piece will lock
        if dropped straight down. It is drawn using a faded fill color
        and an outline to distinguish it from active pieces.

        Args:
            board (Board): The game board, used to calculate the landing
                position of the piece.
            piece (Piece): The active piece whose ghost projection should
                be rendered. Includes type, rotation, color, and current
                x/y position.
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