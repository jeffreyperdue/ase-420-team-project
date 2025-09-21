import random
import src.constants as constants

class Piece:


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(constants.FIGURES) - 1) # pick random shape
        self.color = random.randint(1, len(constants.COLORS) - 1) # pick random color
        self.rotation = 0 # start unrotated