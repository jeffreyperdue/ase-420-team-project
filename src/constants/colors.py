"""Constants for game colors and style."""

import pygame

# Basic colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Piece colors
COLORS = [
    (0, 255, 0),     # Green - I piece
    (255, 0, 0),     # Red - J piece
    (0, 0, 255),     # Blue - L piece
    (255, 255, 0),   # Yellow - O piece
    (0, 255, 255),   # Cyan - S piece
    (255, 0, 255),   # Magenta - T piece
    (255, 128, 0),   # Orange - Z piece
]

# Preview box
NEXT_PAGE_PREVIEW_RECT = pygame.Rect(300, 180, 150, 180)  # x, y, width, height