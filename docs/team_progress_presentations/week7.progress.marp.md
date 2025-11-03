---
marp: true
size: 4:3
paginate: true
---

# ASE 420 Team Project  
## Error 404: Name Not Found  
### Week 7 Progress Report – Tetris

📅 Week 7: Oct 27 – Nov 2  
🎯 Focus: Pause/Resume UX, Score Display & Session High Score

---

## Team Overview

**Team Members**  
- **Jeffrey Perdue** – Team Leader  
- **Anna Dinius** – Scoring & UI  
- **Cody King** – Preview, Pause/Resume  
- **Owen Newberry** – Rendering & Controls

**Sprint 2 Progress**: Continuing feature buildout (advanced scoring, preview integration, pause UX)

---

## Week 7 Goals Summary

### Anna's Goals ✅
- ✅ Expand unit tests to cover multipliers and edge cases  
- ✅ Display current score in the UI and persist until reset  
- ✅ Display session high score in‑game

---

### Cody's Goals ✅
- ✅ Integrate Next Piece preview with piece generation  
- ✅ Add pause state management to the game loop  
- ✅ Modify input handling for pause/resume (ESC, click-to-resume)

---

### Owen's Goals ✅
- ✅ Integrate level progression with line clearing
- ✅ Calculate landing position for ghost piece
- ✅ Implement ghost piece collision detection logic
- ✅ Write unit tests for ghost piece calculation

---

## Statistics Overview

### Lines of Code Added
- **Anna**: 153 LoC total
  - `app.py`: 6  
  - `src/constants.py`: 1  
  - `src/game/game.py`: 10  
  - `src/game/score.py`: 2  
  - `src/utils/session_manager.py`: 29 (new)  
  - `src/view/pygame_renderer.py`: 8  
  - Tests: `tests/test_scoring.py`: 96, `tests/test_score_utils.py`: 1

---
- **Cody**: 74 LoC total
  - `app.py`: 8  
  - `src/game/game.py`: 12  
  - `src/view/input.py`: 8  
  - `src/view/pygame_renderer.py`: 46

 ---
- **Owen**: 77 LoC total
  - `app.py`: 3  
  - `src/game/board.py`: 46  
  - `src/view/pygame_renderer.py`: 28

**Total**: 304 lines of code

---

## Burn Down & Velocity

- **Anna**  
  - Week 7 milestones: 3/3 (100%)  
  - Early Week 8 milestones: 2/3 completed  
  - Sub‑requirements completed (Sprint 2): 8/14 (~57%)

- **Cody**  
  - Week 7 goals: 3/3 (100%)  
  - Sprint 2 milestone completion (per Cody report): 6/12 (~50%)

- **Owen**  
  - Week 7 goals: 3/3 (100%)  
  - Sprint 2 milestone completion: 7/14 (50%)

---

## Major Technical Achievements

### Session High Score & Score Display (Anna)
- Session‑wide `SessionManager` for `high_score` persistence  
- Renderer `draw_score(...)` to place Score/High Score relative to board  
- Tightened `points_for_clear` input validation (TypeError on invalid types)

---

### Pause/Resume UX & Preview Integration (Cody)
- `Game` gains `paused` state; gravity and inputs gated when paused  
- `ESC` maps to `PAUSE`; click emits `CLICK` to resume  
- `draw_pause_screen()` overlay in renderer  
- Next Piece preview centered via 4x4 bounding box of piece

---

### Level Progression Integration & Ghost Piece System (Owen)
- Level progression wired to line clearing
- Ghost piece landing calculation
- Ghost piece visualization

---

## Key Architecture Changes

### 1) Session Manager (New)
```python
# src/utils/session_manager.py - 29 LoC (new)
class SessionManager:
    high_score: int = 0

    def update_high_score(self, score: int) -> None:
        if score > self.high_score:
            self.high_score = score
```
---
- Centralized session state  
- Simple API to atomically update high score

---

### 2) Renderer Score Panel
```python
# src/view/pygame_renderer.py - updated
def draw_score(self, board_x: int, board_y: int, score: int, high_score: int) -> None:
    # Renders labels and values positioned relative to board origin
    ...
```
- Board‑relative layout for stable positioning across screen sizes

---

### 3) Game Pause State
```python
# src/game/game.py - updated
class Game:
    def __init__(self, ...):
        self.paused = False

    def apply(self, intent):
        if intent == PAUSE:
            self.paused = not self.paused
        if self.paused and intent != PAUSE:
            return
```
- Input/updates respect pause; gameplay fully freezes until resume

---

### 4) Pause Overlay & Preview Centering
```python
# src/view/pygame_renderer.py - updated
def draw_pause_screen(self) -> None:
    # Semi-transparent overlay + centered "PAUSED" label
    ...

def draw_next_piece(self, piece) -> None:
    # Center piece in preview rect using 4x4 bounding box
    ...
```
- Consistent preview visuals; clear paused feedback

---

## Testing Coverage Highlights

- Anna expanded tests for scoring, validation, and edge cases  
- Integration checks for session high score updates  
- Cody verified Pause/Resume UX manually; preview centering validated in runs

---

## Week 7 vs Sprint 2 Planning

- **Anna – Ahead of plan**: Completed Week 7 and part of Week 8 work  
- **Cody – On plan**: Completed Week 7 goals including Pause/Resume and preview integration
- **Owen - On plan**: Completed Week 7 goals with Ghost Piece and Level Progression functionalities
- **Team**: Strong momentum toward full Sprint 2 completion

---

## Week 8 Focus (Looking Ahead)

- Anna: Finalize remaining scoring UI polish, high score persistence refinements  
- Cody: Broaden pause UX polish, expand automated tests  
- Owen: Difficulty levels, ghost piece logic  
- Maintain test coverage and UI consistency

---

# 🎯 Week 7 Takeaways

**Priority**: Advanced features shipped with solid UX  
**Outcome**: Score/High Score displays, Pause/Resume, preview centering  
**Next**: Polish, testing depth, and remaining Sprint 2 items

