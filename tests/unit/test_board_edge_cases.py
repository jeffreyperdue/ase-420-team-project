"""
Unit tests for the Board class edge cases.

To run these tests from the repository root:
  python -m unittest tests/test_board_edge_cases.py         # Simple run
  python -m unittest -v tests/test_board_edge_cases.py      # Verbose output
    
To run a specific test:
  python -m unittest tests.test_board_edge_cases.TestBoard.test_invalid_dimensions_raise
"""

import os
import sys
import unittest

# Add repo root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
  sys.path.insert(0, repo_root)

from src.game.board import Board
from src.game.piece import Piece
from src.constants import HEIGHT, WIDTH


def simple_row_factory():
  from src.game.row import Row
  return Row(3)


class TestBoardEdgeCases(unittest.TestCase):
  def test_invalid_dimensions_raise(self):
    with self.assertRaises(ValueError):
      Board(simple_row_factory, height=0, width=3)
    with self.assertRaises(ValueError):
      Board(simple_row_factory, height=3, width=0)

  def test_invalid_row_factory_raises(self):
    with self.assertRaises(TypeError):
      Board(None, height=3, width=3)

  def test_get_cell_row_out_of_range_raises(self):
    b = Board(simple_row_factory, height=3, width=3)
    with self.assertRaises(IndexError):
      b.get_cell(5, 1)

  def test_get_cell_col_out_of_range_raises(self):
    b = Board(simple_row_factory, height=3, width=3)
    with self.assertRaises(IndexError):
      b.get_cell(1, 5)
  
  def setUp(self):
    from src.game.row import Row
    self.board = Board(lambda: Row(WIDTH), height=HEIGHT, width=WIDTH)
    self.color = 1  # Use integer color value for testing

  def test_boundary_index_access(self):
    with self.assertRaises(IndexError):
      self.board.get_cell(-1, 0)
    with self.assertRaises(IndexError):
      self.board.get_cell(HEIGHT, WIDTH)
    with self.assertRaises(IndexError):
      self.board.set_cell(-1, 0, self.color)
    with self.assertRaises(IndexError):
      self.board.set_cell(HEIGHT, WIDTH, self.color)

  def test_bitmask_edge_behavior(self):
    self.board.set_cell(0, WIDTH - 1, self.color)
    self.assertTrue(self.board.get_cell(0, WIDTH - 1))  # Top-right corner

    self.board.set_cell(HEIGHT - 1, 0, self.color)
    self.assertTrue(self.board.get_cell(HEIGHT - 1, 0))  # Bottom-left corner

  def test_empty_board_after_clear_full_lines(self):
    for row in range(HEIGHT):
      for col in range(WIDTH - 1):
        self.board.set_cell(row, col, self.color)
    self.board.clear_full_lines()
    self.assertEqual(self.board.height, HEIGHT)

  def test_all_rows_full(self):
    for row in range(HEIGHT):
      for col in range(WIDTH):
        self.board.set_cell(row, col, self.color)
    self.board.clear_full_lines()
    self.assertEqual(self.board.height, HEIGHT)
    for row in range(HEIGHT):
      for col in range(WIDTH):
        self.assertFalse(self.board.get_cell(row, col))

  def test_alternating_full_and_empty_rows(self):
    for row in range(0, HEIGHT, 2):
      for col in range(WIDTH):
        self.board.set_cell(row, col, self.color)
    self.board.clear_full_lines()
    self.assertEqual(self.board.height, HEIGHT)

  def test_linkedlist_length_integrity(self):
    self.board.clear_full_lines()
    self.assertEqual(self.board.height, HEIGHT)

  def test_color_preservation(self):
    self.board.set_cell(3, 4, self.color)
    self.assertTrue(self.board.get_cell(3, 4))

  def test_multiple_clears_in_succession(self):
    for row in range(HEIGHT):
      for col in range(WIDTH):
        self.board.set_cell(row, col, self.color)
    self.board.clear_full_lines()
    self.board.clear_full_lines()
    for row in range(HEIGHT):
      for col in range(WIDTH):
        self.assertFalse(self.board.get_cell(row, col))

  def test_clear_after_manual_clear(self):
    self.board.clear()
    self.board.clear_full_lines()
    for row in range(HEIGHT):
      for col in range(WIDTH):
        self.assertFalse(self.board.get_cell(row, col))

  def test_stub_method_behavior(self):
    # Test that the Board class has the expected collision detection method
    piece = Piece(0, 0)
    collision_result = self.board.will_piece_collide(piece)
    self.assertIsInstance(collision_result, bool)


if __name__ == '__main__':
  unittest.main()
