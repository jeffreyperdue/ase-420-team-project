class Node:
    """Represents a single node in a linked list, holding a value and a reference to the next node."""

    def __init__(self, value, next=None):
        self.value = value  # The data stored in this node (e.g., a Row object)
        self.next = next    # Reference to the next node in the list (or None if it's the last node)

class LinkedList:
    """A singly linked list used to store rows of the game board."""

    def __init__(self):
        self.head = None    # Reference to first node in the list

    def length(self) -> int:
      """Returns the number of nodes in the linked list."""

      count = 0             # Initialize counter
      curr = self.head      # Start at the head node
      while curr:           # Traverse until the end
          count += 1        # Increment for each node
          curr = curr.next  # Move to the next node
      return count          # Return total count

    def append(self, value) -> None:
        """Adds a new node with the given value to the end of the list."""

        if not self.head:           # If list is empty
            self.head = Node(value) # Create the first (head) node
        else:
            curr = self.head        # Start at head node
            while curr.next:        # Traverse to last node
                curr = curr.next
            curr.next = Node(value) # Append new node at the end

    def insert_top(self, value) -> None:
        """Inserts a new node at the beginning of the list."""

        self.head = Node(value, self.head)  # Create a new node pointing to current head node

    def get_node_at(self, index) -> Node:
        """Returns the node at the specified index (0-based)."""

        curr = self.head            # Start at head node
        for _ in range(index):      # Traverse index times
            if curr:                # Ensure we don't go past the end
                curr = curr.next
        return curr                 # Return the node (or None if out of bounds)

    def delete_node(self, index) -> None:
        """Deletes the node at the specified index (0-based)."""
        
        if index == 0:      # Special case: delete head node
            self.head = self.head.next if self.head else None
            return
        
        prev = self.get_node_at(index - 1)  # Get the node before the one to delete
        if prev and prev.next:              # Ensure valid deletion
            prev.next = prev.next.next      # Skip over the node to delete