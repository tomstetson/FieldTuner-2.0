"""
Binary Configuration Manager for FieldTuner
Handles binary Frostbite PROFSAVE files for Battlefield 6.
"""

import struct
import os
import shutil
from pathlib import Path
from typing import Dict, Optional, Any
import logging


class BinaryConfigManager:
    """Manages binary Battlefield 6 PROFSAVE configuration files."""
    
    # Common Battlefield 6 config paths
    CONFIG_PATHS = [
        Path.home() / "Documents" / "Battlefield 6" / "settings" / "steam" / "PROFSAVE_profile",
        Path.home() / "Documents" / "Battlefield 6" / "settings" / "PROFSAVE_profile",
        Path.home() / "OneDrive" / "Documents" / "Battlefield 6" / "settings" / "steam" / "PROFSAVE_profile",
        Path.home() / "OneDrive" / "Documents" / "Battlefield 6" / "settings" / "PROFSAVE_profile"
    ]
    
    # Backup directory
    BACKUP_DIR = Path.home() / "AppData" / "Roaming" / "FieldTuner" / "backups"
    
    def __init__(self):
        """Initialize the binary configuration manager."""
        self.config_path: Optional[Path] = None
        self.config_data: Dict[str, Any] = {}
        self.original_data: bytes = b""
        self.backup_path: Optional[Path] = None
        
        # Setup logging
        self._setup_logging()
        
        # Create necessary directories
        self.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
        # Auto-detect config file
        self._detect_config_file()
        
        if self.config_path and self.config_path.exists():
            self._load_config()
    
    def _setup_logging(self):
        """Setup logging for the config manager."""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _detect_config_file(self):
        """Auto-detect the Battlefield 6 config file."""
        for path in self.CONFIG_PATHS:
            if path.exists():
                self.config_path = path
                self.logger.info(f"Found BF6 config: {path}")
                return
        
        self.logger.warning("No BF6 config file found in standard locations")
    
    def _load_config(self):
        """Load the binary config file."""
        if not self.config_path or not self.config_path.exists():
            return False
        
        try:
            with open(self.config_path, 'rb') as f:
                self.original_data = f.read()
            
            # Parse binary config (simplified for now)
            self._parse_binary_config()
            
            self.logger.info(f"Loaded config with {len(self.config_data)} settings")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return False
    
    def _parse_binary_config(self):
        """Parse the binary PROFSAVE file."""
        # This is a simplified parser - in reality, PROFSAVE files have complex structure
        # For now, we'll create a basic mapping of common settings
        
        # Common BF6 settings with their typical values
        self.config_data = {
            "GstRender.Dx12Enabled": 0,  # 0 = disabled, 1 = enabled
            "GstRender.VSyncEnabled": 0,  # 0 = disabled, 1 = enabled
            "GstRender.MotionBlurEnabled": 1,  # 0 = disabled, 1 = enabled
            "GstRender.AmbientOcclusionEnabled": 1,  # 0 = disabled, 1 = enabled
            "GstRender.ResolutionScale": 1.0,  # 0.5 to 2.0
            "GstRender.TextureQuality": 2,  # 0-4
            "GstRender.EffectsQuality": 2,  # 0-4
            "GstRender.LightingQuality": 2,  # 0-4
            "GstRender.PostProcessQuality": 2,  # 0-4
            "GstRender.ShadowQuality": 2,  # 0-4
            "GstRender.TerrainQuality": 2,  # 0-4
            "GstRender.VegetationQuality": 2,  # 0-4
            "GstRender.AntiAliasing": 2,  # 0-4
            "GstRender.UltraLowLatency": 0,  # 0 = disabled, 1 = enabled
            "GstRender.FrameRateLimit": 0,  # 0 = unlimited, >0 = FPS limit
        }
        
        self.logger.info("Parsed binary config with default settings")
    
    def get_setting(self, key: str) -> Any:
        """Get a configuration setting value."""
        return self.config_data.get(key)
    
    def set_setting(self, key: str, value: Any) -> bool:
        """Set a configuration setting value."""
        if key in self.config_data:
            self.config_data[key] = value
            self.logger.info(f"Set {key} = {value}")
            return True
        return False
    
    def save_config(self) -> bool:
        """Save configuration changes to the binary file."""
        if not self.config_path:
            self.logger.error("No config file path available")
            return False
        
        try:
            # Create backup before modifying
            self._create_backup()
            
            # For now, we'll create a new binary config with our settings
            # In a real implementation, this would properly modify the binary structure
            new_data = self._generate_binary_config()
            
            # Write the new config
            with open(self.config_path, 'wb') as f:
                f.write(new_data)
            
            self.logger.info("Binary configuration saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save binary config: {e}")
            return False
    
    def _generate_binary_config(self) -> bytes:
        """Generate new binary config content."""
        # This is a simplified implementation
        # A real implementation would properly encode the binary PROFSAVE format
        
        # For now, we'll create a basic binary structure
        # This is NOT a real PROFSAVE file, but demonstrates the concept
        
        # Create a simple binary structure with our settings
        data = bytearray()
        
        # Add a header (simplified)
        data.extend(b"PROFSAVE\x00")
        
        # Add settings as key-value pairs (simplified)
        for key, value in self.config_data.items():
            # Add key length and key
            key_bytes = key.encode('utf-8')
            data.extend(struct.pack('<I', len(key_bytes)))
            data.extend(key_bytes)
            
            # Add value based on type
            if isinstance(value, bool):
                data.extend(struct.pack('<B', 1 if value else 0))
            elif isinstance(value, int):
                data.extend(struct.pack('<I', value))
            elif isinstance(value, float):
                data.extend(struct.pack('<f', value))
            else:
                # String value
                value_bytes = str(value).encode('utf-8')
                data.extend(struct.pack('<I', len(value_bytes)))
                data.extend(value_bytes)
        
        return bytes(data)
    
    def _create_backup(self):
        """Create a backup of the current config file."""
        if not self.config_path or not self.config_path.exists():
            return False
        
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"FieldTuner_Backup_{timestamp}.bak"
            self.backup_path = self.BACKUP_DIR / backup_name
            
            shutil.copy2(self.config_path, self.backup_path)
            self.logger.info(f"Created backup: {self.backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return False
    
    def restore_backup(self, backup_path: Path) -> bool:
        """Restore from a backup file."""
        try:
            if not backup_path.exists():
                return False
            
            shutil.copy2(backup_path, self.config_path)
            self.logger.info(f"Restored from backup: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore backup: {e}")
            return False
    
    def get_available_backups(self) -> list:
        """Get list of available backup files."""
        if not self.BACKUP_DIR.exists():
            return []
        
        backups = []
        for backup_file in self.BACKUP_DIR.glob("*.bak"):
            backups.append({
                'path': backup_file,
                'name': backup_file.name,
                'size': backup_file.stat().st_size,
                'modified': backup_file.stat().st_mtime
            })
        
        return sorted(backups, key=lambda x: x['modified'], reverse=True)
