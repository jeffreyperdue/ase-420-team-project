from src.game.row import Row    # Import the Row class, which represents a single bitboard row
from src.utils.linked_list import LinkedList    # Import the LinkedList class to store Rows in sequence

# Import playing board/grid dimensions from src/constants.py
from src.constants import HEIGHT, WIDTH     # Import board dimensions from a shared constants file

from src.figures import SHAPES
class Board:
    """
        Encapsulates the playing field grid and related operations
        using bitboard rows and a linked list.
    """
    
    def __init__(self) -> None:
        """
            Initialize a board with a fixed height and width,
            and populate it with empty rows.
        """
        
        self.__height = HEIGHT  # Board height (total number of rows)
        self.__width = WIDTH    # Board width (total number of columns)

        Row.set_mask(self.__width)  # Set the bitmask used to detect full rows (e.g., 0b1111111111 for width=10)
        
        self.clear()    # Populate the board with empty Row objects

    def clear(self) -> None:
        """
            Reset the board to an empty state by creating a new
            linked list of empty rows.
        """

        self._rows = LinkedList()   # Create a new empty linked list to hold Row objects

        for _ in range(self.__height):
            self._rows.append(Row())    # Append empty Row objects to match the board height

    def get_height(self) -> int:
        """Return the height of the board (number of rows)."""
        return self.__height
    
    def get_width(self) -> int:
        """Return the width of the board (number of columns)."""
        return self.__width

    def get_cell(self, row, col) -> bool:
        """
            Return whether the cell at (row, col) is occupied (True)
            or empty (False).
        """
        
        node = self._rows.get_node_at(row)  # Retrieve the Row node at the specified row index
        return node.value.get_bit(col)      # Return True if the bit at column index is set (occupied), False otherwise

    def set_cell(self, row, col, color) -> None:
        """Set the cell at (row, col) to occupied and assign its color."""

        node = self._rows.get_node_at(row)  # Retrieve the Row node at the specified row index
        node.value.set_bit(col, color)      # Set the bit at column index and store the color

    def clear_full_lines(self) -> None:
        """
        Remove all full rows from the board and insert empty rows
        at the top to maintain height.
        """

        curr = self._rows.head  # Start at the head of the linked list
        prev = None             # Track the previous node for deletion logic
        index = 0               # Track the current row index

        while curr:
            if curr.value.is_full():    # If the row is full (all bits set)
                self._rows.delete_node(index)   # Remove the row from the list
                curr = prev.next if prev else self._rows.head   # Reset current pointer
                continue    # Skip incrementing index
            
            prev = curr         # Move previous pointer forward
            curr = curr.next    # Move current pointer forward
            index += 1          # Increment row index

        # After deletion, pad the top with empty rows to restore full height
        for _ in range(self.get_height() - self._rows.length()):
            self._rows.insert_top(Row())

    def grid_position_to_coords(self, position) -> tuple:
        """
        Convert the given grid position for the piece cell position into coordinates to be placed on board
        Example: 1 -> (4, 0)
        
        Returns:
            tuple: Tuple that represents coordinates of cell converted from the grid index

        """

        return (position % 4, position // 4)

    def will_piece_collide(self, piece) -> bool:
        """
        Check if placing the given piece at (col, row) would collide
        with existing occupied cells on the board.

        Returns:
            bool: True if piece will collide with other piece, False if not
        """

        # Getting tuple that represents shape of piece to be placed
        shape = SHAPES[piece.type][piece.rotation]

        # Going through each cell in the piece to be placed and ensuring that will not collide with other piece or end of board
        for grid_position in shape:
            coords = self.grid_position_to_coords(grid_position)
            col = coords[0]
            row = coords[1]

            if self.get_cell(row, col):
                return True
            
        return False

    def place_piece(self, piece) -> bool:
        """
        Placing piece cells on the rows needed based on piece passed into method, also setting color of each cell in rows.

        Returns:
            bool: True if placement was successful, False if collision was detected
        """
        
        # Checking if new piece will collide with other pieces or end of board
        if (self.will_piece_collide(piece)):
            return False
        
        # Getting tuple that represents shape of piece to be placed
        shape = SHAPES[piece.type][piece.rotation]

        # Filling in cells for the shape
        for grid_position in shape:
            coords = self.grid_position_to_coords(grid_position)
            col = coords[0]
            row = coords[1]

            self.set_cell(row, col, piece.color)
            
        return True