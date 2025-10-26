"""
FieldTuner V2.0 - User Preferences
Manages user preferences and application settings.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from debug import log_info, log_error, log_warning
from core.path_config import path_config


class UserPreferences:
    """Manages user preferences and application settings."""
    
    def __init__(self):
        """Initialize user preferences."""
        self.preferences_file = path_config.preferences_file
        self.preferences_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.default_preferences = {
            "ui": {
                "theme": "dark",
                "window_size": [1200, 800],
                "window_position": [100, 100],
                "last_tab": "quick_settings",
                "show_tooltips": True,
                "show_status_messages": True
            },
            "performance": {
                "cache_settings": True,
                "lazy_load_tabs": True,
                "search_debounce_ms": 300
            },
            "backup": {
                "auto_backup": True,
                "max_backups": 50,
                "backup_before_save": True
            },
            "advanced": {
                "show_technical_names": False,
                "group_by_category": True,
                "show_descriptions": True
            }
        }
        
        self.preferences = self.load_preferences()
    
    def load_preferences(self) -> Dict[str, Any]:
        """Load user preferences from file."""
        try:
            if self.preferences_file.exists():
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    preferences = json.load(f)
                
                # Merge with defaults to ensure all keys exist
                merged_preferences = self.default_preferences.copy()
                merged_preferences.update(preferences)
                
                log_info("User preferences loaded successfully", "PREFERENCES")
                return merged_preferences
            else:
                log_info("No preferences file found, using defaults", "PREFERENCES")
                return self.default_preferences.copy()
                
        except Exception as e:
            log_error(f"Failed to load preferences: {str(e)}", "PREFERENCES", e)
            return self.default_preferences.copy()
    
    def save_preferences(self) -> bool:
        """Save user preferences to file."""
        try:
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=2, ensure_ascii=False)
            
            log_info("User preferences saved successfully", "PREFERENCES")
            return True
            
        except Exception as e:
            log_error(f"Failed to save preferences: {str(e)}", "PREFERENCES", e)
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get a preference value using dot notation (e.g., 'ui.theme')."""
        try:
            keys = key_path.split('.')
            value = self.preferences
            
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default
            
            return value
            
        except Exception as e:
            log_warning(f"Failed to get preference '{key_path}': {str(e)}", "PREFERENCES")
            return default
    
    def set(self, key_path: str, value: Any) -> bool:
        """Set a preference value using dot notation."""
        try:
            keys = key_path.split('.')
            current = self.preferences
            
            # Navigate to the parent of the target key
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Set the value
            current[keys[-1]] = value
            
            log_info(f"Set preference '{key_path}' = {value}", "PREFERENCES")
            return True
            
        except Exception as e:
            log_error(f"Failed to set preference '{key_path}': {str(e)}", "PREFERENCES", e)
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset all preferences to default values."""
        try:
            self.preferences = self.default_preferences.copy()
            self.save_preferences()
            log_info("Preferences reset to defaults", "PREFERENCES")
            return True
            
        except Exception as e:
            log_error(f"Failed to reset preferences: {str(e)}", "PREFERENCES", e)
            return False
    
    def get_ui_preferences(self) -> Dict[str, Any]:
        """Get UI-specific preferences."""
        return self.get("ui", {})
    
    def get_performance_preferences(self) -> Dict[str, Any]:
        """Get performance-specific preferences."""
        return self.get("performance", {})
    
    def get_backup_preferences(self) -> Dict[str, Any]:
        """Get backup-specific preferences."""
        return self.get("backup", {})
    
    def get_advanced_preferences(self) -> Dict[str, Any]:
        """Get advanced-specific preferences."""
        return self.get("advanced", {})
    
    def save(self) -> bool:
        """Public method to save user preferences."""
        return self.save_preferences()