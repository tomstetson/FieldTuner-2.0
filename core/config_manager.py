"""
Configuration Manager for FieldTuner
Handles detection, parsing, and management of Battlefield 6 config files.
"""

import os
import re
import shutil
import hashlib
from pathlib import Path
from typing import Dict, Optional, Tuple, List
import logging


class ConfigManager:
    """Manages Battlefield 6 configuration files and settings."""
    
    # Common Battlefield 6 config paths
    CONFIG_PATHS = [
        Path.home() / "Documents" / "Battlefield 6" / "settings" / "steam" / "PROFSAVE_profile",
        Path.home() / "Documents" / "Battlefield 6" / "settings" / "PROFSAVE_profile",
        Path.home() / "OneDrive" / "Documents" / "Battlefield 6" / "settings" / "steam" / "PROFSAVE_profile",
        Path.home() / "OneDrive" / "Documents" / "Battlefield 6" / "settings" / "PROFSAVE_profile"
    ]
    
    # Backup directory
    BACKUP_DIR = Path.home() / "AppData" / "Roaming" / "FieldTuner" / "backups"
    
    # Log directory
    LOG_DIR = Path.home() / "AppData" / "Roaming" / "FieldTuner" / "logs"
    
    def __init__(self):
        """Initialize the configuration manager."""
        self.config_path: Optional[Path] = None
        self.config_data: Dict[str, str] = {}
        self.original_data: str = ""
        self.backup_path: Optional[Path] = None
        
        # Setup logging
        self._setup_logging()
        
        # Create necessary directories
        self.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        # Auto-detect config file
        self._detect_config_file()
        
        if self.config_path and self.config_path.exists():
            self._load_config()
            self._create_backup()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        log_file = self.LOG_DIR / "fieldtuner.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _detect_config_file(self) -> bool:
        """Auto-detect the Battlefield 6 config file."""
        for path in self.CONFIG_PATHS:
            if path.exists():
                self.config_path = path
                self.logger.info(f"Found config file: {path}")
                return True
        
        self.logger.warning("No Battlefield 6 config file found")
        return False
    
    def _load_config(self) -> bool:
        """Load configuration from the detected file."""
        if not self.config_path or not self.config_path.exists():
            return False
        
        try:
            with open(self.config_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.original_data = f.read()
            
            # Parse config entries
            self.config_data = self._parse_config_data(self.original_data)
            self.logger.info(f"Loaded {len(self.config_data)} config entries")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return False
    
    def _parse_config_data(self, data: str) -> Dict[str, str]:
        """Parse configuration data into key-value pairs."""
        config = {}
        
        # Pattern to match GstRender entries and other common settings
        patterns = [
            r'(GstRender\.\w+)\s+(\S+)',
            r'(GstAudio\.\w+)\s+(\S+)',
            r'(GstInput\.\w+)\s+(\S+)',
            r'(GstGame\.\w+)\s+(\S+)',
            r'(GstNetwork\.\w+)\s+(\S+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, data)
            for key, value in matches:
                config[key] = value
        
        return config
    
    def _create_backup(self) -> bool:
        """Create a backup of the original config file."""
        if not self.config_path or not self.config_path.exists():
            return False
        
        try:
            timestamp = Path(self.config_path).stat().st_mtime
            backup_name = f"PROFSAVE_profile_backup_{int(timestamp)}.bak"
            self.backup_path = self.BACKUP_DIR / backup_name
            
            shutil.copy2(self.config_path, self.backup_path)
            self.logger.info(f"Created backup: {self.backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return False
    
    def get_setting(self, key: str, default: str = "") -> str:
        """Get a configuration setting value."""
        return self.config_data.get(key, default)
    
    def set_setting(self, key: str, value: str) -> None:
        """Set a configuration setting value."""
        self.config_data[key] = str(value)
        self.logger.info(f"Set {key} = {value}")
    
    def get_available_settings(self) -> List[str]:
        """Get list of all available settings."""
        return list(self.config_data.keys())
    
    def get_graphics_settings(self) -> Dict[str, str]:
        """Get graphics-related settings."""
        graphics_keys = [k for k in self.config_data.keys() if k.startswith('GstRender.')]
        return {k: self.config_data[k] for k in graphics_keys}
    
    def get_audio_settings(self) -> Dict[str, str]:
        """Get audio-related settings."""
        audio_keys = [k for k in self.config_data.keys() if k.startswith('GstAudio.')]
        return {k: self.config_data[k] for k in audio_keys}
    
    def get_input_settings(self) -> Dict[str, str]:
        """Get input-related settings."""
        input_keys = [k for k in self.config_data.keys() if k.startswith('GstInput.')]
        return {k: self.config_data[k] for k in input_keys}
    
    def get_game_settings(self) -> Dict[str, str]:
        """Get game-related settings."""
        game_keys = [k for k in self.config_data.keys() if k.startswith('GstGame.')]
        return {k: self.config_data[k] for k in game_keys}
    
    def get_network_settings(self) -> Dict[str, str]:
        """Get network-related settings."""
        network_keys = [k for k in self.config_data.keys() if k.startswith('GstNetwork.')]
        return {k: self.config_data[k] for k in network_keys}
    
    def validate_setting(self, key: str, value: str) -> Tuple[bool, str]:
        """Validate a setting value."""
        # Common validation rules
        if key == "GstRender.ResolutionScale":
            try:
                scale = float(value)
                if 0.5 <= scale <= 2.0:
                    return True, ""
                else:
                    return False, "Resolution scale must be between 0.5 and 2.0"
            except ValueError:
                return False, "Resolution scale must be a number"
        
        elif key == "GstRender.FullscreenMode":
            if value in ["0", "1"]:
                return True, ""
            else:
                return False, "Fullscreen mode must be 0 (windowed) or 1 (fullscreen)"
        
        elif key in ["GstRender.Dx12Enabled", "GstRender.MotionBlurEnable", "GstRender.DepthOfFieldEnable"]:
            if value in ["0", "1"]:
                return True, ""
            else:
                return False, "Boolean setting must be 0 or 1"
        
        elif key == "GstRender.AntiAliasingDeferred":
            try:
                aa = int(value)
                if 0 <= aa <= 4:
                    return True, ""
                else:
                    return False, "Anti-aliasing level must be between 0 and 4"
            except ValueError:
                return False, "Anti-aliasing level must be a number"
        
        return True, ""  # Default: accept any value
    
    def save_config(self) -> bool:
        """Save configuration changes to file."""
        if not self.config_path:
            self.logger.error("No config file path available")
            return False
        
        try:
            # Create new config content
            new_data = self._generate_config_content()
            
            # Validate before writing
            if not self._validate_config_content(new_data):
                self.logger.error("Generated config content failed validation")
                return False
            
            # Write to file
            with open(self.config_path, 'w', encoding='utf-8') as f:
                f.write(new_data)
            
            self.logger.info("Configuration saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
            return False
    
    def _generate_config_content(self) -> str:
        """Generate new config file content with updated values."""
        lines = self.original_data.split('\n')
        new_lines = []
        
        for line in lines:
            # Check if line contains a setting we've modified
            modified = False
            for key, value in self.config_data.items():
                if key in line:
                    # Replace the value in the line
                    pattern = rf'({re.escape(key)})\s+\S+'
                    replacement = f'{key} {value}'
                    new_line = re.sub(pattern, replacement, line)
                    new_lines.append(new_line)
                    modified = True
                    break
            
            if not modified:
                new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def _validate_config_content(self, content: str) -> bool:
        """Validate the generated config content."""
        # Basic validation - check if content is not empty
        if not content.strip():
            return False
        
        # Check if we can parse it back
        try:
            parsed = self._parse_config_data(content)
            return len(parsed) > 0
        except:
            return False
    
    def restore_backup(self) -> bool:
        """Restore from backup."""
        if not self.backup_path or not self.backup_path.exists():
            self.logger.error("No backup file available")
            return False
        
        try:
            shutil.copy2(self.backup_path, self.config_path)
            self._load_config()  # Reload the restored config
            self.logger.info("Configuration restored from backup")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore backup: {e}")
            return False
    
    def get_config_info(self) -> Dict[str, str]:
        """Get information about the current config."""
        info = {
            "config_path": str(self.config_path) if self.config_path else "Not found",
            "backup_path": str(self.backup_path) if self.backup_path else "Not created",
            "settings_count": str(len(self.config_data)),
            "file_size": str(self.config_path.stat().st_size) if self.config_path and self.config_path.exists() else "Unknown"
        }
        return info
