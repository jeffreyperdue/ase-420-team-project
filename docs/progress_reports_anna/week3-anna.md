## Summary of changes under src/

- Files inspected and reported:
  - `src/constants.py`
  - `src/game/board.py`
  - `src/starter_code/tetris_ver1.py`
  - `src/starter_code/tetris_code_explained.py`

---

### `constants.py`

- Purpose
  - Centralizes application constants: screen size, FPS, board dimensions, colors, and cell size.
- What changed
  - Added playing grid dimensions:
    - HEIGHT = 20 (number of rows)
    - WIDTH = 10 (number of columns)
- Why
  - Provide a single canonical source for board dimensions so caller code (starter scripts) can refer to `HEIGHT` and `WIDTH` instead of local/legacy globals.
- Key lines
  - HEIGHT = 20
  - WIDTH = 10
- Verification
  - Starter scripts were updated to import `HEIGHT`/`WIDTH` and use them in `initialize(HEIGHT, WIDTH)`.

---

### `board.py`

- Purpose
  - Encapsulates the playing field (grid) and operations on it in a `Board` class.
- What changed

  - `Board` constructor now stores integer dimensions as private fields:
    - `init(self, __height: int, __width: int)`
      - Original: `init(self, height: int, width: int)`
  - Updated all `self.height` references to `self.__height`
  - Updated all `self.width` references to `self.__width`
  - Removed error handling statement that checked type of height & width attributes:
    ```python
    if not isinstance(height, int) or not isinstance(width, int):
      raise TypeError("height and width must be integers")
    ```
  - New public API methods:
    - `get_height() -> int`
      - Returns value of `__height` attribute
    - `get_width() -> int`
      - Returns value of `__width` attribute
  - Modified API method:
    - `get_cell(row, col) -> int`
      - Renamed from `cell()` to `get_cell()` to improve function clarity
      - Updated function calls with new name

---

### `tetris_ver1.py` & `tetris_code_explained.py`

- Purpose
  - Starter Tetris implementation (main runtime).
- What changed
  - Replaced local/legacy board globals (Height/Width) with the new global constants and `Board` API:
    - Uses `from src.constants import HEIGHT, WIDTH`
    - Draw logic:
      - Uses `GameBoard.get_height()` instead of `GameBoard.height`
        ```python
        for i in range(GameBoard.get_height()):
        ```
      - Uses `GameBoard.get_width()` instead of `GameBoard.width`
        ```python
        for j in range(GameBoard.get_width()):
        ```
      - Uses `GameBoard.get_cell()` instead of `GameBoard.cell()`
        ```python
        val = GameBoard.get_cell(i, j)
        ```
    - Collision logic:
      - Uses `GameBoard.get_height()` instead of `GameBoard.height`
        ```python
        (i + ShiftY) >= GameBoard.get_height()
        ```
      - Uses `GameBoard.get_width()` instead of `GameBoard.width`
        ```python
        (j + ShiftX) >= GameBoard.get_width()
        ```
      - Uses `GameBoard.get_cell()` instead of `GameBoard.cell()`
        ```python
        GameBoard.get_cell(i + ShiftY, j + ShiftX) > 0:
        ```
    - `main()`
      - Uses `HEIGHT` & `WIDTH` globals instead of legacy `Height` & `Width` variables
        ```python
        initialize(HEIGHT, WIDTH)
        ```
  - Minor naming/format cleanup consistent with other starter file edits.
- Why
  - To rely on the encapsulated Board for grid operations and to centralize board dimensions via `src.constants`.
