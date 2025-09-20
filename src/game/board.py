class Board:
    """Encapsulates the playing field grid and related operations."""
    def __init__(self, height: int, width: int) -> None:
        """Initialize a board with given positive integer height and width."""
        
        # Error handling - checking for positive int dimensions
        if not isinstance(height, int) or not isinstance(width, int):
            raise TypeError("height and width must be integers")
        
        # Error handling - checking for positive int dimensions
        if height <= 0 or width <= 0:
            raise ValueError("height and width must be positive")
        
        # Set board dimensions
        self.height = height
        self.width = width

        # Initialize a grid where each cell is empty (denoted by a zero)
        # The grid is a 2D list (list of lists)
        self._grid = [[0] * width for _ in range(height)]

    def clear(self) -> None:
        """Clear the board."""
        # Set each cell in the grid to zero
        self._grid = [[0] * self.width for _ in range(self.height)]

    def cell(self, row, col) -> int:
        """Return the value of a grid cell"""
        return self._grid[row][col]

    def set_cell(self, row, col, val) -> None:
        """Set the value of a grid cell"""
        self._grid[row][col] = val

    def clear_full_lines(self) -> None:
        """Remove full rows and shift everything down."""
        new_grid = [row[:] for row in self._grid]
        write_row = self.height - 1
        
        # Copy non-full rows from bottom up
        for read_row in range(self.height - 1, -1, -1):
            if any(cell == 0 for cell in self._grid[read_row]):
                new_grid[write_row] = self._grid[read_row][:]
                write_row -= 1
        
        # Fill remaining rows at top with zeros
        for r in range(write_row, -1, -1):
            new_grid[r] = [0] * self.width
        self._grid = new_grid
