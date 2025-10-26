"""
FieldTuner V2.0 - Favorites Manager
Handles persistence of favorite settings.
"""

import json
from pathlib import Path
from typing import List, Set

from debug import log_info, log_error, log_warning
from core.path_config import path_config


class FavoritesManager:
    """Manages favorite settings with persistent storage."""
    
    def __init__(self):
        """Initialize the favorites manager."""
        self.favorites_file = path_config.favorites_file
        self.favorites: Set[str] = set()
        self._load_favorites()
    
    def _load_favorites(self):
        """Load favorites from persistent storage."""
        try:
            self.favorites_file.parent.mkdir(parents=True, exist_ok=True)
            
            if self.favorites_file.exists():
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.favorites = set(data.get('favorites', []))
                    log_info(f"Loaded {len(self.favorites)} favorites", "FAVORITES")
            else:
                log_info("No favorites file found, starting with empty favorites", "FAVORITES")
                
        except Exception as e:
            log_error(f"Failed to load favorites: {str(e)}", "FAVORITES", e)
            self.favorites = set()
    
    def _save_favorites(self):
        """Save favorites to persistent storage."""
        try:
            self.favorites_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                'favorites': list(self.favorites),
                'version': '2.0'
            }
            
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            log_info(f"Saved {len(self.favorites)} favorites", "FAVORITES")
            
        except Exception as e:
            log_error(f"Failed to save favorites: {str(e)}", "FAVORITES", e)
    
    def add_favorite(self, setting_key: str) -> bool:
        """Add a setting to favorites."""
        try:
            if setting_key in self.favorites:
                log_warning(f"Setting {setting_key} is already a favorite", "FAVORITES")
                return False
            
            self.favorites.add(setting_key)
            self._save_favorites()
            log_info(f"Added {setting_key} to favorites", "FAVORITES")
            return True
            
        except Exception as e:
            log_error(f"Failed to add favorite {setting_key}: {str(e)}", "FAVORITES", e)
            return False
    
    def remove_favorite(self, setting_key: str) -> bool:
        """Remove a setting from favorites."""
        try:
            if setting_key not in self.favorites:
                log_warning(f"Setting {setting_key} is not a favorite", "FAVORITES")
                return False
            
            self.favorites.remove(setting_key)
            self._save_favorites()
            log_info(f"Removed {setting_key} from favorites", "FAVORITES")
            return True
            
        except Exception as e:
            log_error(f"Failed to remove favorite {setting_key}: {str(e)}", "FAVORITES", e)
            return False
    
    def toggle_favorite(self, setting_key: str) -> bool:
        """Toggle a setting's favorite status."""
        if setting_key in self.favorites:
            return self.remove_favorite(setting_key)
        else:
            return self.add_favorite(setting_key)
    
    def is_favorite(self, setting_key: str) -> bool:
        """Check if a setting is a favorite."""
        return setting_key in self.favorites
    
    def get_favorites(self) -> List[str]:
        """Get all favorite settings."""
        return sorted(list(self.favorites))
    
    def clear_all_favorites(self) -> bool:
        """Clear all favorites."""
        try:
            self.favorites.clear()
            self._save_favorites()
            log_info("Cleared all favorites", "FAVORITES")
            return True
            
        except Exception as e:
            log_error(f"Failed to clear favorites: {str(e)}", "FAVORITES", e)
            return False
    
    def get_favorites_count(self) -> int:
        """Get the number of favorites."""
        return len(self.favorites)
