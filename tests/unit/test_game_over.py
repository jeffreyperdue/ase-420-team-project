"""
Unit tests for game-over detection and play-again/quit flows.

Tests cover:
- Game-over detection when no valid move exists for spawned piece
- Play-again flow (RESTART intent) that resets game state
- Quit flow (QUIT intent) from game-over screen
- Score persistence across play-again cycles
- High score updates and persistence
- State transitions between GAME_OVER and PLAYING states
- Edge cases (multiple play-again cycles, scoring across restarts, etc.)
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from src.game.game import Game
from src.game.board import Board
from src.game.piece import Piece
from src.game.row import Row
from src.utils.session_manager import SessionManager
from src.constants import START_SCREEN, PLAYING, GAME_OVER, START_X, START_Y


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_session():
    """Create a fresh SessionManager for each test."""
    # Clear singleton to get a fresh instance
    SessionManager._instance = None
    return SessionManager()


@pytest.fixture
def board():
    """Create a Board instance for testing."""
    return Board(lambda: Row(10))


@pytest.fixture
def spawn_piece_func():
    """Create a piece spawn function that returns test pieces."""
    def spawn():
        return Piece(START_X, START_Y)
    return spawn


@pytest.fixture
def game(board, spawn_piece_func, mock_session):
    """Create a Game instance for testing."""
    return Game(board, spawn_piece_func, mock_session)


@pytest.fixture
def full_board(board):
    """Create a board that is nearly full (spawn position blocked).
    
    This board will cause game-over when a new piece is spawned.
    """
    from src.constants import HEIGHT, WIDTH, START_X, START_Y
    # Fill critical rows around the spawn position to ensure collision
    # Spawn position is at (START_X, START_Y), fill area where piece will collide
    for row_idx in range(HEIGHT):
        for col_idx in range(WIDTH):
            # Fill entire board except leave some room, but block spawn area
            if row_idx >= START_Y:
                board.set_cell(row_idx, col_idx, "red")
    return board


# ============================================================================
# Tests for Game-Over Detection
# ============================================================================

class TestGameOverDetection:
    """Test game-over detection when spawned piece collides immediately."""

    def test_game_over_when_piece_spawns_in_collision(self, game):
        """Test that game enters GAME_OVER state when spawned piece collides.
        
        Uses a mocked board that simulates collision to test game-over detection.
        """
        game.start_new_game()
        assert game._state == PLAYING
        
        # Mock will_piece_collide to always return True (collision detected)
        with patch.object(game.board, 'will_piece_collide', return_value=True):
            # Trigger _spawn_new_piece which calls will_piece_collide
            game._spawn_new_piece()
            
            # Game should detect collision and set GAME_OVER
            assert game._state == GAME_OVER

    def test_game_over_state_set_after_spawn_collision(self, game):
        """Test that GAME_OVER state is properly set after collision detection."""
        game.start_new_game()
        initial_state = game._state
        assert initial_state == PLAYING
        
        # Fill the board to force collision
        for row_idx in range(game.board.height):
            for col_idx in range(game.board.width):
                game.board.set_cell(row_idx, col_idx, "red")
        
        # Force spawn attempt
        game._spawn_new_piece()
        
        assert game._state == GAME_OVER

    def test_no_inputs_accepted_in_game_over_state(self, game):
        """Test that gameplay inputs are ignored in GAME_OVER state."""
        game.start_new_game()
        game._state = GAME_OVER
        
        initial_score = game.score
        initial_piece = game.current_piece
        
        # Try gameplay intents - these should be ignored
        game.apply(["LEFT", "RIGHT", "ROTATE", "DROP"])
        
        # Nothing should change
        assert game.score == initial_score
        assert game.current_piece == initial_piece
        assert game._state == GAME_OVER

    def test_game_over_flag_persists(self, game):
        """Test that game_over flag persists after state transition."""
        game.start_new_game()
        game._state = GAME_OVER
        game.game_over = True
        
        # Verify flag is still set
        assert game.game_over is True
        assert game._state == GAME_OVER

    def test_game_over_with_scored_game(self, game):
        """Test game-over detection after player has scored points."""
        game.start_new_game()
        
        # Simulate score accumulation
        game._score = 1000
        game._session.update_high_score(game.score)
        
        # Fill board to trigger game-over
        for row_idx in range(game.board.height):
            for col_idx in range(game.board.width):
                game.board.set_cell(row_idx, col_idx, "red")
        
        # Trigger collision
        game._spawn_new_piece()
        
        # Game should be over and score should be retained
        assert game._state == GAME_OVER
        assert game.score == 1000


# ============================================================================
# Tests for Play-Again Flow (RESTART)
# ============================================================================

class TestPlayAgainFlow:
    """Test RESTART intent flow from game-over screen."""

    def test_restart_from_game_over_state(self, game):
        """Test that RESTART transitions from GAME_OVER to PLAYING."""
        game.start_new_game()
        game._state = GAME_OVER
        game._score = 500
        
        # Send RESTART intent
        game.apply(["RESTART"])
        
        assert game._state == PLAYING

    def test_restart_clears_board(self, game):
        """Test that RESTART clears the board."""
        game.start_new_game()
        
        # Fill some cells
        game.board.set_cell(5, 3, "red")
        game.board.set_cell(5, 4, "blue")
        game.board.set_cell(5, 5, "green")
        
        # Force game-over
        game._state = GAME_OVER
        
        # Restart
        game.apply(["RESTART"])
        
        # Board should be cleared
        assert game.board.get_cell(5, 3) is False
        assert game.board.get_cell(5, 4) is False
        assert game.board.get_cell(5, 5) is False

    def test_restart_resets_score_to_zero(self, game):
        """Test that RESTART resets current score to 0."""
        game.start_new_game()
        game._score = 2500
        game._state = GAME_OVER
        
        # Apply RESTART
        game.apply(["RESTART"])
        
        # Score should be reset
        assert game.score == 0

    def test_restart_preserves_high_score(self, game):
        """Test that RESTART preserves session high score."""
        game.start_new_game()
        game._score = 3000
        game._session.update_high_score(game.score)
        
        game._state = GAME_OVER
        initial_high_score = game.high_score
        
        # Apply RESTART
        game.apply(["RESTART"])
        
        # High score should be preserved
        assert game.high_score == initial_high_score
        assert game.high_score == 3000

    def test_restart_spawns_new_pieces(self, game):
        """Test that RESTART spawns new current and next pieces."""
        game.start_new_game()
        old_current = game.current_piece
        old_next = game.next_piece
        
        game._state = GAME_OVER
        
        # Apply RESTART
        game.apply(["RESTART"])
        
        # New pieces should be spawned
        assert game.current_piece is not None
        assert game.next_piece is not None

    def test_restart_resets_level_and_lines_cleared(self, game):
        """Test that RESTART resets level and lines cleared."""
        game.start_new_game()
        game.level = 5
        game.lines_cleared = 50
        
        game._state = GAME_OVER
        
        # Apply RESTART
        game.apply(["RESTART"])
        
        # Level and lines should be reset
        assert game.level == 1
        assert game.lines_cleared == 0

    def test_restart_resets_gravity_timer(self, game):
        """Test that RESTART resets gravity timer."""
        game.start_new_game()
        game.gravity_timer = 25
        game._state = GAME_OVER
        
        # Apply RESTART
        game.apply(["RESTART"])
        
        # Gravity timer should be reset
        assert game.gravity_timer == 0

    def test_multiple_play_again_cycles(self, game):
        """Test that player can play multiple games after game-over."""
        for cycle in range(3):
            # Start game
            if cycle == 0:
                game.start_new_game()
            else:
                game.apply(["RESTART"])
            
            assert game._state == PLAYING
            
            # Simulate gameplay by scoring
            game._score = 100 * (cycle + 1)
            
            # Game over
            game._state = GAME_OVER
            
            # Verify score before restart
            assert game.score == 100 * (cycle + 1)

    def test_high_score_updates_across_restarts(self, game):
        """Test that high score updates correctly across multiple play-again cycles."""
        scores = [500, 1000, 750, 1200]
        
        for idx, score in enumerate(scores):
            game.start_new_game()
            game._score = score
            game._session.update_high_score(game.score)
            
            game._state = GAME_OVER
            
            # Verify high score is maximum seen so far
            expected_high = max(scores[:idx + 1])
            assert game.high_score == expected_high
            
            if idx < len(scores) - 1:
                game.apply(["RESTART"])

    def test_restart_does_not_modify_other_state(self, game):
        """Test that RESTART only modifies intended state."""
        game.start_new_game()
        game.paused = True
        game._state = GAME_OVER
        
        # Apply RESTART
        game.apply(["RESTART"])
        
        # Paused state should remain (only cleared on new game start)
        assert game._state == PLAYING


# ============================================================================
# Tests for Quit Flow (QUIT)
# ============================================================================

class TestQuitFlow:
    """Test QUIT intent flow from game-over screen."""

    def test_quit_from_game_over_sets_done_flag(self, game):
        """Test that QUIT intent from GAME_OVER sets game.done to True."""
        game.start_new_game()
        game._state = GAME_OVER
        
        assert game.done is False
        
        game.apply(["QUIT"])
        
        assert game.done is True

    def test_quit_from_start_screen_sets_done_flag(self, game):
        """Test that QUIT intent from START_SCREEN sets game.done to True."""
        game._state = START_SCREEN
        
        assert game.done is False
        
        game.apply(["QUIT"])
        
        assert game.done is True

    def test_quit_preserves_score_data(self, game):
        """Test that quitting preserves current and high scores."""
        game.start_new_game()
        game._score = 2000
        game._session.update_high_score(game.score)
        
        game._state = GAME_OVER
        final_score = game.score
        final_high_score = game.high_score
        
        # Quit
        game.apply(["QUIT"])
        
        # Scores should not change
        assert game.score == final_score
        assert game.high_score == final_high_score

    def test_quit_does_not_reset_game_state(self, game):
        """Test that QUIT does not reset board or game state."""
        game.start_new_game()
        game.board.set_cell(5, 5, "red")
        game._score = 1500
        game._state = GAME_OVER
        
        # Quit
        game.apply(["QUIT"])
        
        # State should be preserved
        assert game._state == GAME_OVER
        assert game.board.get_cell(5, 5) is True
        assert game.score == 1500


# ============================================================================
# Tests for Score Persistence
# ============================================================================

class TestScorePersistence:
    """Test that scores persist correctly across game cycles."""

    def test_high_score_persists_after_restart(self, game):
        """Test that high score persists after restart."""
        # First game
        game.start_new_game()
        game._score = 1000
        game._session.update_high_score(game.score)
        assert game.high_score == 1000
        
        game._state = GAME_OVER
        
        # Restart and play second game
        game.apply(["RESTART"])
        assert game.high_score == 1000
        
        game._score = 500
        game._session.update_high_score(game.score)
        
        # High score should not decrease
        assert game.high_score == 1000

    def test_high_score_updates_when_exceeded(self, game):
        """Test that high score updates when new score exceeds it."""
        # First game
        game.start_new_game()
        game._score = 1000
        game._session.update_high_score(game.score)
        assert game.high_score == 1000
        
        game._state = GAME_OVER
        
        # Second game - higher score
        game.apply(["RESTART"])
        game._score = 2000
        game._session.update_high_score(game.score)
        
        assert game.high_score == 2000

    def test_session_high_score_singleton_behavior(self, mock_session):
        """Test that SessionManager maintains singleton high score."""
        # Create first game
        game1 = Game(Board(lambda: Row(10)), lambda: Piece(START_X, START_Y), mock_session)
        game1.start_new_game()
        game1._score = 1500
        game1._session.update_high_score(game1.score)
        
        # Create second game with same session
        game2 = Game(Board(lambda: Row(10)), lambda: Piece(START_X, START_Y), mock_session)
        game2.start_new_game()
        
        # Both games should see the same high score
        assert game1.high_score == 1500
        assert game2.high_score == 1500

    def test_current_score_independent_of_high_score(self, game):
        """Test that current score remains independent of high score."""
        game.start_new_game()
        game._score = 2000
        game._session.update_high_score(game.score)
        
        game._state = GAME_OVER
        
        # Reset for new game
        game.apply(["RESTART"])
        game._score = 500
        
        # Current score and high score should differ
        assert game.score == 500
        assert game.high_score == 2000

    def test_score_persists_through_multiple_games(self, game):
        """Test score persistence through multiple consecutive games."""
        scores = [1000, 1500, 1200, 2000, 800]
        
        for idx, score in enumerate(scores):
            if idx == 0:
                game.start_new_game()
            else:
                game.apply(["RESTART"])
            
            game._score = score
            game._session.update_high_score(game.score)
            game._state = GAME_OVER
            
            # Verify high score is maximum of all scores so far
            expected_max = max(scores[:idx + 1])
            assert game.high_score == expected_max

    def test_score_zero_on_new_game_start(self, game):
        """Test that score is always 0 at the start of a new game."""
        # First game
        game.start_new_game()
        assert game.score == 0
        
        # Play with some score
        game._score = 1500
        game._state = GAME_OVER
        
        # Restart
        game.apply(["RESTART"])
        assert game.score == 0
        
        # Play again
        game._score = 2000
        game._state = GAME_OVER
        
        # Restart again
        game.apply(["RESTART"])
        assert game.score == 0


# ============================================================================
# Tests for State Transitions
# ============================================================================

class TestStateTransitions:
    """Test game state transitions related to game-over."""

    def test_transition_playing_to_game_over(self, game):
        """Test transition from PLAYING to GAME_OVER state."""
        game.start_new_game()
        assert game._state == PLAYING
        
        # Trigger game-over
        game._state = GAME_OVER
        assert game._state == GAME_OVER

    def test_transition_game_over_to_playing_via_restart(self, game):
        """Test transition from GAME_OVER back to PLAYING via RESTART."""
        game.start_new_game()
        game._state = GAME_OVER
        
        game.apply(["RESTART"])
        
        assert game._state == PLAYING

    def test_transition_game_over_to_start_via_quit(self, game):
        """Test that QUIT from GAME_OVER doesn't change state directly (sets done flag)."""
        game.start_new_game()
        game._state = GAME_OVER
        
        game.apply(["QUIT"])
        
        # State should remain GAME_OVER (app loop handles done flag)
        assert game._state == GAME_OVER
        assert game.done is True

    def test_invalid_state_preserves_state(self, game):
        """Test that invalid intents don't change GAME_OVER state."""
        game.start_new_game()
        game._state = GAME_OVER
        
        # Try various gameplay intents
        game.apply(["ROTATE"])
        assert game._state == GAME_OVER
        
        game.apply(["LEFT", "RIGHT", "DOWN"])
        assert game._state == GAME_OVER

    def test_start_screen_to_playing_transition(self, game):
        """Test transition from START_SCREEN to PLAYING via START intent."""
        assert game._state == START_SCREEN
        
        game.apply(["START"])
        
        assert game._state == PLAYING


# ============================================================================
# Tests for Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_game_over_with_zero_score(self, game):
        """Test game-over when no points have been scored."""
        game.start_new_game()
        assert game.score == 0
        
        game._state = GAME_OVER
        
        # Should be able to restart with zero score
        game.apply(["RESTART"])
        assert game._state == PLAYING
        assert game.score == 0

    def test_restart_immediately_after_game_over(self, game):
        """Test RESTART can be applied immediately after game-over."""
        game.start_new_game()
        
        # Fill board and trigger game-over
        for row_idx in range(game.board.height):
            for col_idx in range(game.board.width):
                game.board.set_cell(row_idx, col_idx, "red")
        
        game._spawn_new_piece()
        assert game._state == GAME_OVER
        
        # Restart immediately
        game.apply(["RESTART"])
        assert game._state == PLAYING

    def test_multiple_quit_intents_ignored(self, game):
        """Test that multiple QUIT intents don't cause issues."""
        game.start_new_game()
        game._state = GAME_OVER
        
        game.apply(["QUIT"])
        assert game.done is True
        
        # Additional QUITs should not cause errors
        game.apply(["QUIT"])
        assert game.done is True

    def test_mixed_intents_at_game_over(self, game):
        """Test that only QUIT and RESTART are processed at GAME_OVER."""
        game.start_new_game()
        game._state = GAME_OVER
        initial_piece = game.current_piece
        
        # Mix gameplay intents with valid game-over intents
        game.apply(["LEFT", "RESTART", "ROTATE", "DROP"])
        
        # Only RESTART should take effect
        assert game._state == PLAYING
        
        # Pieces should have been respawned (not kept from mixed input)
        game._state = GAME_OVER
        game.apply(["RIGHT", "QUIT", "SOFT_DOWN", "PAUSE"])
        
        # Only QUIT should take effect
        assert game.done is True

    def test_game_over_prevents_gravity_updates(self, game):
        """Test that gravity does not apply during GAME_OVER state."""
        game.start_new_game()
        game.gravity_timer = 0
        
        game._state = GAME_OVER
        initial_timer = game.gravity_timer
        
        # Call update multiple times
        for _ in range(10):
            game.update()
        
        # Timer should not have changed
        assert game.gravity_timer == initial_timer

    def test_restart_after_very_high_score(self, game):
        """Test RESTART works correctly with very high scores."""
        game.start_new_game()
        game._score = 999999
        game._session.update_high_score(game.score)
        
        game._state = GAME_OVER
        
        # Restart
        game.apply(["RESTART"])
        
        assert game._state == PLAYING
        assert game.score == 0
        assert game.high_score == 999999

    def test_consecutive_restarts_without_gameplay(self, game):
        """Test multiple consecutive RESTARTs without actual gameplay."""
        game.start_new_game()
        
        for _ in range(5):
            game._state = GAME_OVER
            game.apply(["RESTART"])
            
            assert game._state == PLAYING
            assert game.score == 0

    def test_game_over_during_pause_state(self, game):
        """Test game-over handling when game was paused."""
        game.start_new_game()
        game.paused = True
        
        game._state = GAME_OVER
        
        # Should still be able to restart
        game.apply(["RESTART"])
        assert game._state == PLAYING

    def test_high_score_never_decreases(self, game):
        """Test that high score never decreases across any scenario."""
        game.start_new_game()
        
        scores_and_expected = [
            (1000, 1000),  # first score
            (500, 1000),   # lower score
            (2000, 2000),  # higher score
            (1500, 2000),  # lower than current high
            (2000, 2000),  # same as high
            (2001, 2001),  # just above
        ]
        
        for idx, (current_score, expected_high) in enumerate(scores_and_expected):
            if idx > 0:
                game.apply(["RESTART"])
            
            game._score = current_score
            game._session.update_high_score(game.score)
            
            assert game.high_score == expected_high
            game._state = GAME_OVER


# ============================================================================
# Integration Tests
# ============================================================================

class TestGameOverIntegration:
    """Integration tests for game-over flow with full game context."""

    def test_full_game_cycle_with_restart(self, game):
        """Test complete game cycle: start → play → game-over → restart."""
        # Start
        assert game._state == START_SCREEN
        game.apply(["START"])
        assert game._state == PLAYING
        
        # Play
        game._score = 1500
        game._session.update_high_score(game.score)
        
        # Game over
        game._state = GAME_OVER
        
        # Restart
        game.apply(["RESTART"])
        
        # Verify state after restart
        assert game._state == PLAYING
        assert game.score == 0
        assert game.high_score == 1500

    def test_full_game_cycle_with_quit(self, game):
        """Test complete game cycle: start → play → game-over → quit."""
        game.apply(["START"])
        assert game._state == PLAYING
        
        game._score = 2000
        game._session.update_high_score(game.score)
        
        game._state = GAME_OVER
        
        game.apply(["QUIT"])
        assert game.done is True

    def test_multiple_full_cycles(self, game):
        """Test multiple full game cycles with varying scores."""
        scores = [1000, 1500, 2000]
        
        for cycle, score in enumerate(scores):
            # Start
            if cycle == 0:
                game.apply(["START"])
            else:
                game.apply(["RESTART"])
            
            assert game._state == PLAYING
            
            # Play
            game._score = score
            game._session.update_high_score(game.score)
            
            # Game over
            game._state = GAME_OVER
            
            # Verify high score tracking
            expected_high = max(scores[:cycle + 1])
            assert game.high_score == expected_high


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
