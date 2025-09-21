import random
import src.constants as constants

class Piece:
    """
    Represents a falling piece in the game grid.

    Attributes:
        x (int): X-coordinate on the game grid.
        y (int): Y-coordinate on the game grid.
        type (int): Index of the shape from constants.FIGURES.
        color (int): Index of the color from constants.COLORS.
        rotation (int): Current rotation index for the shape.
    """


    def __init__(self, x, y):
        """
        Initializes a new piece with a random shape and color at the given (x, y) position.

        Args:
            x (int): Initial X position.
            y (int): Initial Y position.
        """

        self.x = x
        self.y = y
        self.type = random.randint(0, len(constants.FIGURES) - 1) # pick random shape
        self.color = random.randint(1, len(constants.COLORS) - 1) # pick random color
        self.rotation = 0 # start unrotated

    def intersects(self, field):
        """
        Checks whether the piece intersects with anything on the game field.

        Args:
            field: The game field grid.

        Returns:
            bool: True if piece intersects (collides) with the field or boundaries.
        """

        for row in range(constants.GRID_SIZE):
            for col in range(constants.GRID_SIZE):
                index = row * constants.GRID_SIZE + col

                if index in self.rotation:
                    field_row = row + self.y
                    field_col = col + self.x

                    if (
                        field_row >= field.height or
                        field_col >= field.width or
                        field_col < 0 or
                        field[field_row][field_col] > 0
                    ):
                        return True

        return False

    def freeze(self, field):
        """
        Locks the piece into the game field and spawns a new one.
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
        # TODO: Still need to implement this method in figures.py
        # Attempt to break completed lines
        field.break_lines()

        # End game if new piece collides immediately
        newPiece = Piece(x=constants.START_X, y=constants.START_Y)
        
        # Ending game if new piece immediately intersects
        if newPiece.intersects(field):
            field.game_over = True

    def go_space(self, field):
        """
        Drops the piece straight down until it collides, then freezes it.

        Args:
            field: The game field grid.
        """

        while not self.intersects(field):
            self.y += 1
        self.y -= 1
        self.freeze(field)
    
    def go_down(self, field):
        """
        Moves the piece one row down. If it collides, revert and freeze it.

        Args:
            field: The game field grid.
        """

        self.y += 1
        if self.intersects():
            self.y -= 1
            self.freeze(field)
    
    def go_side(self, x_movement, field):
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
    
    def rotate(self, field):
        """
        Rotates the piece clockwise. If rotation causes collision, reverts it.

        Args:
            field: The game field grid.
        """

        oldRotation = self.rotation
        self.rotation = (self.rotation + 1) % len(constants.FIGURES[self.type])
        if self.intersects(field):
            self.rotation = oldRotation