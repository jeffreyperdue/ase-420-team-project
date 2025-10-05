from src.utils.linked_list import LinkedList    # Import the LinkedList class to store Rows in sequence

# Import playing board/grid dimensions from src/constants.py
from src.constants import HEIGHT, WIDTH

class Board:
    """
        Encapsulates the playing field grid and related operations
        using bitboard rows and a linked list.
    """
    def __init__(self, row_factory, height = HEIGHT, width = WIDTH) -> None:
        """
            Initialize a board with a fixed height and width,
            and populate it with empty rows.
        """
        # Error handling - negative or zero dimensions
        if height <= 0 or width <= 0:
            raise ValueError("Board dimensions must be positive integers")
        
        # row_factory must be provided and callable
        if not callable(row_factory):
            raise TypeError("row_factory must be a callable that returns a Row-like object")
        
        self.__height = height  # Board height (total number of rows)
        self.__width = width    # Board width (total number of columns)
        self._row_factory = row_factory     # Factory function to create Row objects
        self.clear()    # Populate the board with empty Row objects

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width
    
    @property
    def rows(self) -> LinkedList:
        return self._rows
    
    def validate_integrity(self) -> None:
        """Ensure the linked list length matches the board height."""
        if self.rows.length() != self.height:
            raise RuntimeError(f"Row count mismatch: expected {self.height}, found {self.rows.length()}")
    
    def clear(self) -> None:
        """
            Reset the board to an empty state by creating a new
            linked list of empty rows.
        """
        self._rows = LinkedList()   # Create a new empty linked list to hold Row objects

        for _ in range(self.height):
            self.rows.append(self._row_factory())    # Append empty Row objects to match the board height

    def _check_row_index(self, row: int) -> None:
        """Check that the given row index is within board bounds."""
        if not (0 <= row < self.height):
            raise IndexError(f"Row index {row} out of bounds")
    
    def _check_column_index(self, col: int) -> None:
        """Check that the given column index is within board bounds."""
        if not (0 <= col < self.width):
            raise IndexError(f"Column index {col} out of bounds")

    def get_row_object(self, index: int) -> object:
        """Retrieve the Row object at the specified index."""
        self._check_row_index(index)
        node = self.rows.get_node_at(index)
        if node is None:
            # LinkedList returns None for out-of-range indexes (it prints an error).
            # Translate this into an IndexError so callers get a clear exception.
            raise IndexError(f"Row index {index} not present in linked list")
        return node.value

    def get_cell(self, row: int, col: int) -> bool:
        """
            Return whether the cell at (row, col) is occupied (True)
            or empty (False).
        """
        self._check_column_index(col)   # Validate column index

        row_obj = self.get_row_object(row)  # Retrieve the Row node at the specified row index
        if row_obj is None:  # Ensure the Row object exists
            raise ValueError(f"Missing row data at index {row}")
        
        result = row_obj.get_bit(col)    # True if the bit at column index is set (occupied), False otherwise
        if not isinstance(result, bool):
            raise TypeError(f"Expected boolean from get_bit({col}), got {type(result)} in get_cell()")

        return result

    def set_cell(self, row: int, col: int, color: object) -> None:
        """Set the cell at (row, col) to occupied and assign its color."""
        self._check_column_index(col)   # Validate column index

        row_obj = self.get_row_object(row)     # Retrieve the Row row_obj at the specified row index
        row_obj.set_bit(col, color)     # Set the bit at column index and store the color

    def clear_full_lines(self) -> None:
        """
        Remove all full rows from the board and insert empty rows
        at the top to maintain height.
        """
        index = 0
        # Iterate over the current number of rows in the linked list. Using
        # self.height here is incorrect because deletions reduce the list
        # length; iterating up to self.rows.length() keeps the loop within
        # the present bounds.
        while index < self.rows.length():
            row_obj = self.get_row_object(index)
            if row_obj.is_full():
                self.rows.delete_node(index)
                # Don't increment index — the next row shifts into this position
            else:
                index += 1

        # After deletion, pad the top with empty rows to restore full height
        missing_rows = self.height - self.rows.length()
        for _ in range(missing_rows):
            self.rows.insert_top(self._row_factory())

    def check_collision(self, piece_rows, col, row):
        """Stub for collision detection — to be implemented by teammates."""
        raise NotImplementedError("check_collision() is not implemented yet")

    def place_piece_rows(self, piece_rows, col, row, color):
        """Stub for piece placement — to be implemented by teammates."""
        raise NotImplementedError("place_piece_rows() is not implemented yet")
