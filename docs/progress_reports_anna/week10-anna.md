# Week 10 Progress Report - Anna

- Dates: 11/17 - 11/23

---

## Progress

### Week 10 Goals Completed (4/4)

✅ Render game‑over screen with final score, high score, and options. _(completed in Week 9)_

- _Fulfills sub requirement 3.1_

✅ Implement play again flow (reset board and score). _(completed in Week 9)_

- _Fulfills sub requirement 3.2_

✅ Implement exit flow (close application). _(completed in Week 9)_

- _Fulfills sub requirement 3.3_

✅ Write unit tests for game-over detection and play again/quit flows.

- _Fulfills sub requirement 3.4_

---

### Additional Work Completed

✅ Fixed minor bug: scores were always showing as 0 on the Game Over screen

✅ Remove unused functions and images

✅ Added and modified comments/docstrings

---

## Statistics

- **LoC** (my contributions)
  - Source:
    - `app.py`: 1
    - `src\view\pygame_renderer.py`: 1
  - Tests:
    - `tests\test_game_over.py`: 401 (new)
  - **Total**: 403
- **LoC** (entire codebase)
  - Source code:
    - `app.py`: 72
    - `fix_pygame_constants.py`: 25
    - `run_tests.py`: 176
    - `src\__init__.py`: 0
    - `src\constants.py`: 29
    - `src\constants\__init__.py`: 14
    - `src\constants\colors.py`: 15
    - `src\constants\game_dimensions.py`: 9
    - `src\constants\game_states.py`: 3
    - `src\figures.py`: 16
    - `src\game\__init__.py`: 0
    - `src\game\board.py`: 198
    - `src\game\game.py`: 132
    - `src\game\piece.py`: 22
    - `src\game\row.py`: 61
    - `src\ui\button.py`: 29
    - `src\ui\button_manager.py`: 23
    - `src\ui\pop_up.py`: 97
    - `src\ui\pop_up_layout_utils.py`: 4
    - `src\ui\pop_up_render_utils.py`: 13
    - `src\utils\__init__.py`: 0
    - `src\utils\linked_list.py`: 59
    - `src\utils\score.py`: 22
    - `src\utils\session_manager.py`: 22
    - `src\view\__init__.py`: 0
    - `src\view\input.py`: 25
    - `src\view\pygame_renderer.py`: 211
  - Tests:
    - `test_quick.py`: 47
    - `test_simple.py`: 20
    - `tests\__init__.py`: 0
    - `tests\acceptance\test_user_scenarios.py`: 236
    - `tests\conftest.py`: 205
    - `tests\fixtures\test_helpers.py`: 271
    - `tests\integration\test_game_integration.py`: 152
    - `tests\integration\test_input_game_integration.py`: 181
    - `tests\integration\test_next_piece_preview.py`: 62
    - `tests\integration\test_pause_and_preview_comprehensive.py`: 178
    - `tests\integration\test_pause_toggle.py`: 52
    - `tests\regression\test_sprint1_features.py`: 260
    - `tests\test_board_core.py`: 117
    - `tests\test_board_edge_cases.py`: 100
    - `tests\test_game_over.py`: 401
    - `tests\test_linked_list.py`: 35
    - `tests\test_linked_list_core.py`: 55
    - `tests\test_linked_list_edge_cases.py`: 35
    - `tests\test_piece.py`: 73
    - `tests\test_row.py`: 26
    - `tests\test_row_core.py`: 28
    - `tests\test_row_edge_cases.py`: 30
    - `tests\test_score_utils.py`: 30
    - `tests\test_scoring.py`: 145
    - `tests\test_session_score.py`: 85
    - `tests\test_start_screen.py`: 325
    - `tests\unit\test_next_piece_preview_unit.py`: 164
    - `tests\unit\test_pause_unit.py`: 149
  - **Total**: 4,739
- **🔥 Burn down rates**
  - 4/4 _week 10 milestones/requirements_ completed
    - 100% total
    - ~14% per day
  - 3/3 sprint 2 _epic requirements_ completed
    - 100% total
  - 14/14 sprint 2 _sub requirements_ completed
    - 100% total
    - 20% per week
    - ~3% per day
  - 17/17 sprint 2 _total requirements_ completed
    - 100% total
    - 20% per week
    - ~3% per day

---

### Summary of Progress

#### `tests/test_game_over.py` (new)

- Comprehensive unit test suite for game-over detection and play-again/quit flows
- Key coverage areas:
  - **Game-over detection** (5 tests): State transitions when pieces collide, flag persistence, input blocking
  - **Play-again flow** (10 tests): RESTART intent handling, state resets, board clearing, high score preservation, multiple cycles
  - **Quit flow** (4 tests): QUIT intent from GAME_OVER and START_SCREEN, state preservation
  - **Score persistence** (6 tests): High score tracking, singleton behavior, multi-game persistence
  - **State transitions** (5 tests): PLAYING ↔ GAME_OVER transitions, invalid intent handling
  - **Edge cases** (9 tests): Zero score, very high scores, mixed intents, paused state, gravity blocking
  - **Integration tests** (3 tests): Full game cycles with restart and quit flows
- **Total**: 42 tests, all passing (100% pass rate)

#### `src/view/pygame_renderer.py`

- Fixed critical bug: Game-over popup now displays correct current score and high score
- Updated `draw_start_screen()` and `draw_game_over_screen()` to use new Popup parameter names (`button_specs`, `popup_width`)
- Added comprehensive docstrings to all rendering methods:
  - `_scale_by_height()`: Image scaling utility documentation
  - `draw_board()`: Board rendering documentation
  - `draw_next_piece_preview()`: Next piece preview documentation
  - `draw_piece()`: Active piece rendering documentation
  - `draw_score()`: Score rendering documentation
  - `draw_start_screen()`: Updated docstring with clarity on popup usage
  - `draw_game_over_screen()`: Updated docstring with score parameter documentation
  - `draw_next_piece()`: Next piece rendering in preview box
  - `draw_pause_screen()`: Pause overlay rendering
  - `draw_level_info()`: Level and progression info rendering
  - `draw_ghost_piece()`: Ghost piece projection with detailed explanation

#### `src/ui/pop_up_render_utils.py`

- Added comprehensive docstrings to rendering utility functions:
  - `draw_overlay()`: Semi-transparent overlay rendering
  - `draw_popup_background()`: Popup background with shadow effect
- Removed unused `draw_wrapped_label()` function (was used with old control images)

#### `src/ui/pop_up_layout_utils.py`

- Added docstring to layout utility function:
  - `center_popup()`: Calculates the position of a popup so it appears in the center of the screen
- Removed unused `content_area()` function (was used with old pop up code)

#### `src/view/input.py`

- Cleaned up comments and formatting in key mapping configuration
- Improved comment clarity for ESC/PAUSE intent handling

#### `src/view/img/`

- Removed obsolete image assets:
  - `arrow-keys.png`: No longer needed (replaced with unified controls image)
  - `spacebar-key.png`: No longer needed (replaced with unified controls image)

#### Code Quality Improvements

- Updated docstring for `draw_start_screen()` to clarify pause key functionality ("Press 'p' or 'ESC' at any time to pause")
- Improved parameter naming consistency in Popup class integration:
  - Changed `buttons` parameter to `button_specs` for clarity
  - Changed `width` parameter to `popup_width` for clarity
- Removed duplicate docstrings and improved clarity throughout renderer methods
- Enhanced documentation of ghost piece functionality with detailed explanation of purpose and usage
