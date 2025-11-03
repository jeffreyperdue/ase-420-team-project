from src.utils.linked_list import LinkedList    # Import the LinkedList class to store Rows in sequence

# Import playing board/grid dimensions from src/constants.py
from src.constants import HEIGHT, WIDTH
from src.figures import SHAPES

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
        self.__lines_cleared = 0  # Track total lines cleared

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width
    
    @property
    def rows(self) -> LinkedList:
        return self._rows
    
    @property
    def lines_cleared(self) -> int:
        return self.__lines_cleared
    
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

    def clear_cell(self, row, col) -> None:
        node = self._rows.get_node_at(row)
        node.value.clear_bit(col)

    def clear_full_lines(self) -> int:  # Changed: added -> int
        """
        Remove all full rows from the board and insert empty rows
        at the top to maintain height.
        
        Returns:
            int: Number of lines cleared  # ADD THIS
        """
        lines_cleared = 0  # ADD THIS LINE
        index = 0
        # Iterate over the current number of rows in the linked list. Using
        # self.height here is incorrect because deletions reduce the list
        # length; iterating up to self.rows.length() keeps the loop within
        # the present bounds.
        while index < self.rows.length():
            row_obj = self.get_row_object(index)
            if row_obj.is_full():
                self.rows.delete_node(index)
                lines_cleared += 1  # Count for this call
                self.__lines_cleared += 1  # Maintain cumulative total
                # Don't increment index — the next row shifts into this position
            else:
                index += 1

        # After deletion, pad the top with empty rows to restore full height
        missing_rows = self.height - self.rows.length()
        for _ in range(missing_rows):
            self.rows.insert_top(self._row_factory())
        
        return lines_cleared  # ADD THIS LINE at the end

    # Cody's game mechanics methods - PRESERVED FROM CODY'S BRANCH
    def grid_position_to_coords(self, position, x, y) -> tuple:
        """
        Convert the given grid position for the piece cell position into board coordinates,
        applying the piece's position offset.
        
        Args:
            position (int): Position within the 4x4 grid (0 to 15)
            x (int): The x-coordinate of the piece on the board
            y (int): The y-coordinate of the piece on the board

        Returns:
            tuple: (col, row) on the board
        """
        return (x + (position % 4), y + (position // 4))

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
            coords = self.grid_position_to_coords(grid_position, piece.x, piece.y)
            col = coords[0]
            row = coords[1]

            # Checking if within bounds of board
            if row < 0 or row >= self.height or col < 0 or col >= self.width:
                return True

            if self.get_cell(row, col):
                return True
            
        return False

    def place_piece(self, piece) -> bool:
        """
        Placing piece cells on the rows needed based on piece passed into method, also setting color of each cell in rows.

        Returns:
            bool: True if placement was successful, False if collision was detected
        """

        # Checking if this piece has already been placed and removing cells if it has
        if piece.cells:
            for cell in piece.cells:
                col = cell[0]
                row = cell[1]

                self.clear_cell(row, col)

        # Checking if new piece will collide with other pieces or end of board
        if (self.will_piece_collide(piece)):
            return False
        
        # Getting tuple that represents shape of piece to be placed
        shape = SHAPES[piece.type][piece.rotation]

        # Clearing out list of cells for piece
        piece.cells.clear()

        # Filling in cells for the shape
        for grid_position in shape:
            coords = self.grid_position_to_coords(grid_position, piece.x, piece.y)
            col = coords[0]
            row = coords[1]
            
            piece.cells.append((col, row))

            self.set_cell(row, col, piece.color)
        return True
    
    def go_space(self, piece) -> None:
        """
        Drops the piece straight down until it collides, then freezes it.

        Args:
            piece: The piece to be moved.
        """
        while not self.will_piece_collide(piece):
            piece.y += 1
        piece.y -= 1
        self.place_piece(piece)

    def go_down(self, piece) -> bool:
        """
        Moves the piece one row down. If it collides, revert it and place it.
        
        Returns:
            bool: True if moved successfully, False if it hit and was placed.
        """
        piece.y += 1
        if self.will_piece_collide(piece):
            piece.y -= 1
            self.place_piece(piece)
            return False
        return True

    def go_side(self, x_movement, piece) -> None:
        """
        Moves the piece left or right, reverting if it causes a collision.

        Args:
            x_movement (int): Movement in X direction (-1 for left, 1 for right).
            piece: The piece to be moved.
        """
        piece.x += x_movement
        if self.will_piece_collide(piece):
            piece.x -= x_movement
        

    def rotate(self, piece) -> None:
        """
        Rotates the piece clockwise. If rotation causes collision, reverts it.

        Args:
            piece: The piece to be rotated.
        """
        old_rotation = piece.rotation
        piece.rotation = (piece.rotation + 1) % len(SHAPES[piece.type])
        if self.will_piece_collide(piece):
            piece.rotation = old_rotation
        
