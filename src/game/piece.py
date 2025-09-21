import random
import src.constants as constants

class Piece:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(constants.FIGURES) - 1) # pick random shape
        self.color = random.randint(1, len(constants.COLORS) - 1) # pick random color
        self.rotation = 0 # start unrotated

    def intersects(self, field):
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

    # Locks piece in place after landing and spawns new piece
    def freeze(self, field, gameOver):
        for row in range(constants.GRID_SIZE):
            for col in range(constants.GRID_SIZE):
                index = row * constants.GRID_SIZE + col

                if index in self.rotation:
                    field_row = row + self.y
                    field_col = col + self.x
                    field[field_row][field_col] = self.color
        # TODO: Still need to implement this method in figures.py
        field.break_lines()

        newPiece = Piece(x=constants.START_X, y=constants.START_Y)
        # Ending game if new piece immediately intersects
        if newPiece.intersects(field):
            gameOver = True

    def go_space(self, field):
        while not self.intersects(field):
            self.y += 1
        self.y -= 1
        self.freeze(field)
    
    def go_down(self, field):
        self.y += 1
        if self.intersects():
            self.y -= 1
            self.freeze(field)
    
    def go_side(self, x_movement, field):
        oldX = self.x
        self.x += x_movement
        if self.intersects(field):
            self.x = oldX
    
    def rotate(self, field):
        oldRotation = self.rotation
        self.rotation = (self.rotation + 1) % len(constants.FIGURES[self.type])
        if self.intersects(field):
            self.rotation = oldRotation