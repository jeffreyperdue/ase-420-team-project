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

# Global constants - it's OK as it's read only
# code smell - why list when tuple (immutable) is OK? Use immutable objects as much as possible
Colors = [
    (0, 0, 0), # We don't use this 
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# code smell - why use mutable list when tuple (immutable) is OK? Use immutable objects as much as possible
Figures = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]],
]
size = (400, 500)

# Global variables (code smell - we should remove them by refactoring)
Type = 0
Color = 0
Rotation = 0

# Game state
State = "start" # or "gameover"

# Encapsulated board instance (created in initialize)
GameBoard = None

# StartX/Y position in the screen
StartX = 100
StartY= 60

# Block size
Tzoom = 20 # code smell - bad name, can you guess Tzoom from its name? 

# Shift left/right or up/down
ShiftX = 0
ShiftY = 0

# code smell - global variable access, refactor to use
# parameters (if you use a function) or class fields (if you use a class)
def make_figure(x, y):
    global ShiftX, ShiftY, Type, Color, Rotation
    ShiftX = x
    ShiftY = y
    Type = random.randint(0, len(Figures) - 1)
    Color = random.randint(1, len(Colors) - 1)
    Rotation = 0

def intersects(image):
    intersection = False
    # code smell - what is 4? Magic number
    for i in range(4):
        for j in range(4):
            if i * 4 + j in image:
                # out of bounds
                # code smell - confusing, why Y is related i and X is related j?
                if GameBoard is None or \
                   (i + ShiftY) >= GameBoard.get_height() or \
                   (j + ShiftX) >= GameBoard.get_width() or \
                   (j + ShiftX) < 0 or \
                   GameBoard.get_cell(i + ShiftY, j + ShiftX) > 0:
                        intersection = True
    return intersection

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

def freeze(image):
    # code smell - can you guess what it does? why there is no comments on what it does, how, and why?
    global State

    piece_rows = figure_to_bitboard(image) # Convert figure to bitboard rows
    GameBoard.place_piece_rows(piece_rows, ShiftX, ShiftY, Color) # Place piece on the board
    GameBoard.clear_full_lines() # clear any filled lines
    make_figure(3, 0) # spawn a new piece at top
    
    if intersects(Figures[Type][Rotation]):
        State = "gameover"

def go_space():
    global ShiftY
    while not intersects(Figures[Type][Rotation]):
        ShiftY += 1
    ShiftY -= 1
    freeze(Figures[Type][Rotation])

def go_down():
    global ShiftY
    ShiftY += 1
    if intersects(Figures[Type][Rotation]):
        ShiftY -= 1 
        freeze(Figures[Type][Rotation])

def go_side(dx):
    global ShiftX
    old_x = ShiftX
    ShiftX += dx
    if intersects(Figures[Type][Rotation]):
        ShiftX = old_x

def rotate():
    global Rotation
    def rotate_figure():
        global Rotation
        Rotation = (Rotation + 1) % len(Figures[Type])
        
    old_rotation = Rotation
    rotate_figure()
    if intersects(Figures[Type][Rotation]):
        Rotation = old_rotation
        
def draw_board(screen, x, y, zoom):
    screen.fill(WHITE)

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
                                 [x + zoom * j + 1, y + zoom * i + 1, zoom - 2, zoom - 1])

def draw_figure(screen, image, startX, startY, shiftX, shiftY, zoom):
    for i in range(4):
        for j in range(4):
            p = i * 4 + j
            if p in image:
                pygame.draw.rect(screen, Colors[Color],
                                 [startX + zoom * (j + shiftX) + 1,
                                  startY + zoom * (i + shiftY) + 1,
                                  zoom - 2, zoom - 2])
            
def initialize():
    """Initialize game state and create empty board."""
    global GameBoard, State

    # Create an encapsulated GameBoard and initialize it
    GameBoard = Board()

    State = "start"
    
def main():
    # Pygame related init
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # we need pressing_down, fps, and counter to go_down() the Tetris Figure
    fps = 200
    counter = 0
    pressing_down = False

    initialize()
    make_figure(3,0)
    done = False
    level = 1
    while not done:
        counter += 1
        if counter > 100000:
            counter = 0
            
        # Check if we need to automatically go down
        if counter % (fps // 2 // level) == 0 or pressing_down: 
            if State == "start":
                go_down()

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
                
        draw_board(screen, StartX, StartY, Tzoom)
        
        # code smell - how many values duplication Figures[Type][Rotation]
        draw_figure(screen, Figures[Type][Rotation], StartX, StartY, ShiftX, ShiftY, Tzoom)

        if State == "gameover":
            done = True

        # refresh the screen
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()