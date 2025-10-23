# Week 6 Progress Report

- Dates: 10/20 - 10/26

---

## Progress

### Week 6 Goals Completed (3/3)

✅ Implement scoring logic decoupled from rendering (testable module).

- _Fulfills sub requirement 1.1_

✅ Implement base scoring function (award points for clearing one line).

- _Fulfills sub requirement 1.2_

✅ Write initial unit tests for base scoring.

- _Fulfills part of sub requirement 1.7_

---

### Additional Work Completed

#### Week 7 Goals Completed (2/3)

✅ Add multipliers for multiple lines (2, 3, 4)

- _Fulfills sub requirement 1.3_

✅ Integrate scoring logic with the board (trigger only after validated line removal).

- _Fulfills sub requirement 1.4_

---

## Statistics

- **LoC** (my contributions)
  - Source:
    - `src\game\board.py`: 6
    - `src\game\game.py`: 12
    - `src\game\score.py`: 18 (new)
  - Tests:
    - `tests\test_scoring.py`: 71 (new)
    - `tests\test_score_utils.py`: 30 (new)
  - **Total**: 137
- **LoC** (entire codebase)
  - Source code:
    - `app.py`: 57
    - `fix_pygame_constants.py`: 28
    - `run_tests.py`: 192
    - `src\constants.py`: 28
    - `src\figures.py`: 16
    - `src\game\board.py`: 192
    - `src\game\game.py`: 79
    - `src\game\piece.py`: 26
    - `src\game\row.py`: 78
    - `src\game\score.py`: 18
    - `src\starter_code\tetris_code_explained.py`: 189
    - `src\starter_code\tetris_ver1.py`: 202
    - `src\utils\linked_list.py`: 71
    - `src\view\input.py`: 20
    - `src\view\pygame_renderer.py`: 54
  - Tests:
    - `test_quick.py`: 50
    - `test_simple.py`: 20
    - `tests\acceptance\test_user_scenarios.py`: 260
    - `tests\conftest.py`: 232
    - `tests\fixtures\test_helpers.py`: 320
    - `tests\integration\test_game_integration.py`: 175
    - `tests\integration\test_input_game_integration.py`: 202
    - `tests\regression\test_sprint1_features.py`: 290
    - `tests\test_board_core.py`: 128
    - `tests\test_board_edge_cases.py`: 103
    - `tests\test_linked_list.py`: 35
    - `tests\test_linked_list_core.py`: 57
    - `tests\test_linked_list_edge_cases.py`: 37
    - `tests\test_piece.py`: 78
    - `tests\test_row.py`: 26
    - `tests\test_row_core.py`: 30
    - `tests\test_row_edge_cases.py`: 32
    - `tests\test_score_utils.py`: 30
    - `tests\test_scoring.py`: 71
  - **Total**: 3,426
- **🔥 Burn down rates**
  - 3/3 _week 6 milestones/requirements_ completed
    - 100% total
    - ~14% per day
  - 2/3 _week 7 milestones/requirements_ completed early
  - 0/3 sprint 2 _epic requirements_ completed
    - 0% total
  - 5/14 sprint 2 _sub requirements_ completed
    - ~36% total
    - ~36% per week
    - ~5.1% per day
  - 5/17 sprint 2 _total requirements_ completed
    - ~29% total
    - ~29% per week
    - ~4% per day

---

### Summary of Progress

#### `board.py`

- Added `__lines_cleared` attribute to `Board` class
  - Stores an int that represents the number of lines that are cleared at once
  - Added `lines_cleared` property for accessing value
  - Implemented line counting logic in `clear_full_lines()`

#### `score.py` (new)

- New file for scoring utilities
- Currently contains one function: `points_for_clear()`
  - Returns an int representing the total number of points earned based on the total number of lines cleared at once
  - Contains a map mapping the number of lines cleared at once to the number of points
  - Points per lines cleared:
    - 0 lines cleared: 0 points
    - 1 line cleared: 100 points
    - 2 lines cleared: 300 points
    - 3 lines cleared: 500 points
    - 4 lines cleared: 800 points
- Contains documentation

#### `test_score_utils.py` (new)

- New test file containing unit tests for `score.py`
- Currently contains 2 tests

#### `test_scoring.py` (new)

- New test file containing unit tests for other scoring logic
- Currently contains 6 tests
