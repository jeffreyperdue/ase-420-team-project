# Week 3 Progress Report: Refactoring Board Logic & Implementation

- Dates: 9/22 - 9/28

## Week 3 Goals:

✅ Refactored and optimized the line detection and clearing logic  
✅ Wrote unit tests for line detection and clearing

## Additional Work Completed:

✅ Further optimized the playing field grid by refactoring it to use `Row` bitboards and a `LinkedList` to hold the rows in sequence

## Statistics:

- **LoC:**
  - Source code:
    - `src/constants.py`: 28
    - `src/figures.py`: 16
    - `src/game/board.py`: 66
    - `src/game/game.py`: 24
    - `src/game/piece.py`: 106
    - `src/game/row.py`: 63
    - `src/starter_code/tetris_code_explained.py`: 187
    - `src/starter_code/tetris_ver1.py`: 177
    - `src/utils/linked_list.py`: 44
    - `src/view/input.py`: 0
    - `src/view/pygame_renderer.py`: 34
  - Unit tests:
    - `tests/test_board.py`: 64
    - `tests/test_linked_list.py`: 35
    - `tests/test_row.py`: 27
  - **Total**: 871
- **Burn down rates**
  - Week 3:
    - 100% total
    - ~14% per day
    - Based on number of Week 3 goals/milestones completed (2/2)
  - Sprint 1:
    - 40% total
    - 20% per week
    - ~3% per day
    - Based on total number of Sprint 1 goals/milestones completed (4/10)

---

## Summary of changes under src/

- Files changed:
  - `src/constants.py`
  - `src/game/board.py`
  - `src/game/row.py`
  - `src/utils/linked_list.py`
  - `src/starter_code/tetris_ver1.py`
  - `src/starter_code/tetris_code_explained.py`

---

## Major Changes

#### 1. `constants.py`

- Purpose
  - Centralizes application constants: screen size, FPS, board dimensions, colors, and cell size.
- Changes
  - Added board dimensions:
    - `HEIGHT = 20` (number of rows)
    - `WIDTH = 10` (number of columns)
- Why
  - Provide a single canonical source for board dimensions so caller code (starter scripts) can refer to `HEIGHT` and `WIDTH` instead of local/legacy globals.

---

#### 2. `board.py`

- Purpose

  - Encapsulates the playing field in a `Board` class using `Row` bitboards and a `LinkedList` to hold the rows in sequence.
  - Provides board operations such as clearing, cell access, and clearing full lines.

- Changes

  - Board is now fully encapsulated:
    - Constructor
      - `__height` and `__width` are set from `src.constants` (`HEIGHT` and `WIDTH`).
      - `Row` mask initialized via `Row.set_mask(self.__width)`.
      - Rows stored as `Row()` objects in a `LinkedList()` (`self._rows`).
      - Removed error handling statement that checked type of height & width attributes:
        ```python
        if not isinstance(height, int) or not isinstance(width, int):
          raise TypeError("height and width must be integers")
        ```
    - New public accessor methods:
      - `get_height() -> int`
        - Returns value of `__height` attribute
      - `get_width() -> int`
        - Returns value of `__width` attribute
    - Modified API methods:
      - `clear()` initializes the linked list with empty `Row()` objects.
      - `get_cell(row, col)` returns bit/cell boolean occupancy via `node.value.get_bit(col)`.
        - Renamed from `cell()` to `get_cell()` to improve function clarity
      - `set_cell(row, col, color)` sets bit/cell and stores color in the corresponding `Row`.
      - `clear_full_lines()` iterates through linked list, deletes full rows, and inserts new empty rows at top to maintain height.
  - 2 stub methods are present for teammates:
    - `check_collision(self, piece_rows, col, row)` — NotImplemented
    - `place_piece_rows(self, piece_rows, col, row, color)` — NotImplemented

- Why

  - Moves board representation from raw 2D lists to a more compact bitmask+linked-list structure. Encapsulates the operations and provides a clean API `get_cell`, `set_cell`, `clear_full_lines`, and size accessors.

---

#### 3. `linked_list.py`

- Purpose

  - Simple singly linked list implementation used by board.py to store `Row` objects (one node per row).

- Changes

  - New file
  - Provides `Node` and `LinkedList` classes with methods:
    - `length()`
    - `append(value)`
    - `insert_top(value)`
    - `get_node_at(index)`
    - `delete_node(index)`
  - Implementation includes docstrings and standard traversal code.

- Why / Notes
  - Linked list is used to support row-level operations (deleting a full row) while preserving quick top insertions.

---

#### 4. `row.py`

- Purpose

  - Represents a single row using a bitmask for occupied cells and a color mapping for occupied columns.

- Changes

  - New file
  - Stores bits/cells (`__bits`) and a `__colors` dict mapping column indices to colors.
  - Class-level mask `_mask` set via `Row.set_mask(width)`; used to determine row fullness.
  - Methods:
    - `set_mask(width)` sets `_mask` to `(1 << width) - 1`
    - `is_full()` determines whether a row is full by comparing `__bits` to the mask
    - `clear_row()` resets bits/cells and colors
    - `get_bit(col)` returns whether a bit/cell is set
    - `set_bit(col, color)` sets bit/cell and stores color
    - `get_color(col)` retrieves color value for a bit/cell

- Why / Notes
  - Bitmask approach reduces memory and allows quick full-row checks.

---

#### 5. `tetris_ver1.py` & `tetris_code_explained.py`

- Purpose
  - Starter Tetris implementation.
- Changes
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
