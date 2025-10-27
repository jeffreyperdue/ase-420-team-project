class Game:
    def __init__(self, board, spawn_piece_func):
        self.board = board
        self.spawn_piece = spawn_piece_func
        self.current_piece = self.spawn_piece()
        self.done = False
        self.game_over = False  # Add game over state
        self.gravity_timer = 0
        self.level = 1
        self.lines_cleared = 0
        self.base_gravity_delay = 30
        self.gravity_delay = self.base_gravity_delay

    def apply(self, intents):
        """Apply player intents (LEFT/RIGHT/ROTATE/DROP/SOFT_DOWN)"""
        # Don't process input if game is over
        if self.game_over:
            return
            
        for intent in intents:
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
        lines_cleared = self.board.clear_full_lines()  # clear rows - NOW RETURNS COUNT
        print("freeze piece")
        if lines_cleared > 0:
            self._update_level(lines_cleared)
        self._spawn_new_piece()  # spawn new piece (private)

    def _drop_piece(self):
        """Drop piece instantly"""
        if self.game_over:
            return
            
        self.board.go_space(self.current_piece)
        print("drop piece")
        self._freeze_piece()

    def _spawn_new_piece(self):
        """Spawn a new piece and check for game over (private)"""
        self.current_piece = self.spawn_piece()
        if self.board.will_piece_collide(self.current_piece):
            self.game_over = True
            self.done = True

    def update(self):
        """Update game state (gravity)"""
        if self.game_over:
            return
            
        self.gravity_timer += 1
        if self.gravity_timer >= self.gravity_delay:
            if not self.board.go_down(self.current_piece):
                print("freeze piece in update")
                self._freeze_piece()
            self.gravity_timer = 0

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