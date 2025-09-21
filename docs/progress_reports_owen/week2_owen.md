# Week 2 Progress Report: Refactoring Board Logic & Implementation

- Dates: 9/15 - 9/21

## Week 2 Goals:

- Implement board rendering with Pygame
- Add ability to draw active piece from game state
- Confirm rendering updates each frame in the game loop

## Statistics:

- **LoC:**
  - `src/game/game.py`: 36
  - `src/view/pygame_renderer.py`: 41
  - **Total**: 77
- **Burn down rate**
  - 27% per week
  - Based on number of goals/milestones completed (3/11)

## Major Changes Completed

1. **Rendering Implementation & Migration**

   - Refactored rendering logic into a dedicated `PygameRenderer` class.  
   - Moved rendering code out of `tetris_ver1.py` into `src/view/pygame_renderer.py`.  
   - `PygameRenderer` now handles:
     - Drawing the board grid (`draw_board`).  
     - Drawing the active piece (`draw_piece`).  
   - Example usage:  

     ```python
     renderer = PygameRenderer(screen)
     renderer.draw_board(GameBoard)
     renderer.draw_piece(current_piece)
     ```

2. **Import System**

   - Standardized imports across files so rendering can be accessed via:  

     ```python
     from src.view.pygame_renderer import PygameRenderer
     ```

3. **Function Updates**

   - **Board Rendering**
     - Was:  
       ```python
       for i in range(len(board)):
           for j in range(len(board[i])):
               pygame.draw.rect(screen, colors[board[i][j]], ...)
       ```
     - Now:  
       ```python
       renderer.draw_board(GameBoard)
       ```

   - **Active Piece Rendering**
     - Was:  
       ```python
       for i in range(4):
           for j in range(4):
               if i * 4 + j in piece.image():
                   pygame.draw.rect(screen, colors[piece.color], ...)
       ```
     - Now:  
       ```python
       renderer.draw_piece(current_piece)
       ```

   - **Game Loop Integration**
     - Rendering now updated every frame by calling renderer methods inside the loop.  

---

## Current State

- **Functionality**: Rendering now encapsulated in `PygameRenderer`, board and active piece both draw correctly.  
- **Code Quality**: Simplified main loop, removed redundant global drawing logic.  
- **Imports**: Clean and standardized (`from src.view...`).  
- **Dependencies**: Fully integrated with encapsulated `Board` and `Piece`.  
