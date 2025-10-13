import pygame
import random
import os
import sys

# Ensure repository root is on sys.path so imports work when running from starter_code
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Import Board class from src/game/board.py
from src.game.board import Board
# Import Piece class from src/game/piece.py
from src.game.piece import Piece
# Import global constants
import src.constants as constants
import src.figures as figures

# Use constants from the constants module
Colors = constants.COLORS
BLACK = constants.BLACK
WHITE = constants.WHITE
GRAY = constants.GRAY
size = constants.SCREEN_SIZE

# Game state
game_state = "start"  # or "gameover"

# Encapsulated board instance (created in initialize)
game_board = None
current_piece = None

# StartX/Y position in the screen
start_x = 100
start_y = 60

# Block size
cell_size = constants.CELL_SIZE

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
        
def draw_board(screen, x, y, zoom):
    """Draw the game board with all placed pieces."""
    screen.fill(WHITE)

    # Draw using game_board
    if game_board is None:
        return
    for i in range(game_board.height):
        for j in range(game_board.width):
            # draw grid outline
            pygame.draw.rect(screen, GRAY, [x + zoom * j, y + zoom * i, zoom, zoom], 1)
            
            # draw filled block if occupied
            if game_board.get_cell(i, j):
                color = game_board.get_cell_color(i, j)
                if color is not None and color < len(Colors):
                    pygame.draw.rect(screen, Colors[color],
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
        
        pygame.draw.rect(screen, Colors[piece.color],
                         [draw_x + 1, draw_y + 1, zoom - 2, zoom - 2])
            
def initialize():
    """Initialize game state and create empty board."""
    global game_board, game_state

    # Create an encapsulated game_board and initialize it
    from src.game.row import Row
    game_board = Board(lambda: Row(constants.WIDTH))

    game_state = "start"
    
    # Spawn the first piece
    spawn_new_piece()
    
def main():
    # Pygame related init
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # Game timing variables
    fps = constants.FPS
    counter = 0
    pressing_down = False
    level = 1

    # Initialize the game
    initialize()
    
    done = False
    while not done:
        counter += 1
        if counter > 100000:
            counter = 0
            
        # Check if we need to automatically move piece down
        if counter % (fps // 2 // level) == 0 or pressing_down: 
            if game_state == "start" and current_piece is not None:
                # Try to move piece down
                moved = game_board.go_down(current_piece)
                if not moved:  # Piece was placed, spawn new one
                    freeze_current_piece()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if current_piece is not None and game_state == "start":
                    if event.key == pygame.K_UP:
                        game_board.rotate(current_piece)
                    if event.key == pygame.K_LEFT:
                        game_board.go_side(-1, current_piece)
                    if event.key == pygame.K_RIGHT:
                        game_board.go_side(1, current_piece)
                    if event.key == pygame.K_SPACE:
                        game_board.go_space(current_piece)
                        freeze_current_piece()
                    if event.key == pygame.K_DOWN:
                        pressing_down = True

            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                pressing_down = False
                
        # Draw everything
        draw_board(screen, start_x, start_y, cell_size)
        
        # Draw the current falling piece (but don't place it permanently)
        if current_piece is not None and game_state == "start":
            draw_piece(screen, current_piece, start_x, start_y, cell_size)

        # Check for game over
        if game_state == "gameover":
            done = True

        # Refresh the screen
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()