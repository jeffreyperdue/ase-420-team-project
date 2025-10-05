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
        self.color = random.randint(0, len(constants.COLORS) - 1) # pick random color
        self.rotation = 0 # start unrotated

    def freeze(self, field) -> None:
        """
        Locks the piece into the game field and spawns a new one..
        
        Also checks for game over condition.

        Args:
            field: The game field grid.
        """


        for row in range(constants.GRID_SIZE):
            for col in range(constants.GRID_SIZE):
                index = row * constants.GRID_SIZE + col

                if index in self.rotation:
                    field_row = row + self.y
                    field_col = col + self.x
                    field[field_row][field_col] = self.color
        # Attempt to break completed lines
        field.break_lines()

        # End game if new piece collides immediately
        newPiece = Piece(x=constants.START_X, y=constants.START_Y)
        
        # Ending game if new piece immediately intersects
        if newPiece.intersects(field):
            field.game_over = True

    def go_space(self, field) -> None:
        """
        Drops the piece straight down until it collides, then freezes it.

        Args:
            field: The game field grid.
        """

        while not self.intersects(field):
            self.y += 1
        self.y -= 1
        self.freeze(field)
    
    def go_down(self, field) -> None:
        """
        Moves the piece one row down. If it collides, revert and freeze it.

        Args:
            field: The game field grid.
        """

        self.y += 1
        if self.intersects():
            self.y -= 1
            self.freeze(field)

    def go_side(self, x_movement, field) -> None:
        """
        Moves the piece left or right, reverting if it causes a collision.

        Args:
            x_movement (int): Movement in X direction (-1 for left, 1 for right).
            field: The game field grid.
        """

        oldX = self.x
        self.x += x_movement
        if self.intersects(field):
            self.x = oldX

    def rotate(self, field) -> None:
        """
        Rotates the piece clockwise. If rotation causes collision, reverts it.

        Args:
            field: The game field grid.
        """

        oldRotation = self.rotation
        self.rotation = (self.rotation + 1) % len(figures.SHAPES[self.type])
        if self.intersects(field):
            self.rotation = oldRotation