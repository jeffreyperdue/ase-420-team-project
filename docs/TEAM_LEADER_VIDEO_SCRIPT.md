# Team Leader Video Script - Tetris Game Final Demo

**Team:** Error 404 Name Not Found  
**Duration:** ~3-4 minutes (adjust timing as needed)

---

## OPENING (0:00 - 0:30)

"Hello, I'm [Your Name], team leader for Error 404 Name Not Found. While my teammates are showcasing their individual features—the scoring system, next piece preview, pause functionality, difficulty levels, and ghost piece—I want to give you a behind-the-scenes look at how we built this Tetris game as a cohesive team.

Our success came down to three things: clear architecture, strong process, and effective integration. Let me walk you through how we made it all work together."

---

## SECTION 1: Project Architecture & Integration (0:30 - 1:15)

"From day one, we designed the game with a clean separation of concerns. We have three major subsystems:

First, the **Game Logic Layer** - this is where Cody built the Piece class and collision detection, and Anna built the Board class with line-clearing logic. This is the brain of the game.

Second, the **View & Input Layer** - Owen handled this. He built the Pygame renderer to display the board and pieces, and the keyboard input mapper to capture player commands.

Third, the **Integration Layer** - the main game loop that ties everything together. All three subsystems communicate through clean interfaces, which meant we could work independently without constantly stepping on each other's toes.

This architecture was crucial. It allowed Anna, Cody, and Owen to work in parallel on Sprint 1 without constant merge conflicts. Each of them could test their code in isolation, and then I could integrate everything when it was ready."

---

## SECTION 2: Team Coordination & Process (1:15 - 2:00)

"Managing a team of three developers could have been chaotic, but we established clear rules from the start. Everyone commits code regularly to GitHub. No force pushes—ever. We respond to team communication within 24 hours. And we submit weekly progress updates.

We also implemented a smart branching strategy. Each team member creates feature branches off main, works independently, and then we integrate weekly or as needed. When someone's code broke main—and yes, that happened—they were responsible for fixing it. This kept everyone accountable and the main branch stable.

The results speak for themselves: we completed 8 requirements and 8 features in Sprint 1 with an 88.9% burndown rate. In Sprint 2, we pushed to 35 requirements across 6 new features—next piece preview, pause/resume, scoring system, difficulty levels, enhanced screens, and ghost piece preview. That kind of velocity doesn't happen by accident."

---

## SECTION 3: Development Progression (2:00 - 2:45)

"Let me show you how the game evolved.

Week 1, we scaffolded the repository and established the core constants and figure definitions. Nothing running yet, but the foundation was solid.

By Week 2, Anna had the Board class working, Cody had started the Piece class, and Owen was prototyping the renderer. We could start seeing pieces moving on screen.

Week 3, we implemented line clearing—a critical Tetris mechanic—and wired collision detection and keyboard input together. The game was starting to feel like Tetris.

Week 4 and 5, we focused on integration and polish. We stress-tested edge cases, added comprehensive error handling, and got a working game loop running with gravity, rotation, hard drop, and a game over screen.

The key was that each phase built on the previous one. We didn't try to do everything at once. We validated as we went."

---

## SECTION 4: Testing Strategy & Code Quality (2:45 - 3:20)

"One thing that kept us confident during integration was our testing approach. Anna and Cody wrote comprehensive unit tests for the Board, Row, and Piece classes—the core game logic. These tests validated that basic operations worked correctly in isolation.

Owen's rendering and input code we validated through manual testing with the game loop. By the end of Sprint 1, we had high coverage on critical systems. This meant when we merged code, we could quickly catch regressions. It also meant we could refactor with confidence.

Going into Sprint 2, that test suite became even more valuable as we added scoring, pause logic, and difficulty levels. We could change code knowing we wouldn't silently break something that was already working."

---

## SECTION 5: Seeing It All Together (3:20 - 3:50)

"Let me show you the final product running with all the features integrated.

[Optional: Do a brief game demo here—show a few pieces falling, rotate them, clear some lines, pause, resume, maybe show difficulty ramping up. Keep it under 30 seconds.]

This is what teamwork looks like. Anna's Board with line clearing. Cody's Pieces with collision detection. Owen's rendering making it all visible. Combined with the Sprint 2 features my teammates are showcasing—scoring that tracks your performance, next piece preview to plan ahead, pause so you don't lose your spot, and difficulty levels that keep the game challenging—it's a complete, polished Tetris game.

But none of this works without the architecture we designed and the integration process we followed."

---

## CLOSING (3:50 - 4:00)

"Thanks for watching. My role as team leader was to make sure we had the right structure, the right process, and that everything integrated smoothly. Anna, Cody, and Owen did the heavy lifting on features. Together, we built something we're proud of. Thanks."

---

## TIMING NOTES

- **Opening:** 30 seconds
- **Architecture:** 45 seconds
- **Process & Metrics:** 45 seconds
- **Development Progression:** 45 seconds
- **Testing & Quality:** 35 seconds
- **Live Demo:** 30 seconds
- **Closing:** 10 seconds
- **Total:** ~3:20 (without demo) to ~3:50 (with demo)

Adjust the demo length or any section based on your presentation time constraints.

---

## DELIVERY TIPS

1. **Speak clearly and at a moderate pace** - give your audience time to absorb technical concepts
2. **Make eye contact with camera** - pretend you're talking to one person
3. **Use hand gestures** - they naturally emphasize your points about architecture and workflow
4. **Show visuals when possible** - the codebase structure, a git log showing commits, or the game running makes concepts stick
5. **Confidence** - you led this team to successful delivery twice; that's worth being proud of
6. **Practice once or twice** before recording - your timing and pacing will feel more natural
