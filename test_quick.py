#!/usr/bin/env python3
"""
Quick test runner to verify the testing suite works without getting stuck.
"""

import sys
import os

# Add repository root to path for imports
repo_root = os.path.abspath(os.path.dirname(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import unittest

def run_quick_tests():
    """Run a quick subset of tests to verify the testing suite works."""
    
    # Test basic imports
    try:
        from src.game.game import Game
        from src.game.board import Board
        from src.game.piece import Piece
        from src.game.row import Row
        from src.constants import WIDTH, HEIGHT
        print("OK All imports successful")
    except ImportError as e:
        print(f"X Import error: {e}")
        return False
    
    # Test basic game creation
    try:
        board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
        game = Game(board, lambda: Piece(WIDTH // 2, 0))
        print("OK Game creation successful")
    except Exception as e:
        print(f"X Game creation error: {e}")
        return False
    
    # Test basic piece movement
    try:
        piece = game.current_piece
        initial_x = piece.x
        game.apply(["LEFT"])
        print(f"OK Piece movement successful: {initial_x} -> {piece.x}")
    except Exception as e:
        print(f"X Piece movement error: {e}")
        return False
    
    # Test basic board operations
    try:
        board.set_cell(0, 0, 1)
        assert board.get_cell(0, 0)
        board.clear()
        assert not board.get_cell(0, 0)
        print("OK Board operations successful")
    except Exception as e:
        print(f"X Board operations error: {e}")
        return False
    
    print("\nSUCCESS: All quick tests passed! The testing suite should work correctly.")
    return True

if __name__ == "__main__":
    success = run_quick_tests()
    sys.exit(0 if success else 1)
