"""
Tetris Game - Version 1
A complete Tetris implementation using object-oriented design with Board, Piece, and Row classes.

Controls:
- Arrow keys: Move and rotate pieces
- Space: Drop piece instantly
- Down arrow: Fast drop
"""

import pygame
import os
import sys

# Ensure repository root is on sys.path so imports work when running from starter_code
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Import classes and constants
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row
import src.constants as constants
import src.figures as figures

# Constants
COLORS = constants.COLORS
BLACK = constants.BLACK
WHITE = constants.WHITE
GRAY = constants.GRAY
SCREEN_SIZE = constants.SCREEN_SIZE
CELL_SIZE = constants.CELL_SIZE
FPS = constants.FPS

# Game state variables
game_state = "start"
game_board = None
current_piece = None

# Display settings
BOARD_X = 100
BOARD_Y = 60

# Game timing control
piece_moved_this_frame = False
down_key_just_pressed = False


def spawn_new_piece():
    """Create a new piece at the starting position."""
    global current_piece
    current_piece = Piece(constants.START_X, constants.START_Y)
    
    # Check if the new piece immediately collides (game over condition)
    if game_board.will_piece_collide(current_piece):
        return False  # Game over
    return True


def freeze_current_piece():
    """Freeze the current piece in place and spawn a new one."""
    global game_state
    
    # Permanently place the current piece on the board
    if not game_board.freeze_piece(current_piece):
        game_state = "gameover"
        return
        
    game_board.clear_full_lines()  # Clear any full lines
    
    # Try to spawn a new piece
    if not spawn_new_piece():
        game_state = "gameover"


def reset_fall_timer():
    """Reset the fall timer to ensure new pieces start falling immediately."""
    global counter
    counter = 0
        
def draw_board(screen, x, y, zoom):
    """Draw the game board with all placed pieces."""
    screen.fill(WHITE)

    if game_board is None:
        return
        
    for i in range(game_board.height):
        for j in range(game_board.width):
            # Draw grid outline
            pygame.draw.rect(screen, GRAY, [x + zoom * j, y + zoom * i, zoom, zoom], 1)
            
            # Draw filled block if occupied
            if game_board.get_cell(i, j):
                color = game_board.get_cell_color(i, j)
                if color is not None and color < len(COLORS):
                    pygame.draw.rect(screen, COLORS[color],
                                    [x + zoom * j + 1, y + zoom * i + 1, zoom - 2, zoom - 1])


def draw_piece(screen, piece, start_x, start_y, zoom):
    """Draw the current falling piece."""
    if piece is None:
        return
        
    shape = figures.SHAPES[piece.type][piece.rotation]
    for grid_position in shape:
        # Convert grid position to coordinates
        row, col = divmod(grid_position, 4)
        draw_x = start_x + zoom * (col + piece.x)
        draw_y = start_y + zoom * (row + piece.y)
        
        pygame.draw.rect(screen, COLORS[piece.color],
                         [draw_x + 1, draw_y + 1, zoom - 2, zoom - 2])


def initialize():
    """Initialize game state and create empty board."""
    global game_board, game_state

    # Create game board
    game_board = Board(lambda: Row(constants.WIDTH))
    game_state = "start"
    
    # Spawn the first piece
    spawn_new_piece()
    
def main():
    """Main game loop."""
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # Game timing variables
    counter = 0
    pressing_down = False
    level = 1

    # Initialize the game
    initialize()
    
    done = False
    while not done:
        # Reset movement flags at the start of each frame
        global piece_moved_this_frame, down_key_just_pressed
        piece_moved_this_frame = False
        down_key_just_pressed = False
        
        counter += 1
        if counter > 100000:
            counter = 0
            
        # Automatic piece movement
        if counter % (FPS // 2 // level) == 0 and not piece_moved_this_frame: 
            if game_state == "start" and current_piece is not None:
                moved = game_board.go_down(current_piece)
                piece_moved_this_frame = True
                if not moved:
                    freeze_current_piece()
                    reset_fall_timer()
        
        # Manual down movement (faster when down key is pressed)
        elif (pressing_down and counter % max(1, FPS // 15) == 0) or down_key_just_pressed:
            if game_state == "start" and current_piece is not None and not piece_moved_this_frame:
                moved = game_board.go_down(current_piece)
                piece_moved_this_frame = True
                if not moved:
                    freeze_current_piece()
                    reset_fall_timer()

        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN and current_piece is not None and game_state == "start":
                if event.key == pygame.K_UP:
                    game_board.rotate(current_piece)
                elif event.key == pygame.K_LEFT:
                    game_board.go_side(-1, current_piece)
                elif event.key == pygame.K_RIGHT:
                    game_board.go_side(1, current_piece)
                elif event.key == pygame.K_SPACE:
                    game_board.go_space(current_piece)
                    freeze_current_piece()
                    reset_fall_timer()
                elif event.key == pygame.K_DOWN:
                    pressing_down = True
                    down_key_just_pressed = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                pressing_down = False
                
        # Draw everything
        draw_board(screen, BOARD_X, BOARD_Y, CELL_SIZE)
        
        # Draw the current falling piece
        if current_piece is not None and game_state == "start":
            draw_piece(screen, current_piece, BOARD_X, BOARD_Y, CELL_SIZE)

        # Check for game over
        if game_state == "gameover":
            done = True

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()