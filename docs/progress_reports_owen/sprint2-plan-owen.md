# Sprint 2 Plan - Owen Newberry

## Features

- **Total**: 2
  1. Difficulty Levels
  2. Ghost Piece

## Requirements

- **Total**: 11

### Difficulty Levels Requirements

1. As a player, I want the game to increase in difficulty over time so that I am challenged and engaged throughout longer gameplay sessions.
   - Acceptance criteria:
     - Game starts at level 1 with normal piece fall speed
     - Level increases based on lines cleared (e.g., every 10 lines = +1 level)
     - Higher levels have faster piece fall speeds
     - Level progression is displayed to the player
     - Scoring multipliers increase with higher levels
   - Sub requirements:
     - 1.1. As a developer, I want to implement a level system that tracks current difficulty so that the game can scale appropriately.
     - 1.2. As a developer, I want to adjust piece fall speed based on level so that gameplay becomes more challenging over time.
     - 1.3. As a developer, I want to display the current level to the player so that they can track their progress.
     - 1.4. As a developer, I want to integrate level progression with line clearing so that difficulty increases naturally.
     - 1.5. As a developer, I want to write unit tests for level progression so that I can verify correct difficulty scaling.

### Ghost Piece Requirements

2. As a player, I want to see where my current piece will land so I can make more precise placement decisions.
   - Acceptance criteria:
     - A transparent/outlined version of the current piece appears at the landing position
     - The ghost piece updates in real-time as the player moves and rotates the current piece
     - The ghost piece is visually distinct (different color/outline) from the main piece
     - The ghost piece disappears when the current piece is placed
   - Sub requirements:
     - 2.1. As a developer, I want to calculate the landing position of the current piece so that I can show where it will fall.
     - 2.2. As a developer, I want to render the ghost piece with a distinct visual style so that players can distinguish it from the main piece.
     - 2.3. As a developer, I want to update the ghost piece position in real-time so that it follows player movements accurately.
     - 2.4. As a developer, I want to write unit tests for ghost piece calculation so that I can verify correct landing position logic.

## Milestone Schedule

### Week 1 (10/20 - 10/26)

#### Focus: Difficulty Level Framework

- Implement level system that tracks current difficulty
  - _Sub requirement 1.1_: As a developer, I want to implement a level system that tracks current difficulty so that the game can scale appropriately.
- Create level display in the UI
  - _Sub requirement 1.3_: As a developer, I want to display the current level to the player so that they can track their progress.
- Write initial unit tests for level progression
  - _Sub requirement 1.5_: As a developer, I want to write unit tests for level progression so that I can verify correct difficulty scaling.

### Week 2 (10/27 - 11/2)

#### Focus: Level Progression & Ghost Piece Logic

- Integrate level progression with line clearing
  - _Sub requirement 1.4_: As a developer, I want to integrate level progression with line clearing so that difficulty increases naturally.
- Calculate landing position for ghost piece
  - _Sub requirement 2.1_: As a developer, I want to calculate the landing position of the current piece so that I can show where it will fall.
- Implement ghost piece collision detection logic
- Write unit tests for ghost piece calculation
  - _Sub requirement 2.4_: As a developer, I want to write unit tests for ghost piece calculation so that I can verify correct landing position logic.

### Week 3 (11/3 - 11/9)

#### Focus: Speed Adjustment & Ghost Rendering

- Adjust piece fall speed based on level
  - _Sub requirement 1.2_: As a developer, I want to adjust piece fall speed based on level so that gameplay becomes more challenging over time.
- Render ghost piece with distinct visual style
  - _Sub requirement 2.2_: As a developer, I want to render the ghost piece with a distinct visual style so that players can distinguish it from the main piece.
- Update ghost piece position in real-time
  - _Sub requirement 2.3_: As a developer, I want to update the ghost piece position in real-time so that it follows player movements accurately.

### Week 4 (11/10 - 11/16)

#### Focus: Integration & Polish

- Integrate difficulty levels with scoring system (Anna's feature)
- Polish ghost piece visual effects
- Test level progression edge cases
- Ensure smooth integration with existing game mechanics

### Week 5 (11/17 - 11/23)

#### Focus: Final Testing & Documentation

- Comprehensive testing of both features
- Documentation and code comments
- Manual testing and bug fixes
- Prepare for Sprint 2 presentation
