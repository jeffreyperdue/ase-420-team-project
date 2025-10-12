class Game:
    def __init__(self, board, spawn_piece_func):
        self.board = board
        self.spawn_piece = spawn_piece_func
        self.current_piece = self.spawn_piece()
        self.done = False
        self.gravity_timer = 0
        self.gravity_delay = 30 # frames between auto-fall

    def apply(self, intents):
        """Apply player intents (LEFT/RIGHT/ROTATE/DROP/SOFT_DOWN)"""
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
        if dx != 0:
            self.board.go_side(dx, self.current_piece)
        elif dy != 0:
            if not self.board.go_down(self.current_piece):
                # If moving down collides → step back, lock piece, clear rows, spawn new piece
                print("freeze piece in try_move")
                self._freeze_piece()

    def _try_rotate(self):
        """Try rotation → if collision, cancel it"""
        self.board.rotate(self.current_piece)

    def _freeze_piece(self):
        """Freeze step: lock piece, clear rows, spawn new piece"""
        # Piece is already placed by board.go_down() when it returns False
        self.board.clear_full_lines()  # clear rows
        print("freeze piece")
        self._spawn_new_piece()  # spawn new piece (private)

    def _drop_piece(self):
        """Drop piece instantly"""
        self.board.go_space(self.current_piece)
        print("drop piece")
        self._freeze_piece()

    def _spawn_new_piece(self):
        """Spawn a new piece and check for game over (private)"""
        self.current_piece = self.spawn_piece()
        if self.board.will_piece_collide(self.current_piece):
            self.done = True

    def update(self):
        """Update game state (gravity)"""
        self.gravity_timer += 1
        if self.gravity_timer >= self.gravity_delay:
            if not self.board.go_down(self.current_piece):
                print("freeze piece in update")
                self._freeze_piece()
            self.gravity_timer = 0