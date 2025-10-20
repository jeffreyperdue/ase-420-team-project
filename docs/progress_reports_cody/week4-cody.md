# Week 4 Progress Report: Movement & Rotation

- Dates: 9/29 - 10/5

## Week 4 Goals:

✅ Implement logic for movement
✅ Implement rotation logic using rotation states from figures.py
❌ Ensure piece state updates correctly after each action (move or rotate)
✅ Add unit tests to cover basic movement and rotation scenarios

- **LoC**
  - Source code:
    - `src/constants.py`: 28
    - `src/figures.py`: 16
    - `src/game/board.py`: 160
    - `src/game/game.py`: 30
    - `src/game/piece.py`: 26
    - `src/game/row.py`: 71
    - `src/starter_code/tetris_code_explained.py`: 187
    - `src/starter_code/tetris_ver1.py`: 178
    - `src/utils/linked_list.py`: 44
    - `src/view/input.py`: 18
    - `src/view/pygame_renderer.py`: 34
  - Unit tests:
    - `tests/__init__.py`: 0
    - `tests/test_board.py`: 86
    - `tests/test_linked_list.py`: 35
    - `tests/test_piece.py`: 76
    - `tests/test_row.py`: 27
  - **Total**: 1016
- **Burn down rates**
  - Sprint 1: 
    - 69% total
    - Based on total number of Sprint 1 goals/milestones completed (9/13)

---

## Summary of changes under src/

- Files changed:
  - `src/game/piece.py`
  - `src/game/board.py`
  - `src/game/row.py`

---

### Major Changes

### 1. `piece.py`

- Changes
    - Moved all the movement and rotation functions to `board.py`
    - Changed to where piece instance is now passed into movement and rotation functions in board class

### 2. `board.py`

- Changes
    - Added movement and rotation functions to this class
    - Changed piece visual state to be updated after each movement or rotation
    - Fixed a bug in `grid_position_to_coords` causing piece to be placed in wrong position on board

### Other Notes
 - Was not able to completely integrate movement and rotation into starter code this week for manual testing
   - Will finish this up near the end of this week after midterm