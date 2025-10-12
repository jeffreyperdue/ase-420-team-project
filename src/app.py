from src.game.game import Game
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row

def main():
    # Create board
    board = Board(lambda: Row(10))  # 10 = WIDTH from constants
    
    # Create piece generator (you'll need this)
    # piece_generator = PieceGenerator()
    
    # Create and run game
    game = Game(board, piece_generator)
    game.run()

if __name__ == "__main__":
    main()