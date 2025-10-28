"""
Session-level data management.

Provides classes for managing data that should persist across game instances
within a single program session.
"""

class SessionManager:
  """
  Singleton class to manage session-level game data.
  
  This class maintains state that should persist even when the game
  is restarted, like high scores for the current session.
  """
  _instance = None
  
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(SessionManager, cls).__new__(cls)
      cls._instance._high_score = 0  # Initialize on first creation
    return cls._instance
  
  @property
  def high_score(self):
    """Get the current session's high score."""
    return self._high_score
  
  def update_high_score(self, score):
    """
    Update session high score if new score is higher.
    
    Args:
      score (int): The score to compare against current high score
    """
    if score > self._high_score:
      self._high_score = score