"""
Unit tests for the Linked List class edge cases.

To run these tests from the repository root:
  python -m unittest tests/test_linked_list_edge_cases.py         # Simple run
  python -m unittest -v tests/test_linked_list_edge_cases.py      # Verbose output
    
To run a specific test:
  python -m unittest tests.test_linked_list_edge_cases.TestLinkedListEdgeCases.test_append_none_raises
"""

import os
import sys
import unittest

# Add repo root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
  sys.path.insert(0, repo_root)

from src.utils.linked_list import LinkedList


class TestLinkedListEdgeCases(unittest.TestCase):
  def setUp(self):
    self.ll = LinkedList()

  def test_append_none_raises(self):
    with self.assertRaises(ValueError):
      self.ll.append(None)

  def test_insert_top_none_raises(self):
    with self.assertRaises(ValueError):
      self.ll.insert_top(None)

  def test_get_node_invalid_index_raises(self):
    self.ll.append('x')
    with self.assertRaises(IndexError):
      _ = self.ll.get_node_at(5)

  def test_delete_node_invalid_index_raises(self):
    self.ll.append('x')
    with self.assertRaises(IndexError):
      self.ll.delete_node(5)

  def test_delete_node_from_empty_list_raises(self):
    with self.assertRaises(IndexError):
      self.ll.delete_node(0)


if __name__ == '__main__':
  unittest.main()