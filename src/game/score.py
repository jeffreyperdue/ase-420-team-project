"""Scoring utilities for Tetris.

Provide a pure function that maps number of cleared lines to points.
"""
from __future__ import annotations

def points_for_clear(lines_cleared: int) -> int:
    """Return the number of points awarded for clearing lines.

    This is a pure, deterministic function with no side-effects and is
    easy to unit-test.

    Current mapping follows classic Tetris-like values:
      0 -> 0
      1 -> 100
      2 -> 300
      3 -> 500
      4 -> 800

    Any other value returns 0.
    """
    scoring = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
    return scoring.get(lines_cleared, 0)
