# Week 9 Progress Report - Anna

- Dates: 11/10 - 11/16

---

## Progress

### Week 9 Goals Completed (3/3)

✅ Render start screen with title, controls, and prompt. _(completed in Week 8)_

- _Fulfills sub requirement 2.1_

✅ Implement transition from start screen into the game loop with a start button. _(completed in Week 8)_

- _Fulfills sub requirement 2.2_

✅ Write unit tests for start screen transition logic.

- _Fulfills sub requirement 2.3_

---

### Additional Work Completed

#### Week 10 Goals Completed Early (3/4)

✅ Render game‑over screen with final score, high score, and options.

- _Fulfills sub requirement 3.1_

✅ Implement play again flow (reset board and score).

- _Fulfills sub requirement 3.2_

✅ Implement exit flow (close application).

- _Fulfills sub requirement 3.3_

---

## Statistics

- **LoC** (my contributions)
  - Source:
    - `app.py`: 1
    - `src\ui\button_manager.py`: 2
    - `src\ui\pop_up.py`: 102 (new)
    - `src\view\pygame_renderer.py`: 26
  - Tests:
    - `tests\test_start_screen.py`: 365 (new)
  - **Total**: 496
- **LoC** (entire codebase)
  - Source code:
    - `app.py`: 66
    - `fix_pygame_constants.py`: 28
    - `src\__init__.py`: 0
    - `src\constants.py`: 29
    - `src\constants\__init__.py`: 15
    - `src\constants\colors.py`: 16
    - `src\constants\game_dimensions.py`: 10
    - `src\constants\game_states.py`: 4
    - `src\figures.py`: 16
    - `src\game\__init__.py`: 0
    - `src\game\board.py`: 192
    - `src\game\game.py`: 109
    - `src\game\piece.py`: 26
    - `src\game\row.py`: 78
    - `src\starter_code\tetris_code_explained.py`: 189
    - `src\starter_code\tetris_ver1.py`: 202
    - `src\ui\button.py`: 29
    - `src\ui\button_manager.py`: 24
    - `src\ui\pop_up.py`: 102
    - `src\ui\pop_up_layout_utils.py`: 10
    - `src\ui\pop_up_render_utils.py`: 23
    - `src\utils\__init__.py`: 0
    - `src\utils\linked_list.py`: 71
    - `src\utils\score.py`: 26
    - `src\utils\session_manager.py`: 29
    - `src\view\__init__.py`: 0
    - `src\view\input.py`: 20
    - `src\view\pygame_renderer.py`: 115
  - Tests:
    - `run_tests.py`: 192
    - `test_quick.py`: 50
    - `test_simple.py`: 20
    - `tests\__init__.py`: 0
    - `tests\acceptance\test_user_scenarios.py`: 260
    - `tests\conftest.py`: 232
    - `tests\fixtures\test_helpers.py`: 320
    - `tests\integration\test_game_integration.py`: 175
    - `tests\integration\test_input_game_integration.py`: 202
    - `tests\integration\test_next_piece_preview.py`: 69
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
    - `tests\test_scoring.py`: 154
    - `tests\test_session_score.py`: 94
    - `tests\test_start_screen.py`: 365
  - **Total**: 4,408
- **🔥 Burn down rates**
  - 3/3 _week 9 milestones/requirements_ completed
    - 100% total
    - ~14% per day
  - 3/4 _week 10 milestones/requirements_ completed early
  - 2/3 sprint 2 _epic requirements_ completed
    - ~33% total
  - 13/14 sprint 2 _sub requirements_ completed
    - ~93% total
    - ~23% per week
    - ~3% per day
  - 15/17 sprint 2 _total requirements_ completed
    - ~88% total
    - ~22% per week
    - ~3% per day

---

### Summary of Progress

#### `src/ui/pop_up.py` (new)

- Implemented flexible popup abstraction to unify start screen and game-over screen rendering
- Key features:
  - Dynamic height computation based on content (title, images, body lines, buttons)
  - Proper button stacking with correct spacing calculations
  - Automatic button manager integration and clearance
  - Centered positioning on screen
  - Support for multiple content types (text, images, buttons)

#### `src/ui/button_manager.py`

- Extended button manager with popup support
- Key changes:
  - Added `clear()` method to remove all buttons before rendering new popups
  - Enables popup abstraction to manage its own button lifecycle

#### `src/view/pygame_renderer.py`

- Refactored start screen and game-over screen to use Popup abstraction
- Key changes:
  - Replaced manual layout/rendering code with Popup class
  - Updated `draw_start_screen()` and `draw_game_over_screen()` to use flexible Popup with images and buttons
    - Added score and high score to game over screen
  - Significantly reduced code complexity (153 lines → 115 lines in this module)
  - Improved code maintainability by centralizing popup rendering logic

#### `src/view/img/controls.png` (new)

- Added controls image asset showing keyboard controls
- Key features:
  - Single unified image asset for control instructions
  - Replaces separate arrow keys and spacebar images and text descriptions
  - Automatically scaled by renderer based on target height

#### `tests/test_start_screen.py` (new)

- Comprehensive unit test suite for start screen and popup functionality
- Key features:
  - 28 test cases covering initialization, height computation, rendering, and button integration
  - Tests for Popup with various content combinations (title, images, body lines, buttons)
  - Integration tests validating end-to-end popup and button interaction
  - Tests ensuring popup height correctly accommodates all visual elements
  - Tests for PygameRenderer.draw_start_screen() and button registration
  - All tests passing (100% pass rate)
