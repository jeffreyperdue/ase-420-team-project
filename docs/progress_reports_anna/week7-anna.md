# Week 7 Progress Report - Anna

- Dates: 10/27 - 11/2

---

## Progress

### Week 7 Goals Completed (3/3)

✅ Add multipliers for multiple lines (2, 3, 4) _(completed in Week 6)_

- _Fulfills sub requirement 1.3_

✅ Integrate scoring logic with the board (trigger only after validated line removal) _(completed in Week 6)_

- _Fulfills sub requirement 1.4_

✅ Expand unit tests to cover multipliers and edge cases.

- _Fulfills part of sub requirement 1.7_

---

### Additional Work Completed

#### Week 8 Goals Completed (2/3)

✅ Display current score in the UI and persist until reset.

- _Fulfills sub requirement 1.5_

✅ Display high score of the current session in‑game.

- _Fulfills sub requirement 1.6_

---

## Statistics

- **LoC** (my contributions)
  - Source:
    - `app.py`: 6
    - `src\constants.py`: 1
    - `src\game\game.py`: 10
    - `src\game\score.py`: 2
    - `src\utils\session_manager.py`: 29 (new)
    - `src\view\pygame_renderer.py`: 8
  - Tests:
    - `tests\test_scoring.py`: 96
    - `tests\test_score_utils.py`: 1
  - **Total**: 153
- **LoC** (entire codebase)
  - Source code:
    - `app.py`: 63
    - `fix_pygame_constants.py`: 28
    - `run_tests.py`: 192
    - `src\constants.py`: 29
    - `src\figures.py`: 16
    - `src\game\board.py`: 192
    - `src\game\game.py`: 88
    - `src\game\piece.py`: 26
    - `src\game\row.py`: 78
    - `src\starter_code\tetris_code_explained.py`: 189
    - `src\starter_code\tetris_ver1.py`: 202
    - `src\utils\linked_list.py`: 71
    - `src\utils\score.py`: 26
    - `src\utils\session_manager.py`: 29
    - `src\view\input.py`: 20
    - `src\view\pygame_renderer.py`: 91
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
    - `tests\test_scoring.py`: 150
  - **Total**: 3,664
- **🔥 Burn down rates**
  - 3/3 _week 7 milestones/requirements_ completed
    - 100% total
    - ~14% per day
  - 2/3 _week 8 milestones/requirements_ completed early
  - 0/3 sprint 2 _epic requirements_ completed
    - 0% total
  - 8/14 sprint 2 _sub requirements_ completed
    - ~57% total
    - ~29% per week
    - ~4% per day
  - 8/17 sprint 2 _total requirements_ completed
    - ~47% total
    - ~24% per week
    - ~3% per day

---

### Summary of Progress

#### `session_manager.py` (new)

- New singleton-style session manager added to persist session data across game instances.
- Key changes:
  - New module `src/utils/session_manager.py` implementing `SessionManager`.
  - `SessionManager` holds the session `high_score` and provides `update_high_score(score)` to update it atomically.
  - Implemented as a simple singleton so all parts of the program (different `Game` instances) share the same session state.

#### `app.py`

- Updated to integrate session-level high score handling and to centralize score rendering.
- Key changes:
  - Added import and instantiation of `SessionManager` so a single session-wide high score object persists across restarts.
  - Updated `Game` construction to pass the session manager instance into new game instances (so the game uses the session-managed high score).
  - Updated rendering calls to use the renderer's board-relative `draw_score(...)` method (removed hard-coded pixel offsets in `app.py`).
  - Ensured restart flow re-uses the same `SessionManager` instance so the session high score is not reset when pressing Restart.

#### `pygame_renderer.py`

- Added a function to render both the scores relative to the board.
- Key change:
  - Implemented `draw_score` to render both the current "Score" and the session "High Score".
    - Computes its position based on `board_x` / `board_y` and `CELL_SIZE` so the score stays correctly placed even if the board origin or screen size changes.

#### `constants.py`

- Small configuration update to support UI/layout changes.
- Key change:
  - Screen layout adjustments (screen width increased) to provide more horizontal space for the score panel.
    - (This made it easier to place the session high score to the right of the board without clipping.)

#### `game.py`

- Integrated session-level high score management and refined scoring interactions.
- Key changes:
  - The `Game` class now obtains the `SessionManager` instance (injected via `app.py`).
  - `_update_score` was updated to update the session manager's high score via `SessionManager.update_high_score(...)` when the player's score increases.
  - Added safety checks (no points after `game_over`) and ensured score-update logic remains encapsulated.

#### `score.py`

- Added type validation and expanded documentation.
- Key changes:
  - Input validation tightened for the scoring helper (`points_for_clear`): non-integer inputs (including `bool`) now raise `TypeError` so tests and call-sites cannot pass unexpected types.
  - Scoring mapping preserved (0→0, 1→100, 2→300, 3→500, 4→800); out-of-range integer values still return 0 by design.

#### `test_score_utils.py`

- Tests updated to reflect improved validation and to exercise new scoring edge-cases.
- Key changes:
  - Added/updated unit tests that validate `points_for_clear` rejects invalid input types (e.g., `None`, strings, floats, lists, dicts, booleans) and that it behaves correctly for out-of-range integer inputs.
  - Adjusted assertions to match the tightened `TypeError` behavior.

#### `test_scoring.py`

- Test suite expanded and fixed to cover integration and edge cases around scoring.
- Key changes:
  - Added tests verifying score accumulation, game-over freeze (no more points after game over), and that the session high score is updated only when appropriate.
  - Fixed a small expectation mismatch uncovered by new tests (score accumulation math and order-of-operations) and added negative/invalid input checks for `points_for_clear`.
