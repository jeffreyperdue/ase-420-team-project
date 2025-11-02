# Week 7 Progress Report: Pause/Resume

- Dates: 10/27 - 11/2

## Week 7 Goals:

✅ Integrate preview with next piece generation system
✅ Add pause state management to the game loop
✅ Modify input handling for pause/resume commands

- **LoC**
  - Source code:
    - `app.py`: 8
    - `src/game/game.py`: 12
    - `src/view/input.py`: 8
    - `src/view/pygame_renderer.py`: 46
  - **Total**: 74
- **Burn down rates**
  - Sprint 2:
    - 50% total
    - Based on Sprint 2 goals/milestones completed (6/12)

---

## Summary of changes under src/

- Files changed:
  - `app.py`
  - `src/game/game.py`
  - `src/view/input.py`
  - `src/view/pygame_renderer.py`

---

## Major Changes

### 1. `src/view/pygame_renderer.py`

- Changes
  - Fixed next piece preview centering by computing the piece's 4x4 bounding box (min/max rows/cols) and offsetting so the shape is centered within `NEXT_PAGE_PREVIEW_RECT`.
  - Added `draw_pause_screen()` to render a semi-transparent overlay with a centered "PAUSED" label and instruction text.

### 2. `src/game/game.py`

- Changes
  - Added `paused` state to the `Game` class.
  - Updated `apply()` to toggle pause on `PAUSE` and resume on `CLICK` when paused; movement/rotate/drop are ignored while paused.
  - Gated gravity updates in `update()` so the game state freezes when paused.

### 3. `src/view/input.py`

- Changes
  - Mapped `ESC` to `PAUSE`.
  - Emitted a `CLICK` intent on `MOUSEBUTTONDOWN` to support click-to-resume.

### 4. `app.py`

- Changes
  - Integrated pause overlay rendering when the game is paused.

---

**Other Notes**
- Next Piece Preview now renders centered consistently across all shapes/rotations.
- Pause/Resume UX verified in manual runs (ESC to pause/resume; click also resumes).
