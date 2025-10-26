"""
FieldTuner V2.0 - Core Module
Contains core business logic and managers.
"""

from .config_manager import ConfigManager
from .favorites_manager import FavoritesManager
from .app_state import AppState

__all__ = ['ConfigManager', 'FavoritesManager', 'AppState']
