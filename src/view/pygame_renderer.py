import pygame
from src.constants import COLORS, CELL_SIZE, WHITE, GRAY, BLACK, NEXT_PAGE_PREVIEW_RECT
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

        # Calculate bounding box of the shape to center it properly
        cols = [grid_position % 4 for grid_position in shape]
        rows = [grid_position // 4 for grid_position in shape]
        
        min_col = min(cols)
        max_col = max(cols)
        min_row = min(rows)
        max_row = max(rows)
        
        # Calculate width and height of the piece
        piece_width = max_col - min_col + 1
        piece_height = max_row - min_row + 1
        
        # Calculate offset to center the piece in the preview box
        # Preview box is NEXT_PAGE_PREVIEW_RECT = [290, 200, 150, 150]
        # We want to center it in a ~4x4 cell area
        preview_center_x = 290 + 150 // 2  # center x of preview box
        preview_center_y = 200 + 150 // 2  # center y of preview box
        
        # Calculate the offset needed to center this specific piece
        offset_x = (4 - piece_width) / 2 - min_col
        offset_y = (4 - piece_height) / 2 - min_row

        for grid_position in shape:
            # Convert 4x4 grid position to preview box coordinates
            col = (grid_position % 4) + offset_x
            row = (grid_position // 4) + offset_y
            
            # Calculate position relative to the preview box center
            rect = [
                preview_center_x - (2 * CELL_SIZE) + (col * CELL_SIZE),
                preview_center_y - (2 * CELL_SIZE) + (row * CELL_SIZE),
                CELL_SIZE - 1,
                CELL_SIZE - 1
            ]

            pygame.draw.rect(self.screen, color, rect)