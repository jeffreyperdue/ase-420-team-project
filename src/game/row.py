class Row:
  """
    Represents a single row in the game board using bit manipulation.
    Each row tracks which cells are occupied using a bitmask (`bits`) and stores color data per cell.
  """
  def __init__(self, width: int):
    """
      Initializes a row with a given width and bitmask value.

      Args:
        width (int): Number of columns in the row.
    """
    if width <= 0:
      raise ValueError("Row width must be a positive integer")

    self._width = width
    self._mask = (1 << width) - 1  # e.g., width=10 → mask=0b1111111111

    self.__bits = 0  # Bitmask representing occupied cells
    self.__colors = {} # Dictionary mapping x (cell) index to color

  @property
  def width(self) -> int:
      return self._width

  @property
  def mask(self) -> int:
      return self._mask

  def is_full(self) -> bool:
    """
      Checks if the row is completely filled.

      Returns:
        bool: True if all bits match the mask, False otherwise.
    """
    return self.__bits == self.mask

  def clear_row(self) -> None:
    """
      Clears the row by setting all bits to 0 and removing color data
    """
    self.__bits = 0
    self.__colors.clear()

  def _check_column_index(self, col: int, func: str) -> None:
    """Check that the given column index is within row bounds."""
    if not (0 <= col < self.width):
      raise IndexError(f"Column index {col} out of bounds in {func}()")

  def get_bit(self, col: int) -> bool:
    """
      Checks if the bit at column col is set.

      Args:
        col (int): Column index.

      Returns:
        bool: True if the bit is set, False otherwise.
    """
    self._check_column_index(col, "get_bit")  # Validate column index
    return bool(self.__bits & (1 << col))
  
  def set_bit(self, col: int, color: object) -> None:
    """
      Sets the bit at column col and assigns a color.

      Args:
        col (int): Column index.
        color: Color value to assign.
    """
    self._check_column_index(col, "set_bit")  # Validate column index
    self.__bits |= (1 << col)   # Set the bit at position col to 1
    self.__colors[col] = color  # Store the color for that cell

  def clear_bit(self, col) -> None:
    """
    Clears the bit at column `col` and removes the associated color.

    Args:
        col (int): Column index to clear.
    """
    self.__bits &= ~(1 << col)  # Unset the bit at position `col`
    self.__colors.pop(col, None)  # Remove color if it exists

  def get_color(self, col: int):
    """
      Retrieves the color at column col.
      
      Args:
        col (int): Column index.
      
      Returns:
        The color value.
    """
    self._check_column_index(col, "get_color")  # Validate column index
    return self.__colors.get(col)