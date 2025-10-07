# Define the shapes of the Tetris pieces in each rotation
# Represented as tuples of grid positions in a 4x4 matrix
I_SHAPE = ((1, 5, 9, 13), (4, 5, 6, 7))
Z_SHAPE = ((4, 5, 9, 10), (2, 6, 5, 9))
S_SHAPE = ((6, 7, 9, 10), (1, 5, 6, 10))
L_SHAPE = ((1, 2, 5, 9), (0, 4, 5, 6), (1, 5, 9, 8), (4, 5, 6, 10))
J_SHAPE = ((1, 2, 6, 10), (5, 6, 7, 9), (2, 6, 10, 11), (3, 5, 6, 7))
T_SHAPE = ((1, 4, 5, 6), (1, 4, 5, 9), (4, 5, 6, 9), (1, 5, 6, 9))
O_SHAPE = ((1, 2, 5, 6),)

SHAPES = (
I_SHAPE,
Z_SHAPE,
S_SHAPE,
L_SHAPE,
J_SHAPE,
T_SHAPE,
O_SHAPE,
)