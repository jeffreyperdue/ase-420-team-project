Features (Sprint 1)

Total Features: 9

Core Features

Anna – Board & Line Clearing

Files:

board.py
services.py (line clear part)
test_lineclear.py
Features:
Build playing field grid
Detect and clear full lines

Responsibilities:

Build the playing field grid (empty rows/columns).
Implement line-clearing logic (detect full rows, collapse them).
Write simple tests to check that a full row disappears and rows above fall down.
Document how the board is represented (for team slides).
Cody – Pieces & Collision

Files:

piece.py
services.py (collision part)
figures.py
test_piece.py, test_collision.py
Features:
Represent game pieces with type, rotation, position, and color
Allow pieces to move and rotate
Prevent illegal moves with collision detection

Responsibilities:

Represent a piece (type, rotation, position, color).
Implement rotation and movement logic.
Implement collision checks (walls, floor, other pieces).
Write tests for rotations and collision scenarios.
Document how pieces/rotations are represented (for team slides).
Owen – Rendering & Controls

Files:

pygame_renderer.py
input.py
app.py (game loop wiring)

Features:

Render empty board on screen
Render falling piece and locked pieces
Map keyboard input to intents
Display “Game Over” overlay when game ends

Responsibilities:

Draw the board and pieces using Pygame.
Handle keyboard input (left, right, rotate, drop, quit).
Hook Game + Board + Piece together into a working loop (with leader guidance).
Add a simple “Game Over” overlay.
Document how input and rendering work (for team slides)
Requirements (Sprint 1)




Total Requirements: 9

Anna Dinius

As a player, I want to see a grid playing field so I know where the boundaries of the game are.
As a player, I want full lines to be automatically cleared from the playing field so I can continue playing.

Cody King

As a player, I want each piece to have a distinct shape, orientation, and color so I can easily understand how it fits on the board.
As a player, I want to be able to move and rotate pieces so I can place them where I want on the grid.
As a player, I want pieces to stop at the walls, floor, or other pieces so the game follows logical physical boundaries.

Owen Newberry

As a player, I should be able to use the keyboard as input so that I can move the pieces on the grid and control gameplay.
As a player, I should be able to see a "Game Over" window when the loss conditions are met so that I know the game is over.
As a player, I should see an empty grid be rendered at the beginning.
As a player, I want to see the current falling piece and locked pieces so that I can track the game state.







Schedule / Milestones (Sprint 1)

Anna Dinius

Week 2 (9/15 - 9/21)
Refactor and optimize the playing field grid
Write unit tests for the playing field grid
Week 3 (9/22 - 9/28)
Refactor and optimize the line detection and clearing logic
Write unit tests for line detection and clearing
Week 4 (9/29 - 10/5)
Test edge cases and error handling
Optimize code further (if possible) and clean up code
Add code comments and documentation
Week 5 (10/6 - 10/12)
Finalize comments and documentation
Integrate changes with other teammates' changes
Prepare for Sprint 1 presentation

Cody King

Week 2 (9/15 – 9/21): Requirements & Design
Finalize requirements for piece representation and movement/rotation features.
Design the Piece class structure
Start defining structure of figures.py to hold shape and rotation data for all pieces
Week 3 (9/22 – 9/28): Piece Representation
Implement Piece class in current code
Define all piece shapes and rotation states in figures.py
Write unit tests to verify proper piece initialization
Week 4 (9/29 – 10/5): Movement & Rotation
Implement logic for movement
Implement rotation logic using rotation states from figures.py
Ensure piece state updates correctly after each action (move or rotate)
Add unit tests to cover basic movement and rotation scenarios
Week 5 (10/6 – 10/12): Polish & Wrap Up
Do more manual testing to ensure logic of game is working correctly
Add more unit tests to fill in any gaps where needed
Review implementation against initial requirements and fix any discrepancies

Owen Newberry

Week 2
Implement board rendering with Pygame
Add ability to draw active piece from game state
Confirm rendering updates each frame in the game loop
Week 3
Implement keyboard input mapping
Return intents as simple command lists for the game loop
Verify intents by logging them in console
Week 4
Set up app.py main loop
Integrate rendering and input with the shared Game object
Demo a working cycle where piece responds to arrow key movement
Week 5
Add “Game Over” overlay
consistent colors, readable grid, quit behavior stable
Decisions Made

We decided to work from the same repository, where the main branch will serve as our "production" branch, and each team member will create branches as necessary beginning with their name.

We decided if your code breaks the main branch, it is your responsibility to fix it.