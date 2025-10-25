# Week 6 Progress Report: Next Piece Preview UI

- Dates: 10/20 - 10/26

## Week 6 Goals:

✅ Create preview display area in the renderer
✅ Design and position the preview area consistently
✅ Write initial unit tests for preview display

- **LoC**
  - Source code:
    - `src/starter_code/tetris_ver1.py`: 213
    - `src/game/board.py`: 293
    - `src/game/row.py`: 95
  - **Total**: 642
- **Burn down rates**
  - Sprint 1: 
    - 100% total
    - Based on total number of Sprint 1 goals/milestones completed (13/13)

---

## Summary of changes under src/

- Files changed:
  - `src/starter_code/tetris_ver1.py`
  - `src/game/board.py`
  - `src/game/row.py`

---

## Major Changes

### 1. `tetris_ver1.py`

- Changes
    - **Fixed mixed logic approaches**: Removed conflicting global variable functions and converted to pure class-based approach
    - **Resolved race conditions**: Fixed timing issues where pieces could move multiple times per frame when using manual controls
    - **Improved piece placement logic**: Separated temporary piece positioning from permanent freezing to prevent incorrect placement
    - **Enhanced timing control**: Added frame-based movement protection and proper timer resets for consistent new piece spawning
    - **Code cleanup and organization**: Improved structure, naming conventions, documentation, and removed unused variables
    - **Fixed game over detection**: Properly handles collision detection for new pieces at the top of the board

### 2. `board.py`

- Changes
    - **Added `freeze_piece()` method**: Dedicated method for permanent piece placement without tracking for removal
    - **Fixed movement methods**: Updated `go_down()`, `go_side()`, and `rotate()` to only modify piece position without permanent placement
    - **Improved collision detection**: Enhanced position state management with proper original position storage and restoration
    - **Added `get_cell_color()` method**: Enables proper color retrieval for drawing placed pieces

### 3. `row.py`

- Changes
    - **Added `clear_bit()` method**: Missing method that was being called by Board class for clearing individual cells
    - **Enhanced bit manipulation**: Proper bit clearing with color data removal

### Other Notes
- Game now runs smoothly with proper piece movement, rotation, and placement
- All major timing and collision issues have been resolved
- Manual controls (arrow keys, space, down key) work correctly without race conditions
- Game properly handles piece freezing, line clearing, and game over conditions
