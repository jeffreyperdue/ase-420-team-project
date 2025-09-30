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

# ===========================
# COLORS
# ===========================
# These are RGB values (Red, Green, Blue) that define colors.
# Each value is from 0–255.
# Colors is a list we use to paint Tetris blocks.
Colors = [
    (0, 0, 0),      # Black, not used for blocks
    (120, 37, 179), # Purple
    (100, 179, 179),# Teal
    (80, 34, 22),   # Brown
    (80, 134, 22),  # Green
    (180, 34, 22),  # Red
    (180, 34, 122), # Pink
]

# Some extra named colors for drawing background/lines
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY  = (128, 128, 128)

# ===========================
# FIGURES (Tetris shapes)
# ===========================
# Each figure is described using a 4x4 mini-grid (16 positions).
# Example: position = row*4 + column
# If the number is in the list, that square is filled.
# Each shape has several rotations.
Figures = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],                # I shape (line)
    [[4, 5, 9, 10], [2, 6, 5, 9]],                # Z shape
    [[6, 7, 9, 10], [1, 5, 6, 10]],               # S shape
    [[1, 2, 5, 9], [0, 4, 5, 6],                  # L shape (and its rotations)
     [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9],                 # J shape (and its rotations)
     [2, 6, 10, 11], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9],                  # T shape (and its rotations)
     [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]],                               # O shape (square, only 1 rotation)
]

# Window size in pixels
size = (400, 500)

# ===========================
# GAME STATE VARIABLES
# ===========================
# These globals hold the current piece, board, and game status.

Type     = 0  # Which figure type is falling
Color    = 0  # Which color is used
Rotation = 0  # Which rotation is used

State = "start" # Game state: "start" (playing) or "gameover"

# Where on the screen to start drawing the board
StartX = 100
StartY = 60

# Size of each block (in pixels)
Tzoom = 20

# Current piece’s position on the grid
ShiftX = 0  # left/right
ShiftY = 0  # up/down

# Encapsulated Board (created in initialize)
GameBoard = None

# ===========================
# PIECE CREATION
# ===========================
def make_figure(x, y):
    """Create a new random piece at position (x,y)."""
    global ShiftX, ShiftY, Type, Color, Rotation
    ShiftX = x
    ShiftY = y
    Type   = random.randint(0, len(Figures) - 1) # pick random shape
    Color  = random.randint(1, len(Colors) - 1)  # pick random color
    Rotation = 0                                 # start unrotated

# Board implementation moved to `src/game/board.py`

# ===========================
# COLLISION DETECTION
# ===========================
def intersects(image):
    """Check if the current piece (image) collides with the board or walls."""
    intersection = False
    # code smell - what is 4? Magic number
    for i in range(4):              # rows in 4x4 mini-grid
        for j in range(4):          # columns in 4x4 mini-grid
            if i * 4 + j in image: # if this square is part of the shape
                # Check boundaries and if cell is already filled
                if GameBoard is None or \
                   (i + ShiftY) >= GameBoard.get_height() or \
                   (j + ShiftX) >= GameBoard.get_width() or \
                   (j + ShiftX) < 0 or \
                   GameBoard.get_cell(i + ShiftY, j + ShiftX) > 0:
                        intersection = True
    return intersection

# =============================
# FIGURE TO BITBOARD CONVERSION
# =============================
def figure_to_bitboard(image):
    """
    Convert a flat 4x4 shape representation into bitboard rows.

    Args:
        image (list[int]): A list of indices (0–15) representing filled cells in a 4x4 grid.

    Returns:
        list[int]: A list of 4 integers, each representing a row in bitboard format.
        Example: [0b0000, 0b1110, 0b0100, 0b0000] for a T shape
    """

    rows = [0] * 4 # Initialize 4 empty rows (bitboards)
    for index in image:
        row, col = divmod(index, 4) # Convert flat index to its corresponding (row, column) coordinates
        rows[row] |= (1 << col) # Set the bit at col in row
    return rows # Return the 4-row bitboard representation

# ===========================
# FREEZE (lock piece in place)
# ===========================
def freeze(image):
    # code smell - can you guess what it does? why there is no comments on what it does, how, and why?
    global State
    
    piece_rows = figure_to_bitboard(image) # Convert figure to bitboard rows
    GameBoard.place_piece_rows(piece_rows, ShiftX, ShiftY, Color) # Place piece on the board
    GameBoard.clear_full_lines() # clear any filled lines
    make_figure(3, 0) # spawn a new piece at top

    # If new piece immediately collides, game is over
    if intersects(Figures[Type][Rotation]):
        State = "gameover"

# ===========================
# MOVEMENT
# ===========================
def go_space():
    """Hard drop: move piece straight down until it hits."""
    global ShiftY
    while not intersects(Figures[Type][Rotation]):
        ShiftY += 1
    ShiftY -= 1
    freeze(Figures[Type][Rotation])

def go_down():
    """Soft drop: move piece down by 1 row (gravity)."""
    global ShiftY
    ShiftY += 1
    if intersects(Figures[Type][Rotation]):
        ShiftY -= 1 
        freeze(Figures[Type][Rotation])

def go_side(dx):
    """Move piece left (dx=-1) or right (dx=+1)."""
    global ShiftX
    old_x = ShiftX
    ShiftX += dx
    if intersects(Figures[Type][Rotation]):
        ShiftX = old_x  # undo move if collides

def rotate():
    """Rotate piece clockwise if possible."""
    global Rotation
    old_rotation = Rotation
    Rotation = (Rotation + 1) % len(Figures[Type])
    if intersects(Figures[Type][Rotation]):
        Rotation = old_rotation  # undo if collides

# ===========================
# DRAWING FUNCTIONS
# ===========================
def draw_board(screen, x, y, zoom):
    """Draw the playing field and placed blocks."""
    screen.fill(WHITE) # clear background

    # Draw using GameBoard
    if GameBoard is None:
        return
    for i in range(GameBoard.get_height()):
        for j in range(GameBoard.get_width()):
            # draw grid outline
            pygame.draw.rect(screen, GRAY, [x + zoom * j, y + zoom * i, zoom, zoom], 1)
            
            # draw filled block if > 0
            val = GameBoard.get_cell(i, j)
            if val > 0:
                pygame.draw.rect(screen, Colors[val],
                                    [x + zoom * j + 1, y + zoom * i + 1,
                                    zoom - 2, zoom - 1])

def draw_figure(screen, image, x, y, shift_x, shift_y, zoom):
    """Draw the current falling piece."""
    for i in range(4):
        for j in range(4):
            p = i * 4 + j
            if p in image: # if part of shape
                pygame.draw.rect(screen, Colors[Color],
                                 [x + zoom * (j + shift_x) + 1,
                                  y + zoom * (i + shift_y) + 1,
                                  zoom - 2, zoom - 2])

# ===========================
# INITIALIZATION
# ===========================
def initialize():
    """Initialize game state and create empty board."""
    global State, GameBoard

    # Create an encapsulated GameBoard and initialize it
    GameBoard = Board()
    
    State  = "start"

# ===========================
# MAIN GAME LOOP
# ===========================
def main():
    # Setup pygame window
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # Game control variables
    fps = 200           # frames per second (speed)
    counter = 0
    pressing_down = False

    # Start game
    initialize()
    make_figure(3, 0)   # spawn first piece
    done = False
    level = 1

    # Main loop
    while not done:
        counter += 1
        if counter > 100000: # reset counter if too large
            counter = 0
            
        # Gravity: piece falls every few ticks or when holding down key
        if counter % (fps // 2 // level) == 0 or pressing_down: 
            if State == "start":
                go_down()

        # Handle keyboard and quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rotate()
                if event.key == pygame.K_LEFT:
                    go_side(-1)
                if event.key == pygame.K_RIGHT:
                    go_side(1)
                if event.key == pygame.K_SPACE:
                    go_space()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                pressing_down = False
                
        # Draw everything
        draw_board(screen, StartX, StartY, Tzoom)
        draw_figure(screen, Figures[Type][Rotation],
                    StartX, StartY, ShiftX, ShiftY, Tzoom)

        # End game if state says gameover
        if State == "gameover":
            done = True

        # Refresh screen
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

# Run if file is executed directly
if __name__ == "__main__":
    main()