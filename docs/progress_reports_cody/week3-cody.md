# Week 3 Progress Report: Piece Representation

- Dates: 9/22 - 9/28

## Week 3 Goals:

✅ Implement Piece class in current code
✅ Define all piece shapes and rotation states in figure.py
✅ Write unit tests to verify proper piece initalization

- **LoC:**
  - Source code:
    - `src/constants.py`: 28
    - `src/figures.py`: 16
    - `src/game/board.py`: 99
    - `src/game/game.py`: 30
    - `src/game/piece.py`: 66
    - `src/game/row.py`: 63
    - `src/starter_code/tetris_code_explained.py`: 187
    - `src/starter_code/tetris_ver1.py`: 177
    - `src/utils/linked_list.py`: 44
    - `src/view/input.py`: 18
    - `src/view/pygame_renderer.py`: 34
  - Unit tests:
    - `tests/__init__.py`: 0
    - `tests/test_board.py`: 86
    - `tests/test_linked_list.py`: 35
    - `tests/test_piece.py`: 20
    - `tests/test_row.py`: 27
  - **Total**: 930
- **Burn down rates**
  - Sprint 1:
    - 46% total
    - Based on total number of Sprint 1 goals/milestones completed (6/13)

---

## Summary of changes under src/

- Files changed:
  - `src/game/piece.py`
  - `src/game/board.py`

---

## Major Changes

### 1. `board.py`

- Encapsulates the playing field in a `Board` class using `Row` bitboards and a `LinkedList` to hold the rows in sequence.
- Provides board operations such as clearing, cell access, and clearing full lines.

- Changes

    - Completed the `will_piece_collide` and `place_piece` methods
    - Methods are using the piece class to place tetronimo on board or to check for collision with other piece

### 2. `piece,py`

- Encapsulates the information about a piece in a class. Does not actively initalize a piece onto the board but stores information about a piece.
- Provides movement methods for the piece (not implemented yet but will be in week 4)

- Changes

    - Removed the check collision method from this class since it makes more sense to belond in the board