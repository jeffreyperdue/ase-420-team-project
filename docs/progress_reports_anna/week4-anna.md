# Week 4 Progress Report

- Dates: 9/29 - 10/5

## Week 4 Goals Completed (3/3)

✅ As a developer, I want to generate tests for edge cases and error handling to ensure the logic works as expected.  
✅ As a developer, I want to continue optimizing and cleaning up the code to ease future development.  
✅ As a developer, I want to add code comments and documentation so my teammates can easily understand my code.

## Additional Work Completed

✅ Added error handling for `Row`, `Board`, and `LinkedList` classes  
✅ Converted milestones into Actor-Goal format (user stories)

## Statistics

- **LoC**
  - Source code:
    - `src\constants.py`: 28
    - `src\figures.py`: 16
    - `src\game\board.py`: 95
    - `src\game\game.py`: 24
    - `src\game\piece.py`: 106
    - `src\game\row.py`: 70
    - `src\starter_code\tetris_code_explained.py`: 189
    - `src\starter_code\tetris_ver1.py`: 178
    - `src\utils\linked_list.py`: 71
    - `src\view\input.py`: 0
    - `src\view\pygame_renderer.py`: 34
  - Unit tests:
    - `tests\test_board_core.py`: 88
    - `tests\test_board_edge_cases.py`: 101
    - `tests\test_linked_list_core.py`: 57
    - `tests\test_linked_list_edge_cases.py`: 37
    - `tests\test_row_core.py`: 30
    - `tests\test_row_edge_cases.py`: 32
  - **Total**: 1156
- **Burn down rates**
  - Week 4:
    - 100% total
    - ~14% per day
    - Based on number of Week 4 goals/milestones completed (3/3)
  - Sprint 1:
    - 70% total
    - ~23% per week
    - ~3.3% per day
    - Based on total number of Sprint 1 goals/milestones completed (7/10)

---

## Summary of changes under `src/` and `tests/`

- Files changed:
  - `src\game\board.py`
  - `src\game\row.py`
  - `src\starter_code\tetris_code_explained.py`
  - `src\starter_code\tetris_ver1.py`
  - `src\utils\linked_list.py`
  - `tests\test_board_core.py`
  - `tests\test_board_edge_cases.py` (new)
  - `tests\test_linked_list_core.py`
  - `tests\test_linked_list_edge_cases.py` (new)
  - `tests\test_row_core.py`
  - `tests\test_row_edge_cases.py` (new)

---

## Major Changes

### 1. `board.py`

- Purpose

  - Encapsulates the playing field and provides board-level operations (cell access, clearing, full-line detection and removal) using `Row` bitboards stored in a `LinkedList`.

- Changes

  - Constructor / API
    - `Board` now requires a `row_factory` callable (zero-arg factory that returns a `Row`-like object). Passing a non-callable raises `TypeError`.
    - Exposes `.height` and `.width` properties (backing attributes `__height` and `__width`).
    - `clear()` now re-initializes the internal `LinkedList` of rows using the factory to produce exactly `height` rows.
  - Robustness and error handling
    - Added index checks (`_check_row_index`, `_check_column_index`) and clear error messages (`IndexError`) for out-of-bounds accesses.
    - `get_row_object()` validates that a node exists and raises `IndexError` when a linked-list access would otherwise return `None`.
    - `get_cell()` validates return types and raises `TypeError` if a `Row.get_bit()` implementation returns a non-boolean value.
  - Line clearing behavior
    - `clear_full_lines()` iterates against the current linked-list length (via `_rows.length()`), deletes full rows in-place, then pads the top of the list with empty rows created by the factory to restore `height`.
  - Removed backward-compatible shims that provided `get_height()`/`get_width()` helpers — callers/tests were updated to use the `.height`/`.width` properties.

- Why
  - Remove coupling between `Board` and `Row` classes by injecting the `Row` dependency into the `Board` class using the `row_factory`.
  - Enforce a clear contract: callers must provide a compatible `Row` factory so the `Board` doesn't make hidden assumptions about row construction.
  - Robust error handling and clearer exceptions make the module easier to test and maintain.

---

### 2. `linked_list.py`

- Purpose

  - Lightweight singly linked-list implementation used to store `Row` objects in `Board` (one node per row) and support efficient top insertion and mid-list deletion.

- Changes

  - Validation & exceptions
    - Insert/append operations now validate values and raise `ValueError` when attempting to append/insert `None`.
    - Index checks (`_check_index()`) raise `IndexError` for out-of-range indices; `get_node_at()` and `delete_node()` propagate these exceptions rather than printing errors or returning `None`.
  - Length tracking
    - Internal length counter (`_length`) is maintained via increment/decrement helpers and used by callers (`Board`) to avoid iteration bugs during deletions.

- Why
  - Fail-fast behavior (raising exceptions) is clearer for tests and callers and avoids silent failures that complicate debugging.
  - Length tracking via internal length variable (O(1) time) is faster than calling a `.length()` method that traverses the nodes each time it's called (O(n) time).

---

### 3. `row.py`

- Purpose

  - Represents a single board row using a compact bitmask (`__bits`) and a per-cell color mapping; provides bit operations and fullness checks.

- Changes

  - Input validation: `Row(width)` raises `ValueError` for non-positive widths.
  - Column index checks: `get_bit()`, `set_bit()`, and `get_color()` validate column indices and raise `IndexError` for out-of-range accesses.
  - Core operations: `is_full()`, `clear_row()`, `set_bit()`, `get_bit()`, and `get_color()` implemented with clear semantics and internal color tracking.

- Why
  - Prevent invalid row construction and out-of-bounds bit access. The explicit checks make the `Row` class robust and safe for the `Board` to use without defensive workarounds.

---

### 4. Tests (`tests/`)

- Purpose

  - Provide both small, fast core tests and more comprehensive edge-case tests exercising the new error behavior and board semantics.

- Changes

  - Renamed existing files:
    - `test_board.py` -> `test_board_core.py`
    - `test_row.py` -> `test_row_core.py`
    - `test_linked_list.py` -> `test_linked_list_core.py`
  - New files for testing edge cases:
    - `test_board_edge_cases.py`
    - `test_row_edge_cases.py`
    - `test_linked_list_edge_cases.py`
  - Updated all board tests to construct `Board` instances by passing an explicit `row_factory` (e.g., `lambda: Row(constants.WIDTH)`) and to access size via `.height`/`.width` properties.
  - Linked List tests updated to expect exceptions (`ValueError` / `IndexError`) for invalid operations (e.g., `append(None)`, `get_node_at(invalid)`, `delete_node(invalid)`) rather than silent prints or `None` returns.
  - Added and updated tests for full test coverage of core functionality.
  - Added edge-case tests for `Row` (index bounds, invalid width), `Board` (invalid constructor args, out-of-range cell access, full-row clearing scenarios, multiple clears in succession), and `LinkedList` (invalid indices, passing `None` as an arg).

- Why
  - Keep fast smoke tests and core functionality tests separate from edge-case tests.
  - Ensure tests express and verify the new fail-fast behaviors.

---

### 5. Starter code (`tetris_ver1.py`, `tetris_code_explained.py`)

- Purpose

  - Provide runnable example/starter scripts that exercise the `Board` API and demonstrate usage.

- Changes

  - Updated initialization to construct a `Board` with an explicit factory (example: `Board(lambda: Row(constants.WIDTH))`).
  - Replaced legacy helper calls with the new API: use `GameBoard.height`/`GameBoard.width` instead of older `get_height()`/`get_width()` methods.

- Why
  - Keep examples in sync with the library API so new contributors can run the starter code without having to patch compatibility shims.

---

### 6. Misc / Notes

- Tests and CI

  - After these changes, the repository unit test suite was executed and all tests passed (41 tests).

- Rationale summary
  - The week focused on hardening the board/row/linked-list abstractions with proper input validation and explicit failure modes, simplifying test expectations and making the codebase easier to reason about and extend.
