class Board:
    """Encapsulates the playing field grid and related operations."""
    def __init__(self, __height: int, __width: int) -> None:
        """Initialize a board with a grid and given positive integer __height and __width."""
        
        # Error handling - checking for positive int dimensions
        if not __height > 0 or not __width > 0:
            raise ValueError("__height and __width must be positive")
        
        # Set board dimension variables
        self.__height = __height
        self.__width = __width

        # Initialize a grid where each cell is empty (denoted by a zero)
        # The grid is a 2D list (list of lists)
        self._grid = [[0] * __width for _ in range(__height)]

    def get_height(self) -> int:
        """Return the height of the board."""
        return self.__height
    
    def get_width(self) -> int:
        """Return the width of the board."""
        return self.__width

    def clear(self) -> None:
        """Clear the board."""

        # Set each cell in the grid to zero
        self._grid = [[0] * self.__width for _ in range(self.__height)]

    def get_cell(self, row, col) -> int:
        """Return the value of a grid cell"""
        return self._grid[row][col]

    def set_cell(self, row, col, val) -> None:
        """Set the value of a grid cell"""
        self._grid[row][col] = val

    def clear_full_lines(self) -> None:
        """Remove full rows and shift everything down."""
        new_grid = [row[:] for row in self._grid]
        write_row = self.__height - 1
        
        # Copy non-full rows from bottom up
        for read_row in range(self.__height - 1, -1, -1):
            if any(cell == 0 for cell in self._grid[read_row]):
                new_grid[write_row] = self._grid[read_row][:]
                write_row -= 1
        
        # Fill remaining rows at top with zeros
        for r in range(write_row, -1, -1):
            new_grid[r] = [0] * self.__width
        self._grid = new_grid
