# Sprint 2 Plan - Anna Dinius

## Features

- **Total**: 3
  1. Scoring system
  2. Game start screen
  3. Enhanced game over screen

## Requirements

- **Total**: 14

### Scoring System Requirements

1. As a player, I want the game to award points for cleared lines so that I can track progress and compete for a higher score.
   - Acceptance criteria:
     - Clearing one line awards a base number of points (configurable constant).
     - Clearing multiple lines in a single drop awards bonus multipliers (e.g., double/triple points for 2/3+ lines).
     - The current score is displayed in-game and persists until the game is reset or a new game is started.
     - Score increments are triggered only after lines are validated and removed by the board logic.
     - The high score of the current session is displayed in-game.
   - Sub requirements:
     - 1.1. As a developer, I want to implement scoring logic that is decoupled from rendering so that it can be unit-tested independently.
     - 1.2. As a developer, I want to implement a base scoring function that awards points for clearing one line so that the game has a foundation for tracking player progress.
     - 1.3. As a developer, I want to add multipliers for clearing multiple lines (2, 3, 4) so that the scoring system reflects increasing difficulty and rewards skilled play.
     - 1.4. As a developer, I want to integrate the scoring logic with the board so that points are only awarded after lines are validated and removed, ensuring accuracy.
     - 1.5. As a developer, I want to display the current score in the UI and persist it until reset so that players can see their progress throughout the game.
     - 1.6. As a developer, I want to display the high score of the current session in-game
     - 1.7. As a developer, I want to write unit tests for the scoring logic (base, multipliers, edge cases) so that I can verify correctness and prevent regressions.

### Start Screen Requirements

2. As a player, I want an informative game-over screen that shows my final score and a simple option to restart or quit so that I can quickly play again or exit.
   - Acceptance criteria:
     - When the board determines a game-over condition (piece cannot spawn), the game loop stops and the game-over screen is displayed.
     - The game-over screen displays the final score, the highest score for the current session (if tracked), and two options: Restart or Main Menu.
     - Selecting Restart resets the board, score, and level and begins a new game; selecting Main Menu returns to the start screen.
     - The screen is rendered using the existing `pygame_renderer` and does not require changes to core game logic.
   - Sub requirements:
     - 2.1. As a developer, I want to render a start screen with the title, controls, and a prompt so that players have clear instructions before beginning.
     - 2.2. As a developer, I want to implement a transition from the start screen into the game loop when any key is pressed so that players can begin play intuitively.
     - 2.3. As a developer, I want to write unit tests for the start screen transition logic so that I can verify the game begins correctly when a key is pressed.

### Game Over Screen Requirements

3. As a player, I want a clear start screen with a visible "Press any key to start" prompt and explanation of the game controls so that I know how to begin a game and which keys to use to play the game.
   - Acceptance criteria:
     - A start screen is shown when the application launches and when returning to the main menu (start screen) after a game over.
     - The start screen shows the game title, basic controls (arrow keys, space, rotate), and a short prompt to begin.
     - Pressing any key transitions from the start screen into the active game loop and spawns the first piece.
   - Sub requirements:
     - 3.1. As a developer, I want to render a game-over screen showing the final score, high score, and options so that players receive feedback and choices after losing.
     - 3.2. As a developer, I want to implement a restart flow that resets the board, score, and level so that players can quickly start a new game.
     - 3.3. As a developer, I want to implement a return-to-menu (start screen) flow that navigates back to the start screen so that players can exit gracefully and choose when to play again.
     - 3.4. As a developer, I want to write unit tests for game-over detection and restart/menu flows so that I can ensure players receive the correct options and state resets after losing.

## Milestone Schedule

### Week 1 (10/20 - 10/26)

#### Focus: Scoring system foundation

- Implement scoring logic decoupled from rendering (testable module).
  - _Sub requirement 1.1_: As a developer, I want to implement scoring logic that is decoupled from rendering so that it can be unit-tested independently.
- Implement base scoring function (award points for clearing one line).
  - _Sub requirement 1.2_: As a developer, I want to implement a base scoring function that awards points for clearing one line so that the game has a foundation for tracking player progress.
- Write initial unit tests for base scoring.
  - _Sub requirement 1.7_: As a developer, I want to write unit tests for the scoring logic (base, multipliers, edge cases) so that I can verify correctness and prevent regressions.

### Week 2 (10/27 - 11/2)

#### Focus: Scoring enhancements

- Add multipliers for multiple lines (2, 3, 4).
  - _Sub requirement 1.3_: As a developer, I want to add multipliers for clearing multiple lines (2, 3, 4) so that the scoring system reflects increasing difficulty and rewards skilled play.
- Integrate scoring logic with the board (trigger only after validated line removal).
  - _Sub requirement 1.4_: As a developer, I want to integrate the scoring logic with the board so that points are only awarded after lines are validated and removed, ensuring accuracy.
- Expand unit tests to cover multipliers and edge cases.
  - _Sub requirement 1.7_: As a developer, I want to write unit tests for the scoring logic (base, multipliers, edge cases) so that I can verify correctness and prevent regressions.

### Week 3 (11/3 - 11/9)

#### Focus: Score display & persistence

- Display current score in the UI and persist until reset.
  - _Sub requirement 1.5_: As a developer, I want to display the current score in the UI and persist it until reset so that players can see their progress throughout the game.
- Display high score of the current session in‑game.
  - _Sub requirement 1.6_: As a developer, I want to display the high score of the current session in-game.
- Finalize scoring system unit test coverage.
  - _Sub requirement 1.7_: As a developer, I want to write unit tests for the scoring logic (base, multipliers, edge cases) so that I can verify correctness and prevent regressions.

### Week 4 (11/10 - 11/16)

#### Focus: Start screen implementation

- Render start screen with title, controls, and prompt.
  - _Sub requirement 2.1_: As a developer, I want to render a start screen with the title, controls, and a prompt so that players have clear instructions before beginning.
- Implement transition from start screen into the game loop (press any key → spawn first piece).
  - _Sub requirement 2.2_: As a developer, I want to implement a transition from the start screen into the game loop when any key is pressed so that players can begin play intuitively.
- Write unit tests for start screen transition logic.
  - _Sub requirement 2.3_: As a developer, I want to write unit tests for the start screen transition logic so that I can verify the game begins correctly when a key is pressed.

### Week 5 (11/17 - 11/23)

#### Focus: Game over screen implementation

- Render game‑over screen with final score, high score, and options.
  - _Sub requirement 3.1_: As a developer, I want to render a game-over screen showing the final score, high score, and options so that players receive feedback and choices after losing.
- Implement restart flow (reset board, score, level).
  - _Sub requirement 3.2_: As a developer, I want to implement a restart flow that resets the board, score, and level so that players can quickly start a new game.
- Implement return‑to‑menu flow (navigate back to start screen).
  - _Sub requirement 3.3_: As a developer, I want to implement a return-to-menu (start screen) flow that navigates back to the start screen so that players can exit gracefully and choose when to play again.
- Write unit tests for game-over detection and restart/menu flows.
  - _Sub requirement 3.4_: As a developer, I want to write unit tests for game-over detection and restart/menu flows so that I can ensure players receive the correct options and state resets after losing.
