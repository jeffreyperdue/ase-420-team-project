from tests.fixtures.test_helpers import create_test_game, create_test_board, create_test_piece


def test_level_and_gravity_progression_and_scoring():
    game = create_test_game()

    # Initial conditions
    assert game.level == 1
    initial_delay = game.gravity_delay
    assert initial_delay >= 10
    initial_score = game.score

    # Simulate clearing 10 lines at once (should bump level by 1)
    game._update_level(10)

    assert game.lines_cleared == 10
    assert game.level == 2

    # Gravity should have been recalculated and obey the minimum cap (>= 10)
    assert game.gravity_delay >= 10

    # Score should have increased after clearing lines
    assert game.score > initial_score

    # The multiplier should have increased slightly at level 2
    assert game.get_score_multiplier() == 1.0 + (game.level - 1) * 0.1
