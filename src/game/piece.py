import random
import src.constants as constants
import src.figures as figures

class Piece:
    """
    Represents a falling piece in the game grid.

    Attributes:
        x (int): X-coordinate on the game grid.
        y (int): Y-coordinate on the game grid.
        type (int): Index of the shape from figures.SHAPES.
        color (int): Index of the color from constants.COLORS.
        rotation (int): Current rotation index for the shape.
    """


    def __init__(self, x, y) -> None:
        """
        Initializes a new piece with a random shape and color at the given (x, y) position.

        Args:
            x (int): Initial X position.
            y (int): Initial Y position.
        """

        self.x = x
        self.y = y
        self.type = random.randint(0, len(figures.SHAPES) - 1) # pick random shape
        self.color = random.randint(1, len(constants.COLORS) - 1) # pick random color
        self.rotation = 0 # start unrotated