class Node:
    """Represents a single node in a linked list, holding a value and a reference to the next node."""
    def __init__(self, value, next=None):
        self.value = value  # The data stored in this node (e.g., a Row object)
        self.next = next    # Reference to the next node in the list (or None if it's the last node)

class LinkedList:
    """A singly linked list used to store rows of the game board."""
    def __init__(self):
        self.head = None    # Reference to first node in the list
        self._length = 0    # Track the number of nodes in the list

    def length(self) -> int:
        """Returns the number of nodes in the linked list."""
        return self._length

    def _decrement_length(self) -> None:
        """Decreases the length counter by one."""
        if self.length() > 0:
            self._length -= 1
    
    def _increment_length(self) -> None:
        """Increases the length counter by one."""
        self._length += 1

    def count_nodes(self) -> int:
        """Returns the number of nodes in the linked list."""
        count = 0             # Initialize counter
        curr = self.head      # Start at the head node
        while curr:           # Traverse until the end
            count += 1        # Increment for each node
            curr = curr.next  # Move to the next node
        return count          # Return total count

    def _check_value(self, value, action) -> None:
        """Checks if the given value is valid (not None)."""
        if value is None:
            raise ValueError(f"Cannot {action} the list")

    def append(self, value) -> None:
        """Adds a new node with the given value to the end of the list."""
        # Validate value (raises ValueError for None)
        self._check_value(value, "append None to")

        if not self.head:           # If list is empty
            self.head = Node(value) # Create the first (head) node
        else:
            curr = self.head        # Start at head node
            while curr.next:        # Traverse to last node
                curr = curr.next
            curr.next = Node(value) # Append new node at the end

        self._increment_length()            # Increment length counter

    def insert_top(self, value) -> None:
        """Inserts a new node at the beginning of the list."""
        # Validate value (raises ValueError for None)
        self._check_value(value, "insert None at top of")

        self.head = Node(value, self.head)  # Create a new node pointing to current head node
        self._increment_length()   # Increment length counter

    def _check_index(self, index) -> None:
        """Checks if the given index is valid."""
        if index < 0 or index >= self.length():
            raise IndexError(f"Index {index} out of bounds")

    def get_node_at(self, index) -> Node:
        """Returns the node at the specified index."""
        # Validate index (raises IndexError if invalid)
        self._check_index(index)

        curr = self.head            # Start at head node
        for _ in range(index):      # Traverse index times
            curr = curr.next
        return curr                 # Return the node

    def delete_node(self, index) -> None:
        """Deletes the node at the specified index."""
        # Validate index (raises IndexError if invalid)
        self._check_index(index)

        if index == 0:  # Special case: delete head node
            self.head = self.head.next
            self._decrement_length()     # Decrement length counter
            return

        prev = self.get_node_at(index - 1)  # Get the node before the one to delete

        if not prev or not prev.next:       # Ensure valid deletion
            raise IndexError(f"No node exists at index {index}")

        prev.next = prev.next.next      # Skip over the node to delete
        self._decrement_length()        # Decrement length counter
