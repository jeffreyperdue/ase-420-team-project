# Sprint 2 Plan - Anna Dinius

## Features

- **Total**: 3
  1. Scoring system
  2. Game start screen
  3. Enhanced game over screen

## Scoring System Requirements

1. As a player, I want the game to award points for cleared lines so that I can track progress and compete for a higher score.
   - Acceptance criteria:
     - Clearing one line awards a base number of points (configurable constant).
     - Clearing multiple lines in a single drop awards bonus multipliers (e.g., double/triple points for 2/3+ lines).
     - The current score is displayed in-game and persists until the game is reset or a new game is started.
     - Score increments are triggered only after lines are validated and removed by the board logic.
     - The high score of the current session is displayed in-game.
   - Sub requirements:
     1. As a developer, I want to implement scoring logic that is decoupled from rendering so that it can be unit-tested independently.
     2. As a developer, I want to implement a base scoring function that awards points for clearing one line so that the game has a foundation for tracking player progress.
     3. As a developer, I want to add multipliers for clearing multiple lines (2, 3, 4) so that the scoring system reflects increasing difficulty and rewards skilled play.
     4. As a developer, I want to integrate the scoring logic with the board so that points are only awarded after lines are validated and removed, ensuring accuracy.
     5. As a developer, I want to display the current score in the UI and persist it until reset so that players can see their progress throughout the game.
     6. As a developer, I want to write unit tests for the scoring logic (base, multipliers, edge cases) so that I can verify correctness and prevent regressions.

## Start Screen Requirements

1. As a player, I want an informative game-over screen that shows my final score and a simple option to restart or quit so that I can quickly play again or exit.
   - Acceptance criteria:
     - When the board determines a game-over condition (piece cannot spawn), the game loop stops and the game-over screen is displayed.
     - The game-over screen displays the final score, the highest score for the current session (if tracked), and two options: Restart or Main Menu.
     - Selecting Restart resets the board, score, and level and begins a new game; selecting Main Menu returns to the start screen.
     - The screen is rendered using the existing `pygame_renderer` and does not require changes to core game logic.
   - Sub requirements:
     1. As a developer, I want to render a start screen with the title, controls, and a prompt so that players have clear instructions before beginning.
     2. As a developer, I want to implement a transition from the start screen into the game loop when any key is pressed so that players can begin play intuitively.

## Game Over Screen Requirements

1. As a player, I want a clear start screen with a visible "Press any key to start" prompt and explanation of the game controls so that I know how to begin a game and which keys to use to play the game.
   - Acceptance criteria:
     - A start screen is shown when the application launches and when returning to the main menu (start screen) after a game over.
     - The start screen shows the game title, basic controls (arrow keys, space, rotate), and a short prompt to begin.
     - Pressing any key transitions from the start screen into the active game loop and spawns the first piece.
   - Sub requirements:
     1. As a developer, I want to detect when a new piece cannot spawn so that I can trigger the game-over state at the correct time.
     2. As a developer, I want to render a game-over screen showing the final score, high score, and options so that players receive feedback and choices after losing.
     3. As a developer, I want to implement a restart flow that resets the board, score, and level so that players can quickly start a new game.
     4. As a developer, I want to implement a return-to-menu (start screen) flow that navigates back to the start screen so that players can exit gracefully and choose when to play again.
