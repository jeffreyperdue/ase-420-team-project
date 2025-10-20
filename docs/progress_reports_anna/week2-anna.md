# Week 2 Progress Report: Refactoring Board Logic & Implementation

- Dates: 9/15 - 9/21

## Week 2 Goals:

✅ Refactor and optimize the playing field grid  
✅ Write unit tests for the playing field grid

## Statistics:

- **LoC:**
  - `src/starter_code/tetris_code_explained.py`: 289
  - `src/starter_code/tetris_ver1.py`: 206
  - `src/game/board.py`: 39
  - `src/tests/test_board.py` : 71
  - **Total**: 605
- **Burn down rate**
  - 20% per week
  - ~3% per day
  - Based on number of goals/milestones completed (2/10)

## Major Changes Completed

1. **Board Implementation & Migration**

   - Refactored board implementation to create a `Board` class
   - Moved `Board` class implementation to `board.py`
   - Placed import statements in `tetris_code_explained.py` and `tetris_ver1.py` to import `Board` class
   - Initialized a `Board` class instance

     ```python
     GameBoard = None
     ...
     def initialize(height, width):
       ...
       GameBoard = Board(height, width)
       ...
     ```

2. **Import System**

   - Added repository root to `sys.path` for reliable imports
   - Standardized import path to `from src.game.board import Board`
   - Fixed module resolution when running from `starter_code/` directory

   ```python
   import os
   import sys
   # Ensure repository root is on sys.path so imports work when running from starter_code
   repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
   if repo_root not in sys.path:
       sys.path.insert(0, repo_root)
   from src.game.board import Board
   ```

3. **Legacy Code Removal & Variable Updates**

   - Eliminated global `Field` variable
   - Initialized `Height` and `Width` variables with their respective values (`20` & `10`)

     ```python
      # Dimensions of the playing grid
      Height = 20
      Width = 10
     ```

   - Simplified board operations to always use `GameBoard` instance

4. **Function Updates**

   - `break_lines()`

     - Removed (unnecessary)
     - Called once in `freeze()`

       - Replaced with call to `clear_full_lines()` function of `Board` class

         ```python
         GameBoard.clear_full_lines()
         ```

   - `init_board()`

     - Removed (unnecessary)
     - Called once in `initialize()`

       - Replaced with call to `clear()` function of `Board` class

         ```python
         GameBoard.clear()
         ```

   - `draw_board()`

     - Now exclusively uses `GameBoard` for dimensions and cell values

5. **Unit Tests**

   - Generated unit tests in `test_board.py` for `Board` class
     - Board initialization
       - Valid dimensions
       - Invalid types
       - Invalid values
     - Board clearing
     - Setting & getting cell values
   - Total number of unit tests: 5

## Preserved Elements

1. **Comments and Documentation**

   - Kept original comments and section headers

2. **Game Logic**

   - Core gameplay mechanics unchanged
   - Piece movement and rotation behavior preserved

3. **Visual Elements**

   - Colors and figures definitions kept intact
   - UI constants (window size, block size) unchanged
   - Drawing routines preserved (just simplified to use `GameBoard`)

## Current State

- **Functionality**: Kept original functionality
- **Code Quality**: Improved by simplifying board logic into a class
- **Imports**: Working correctly (verified via import tests)
- **Dependencies**: Successfully using encapsulated `Board` from `src.game.board`
