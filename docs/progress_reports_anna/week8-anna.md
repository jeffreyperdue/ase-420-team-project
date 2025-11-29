# Week 8 Progress Report - Anna

- Dates: 11/3 - 11/9

---

## Progress

### Week 8 Goals Completed (3/3)

✅ Display current score in the UI and persist until reset _(completed in Week 7)_

- _Fulfills sub requirement 1.5_

✅ Display high score of the current session in‑game _(completed in Week 7)_

- _Fulfills sub requirement 1.6_

✅ Finalize scoring system unit test coverage.

- _Fulfills the rest of sub requirement 1.7_

---

### Additional Work Completed

#### Week 9 Goals Completed Early (2/3)

✅ Render start screen with title, controls, and prompt.

- _Fulfills sub requirement 2.1_

✅ Implement transition from start screen into the game loop with a start button.

- _Fulfills sub requirement 2.2_

---

## Statistics

- **LoC** (my contributions)
  - Source:
    - `app.py`: 49
    - `src\game\game.py`: 31
    - `src\ui\button.py`: 29 (new)
    - `src\ui\button_manager.py`: 21 (new)
    - `src\ui\start_screen_layout_utils.py`: 10 (new)
    - `src\ui\start_screen_render_utils.py`: 23 (new)
    - `src\view\pygame_renderer.py`: 73
    - `src\constants\__init__.py`: 14 (new)
    - `src\constants\colors.py`: 15 (new)
    - `src\constants\game_dimensions.py`: 9 (new)
    - `src\constants\game_states.py`: 3 (new)
  - Tests:
    - `tests\test_scoring.py`: 13
    - `tests\test_session_score.py`: 94 (new)
  - **Total**: 384
- **LoC** (entire codebase)
  - Source code:
    - `app.py`: 86
    - `fix_pygame_constants.py`: 28
    - `run_tests.py`: 192
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
    - `src\ui\button_manager.py`: 21
    - `src\ui\start_screen_layout_utils.py`: 10
    - `src\ui\start_screen_render_utils.py`: 23
    - `src\utils\__init__.py`: 0
    - `src\utils\linked_list.py`: 71
    - `src\utils\score.py`: 26
    - `src\utils\session_manager.py`: 29
    - `src\view\__init__.py`: 0
    - `src\view\input.py`: 20
    - `src\view\pygame_renderer.py`: 165
  - Tests:
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
  - **Total**: 4,008
- **🔥 Burn down rates**
  - 3/3 _week 8 milestones/requirements_ completed
    - 100% total
    - ~14% per day
  - 2/3 _week 9 milestones/requirements_ completed early
  - 1/3 sprint 2 _epic requirements_ completed
    - ~33% total
  - 9/14 sprint 2 _sub requirements_ completed
    - ~64% total
    - ~21% per week
    - ~3% per day
  - 10/17 sprint 2 _total requirements_ completed
    - ~59% total
    - ~20% per week
    - ~3% per day

---

### Summary of Progress

#### `game.py`

- Refactored state management system to use constants instead of booleans
- Key changes:
  - Added state management using `START_SCREEN`, `PLAYING`, and `GAME_OVER` constants
  - Implemented `start_new_game()` method to properly initialize/reset game state
  - Fixed game over state handling for escape and 'r' key inputs
  - Added proper state transitions between menus and gameplay

#### `app.py`

- Completely restructured main game loop to support start screen and state transitions
- Key changes:
  - Integrated state-based rendering system
  - Improved event processing for combined keyboard and mouse input
  - Separated rendering logic based on game state
  - Fixed game state transitions and input handling

#### `src/view/pygame_renderer.py`

- Added comprehensive start screen UI with game controls visualization
- Key changes:
  - Implemented visual key binding displays using arrow keys and spacebar images
  - Added interactive button system with hover and click effects
  - Created layered rendering with semi-transparent overlays
  - Added cursor state management for UI interaction
  - Improved game over screen with proper cursor reset

#### `src/ui/button.py` (new)

- Implemented new interactive button class
- Key features:
  - Configurable colors for normal, hover, and clicked states
  - Built-in color brightening/darkening effects
  - Rounded rectangle styling
  - Mouse position tracking for hover effects
  - Click state management

#### `src/ui/button_manager.py` (new)

- Created button management system
- Key features:
  - Centralized button collection management
  - Automated cursor state updates based on button hover
  - Unified button rendering
  - Click event handling with action dispatching

#### `src/ui/start_screen_layout_utils.py` (new)

- Added utilities for start screen layout calculations
- Key features:
  - Functions for centering popups on screen
  - Content area calculation with padding
  - Reusable layout helper functions

#### `src/ui/start_screen_render_utils.py` (new)

- Implemented rendering utilities for start screen
- Key features:
  - Semi-transparent overlay rendering
  - Popup background with drop shadow
  - Multi-line label rendering with auto-centering
  - Standardized rendering helpers for UI elements
