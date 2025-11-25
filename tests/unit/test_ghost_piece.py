from tests.fixtures.test_helpers import create_test_board, create_test_piece
from src.constants import HEIGHT


def test_get_landing_y_for_o_piece_on_empty_board():
    board = create_test_board()

    # Create an O piece (square) which has relative bottom offset of 1
    piece = create_test_piece(x=None, y=0, piece_type=6, color=1)

    landing_y = board.get_landing_y(piece)

    # For an empty board, the O piece should land so its bottom row is at index HEIGHT-1
    # Therefore landing_y == HEIGHT - 2
    assert landing_y == HEIGHT - 2
