class Row:
  """
    Represents a single row in the game board using bit manipulation.
    Each row tracks which cells are occupied using a bitmask (`bits`) and stores color data per cell.
  """

  _mask = None  # Class-level mask indicating a fully occupied row

  @classmethod
  def set_mask(cls, width) -> None:
    """
      Sets the mask used to determine if a row is full.
        Example: width = 10 sets mask to 0b1111111111.

      Args:
        width (int): The width of the row/board (number of columns).
    """

    cls._mask = (1 << width) - 1
  
  def __init__(self):
    """
      Initializes a row with optional bitmask value.

      Args:
        bits (int): Initial bitmask for the row (default is 0).
    """

    self.__bits = 0  # Bitmask representing occupied cells
    self.__colors = {} # Dictionary mapping x (cell) index to color

  def is_full(self) -> bool:
    """
      Checks if the row is completely filled.

      Returns:
        bool: True if all bits match the mask, False otherwise.
    """

    return self.__bits == Row._mask

  def clear_row(self) -> None:
    """
      Clears the row by setting all bits to 0 and removing color data
    """

    self.__bits = 0
    self.__colors.clear()

  def get_bit(self, col) -> bool:
    """
      Checks if the bit at column col is set.

      Args:
        col (int): Column index.

      Returns:
        bool: True if the bit is set, False otherwise.
    """

    return bool(self.__bits & (1 << col))
  
  def set_bit(self, col, color) -> None:
    """
      Sets the bit at column col and assigns a color.

      Args:
        col (int): Column index.
        color: Color value to assign.
    """

    self.__bits |= (1 << col) # Set the bit at position col to 1
    self.__colors[col] = color  # Store the color for that cell

  def get_color(self, col):
    """
      Retrieves the color at column col.
      
      Args:
        col (int): Column index.
      
      Returns:
        The color value.
    """
    
    return self.__colors.get(col)