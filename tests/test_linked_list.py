import os
import sys
import unittest

# Add repo root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from src.utils.linked_list import LinkedList


class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.ll = LinkedList()

    def test_append_and_length(self):
        self.assertEqual(self.ll.length(), 0)
        self.ll.append(1)
        self.ll.append(2)
        self.ll.append(3)
        self.assertEqual(self.ll.length(), 3)

    def test_insert_top_and_get_node(self):
        self.ll.append('a')
        self.ll.append('b')
        self.ll.insert_top('top')
        self.assertEqual(self.ll.length(), 3)
        node = self.ll.get_node_at(0)
        self.assertIsNotNone(node)
        self.assertEqual(node.value, 'top')

    def test_delete_node(self):
        self.ll.append(10)
        self.ll.append(20)
        self.ll.append(30)
        self.assertEqual(self.ll.length(), 3)
        self.ll.delete_node(1)  # remove middle
        self.assertEqual(self.ll.length(), 2)
        # Ensure values are 10 and 30 now
        self.assertEqual(self.ll.get_node_at(0).value, 10)
        self.assertEqual(self.ll.get_node_at(1).value, 30)


if __name__ == '__main__':
    unittest.main()
