from src.utils.score import points_for_clear
from src.constants.game_states import START_SCREEN, PLAYING, GAME_OVER

class Game:
    def __init__(self, board, spawn_piece_func, session):
        self.board = board
        self.spawn_piece = spawn_piece_func
        self.current_piece = None
        self.next_piece = None
        self.done = False
        self.game_over = False  # Add game over state
        self.paused = False
        self.gravity_timer = 0
        # Scoring/session (HEAD)
        self._score = 0
        self._session = session  # Session manager dependency injection
        self._state = START_SCREEN
        
        # Progression (Owen)
        self.level = 1
        self.lines_cleared = 0
        self.base_gravity_delay = 30
        self.gravity_delay = self.base_gravity_delay  # frames between auto-fall
        
    def start_new_game(self):
        """Initialize a new game."""
        self.board.clear()  # Clear the board before starting a new game
        self.current_piece = self.spawn_piece()
        self.next_piece = self.spawn_piece()
        self.done = False
        self.game_over = False
        self._score = 0
        self._state = PLAYING
        self.gravity_timer = 0
        self.level = 1
        self.lines_cleared = 0
        self.gravity_delay = self.base_gravity_delay

    @property
    def score(self):
        return self._score
        
    @property
    def high_score(self):
        return self._session.high_score

    def apply(self, intents):
        """Apply player intents (LEFT/RIGHT/ROTATE/DROP/SOFT_DOWN/PAUSE/CLICK/START/EXIT)"""
        # Handle start screen and game over states
        if self._state == START_SCREEN:
            for intent in intents:
                if intent == "START":
                    self.start_new_game()
                elif intent == "QUIT":
                    self.done = True
            return
            
        if self._state == GAME_OVER:
            for intent in intents:
                if intent == "QUIT":
                    self.done = True
                elif intent == "RESTART":
                    self.start_new_game()
            return
            
        # Game is in progress - handle gameplay inputs
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
        if self._state == GAME_OVER:
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
        if self._state == GAME_OVER:
            return
            
        self.board.rotate(self.current_piece)

    def _freeze_piece(self):
        """Freeze step: lock piece, clear rows, spawn new piece"""
        # Piece is already placed by board.go_down() when it returns False
        lines_cleared = self.board.clear_full_lines()  # clear rows, returns count
        print("freeze piece")
        # Update score and level if lines cleared
        if lines_cleared > 0:
            self._update_score(lines_cleared)
            self._update_level(lines_cleared)
        self._spawn_new_piece()  # spawn new piece (private)

    def _drop_piece(self):
        """Drop piece instantly"""
        if self._state == GAME_OVER:
            return
            
        self.board.go_space(self.current_piece)
        print("drop piece")
        self._freeze_piece()

    def _spawn_new_piece(self):
        """Replaces current piece with next piece and spawns a new next piece then checks for game over (private)"""
        self.current_piece = self.next_piece
        self.next_piece = self.spawn_piece()
        if self.board.will_piece_collide(self.current_piece):
            self._state = GAME_OVER

    def update(self):
        """Update game state (gravity)"""
        if self._state == GAME_OVER:
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
        
        No points are awarded after game state is set to GAME_OVER.
        """
        if not self._state == GAME_OVER:
            self._score += points_for_clear(lines_cleared)
            # Update session high score if current score is higher
            self._session.update_high_score(self._score)

    def _calculate_gravity_delay(self) -> int:
        """Calculate gravity delay based on current level.
        As level increases, pieces fall faster.
        
        Returns:
            int: Frames between auto-fall
        """
        speed_increase = 3
        calculated_delay = max(1, self.base_gravity_delay - (self.level - 1) * speed_increase)
        return calculated_delay

    def _update_level(self, lines_cleared_count: int) -> None:
        """Update level based on lines cleared.
        
        Args:
            lines_cleared_count (int): Number of lines cleared in this action
        """
        if lines_cleared_count > 0:
            self.lines_cleared += lines_cleared_count
            new_level = (self.lines_cleared // 10) + 1
            if new_level > self.level:
                self.level = new_level
                self.gravity_delay = self._calculate_gravity_delay()
