from src.utils.score import points_for_clear

class Game:
    def __init__(self, board, spawn_piece_func, session):
        self.board = board
        self.spawn_piece = spawn_piece_func
        self.current_piece = self.spawn_piece()
        self.next_piece = self.spawn_piece()
        self.done = False
        self.game_over = False  # Add game over state
        self.paused = False
        self.gravity_timer = 0
        self.gravity_delay = 30 # frames between auto-fall
        self._score = 0
        self._session = session  # Session manager dependency injection

    @property
    def score(self):
        return self._score
        
    @property
    def high_score(self):
        return self._session.high_score

    def apply(self, intents):
        """Apply player intents (LEFT/RIGHT/ROTATE/DROP/SOFT_DOWN/PAUSE/CLICK)"""
        # Don't process input if game is over
        if self.game_over:
            return
            
        for intent in intents:
            if intent == "PAUSE":
                self.paused = not self.paused
            elif intent == "CLICK" and self.paused:
                self.paused = False
            elif not self.paused:
                if intent == "LEFT":
                    self._try_move(-1, 0)
                elif intent == "RIGHT":
                    self._try_move(1, 0)
                elif intent == "DOWN" or intent == "SOFT_DOWN":
                    self._try_move(0, 1)
                elif intent == "ROTATE":
                    self._try_rotate()
                elif intent == "DROP":
                    self._drop_piece()

    def _try_move(self, dx, dy):
        """Try a move/rotate → if collision, cancel it"""
        if self.game_over:
            return
            
        if dx != 0:
            self.board.go_side(dx, self.current_piece)
        elif dy != 0:
            if not self.board.go_down(self.current_piece):
                # If moving down collides → step back, lock piece, clear rows, spawn new piece
                print("freeze piece in try_move")
                self._freeze_piece()

    def _try_rotate(self):
        """Try rotation → if collision, cancel it"""
        if self.game_over:
            return
            
        self.board.rotate(self.current_piece)

    def _freeze_piece(self):
        """Freeze step: lock piece, clear rows, spawn new piece"""
        # Piece is already placed by board.go_down() when it returns False
        self.board.clear_full_lines()  # clear rows
        print("freeze piece")
        self._update_score(self.board.lines_cleared)  # update score
        self._spawn_new_piece()  # spawn new piece (private)

    def _drop_piece(self):
        """Drop piece instantly"""
        if self.game_over:
            return
            
        self.board.go_space(self.current_piece)
        print("drop piece")
        self._freeze_piece()

    def _spawn_new_piece(self):
        """Replaces current piece with next piece and spawns a new next piece then checks for game over (private)"""
        self.current_piece = self.next_piece
        self.next_piece = self.spawn_piece()
        if self.board.will_piece_collide(self.current_piece):
            self.game_over = True
            self.done = True

    def update(self):
        """Update game state (gravity)"""
        if self.game_over:
            return
            
        if not self.paused:
            self.gravity_timer += 1
            if self.gravity_timer >= self.gravity_delay:
                if not self.board.go_down(self.current_piece):
                    print("freeze piece in update")
                    self._freeze_piece()
                self.gravity_timer = 0

    def _update_score(self, lines_cleared):
        """Update score based on number of lines cleared.

        Delegates scoring logic to the pure helper points_for_clear so the
        scoring table is defined in one place and is easy to unit-test.
        
        No points are awarded after game_over is set to True.
        """
        if not self.game_over:
            self._score += points_for_clear(lines_cleared)
            # Update session high score if current score is higher
            self._session.update_high_score(self._score)
