---
marp: true
size: 4:3
paginate: true
theme: default
---

# Tetris Game
## User Guide

**Version:** 1.0  
**Welcome to Tetris!** This guide will help you get started and master the game.

---

## Table of Contents

1. **Getting Started**
2. **Game Controls**
3. **Gameplay Basics**
4. **Scoring System**
5. **Levels & Progression**
6. **Game Features**
7. **Tips & Strategies**
8. **Troubleshooting**

---

## Getting Started

### System Requirements

- **Operating System:** Windows, macOS, or Linux
- **Python:** Version 3.x
- **Dependencies:** Pygame library
- **Display:** 600x500 pixel window

### Launching the Game

1. Open a terminal/command prompt
2. Navigate to the game directory
3. Run: `python app.py`
4. The game window will open with the start screen

---

## Getting Started (Continued)

### First Launch

When you first start the game, you'll see:
- **Start Screen** with game title
- **Controls diagram** showing keyboard layout
- **Start Game** button (or press Enter)
- **Exit** button (or press ESC)

Click "Start Game" or press **Enter** to begin playing!

---

## Game Controls

### Movement Controls

**Arrow Keys:**
- **↑ (Up Arrow):** Rotate piece clockwise
- **← (Left Arrow):** Move piece left
- **→ (Right Arrow):** Move piece right
- **↓ (Down Arrow):** Soft drop (move down faster)

**Space Bar:** Hard drop (instantly drop piece to bottom)

---

## Game Controls (Continued)

### Game Management Controls

**P:** Pause/Resume game  
**ESC:** Pause game (also quits from start/game over screens)  
**R:** Restart current game  
**Enter:** Start new game (from start screen)  
**Mouse:** Click buttons in menus

**Note:** You can also click the "Pause" button in the top-right corner during gameplay.

---

## Gameplay Basics

### Objective

The goal of Tetris is to:
1. **Rotate and position** falling pieces to create complete horizontal lines
2. **Clear lines** by filling them completely
3. **Prevent** the stack from reaching the top
4. **Score points** and advance to higher levels

---

## Gameplay Basics (Continued)

### How Pieces Work

- Pieces fall from the top of the board
- Each piece has a unique shape (I, Z, S, L, J, T, O)
- Pieces can be rotated and moved left/right
- Pieces lock in place when they land
- Complete horizontal lines are automatically cleared

---

## Gameplay Basics (Continued)

### Game Over

The game ends when:
- A new piece cannot spawn because the spawn area is blocked
- The stack reaches the top of the playing field

When the game ends:
- Your final score is displayed
- You can choose to "Play Again" or "Quit"
- Your high score is tracked for the session

---

## Scoring System

### Base Scoring

Points are awarded when you clear lines:

- **1 line cleared:** 100 points
- **2 lines cleared:** 300 points
- **3 lines cleared:** 500 points
- **4 lines cleared:** 800 points

**Tip:** Clearing multiple lines at once gives bonus points!

---

## Scoring System (Continued)

### Level-Based Scoring

As you progress through levels, you earn additional points:
- A **level multiplier** increases your score
- Higher levels = higher multipliers
- The multiplier formula: `1.0 + (level - 1) × 0.1`

**Example:** At level 3, you get a 1.2× multiplier on base points.

---

## Scoring System (Continued)

### High Score

- Your **current score** is displayed during gameplay
- Your **high score** (best score this session) is tracked
- High score persists across game restarts in the same session
- Beat your high score to set a new record!

---

## Levels & Progression

### Level System

- **Starting Level:** Level 1
- **Level Advancement:** Every 10 lines cleared = +1 level
- **Display:** Current level shown in top-left corner

**Example:**
- Clear 10 lines → Level 2
- Clear 20 lines total → Level 3
- Clear 30 lines total → Level 4

---

## Levels & Progression (Continued)

### Gravity System

As levels increase, pieces fall faster:
- **Level 1:** Base speed (30 frames per move)
- **Each level:** Pieces fall 3 frames faster
- **Minimum speed:** Caps at 10 frames per move

**Display:** Current gravity delay shown in top-right corner

**Challenge:** Higher levels require faster decision-making!

---

## Game Features

### Visual Aids

**Ghost Piece:**
- Semi-transparent outline shows where the piece will land
- Helps you plan placement
- Only visible during active gameplay (not when paused)

**Next Piece Preview:**
- Shows the upcoming piece in the preview box
- Located on the right side of the screen
- Helps you plan ahead

---

## Game Features (Continued)

### On-Screen Information

**Top-Left Display:**
- Current **Level**
- Total **Lines** cleared

**Top-Right Display:**
- **Gravity** delay (frames)

**Right Side Display:**
- Current **Score**
- Session **High Score**

---

## Game Features (Continued)

### Pause Functionality

**To Pause:**
- Press **P** or **ESC**
- Click the "Pause" button (top-right)

**While Paused:**
- Game stops completely
- Pause menu shows current score and high score
- Options: Resume, Restart, or Quit

**To Resume:**
- Press **P** or **ESC** again
- Click "Resume" button
- Click anywhere on the pause screen

---

## Tips & Strategies

### Basic Tips

1. **Plan Ahead:** Use the next piece preview to think ahead
2. **Use Ghost Piece:** The ghost outline shows landing position
3. **Clear Multiple Lines:** Aim for 2-4 line clears for bonus points
4. **Keep Left Side Clear:** Leave space for the I-piece (long vertical)
5. **Don't Panic:** Take your time, especially at higher levels

---

## Tips & Strategies (Continued)

### Advanced Strategies

**Tetris (4-line clear):**
- Try to build a well on one side
- Save the I-piece for clearing 4 lines at once
- Highest scoring move!

**Soft Drop vs Hard Drop:**
- Use **Down Arrow** for controlled placement
- Use **Space** when you're sure of placement
- Hard drop locks immediately

---

## Tips & Strategies (Continued)

### Rotation Tips

- Pieces rotate **clockwise** (Up Arrow)
- Some pieces have 4 rotation states, others have fewer
- The O-piece (square) doesn't change when rotated
- Practice rotating pieces in tight spaces

**Pro Tip:** Learn the rotation patterns for each piece type!

---

## Troubleshooting

### Common Issues

**Game won't start:**
- Ensure Python 3.x is installed
- Check that Pygame is installed: `pip install pygame`
- Verify you're in the correct directory

**Controls not responding:**
- Make sure the game window has focus (click on it)
- Check that no other application is capturing keyboard input
- Try clicking the window to refocus

---

## Troubleshooting (Continued)

### Display Issues

**Window too small/large:**
- Game window is fixed at 600x500 pixels
- Cannot be resized in current version

**Graphics look blurry:**
- This is normal for pixel-based graphics
- Game uses 20x20 pixel cells for optimal retro look

**Pieces not visible:**
- Ensure game is not paused
- Check that pieces are within board boundaries

---

## Troubleshooting (Continued)

### Gameplay Issues

**Piece stuck or not moving:**
- Game may be paused (check for pause menu)
- Piece may have locked in place (normal behavior)
- Try pressing P to toggle pause

**Score not updating:**
- Score only increases when lines are cleared
- Check that you're completing full horizontal lines
- Score updates immediately after line clear

---

## Quick Reference

### Essential Controls

| Action | Key |
|--------|-----|
| Rotate | ↑ |
| Move Left | ← |
| Move Right | → |
| Soft Drop | ↓ |
| Hard Drop | Space |
| Pause | P or ESC |
| Restart | R |
| Start Game | Enter |

---

## Quick Reference (Continued)

### Scoring Reference

| Lines Cleared | Base Points |
|---------------|-------------|
| 1 line | 100 |
| 2 lines | 300 |
| 3 lines | 500 |
| 4 lines | 800 |

**Remember:** Level multiplier increases these values!

---

## Quick Reference (Continued)

### Level Progression

- **Level 1:** Start here
- **+1 Level:** Every 10 lines cleared
- **Speed Increase:** 3 frames faster per level
- **Minimum Speed:** 10 frames (reached around level 8)

**Challenge yourself:** How high can you go?

---

## Game Screen Layout

### Visual Overview

```
┌─────────────────────────────────────┐
│ Level: X    Gravity: X frames       │
│ Lines: X                            │
│                                     │
│  ┌──────────┐  Score: XXXX         │
│  │          │  High: XXXX          │
│  │  BOARD   │                       │
│  │          │  ┌─────────┐         │
│  │          │  │  Next   │         │
│  │          │  │  Piece  │         │
│  └──────────┘  └─────────┘         │
│                                     │
│              [Pause Button]         │
└─────────────────────────────────────┘
```

---

## Piece Types

### The Seven Tetris Pieces

**I-Piece (Line):**
- Long vertical/horizontal bar
- Best for clearing 4 lines (Tetris!)

**O-Piece (Square):**
- 2x2 block
- Doesn't rotate
- Good for filling gaps

---

## Piece Types (Continued)

**T-Piece:**
- T-shaped
- Versatile for many situations

**L-Piece & J-Piece:**
- Mirror images of each other
- Good for corners and edges

**S-Piece & Z-Piece:**
- Mirror images
- Useful for interlocking patterns

---

## Best Practices

### For Beginners

1. **Start Slow:** Focus on clearing 1-2 lines at a time
2. **Learn Rotations:** Practice rotating each piece type
3. **Watch the Preview:** Always check the next piece
4. **Use Pause:** Don't hesitate to pause and think
5. **Have Fun:** Enjoy the challenge!

---

## Best Practices (Continued)

### For Advanced Players

1. **Build Strategically:** Create wells for Tetris clears
2. **Manage Gaps:** Avoid creating unfillable holes
3. **Speed Control:** Master soft drop for precision
4. **Pattern Recognition:** Learn common piece sequences
5. **High Score Challenge:** Compete against yourself!

---

## Game States

### Understanding Game Flow

**Start Screen:**
- Initial screen when game launches
- Shows controls and start options
- Press Enter or click "Start Game"

**Playing:**
- Active gameplay state
- Pieces falling and gameplay happening
- Can pause at any time

---

## Game States (Continued)

### Understanding Game Flow

**Paused:**
- Game temporarily stopped
- Can resume, restart, or quit
- Score and high score still visible

**Game Over:**
- Game has ended
- Final score displayed
- Options to play again or quit

---

## Additional Information

### Session Management

- **High Score:** Tracks your best score for the current session
- **Session Persistence:** High score remains until you close the game
- **New Game:** Each new game starts fresh (score resets, level resets)

**Note:** High scores are not saved between game sessions (closing and reopening the application).

---

## Additional Information (Continued)

### Technical Details

**Frame Rate:** 60 FPS  
**Board Size:** 10 columns × 20 rows  
**Cell Size:** 20×20 pixels  
**Starting Position:** Pieces spawn at column 3, row 0

These settings are optimized for smooth gameplay and classic Tetris feel.

---

## Getting Help

### Resources

- **This User Guide:** Comprehensive reference
- **In-Game Controls:** Shown on start screen
- **Design Documentation:** See `docs/design_architecture.marp.md` for technical details

### Common Questions

**Q: Can I change the controls?**  
A: Not in the current version. Controls are fixed as documented.

**Q: Can I save my high score?**  
A: High scores persist during the session but reset when you close the game.

---

## Getting Help (Continued)

### Common Questions

**Q: Why do pieces fall faster over time?**  
A: This is the level progression system. Every 10 lines cleared increases the level and speed.

**Q: What's the ghost piece for?**  
A: It shows where your current piece will land, helping you plan placement.

**Q: Can I play with a gamepad?**  
A: Currently only keyboard and mouse are supported.

---

## Conclusion

### Enjoy the Game!

You now have all the information you need to play Tetris!

**Remember:**
- Practice makes perfect
- Start slow and build speed
- Challenge yourself to beat your high score
- Most importantly, have fun!

**Good luck and happy stacking!**

---

## End of User Guide

**Thank you for playing Tetris!**

For technical documentation, see:  
`docs/design_architecture.marp.md`

For project information, see:  
`docs/final_presentation.marp.md`

