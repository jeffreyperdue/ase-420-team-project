# Week 2 Progress Report: Requirements & Design

- Dates: 9/15 - 9/21

## Week 2 Goals:

✅ Finalize requirements for piece representation and movement/rotation features.  
✅ Design the Piece class structure.
✅ Start Defining structure of figures.py to hold shape and rotation data for all pieces.

## Statistics:

- **LoC:**
  - `src/game/piece.py`: 141
  - `src/figures.py` : 18
  - **Total**: 159
- **Burn down rate**
  - 20% per week
  - 6.7% per day
  - Based on number of goals/milestones completed (2/10)

## Major Changes Completed

1. **Board Implementation & Migration**

   - Created Piece class with constructor and functions for movement/rotation
   - Refactored movement/rotation functions from original code to be more readable
   - Created figures.py file to store the pieces and each of their rotations
   - Moved colors to the constants.py file
   - Changed Piece class to pull figure and color information from constants.py and figures.py to ensure no magic numbers


2. **Variable and Function Updates**

   - Changed lots of variables names in the movement and rotation functions to ensure better readability
   - Changed hard coded figure and color data to pull from constants.py and figures.py
   - Updated structure of some of movements/rotation functions to be more readable

## Preserved Elements


1. **Game Logic**

   - Piece functionality the same, just consolidated to class now
   - Movement/Rotation functionality stays the same

## Current State

- **Functionality**: Kept original functionality
- **Code Quality**: Improved by simplifying piece logic into class
- **Plan**: Next week going to work on implementing piece class into existing code and doing some testing