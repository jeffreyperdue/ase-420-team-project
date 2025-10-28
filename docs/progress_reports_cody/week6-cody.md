# Week 6 Progress Report: Next Piece Preview UI

- Dates: 10/20 - 10/26

## Week 6 Goals:

✅ Create preview display area in the renderer
✅ Design and position the preview area consistently
✅ Write initial unit tests for preview display

- **LoC**
  - Source code:
    - `app.py`: 2
    - `src/game/game.py`: 2
    - `src/view/pygame_renderer.py`: 33
    - `src/constants.py`: 3
    - `tests/test_next_piece_preview.py`: 102
  - **Total**: 142
- **Burn down rates**
  - Sprint 2: 
    - 27% total
    - Based on total number of Sprint 2 goals/milestones completed (3/11)

---

## Summary of changes under src/

- Files changed:
  - `app.py`
  - `src/game/game.py`
  - `src/view/pygame_renderer.py`
  - `src/constants.py`
  - `tests/test_next_piece_preview.py`

---

## Major Changes

### 1. `app.py` & `game.py`

- Changes
    - **Implemented next piece preview feature**: Changed app and game files to use and render the next piece preview feature

### 2. `pygame_renderer.py`

- Changes
    - **Added `draw_next_piece_preview()` method**: Added a method to draw the box to display the next piece preview and the text that says "Next Piece"
    - **Added `draw_next_piece()` method**: Added method to draw the next piece inside of the next piece preview box on the right of the screen. Uses very similar logic to the draw_piece method except places the piece inside of the next piece preview box.

### 3. `constants.py`

- Changes
    - **Added `NEXT_PIECE_PREVIEW_RECT` method**: Added the rectangle to be drawn to store the next piece shape

### 4. `test_next_piece_preview.py`

- Changes
    - **Added unit tests for next piece preview feature**: Added unit tests to test next piece preview functionality

**Other Notes**: 
- Next Piece Preview Feature working
- All tests for next piece preview passing
- Minor visual bug can happen sometimes when certain shapes are rendered in next piece preview box where the pieces can appear slightly off centered, will see about fixing this next week