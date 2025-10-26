"""
FieldTuner V2.0 - Application State
Manages global application state and settings.
"""

from typing import Dict, Any, Optional
from pathlib import Path

from debug import log_info, log_error, log_warning
from core.path_config import path_config


class AppState:
    """Manages global application state and settings."""
    
    def __init__(self):
        """Initialize the application state."""
        self.state_file = path_config.app_state_file
        self.state: Dict[str, Any] = {}
        self._load_state()
    
    def _load_state(self):
        """Load application state from persistent storage."""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            
            if self.state_file.exists():
                import json
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    self.state = json.load(f)
                    log_info("Loaded application state", "APP_STATE")
            else:
                log_info("No state file found, starting with default state", "APP_STATE")
                self._set_default_state()
                
        except Exception as e:
            log_error(f"Failed to load app state: {str(e)}", "APP_STATE", e)
            self._set_default_state()
    
    def _set_default_state(self):
        """Set default application state."""
        self.state = {
            'version': '2.0',
            'last_config_path': None,
            'window_geometry': None,
            'theme': 'dark',
            'auto_backup': True,
            'show_advanced': False,
            'last_tab': 'quick',
            'settings': {
                'auto_detect_config': True,
                'warn_on_game_running': True,
                'create_backup_on_start': True,
                'show_debug_info': False,
            }
        }
    
    def _save_state(self):
        """Save application state to persistent storage."""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            
            import json
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2)
            
            log_info("Saved application state", "APP_STATE")
            
        except Exception as e:
            log_error(f"Failed to save app state: {str(e)}", "APP_STATE", e)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a state value."""
        return self.state.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a state value."""
        self.state[key] = value
        self._save_state()
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.state.get('settings', {}).get(key, default)
    
    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        if 'settings' not in self.state:
            self.state['settings'] = {}
        self.state['settings'][key] = value
        self._save_state()
    
    def get_last_config_path(self) -> Optional[str]:
        """Get the last used config path."""
        return self.state.get('last_config_path')
    
    def set_last_config_path(self, path: str) -> None:
        """Set the last used config path."""
        self.set('last_config_path', path)
    
    def get_window_geometry(self) -> Optional[Dict[str, int]]:
        """Get the last window geometry."""
        return self.state.get('window_geometry')
    
    def set_window_geometry(self, geometry: Dict[str, int]) -> None:
        """Set the window geometry."""
        self.set('window_geometry', geometry)
    
    def get_theme(self) -> str:
        """Get the current theme."""
        return self.state.get('theme', 'dark')
    
    def set_theme(self, theme: str) -> None:
        """Set the theme."""
        self.set('theme', theme)
    
    def is_auto_backup_enabled(self) -> bool:
        """Check if auto backup is enabled."""
        return self.state.get('auto_backup', True)
    
    def set_auto_backup(self, enabled: bool) -> None:
        """Set auto backup setting."""
        self.set('auto_backup', enabled)
    
    def get_last_tab(self) -> str:
        """Get the last active tab."""
        return self.state.get('last_tab', 'quick')
    
    def set_last_tab(self, tab: str) -> None:
        """Set the last active tab."""
        self.set('last_tab', tab)
    
    def should_show_advanced(self) -> bool:
        """Check if advanced settings should be shown."""
        return self.state.get('show_advanced', False)
    
    def set_show_advanced(self, show: bool) -> None:
        """Set whether to show advanced settings."""
        self.set('show_advanced', show)
    
    def save(self) -> None:
        """Public method to save application state."""
        self._save_state()
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        self._set_default_state()
        self._save_state()
        log_info("Reset application state to defaults", "APP_STATE")
