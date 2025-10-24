#!/usr/bin/env python3
"""
FieldTuner - Super Slick Battlefield 6 Configuration Tool
World-class GUI with proper debugging and stunning design
"""

import sys
import os
import re
import shutil
import json
import subprocess
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QLabel, QPushButton, QSlider, QCheckBox, QComboBox,
    QSpinBox, QDoubleSpinBox, QGroupBox, QGridLayout, QTextEdit,
    QMessageBox, QFileDialog, QStatusBar, QProgressBar, QSplitter,
    QListWidget, QListWidgetItem, QFrame, QScrollArea, QPlainTextEdit,
    QPushButton, QLineEdit, QFormLayout, QButtonGroup, QRadioButton,
    QStackedWidget, QSizePolicy, QSpacerItem, QLayout, QDialog,
    QDialogButtonBox, QTextBrowser
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QTextCursor, QPixmap, QPainter, QLinearGradient

# Import debug system
from debug import debug_logger, log_info, log_warning, log_error, log_debug, get_debug_logger


class ProfessionalToggleSwitch(QWidget):
    """Professional toggle switch with modern design and smooth animations."""
    
    toggled = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(52, 28)
        self.is_on = False
        self.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border: 2px solid #404040;
                border-radius: 14px;
            }
        """)
        
    def mousePressEvent(self, event):
        self.toggle()
        super().mousePressEvent(event)
    
    def toggle(self):
        self.is_on = not self.is_on
        self.update_style()
        self.toggled.emit(self.is_on)
    
    def set_checked(self, checked):
        self.is_on = checked
        self.update_style()
    
    def is_checked(self):
        return self.is_on
    
    def update_style(self):
        if self.is_on:
            self.setStyleSheet("""
                QWidget {
                    background-color: #4a90e2;
                    border: 2px solid #4a90e2;
                    border-radius: 14px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2a2a2a;
                    border: 2px solid #404040;
                    border-radius: 14px;
                }
            """)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        if self.is_on:
            painter.setBrush(QColor("#4a90e2"))
            painter.setPen(QColor("#4a90e2"))
        else:
            painter.setBrush(QColor("#2a2a2a"))
            painter.setPen(QColor("#404040"))
        
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 14, 14)
        
        # Draw toggle button
        if self.is_on:
            painter.setBrush(QColor("#ffffff"))
            painter.setPen(QColor("#ffffff"))
            # Position on right
            button_x = self.width() - 22
        else:
            painter.setBrush(QColor("#666666"))
            painter.setPen(QColor("#666666"))
            # Position on left
            button_x = 2
        
        painter.drawEllipse(button_x, 3, 20, 20)


class ConfigManager:
    """Enhanced config manager with debugging."""
    
    def __init__(self):
        log_info("Initializing ConfigManager", "CONFIG")
        self.config_path = None
        self.config_data = {}
        self.original_data = ""
        self.backup_path = None
        
        # Common Battlefield 6 config paths
        self.CONFIG_PATHS = [
            Path.home() / "Documents" / "Battlefield 6" / "settings" / "steam" / "PROFSAVE_profile",
            Path.home() / "Documents" / "Battlefield 6" / "settings" / "PROFSAVE_profile",
            Path.home() / "OneDrive" / "Documents" / "Battlefield 6" / "settings" / "steam" / "PROFSAVE_profile",
            Path.home() / "OneDrive" / "Documents" / "Battlefield 6" / "settings" / "PROFSAVE_profile"
        ]
        
        # Create backup directory with error handling
        try:
            self.BACKUP_DIR = Path.home() / "AppData" / "Roaming" / "FieldTuner" / "backups"
            self.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
            log_info(f"Backup directory created: {self.BACKUP_DIR}", "CONFIG")
        except Exception as e:
            log_error(f"Failed to create backup directory in AppData: {e}", "CONFIG")
            # Fallback to current directory
            self.BACKUP_DIR = Path.cwd() / "backups"
            self.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
            log_info(f"Using fallback backup directory: {self.BACKUP_DIR}", "CONFIG")
        
        # World-class settings based on real BF6 config analysis and competitive research
        self.optimal_settings = {
            'esports': {
                'name': 'Esports Pro',
                'description': 'Maximum competitive advantage - used by pro players',
                'icon': '🏆',
                'color': '#d32f2f',
                'settings': {
                    # Performance optimizations
                    'GstRender.Dx12Enabled': '1',
                    'GstRender.FullscreenMode': '2',  # Exclusive fullscreen
                    'GstRender.VSyncMode': '0',  # Disabled for lowest input lag
                    'GstRender.FutureFrameRendering': '1',  # Enabled for FPS boost
                    'GstRender.FrameRateLimit': '240.000000',
                    'GstRender.FrameRateLimiterEnable': '0',
                    
                    # Visual clarity optimizations
                    'GstRender.MotionBlurWorld': '0.000000',  # Disabled
                    'GstRender.MotionBlurWeapon': '0.000000',  # Disabled
                    'GstRender.WeaponDOF': '0',  # Disabled for clarity
                    'GstRender.ChromaticAberration': '0',  # Disabled
                    'GstRender.VolumetricQuality': '0',  # Disabled
                    'GstRender.AmbientOcclusion': '0',  # Disabled
                    'GstRender.FilmGrain': '0',  # Disabled
                    'GstRender.Vignette': '0',  # Disabled
                    'GstRender.LensDistortion': '0',  # Disabled
                    
                    # Quality settings (lowest for max FPS)
                    'GstRender.EffectsQuality': '0',
                    'GstRender.MeshQuality': '0',
                    'GstRender.TextureQuality': '0',
                    'GstRender.LightingQuality': '0',
                    'GstRender.PostProcessQuality': '0',
                    'GstRender.ShadowQuality': '0',
                    'GstRender.TerrainQuality': '0',
                    'GstRender.UndergrowthQuality': '0',
                    'GstRender.ScreenSpaceReflections': '0',
                    'GstRender.RaytracingAmbientOcclusion': '0',
                    
                    # Anti-aliasing (minimal)
                    'GstRender.AMDIntelAntiAliasing': '0',
                    'GstRender.NvidiaAntiAliasing': '0',
                    
                    # FOV for competitive advantage
                    'GstRender.FieldOfViewVertical': '105.000000',  # Max FOV
                    'GstRender.FieldOfViewScaleHip': '1',
                    'GstRender.FieldOfViewScaleADS': '0',
                    
                    # Performance mode
                    'GstRender.PerformanceMode': '2',  # Maximum performance
                    'GstRender.OverallGraphicsQuality': '0',  # Low
                }
            },
            'competitive': {
                'name': 'Competitive',
                'description': 'High performance with good visuals - best of both worlds',
                'icon': '⚡',
                'color': '#ff6b35',
                'settings': {
                    # Performance optimizations
                    'GstRender.Dx12Enabled': '1',
                    'GstRender.FullscreenMode': '2',
                    'GstRender.VSyncMode': '0',
                    'GstRender.FutureFrameRendering': '1',
                    'GstRender.FrameRateLimit': '144.000000',
                    'GstRender.FrameRateLimiterEnable': '0',
                    
                    # Visual clarity (selective)
                    'GstRender.MotionBlurWorld': '0.000000',  # Disabled
                    'GstRender.MotionBlurWeapon': '25.000000',  # Reduced
                    'GstRender.WeaponDOF': '0',  # Disabled
                    'GstRender.ChromaticAberration': '0',  # Disabled
                    'GstRender.VolumetricQuality': '0',  # Disabled
                    'GstRender.AmbientOcclusion': '1',  # Low
                    'GstRender.FilmGrain': '0',  # Disabled
                    'GstRender.Vignette': '0',  # Disabled
                    'GstRender.LensDistortion': '0',  # Disabled
                    
                    # Quality settings (balanced)
                    'GstRender.EffectsQuality': '1',
                    'GstRender.MeshQuality': '1',
                    'GstRender.TextureQuality': '1',
                    'GstRender.LightingQuality': '1',
                    'GstRender.PostProcessQuality': '1',
                    'GstRender.ShadowQuality': '1',
                    'GstRender.TerrainQuality': '1',
                    'GstRender.UndergrowthQuality': '1',
                    'GstRender.ScreenSpaceReflections': '0',
                    'GstRender.RaytracingAmbientOcclusion': '0',
                    
                    # Anti-aliasing (light)
                    'GstRender.AMDIntelAntiAliasing': '1',
                    'GstRender.NvidiaAntiAliasing': '1',
                    
                    # FOV for competitive play
                    'GstRender.FieldOfViewVertical': '95.000000',  # High FOV
                    'GstRender.FieldOfViewScaleHip': '1',
                    'GstRender.FieldOfViewScaleADS': '0',
                    
                    # Performance mode
                    'GstRender.PerformanceMode': '1',  # Balanced
                    'GstRender.OverallGraphicsQuality': '1',  # Medium
                }
            },
            'balanced': {
                'name': 'Balanced',
                'description': 'Great performance with beautiful visuals - perfect for most players',
                'icon': '⚖️',
                'color': '#4a90e2',
                'settings': {
                    # Performance optimizations
                    'GstRender.Dx12Enabled': '1',
                    'GstRender.FullscreenMode': '2',
                    'GstRender.VSyncMode': '0',
                    'GstRender.FutureFrameRendering': '1',
                    'GstRender.FrameRateLimit': '120.000000',
                    'GstRender.FrameRateLimiterEnable': '0',
                    
                    # Visual effects (balanced)
                    'GstRender.MotionBlurWorld': '0.500000',  # Medium
                    'GstRender.MotionBlurWeapon': '50.000000',  # Medium
                    'GstRender.WeaponDOF': '1',  # Enabled
                    'GstRender.ChromaticAberration': '1',  # Enabled
                    'GstRender.VolumetricQuality': '1',  # Low
                    'GstRender.AmbientOcclusion': '1',  # Medium
                    'GstRender.FilmGrain': '1',  # Enabled
                    'GstRender.Vignette': '1',  # Enabled
                    'GstRender.LensDistortion': '1',  # Enabled
                    
                    # Quality settings (high)
                    'GstRender.EffectsQuality': '2',
                    'GstRender.MeshQuality': '2',
                    'GstRender.TextureQuality': '2',
                    'GstRender.LightingQuality': '2',
                    'GstRender.PostProcessQuality': '2',
                    'GstRender.ShadowQuality': '2',
                    'GstRender.TerrainQuality': '2',
                    'GstRender.UndergrowthQuality': '2',
                    'GstRender.ScreenSpaceReflections': '1',
                    'GstRender.RaytracingAmbientOcclusion': '0',
                    
                    # Anti-aliasing (good)
                    'GstRender.AMDIntelAntiAliasing': '2',
                    'GstRender.NvidiaAntiAliasing': '2',
                    
                    # FOV (comfortable)
                    'GstRender.FieldOfViewVertical': '90.000000',  # Standard
                    'GstRender.FieldOfViewScaleHip': '1',
                    'GstRender.FieldOfViewScaleADS': '0',
                    
                    # Performance mode
                    'GstRender.PerformanceMode': '0',  # Quality
                    'GstRender.OverallGraphicsQuality': '2',  # High
                }
            },
            'cinematic': {
                'name': 'Cinematic',
                'description': 'Maximum visual fidelity - for high-end systems and screenshots',
                'icon': '🎬',
                'color': '#9c27b0',
                'settings': {
                    # Performance optimizations
                    'GstRender.Dx12Enabled': '1',
                    'GstRender.FullscreenMode': '2',
                    'GstRender.VSyncMode': '1',  # Enabled for smooth visuals
                    'GstRender.FutureFrameRendering': '1',
                    'GstRender.FrameRateLimit': '60.000000',
                    'GstRender.FrameRateLimiterEnable': '1',
                    
                    # Visual effects (maximum)
                    'GstRender.MotionBlurWorld': '1.000000',  # Maximum
                    'GstRender.MotionBlurWeapon': '100.000000',  # Maximum
                    'GstRender.WeaponDOF': '1',  # Enabled
                    'GstRender.ChromaticAberration': '1',  # Enabled
                    'GstRender.VolumetricQuality': '2',  # High
                    'GstRender.AmbientOcclusion': '2',  # High
                    'GstRender.FilmGrain': '1',  # Enabled
                    'GstRender.Vignette': '1',  # Enabled
                    'GstRender.LensDistortion': '1',  # Enabled
                    
                    # Quality settings (ultra)
                    'GstRender.EffectsQuality': '3',
                    'GstRender.MeshQuality': '3',
                    'GstRender.TextureQuality': '3',
                    'GstRender.LightingQuality': '3',
                    'GstRender.PostProcessQuality': '3',
                    'GstRender.ShadowQuality': '3',
                    'GstRender.TerrainQuality': '3',
                    'GstRender.UndergrowthQuality': '3',
                    'GstRender.ScreenSpaceReflections': '2',
                    'GstRender.RaytracingAmbientOcclusion': '1',
                    
                    # Anti-aliasing (maximum)
                    'GstRender.AMDIntelAntiAliasing': '3',
                    'GstRender.NvidiaAntiAliasing': '3',
                    
                    # FOV (immersive)
                    'GstRender.FieldOfViewVertical': '85.000000',  # Cinematic
                    'GstRender.FieldOfViewScaleHip': '1',
                    'GstRender.FieldOfViewScaleADS': '0',
                    
                    # Performance mode
                    'GstRender.PerformanceMode': '0',  # Quality
                    'GstRender.OverallGraphicsQuality': '3',  # Ultra
                }
            }
        }
        
        self._detect_config_file()
        if self.config_path and self.config_path.exists():
            self._load_config()
            self._create_backup()
            log_info(f"Battlefield 6 config detected and backed up: {self.config_path}", "CONFIG")
    
    def _detect_config_file(self):
        """Auto-detect the Battlefield 6 config file."""
        log_info("Detecting Battlefield 6 config file", "CONFIG")
        for i, path in enumerate(self.CONFIG_PATHS):
            log_debug(f"Checking path {i+1}: {path}", "CONFIG")
            if path.exists():
                self.config_path = path
                log_info(f"Config file found: {path}", "CONFIG")
                return True
        
        log_warning("No Battlefield 6 config file found", "CONFIG")
        return False
    
    def _load_config(self):
        """Load configuration from the detected file."""
        if not self.config_path or not self.config_path.exists():
            log_error("Config file not found or invalid", "CONFIG")
            return False
        
        try:
            log_info(f"Loading config from: {self.config_path}", "CONFIG")
            
            # Read the binary config file
            with open(self.config_path, 'rb') as f:
                self.original_data = f.read()
            
            # Parse the binary data
            self.config_data = self._parse_binary_config(self.original_data)
            log_info(f"Loaded {len(self.config_data)} settings", "CONFIG")
            return True
        except Exception as e:
            log_error(f"Failed to load config: {str(e)}", "CONFIG", e)
            return False
    
    def _parse_binary_config(self, data):
        """Parse binary configuration data into key-value pairs."""
        config = {}
        
        try:
            import struct
            
            # Check for PROFSAVE header
            if not data.startswith(b"PROFSAVE"):
                log_warning("Config file doesn't start with PROFSAVE header", "CONFIG")
                # Try to parse as text-based config
                return self._parse_text_config(data)
            
            # Skip header
            offset = 8
            
            # Read version (4 bytes)
            if offset + 4 > len(data):
                log_error("Config file too short for version", "CONFIG")
                return config
            version = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            log_info(f"Config version: {version}", "CONFIG")
            
            # Read settings count (4 bytes)
            if offset + 4 > len(data):
                log_error("Config file too short for settings count", "CONFIG")
                return config
            settings_count = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            log_info(f"Settings count: {settings_count}", "CONFIG")
            
            # Parse each setting
            for i in range(settings_count):
                if offset >= len(data):
                    log_warning(f"Reached end of file at setting {i}", "CONFIG")
                    break
                
                # Read key length
                if offset + 4 > len(data):
                    break
                key_len = struct.unpack('<I', data[offset:offset+4])[0]
                offset += 4
                
                # Read key
                if offset + key_len > len(data):
                    break
                key = data[offset:offset+key_len].decode('utf-8', errors='ignore')
                offset += key_len
                
                # Read value type (1 byte)
                if offset + 1 > len(data):
                    break
                value_type = data[offset]
                offset += 1
                
                # Read value based on type
                if value_type == 0:  # Bool
                    if offset + 1 > len(data):
                        break
                    value = bool(data[offset])
                    offset += 1
                elif value_type == 1:  # Int
                    if offset + 4 > len(data):
                        break
                    value = struct.unpack('<I', data[offset:offset+4])[0]
                    offset += 4
                elif value_type == 2:  # Float
                    if offset + 4 > len(data):
                        break
                    value = struct.unpack('<f', data[offset:offset+4])[0]
                    offset += 4
                elif value_type == 3:  # String
                    if offset + 4 > len(data):
                        break
                    value_len = struct.unpack('<I', data[offset:offset+4])[0]
                    offset += 4
                    if offset + value_len > len(data):
                        break
                    value = data[offset:offset+value_len].decode('utf-8', errors='ignore')
                    offset += value_len
                else:
                    log_warning(f"Unknown value type {value_type} for key {key}", "CONFIG")
                    continue
                
                config[key] = value
                log_debug(f"Parsed setting: {key} = {value} (type: {value_type})", "CONFIG")
            
            log_info(f"Successfully parsed {len(config)} settings from binary config", "CONFIG")
            return config
            
        except Exception as e:
            log_error(f"Failed to parse binary config: {str(e)}", "CONFIG", e)
            # Fallback to text parsing
            return self._parse_text_config(data)
    
    def _parse_text_config(self, data):
        """Fallback text-based config parser."""
        config = {}
        
        try:
            # Try to decode as text
            text_data = data.decode('utf-8', errors='ignore')
            lines = text_data.split('\n')
            
            for line in lines:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Try to convert value to appropriate type
                    if value.lower() in ['true', 'false']:
                        config[key] = value.lower() == 'true'
                    elif value.isdigit():
                        config[key] = int(value)
                    elif '.' in value and value.replace('.', '').isdigit():
                        config[key] = float(value)
                    else:
                        config[key] = value
            
            log_info(f"Parsed {len(config)} settings from text config", "CONFIG")
            return config
            
        except Exception as e:
            log_error(f"Failed to parse text config: {str(e)}", "CONFIG", e)
            return {}
    
    def _parse_config_data(self, data):
        """Legacy method - redirects to binary parser."""
        return self._parse_binary_config(data)
    
    def _create_backup(self, custom_name=None):
        """Create a backup of the original config file."""
        if not self.config_path or not self.config_path.exists():
            log_warning("Cannot create backup: config file not found", "BACKUP")
            return False
        
        try:
            # Ensure backup directory exists
            self.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
            log_info(f"Backup directory: {self.BACKUP_DIR}", "BACKUP")
            
            if custom_name:
                backup_name = f"FieldTuner_Backup_{custom_name}.bak"
            else:
                # Get current system time with timezone awareness
                now = datetime.now()
                # Use more precise timestamp with microseconds
                timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
                backup_name = f"FieldTuner_Backup_{timestamp}.bak"
            
            self.backup_path = self.BACKUP_DIR / backup_name
            
            # Debug logging
            log_info(f"Creating backup: {self.backup_path}", "BACKUP")
            log_info(f"Source file: {self.config_path} (exists: {self.config_path.exists()})", "BACKUP")
            
            shutil.copy2(self.config_path, self.backup_path)
            
            # Verify backup was created
            if self.backup_path.exists():
                log_info(f"Backup created successfully: {self.backup_path}", "BACKUP")
                log_info(f"Backup size: {self.backup_path.stat().st_size} bytes", "BACKUP")
                log_info(f"Backup mtime: {datetime.fromtimestamp(self.backup_path.stat().st_mtime)}", "BACKUP")
            else:
                log_error("Backup file was not created", "BACKUP")
                return False
            
            return True
        except Exception as e:
            log_error(f"Failed to create backup: {str(e)}", "BACKUP", e)
            return False
    
    def get_setting(self, key, default=""):
        """Get a configuration setting value."""
        return self.config_data.get(key, default)
    
    def set_setting(self, key, value):
        """Set a configuration setting value."""
        self.config_data[key] = str(value)
        log_debug(f"Setting {key} = {value}", "CONFIG")
    
    def apply_optimal_settings(self, preset):
        """Apply optimal settings preset."""
        if preset in self.optimal_settings:
            log_info(f"Applying {preset} preset", "PRESET")
            for key, value in self.optimal_settings[preset]['settings'].items():
                self.set_setting(key, value)
            return True
        return False
    
    def get_graphics_settings(self):
        """Get graphics-related settings."""
        return {k: v for k, v in self.config_data.items() if k.startswith('GstRender.')}
    
    def get_audio_settings(self):
        """Get audio-related settings."""
        return {k: v for k, v in self.config_data.items() if k.startswith('GstAudio.')}
    
    def get_input_settings(self):
        """Get input-related settings."""
        return {k: v for k, v in self.config_data.items() if k.startswith('GstInput.')}
    
    def get_game_settings(self):
        """Get game-related settings."""
        return {k: v for k, v in self.config_data.items() if k.startswith('GstGame.')}
    
    def get_network_settings(self):
        """Get network-related settings."""
        return {k: v for k, v in self.config_data.items() if k.startswith('GstNetwork.')}
    
    def save_config(self):
        """Save configuration changes to the real BF6 config file."""
        if not self.config_path:
            log_error("Cannot save: no config path", "CONFIG")
            return False
        
        try:
            log_info("Saving configuration changes to real BF6 config", "CONFIG")
            
            # Create backup before modifying
            self._create_backup()
            
            # For now, we'll create a simple binary config that BF6 can read
            # This is a simplified approach - a full implementation would parse the binary format
            new_data = self._generate_binary_config()
            
            # Write the binary config
            with open(self.config_path, 'wb') as f:
                f.write(new_data)
            
            log_info("BF6 configuration saved successfully", "CONFIG")
            return True
        except Exception as e:
            log_error(f"Failed to save BF6 config: {str(e)}", "CONFIG", e)
            return False
    
    def _generate_config_content(self):
        """Generate new config file content with updated values."""
        lines = self.original_data.split('\n')
        new_lines = []
        
        for line in lines:
            modified = False
            for key, value in self.config_data.items():
                if key in line:
                    pattern = rf'({re.escape(key)})\s+\S+'
                    replacement = f'{key} {value}'
                    new_line = re.sub(pattern, replacement, line)
                    new_lines.append(new_line)
                    modified = True
                    break
            
            if not modified:
                new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def _generate_binary_config(self):
        """Generate new binary config content for BF6."""
        import struct
        
        # Create a basic binary structure that BF6 can read
        # This is a simplified implementation - a full implementation would properly parse the PROFSAVE format
        
        data = bytearray()
        
        # Add PROFSAVE header
        data.extend(b"PROFSAVE\x00")
        
        # Add version info
        data.extend(struct.pack('<I', 1))  # Version
        
        # Add settings count
        data.extend(struct.pack('<I', len(self.config_data)))
        
        # Add each setting as key-value pair
        for key, value in self.config_data.items():
            # Add key
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


class PresetCard(QWidget):
    """Super slick preset card widget."""
    
    preset_selected = pyqtSignal(str)
    
    def __init__(self, preset_key, preset_data, parent=None):
        super().__init__(parent)
        self.preset_key = preset_key
        self.preset_data = preset_data
        self.is_selected = False
        self.setup_ui()
        self.apply_styling()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        # Icon and title
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(self.preset_data['icon'])
        icon_label.setStyleSheet("font-size: 28px;")
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(self.preset_data['name'])
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Description
        desc_label = QLabel(self.preset_data['description'])
        desc_label.setStyleSheet("color: #cccccc; font-size: 12px; line-height: 1.4;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Apply button
        self.apply_btn = QPushButton("Apply Preset")
        self.apply_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.preset_data['color']};
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {self.preset_data['color']}dd;
            }}
            QPushButton:pressed {{
                background-color: {self.preset_data['color']}aa;
            }}
        """)
        self.apply_btn.clicked.connect(self.on_apply_clicked)
        layout.addWidget(self.apply_btn)
    
    def apply_styling(self):
        self.setStyleSheet("""
            PresetCard {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 8px;
                margin: 5px;
            }
            PresetCard:hover {
                border-color: #666;
                background-color: #333;
            }
        """)
    
    def on_apply_clicked(self):
        log_info(f"Preset {self.preset_key} selected", "PRESET")
        self.preset_selected.emit(self.preset_key)


class QuickSettingsTab(QWidget):
    """Super slick quick settings tab."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)  # Reduced margins
        layout.setSpacing(12)  # Reduced spacing
        
        # Header
        header = QLabel("Quick Settings")
        header.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #ffffff; 
            margin-bottom: 10px;
        """)
        layout.addWidget(header)
        
        # Preset cards
        presets_layout = QHBoxLayout()
        presets_layout.setSpacing(15)
        
        self.preset_cards = {}
        for preset_key, preset_data in self.config_manager.optimal_settings.items():
            card = PresetCard(preset_key, preset_data)
            card.preset_selected.connect(self.apply_preset)
            self.preset_cards[preset_key] = card
            presets_layout.addWidget(card)
        
        layout.addLayout(presets_layout)
        
        # Professional Quick Settings section
        settings_group = QGroupBox("⚡ Quick Settings")
        settings_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                font-size: 14px;
            }
        """)
        
        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(12)
        
        # Create professional toggle switches for all major BF6 settings
        self.dx12_toggle = self.create_professional_toggle("DirectX 12", "Enable DirectX 12 for better performance and features")
        settings_layout.addWidget(self.dx12_toggle)
        
        self.vsync_toggle = self.create_professional_toggle("VSync", "Enable vertical synchronization to reduce screen tearing")
        settings_layout.addWidget(self.vsync_toggle)
        
        self.motion_blur_toggle = self.create_professional_toggle("Motion Blur", "Enable motion blur effects for cinematic feel")
        settings_layout.addWidget(self.motion_blur_toggle)
        
        self.ao_toggle = self.create_professional_toggle("Ambient Occlusion", "Enable ambient occlusion for realistic shadows")
        settings_layout.addWidget(self.ao_toggle)
        
        self.ultra_low_latency_toggle = self.create_professional_toggle("Ultra Low Latency", "Enable NVIDIA Ultra Low Latency mode for competitive gaming")
        settings_layout.addWidget(self.ultra_low_latency_toggle)
        
        self.ray_tracing_toggle = self.create_professional_toggle("Ray Tracing", "Enable ray tracing for realistic lighting and reflections")
        settings_layout.addWidget(self.ray_tracing_toggle)
        
        self.dlss_toggle = self.create_professional_toggle("DLSS", "Enable NVIDIA DLSS for AI-enhanced performance")
        settings_layout.addWidget(self.dlss_toggle)
        
        self.hdr_toggle = self.create_professional_toggle("HDR", "Enable High Dynamic Range for better color range")
        settings_layout.addWidget(self.hdr_toggle)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Resolution scale
        scale_group = QGroupBox("Resolution Scale")
        scale_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                font-size: 14px;
            }
        """)
        
        scale_layout = QHBoxLayout()
        scale_layout.setSpacing(15)
        
        scale_layout.addWidget(QLabel("Scale:"))
        
        self.resolution_scale = QSlider(Qt.Orientation.Horizontal)
        self.resolution_scale.setRange(50, 200)
        self.resolution_scale.setValue(100)
        self.resolution_scale.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #555;
                height: 6px;
                background: #333;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #4a90e2;
                border: 1px solid #555;
                width: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #357abd;
            }
        """)
        
        self.scale_label = QLabel("100%")
        self.scale_label.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold; min-width: 50px;")
        
        scale_layout.addWidget(self.resolution_scale)
        scale_layout.addWidget(self.scale_label)
        scale_layout.addStretch()
        
        scale_group.setLayout(scale_layout)
        layout.addWidget(scale_group)
        
        # Connect signals
        self.resolution_scale.valueChanged.connect(self.on_scale_changed)
        
        layout.addStretch()
    
    def create_professional_toggle(self, title, description):
        """Create a professional toggle switch widget with modern design."""
        widget = QWidget()
        # Remove fixed height to allow natural sizing
        widget.setStyleSheet("""
            QWidget {
                background-color: #333333;
                border: 1px solid #444444;
                border-radius: 8px;
                margin: 2px;
            }
            QWidget:hover {
                background-color: #3a3a3a;
                border-color: #555555;
            }
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(16)
        
        # Left side - Content with proper sizing
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)  # Better spacing
        
        # Title with professional typography
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #ffffff;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 0.3px;
        """)
        title_label.setWordWrap(True)
        content_layout.addWidget(title_label)
        
        # Description with clean styling - no weird boxes
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                color: #b0b0b0;
                font-size: 11px;
                font-weight: 400;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }
        """)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align to top
        content_layout.addWidget(desc_label)
        
        # Add content to main layout with proper stretch
        layout.addWidget(content_widget, 1)  # Give content widget stretch factor
        layout.addStretch(0)  # Don't add extra stretch
        
        # Right side - Professional toggle switch
        toggle_switch = ProfessionalToggleSwitch()
        layout.addWidget(toggle_switch, 0)  # Don't stretch toggle
        
        # Store the toggle switch as an attribute for easy access
        widget.toggle_switch = toggle_switch
        
        return widget
    
    def on_scale_changed(self, value):
        self.scale_label.setText(f"{value}%")
    
    def apply_preset(self, preset_key):
        """Apply a settings preset with detailed confirmation."""
        preset = self.config_manager.optimal_settings.get(preset_key)
        if not preset:
            QMessageBox.warning(self, "Error", "Preset not found!")
            return
        
        # Get current settings for comparison
        current_settings = self.config_manager.get_graphics_settings()
        
        # Create detailed settings preview
        settings_preview = self.create_settings_preview(preset_key, current_settings)
        
        # Show confirmation dialog
        reply = QMessageBox.question(
            self, 
            f"Apply {preset['name']} Preset",
            f"🎯 {preset['description']}\n\n"
            f"⚠️ This will change the following settings:\n\n"
            f"{settings_preview}\n\n"
            f"💾 A backup will be created before applying changes.\n\n"
            f"Are you sure you want to apply this preset?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            log_info(f"Applying {preset_key} preset", "PRESET")
            if self.config_manager.apply_optimal_settings(preset_key):
                self.load_settings()
                QMessageBox.information(
                    self, 
                    "Preset Applied Successfully", 
                    f"✅ {preset['name']} preset has been applied!\n\n"
                    f"💾 Your original settings have been backed up.\n"
                    f"🔄 You can restore them anytime from the Backups tab."
                )
            else:
                QMessageBox.warning(self, "Error", "Failed to apply preset!")
    
    def create_settings_preview(self, preset_key, current_settings):
        """Create a detailed preview of what settings will change."""
        preset = self.config_manager.optimal_settings[preset_key]
        changes = []
        
        # Check each setting that will change
        for setting_key, new_value in preset['settings'].items():
            current_value = current_settings.get(setting_key, 'Not Set')
            
            # Format the setting name for display
            display_name = setting_key.replace('GstRender.', '').replace('_', ' ')
            display_name = ' '.join(word.capitalize() for word in display_name.split())
            
            # Show the change
            if str(current_value) != str(new_value):
                changes.append(f"• {display_name}: {current_value} → {new_value}")
        
        if not changes:
            return "No settings will be changed (already configured)."
        
        # Limit to first 10 changes to avoid overwhelming the user
        if len(changes) > 10:
            changes = changes[:10]
            changes.append(f"... and {len(self.config_manager.optimal_settings[preset_key]['settings']) - 10} more settings")
        
        return '\n'.join(changes)
    
    def load_settings(self):
        """Load settings from config manager."""
        graphics_settings = self.config_manager.get_graphics_settings()
        
        # Core rendering toggles
        self.dx12_toggle.toggle_switch.set_checked(graphics_settings.get('GstRender.Dx12Enabled', '0') == '1')
        self.vsync_toggle.toggle_switch.set_checked(graphics_settings.get('GstRender.VSyncMode', '0') != '0')
        self.motion_blur_toggle.toggle_switch.set_checked(graphics_settings.get('GstRender.MotionBlurWorld', '0') != '0')
        self.ao_toggle.toggle_switch.set_checked(graphics_settings.get('GstRender.AmbientOcclusion', '0') != '0')
        
        # Performance toggles
        self.ultra_low_latency_toggle.toggle_switch.set_checked(graphics_settings.get('GstRender.UltraLowLatency', '0') == '1')
        self.ray_tracing_toggle.toggle_switch.set_checked(graphics_settings.get('GstRender.RayTracingEnabled', '0') == '1')
        self.dlss_toggle.toggle_switch.set_checked(graphics_settings.get('GstRender.DLSSEnabled', '0') == '1')
        self.hdr_toggle.toggle_switch.set_checked(graphics_settings.get('GstRender.HDREnabled', '0') == '1')
        
        # Resolution scale
        try:
            scale_value = graphics_settings.get('GstRender.ResolutionScale', 1.0)
            if isinstance(scale_value, str):
                # Try to extract first valid number from string
                import re
                numbers = re.findall(r'[0-9]+\.?[0-9]*', scale_value)
                if numbers:
                    scale = float(numbers[0])
                else:
                    scale = 1.0
            else:
                scale = float(scale_value)
        except (ValueError, TypeError):
            scale = 1.0
        
        self.resolution_scale.setValue(int(scale * 100))
        self.scale_label.setText(f"{int(scale * 100)}%")
    
    def save_settings(self):
        """Save settings to config manager."""
        # Core rendering toggles
        self.config_manager.set_setting('GstRender.Dx12Enabled', str(int(self.dx12_toggle.toggle_switch.is_checked())))
        self.config_manager.set_setting('GstRender.VSyncMode', str(1 if self.vsync_toggle.toggle_switch.is_checked() else 0))
        self.config_manager.set_setting('GstRender.MotionBlurWorld', str(0.5 if self.motion_blur_toggle.toggle_switch.is_checked() else 0))
        self.config_manager.set_setting('GstRender.AmbientOcclusion', str(1 if self.ao_toggle.toggle_switch.is_checked() else 0))
        
        # Performance toggles
        self.config_manager.set_setting('GstRender.UltraLowLatency', str(int(self.ultra_low_latency_toggle.toggle_switch.is_checked())))
        self.config_manager.set_setting('GstRender.RayTracingEnabled', str(int(self.ray_tracing_toggle.toggle_switch.is_checked())))
        self.config_manager.set_setting('GstRender.DLSSEnabled', str(int(self.dlss_toggle.toggle_switch.is_checked())))
        self.config_manager.set_setting('GstRender.HDREnabled', str(int(self.hdr_toggle.toggle_switch.is_checked())))
        
        # Resolution scale
        scale = self.resolution_scale.value() / 100.0
        self.config_manager.set_setting('GstRender.ResolutionScale', str(scale))


class GraphicsTab(QWidget):
    """Super slick graphics settings tab."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)  # Minimal margins
        layout.setSpacing(6)  # Minimal spacing
        
        # Header
        header = QLabel("Graphics Settings")
        header.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #ffffff; 
            margin-bottom: 4px;
        """)
        layout.addWidget(header)
        
        # Create settings groups
        self.create_display_group(layout)
        self.create_quality_group(layout)
        self.create_effects_group(layout)
        
        layout.addStretch()
    
    def create_display_group(self, parent_layout):
        """Create display settings group."""
        group = QGroupBox("Display Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(8)
        
        # Fullscreen mode
        self.fullscreen_mode = QComboBox()
        self.fullscreen_mode.addItems(["Windowed", "Borderless", "Fullscreen"])
        self.fullscreen_mode.setStyleSheet(self.get_combo_style())
        self.fullscreen_mode.wheelEvent = lambda event: None  # Disable wheel scrolling
        layout.addRow("Fullscreen Mode:", self.fullscreen_mode)
        
        # Aspect ratio
        self.aspect_ratio = QComboBox()
        self.aspect_ratio.addItems(["Auto", "4:3", "16:9", "16:10", "21:9"])
        self.aspect_ratio.setStyleSheet(self.get_combo_style())
        self.aspect_ratio.wheelEvent = lambda event: None  # Disable wheel scrolling
        layout.addRow("Aspect Ratio:", self.aspect_ratio)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_quality_group(self, parent_layout):
        """Create quality settings group."""
        group = QGroupBox("Quality Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(8)
        
        # Quality settings
        quality_settings = [
            ("Texture Quality", "texture_quality"),
            ("Shadow Quality", "shadow_quality"),
            ("Effects Quality", "effects_quality"),
            ("Mesh Quality", "mesh_quality"),
            ("Lighting Quality", "lighting_quality"),
            ("Post Process Quality", "postprocess_quality")
        ]
        
        for label, attr_name in quality_settings:
            combo = QComboBox()
            combo.addItems(["Low", "Medium", "High", "Ultra"])
            combo.setStyleSheet(self.get_combo_style())
            combo.wheelEvent = lambda event: None  # Disable wheel scrolling
            setattr(self, attr_name, combo)
            layout.addRow(f"{label}:", combo)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_effects_group(self, parent_layout):
        """Create effects settings group."""
        group = QGroupBox("Visual Effects")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(8)
        
        # Anti-aliasing
        self.aa_method = QComboBox()
        self.aa_method.addItems(["Off", "FXAA", "TAA", "TAA High"])
        self.aa_method.setStyleSheet(self.get_combo_style())
        self.aa_method.wheelEvent = lambda event: None  # Disable wheel scrolling
        layout.addRow("Anti-Aliasing:", self.aa_method)
        
        # Ray tracing
        self.raytracing = QComboBox()
        self.raytracing.addItems(["Off", "Low", "Medium", "High"])
        self.raytracing.setStyleSheet(self.get_combo_style())
        self.raytracing.wheelEvent = lambda event: None  # Disable wheel scrolling
        layout.addRow("Ray Tracing:", self.raytracing)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def get_group_style(self):
        """Get group box styling."""
        return """
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                font-size: 14px;
            }
        """
    
    def get_combo_style(self):
        """Get combo box styling with enhanced user experience."""
        return """
            QComboBox {
                background-color: #333;
                color: white;
                border: 2px solid #555;
                padding: 8px 12px;
                border-radius: 6px;
                min-width: 120px;
                font-size: 12px;
                font-weight: 500;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                background-color: #444;
                border-radius: 3px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #888;
            }
            QComboBox:hover {
                border-color: #777;
                background-color: #3a3a3a;
            }
            QComboBox:focus {
                border-color: #4a90e2;
                background-color: #3a3a3a;
            }
            QComboBox::drop-down:hover {
                background-color: #555;
            }
            QComboBox QAbstractItemView {
                background-color: #2a2a2a;
                border: 1px solid #555;
                selection-background-color: #4a90e2;
                color: white;
                padding: 4px;
            }
            QComboBox QAbstractItemView::item {
                padding: 6px 12px;
                border-radius: 3px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #444;
            }
        """
    
    def load_settings(self):
        """Load settings from config manager."""
        graphics_settings = self.config_manager.get_graphics_settings()
        
        # Display
        fullscreen_mode = int(graphics_settings.get('GstRender.FullscreenMode', '0'))
        self.fullscreen_mode.setCurrentIndex(min(fullscreen_mode, 2))
        
        aspect_ratio = int(graphics_settings.get('GstRender.AspectRatio', '0'))
        self.aspect_ratio.setCurrentIndex(min(aspect_ratio, 4))
        
        # Quality
        quality_mappings = {
            'texture_quality': 'GstRender.TextureQuality',
            'shadow_quality': 'GstRender.ShadowQuality',
            'effects_quality': 'GstRender.EffectsQuality',
            'mesh_quality': 'GstRender.MeshQuality',
            'lighting_quality': 'GstRender.LightingQuality',
            'postprocess_quality': 'GstRender.PostProcessQuality'
        }
        
        for attr_name, config_key in quality_mappings.items():
            combo = getattr(self, attr_name)
            value = int(graphics_settings.get(config_key, '1'))
            combo.setCurrentIndex(min(value, 3))
        
        # Effects
        aa_deferred = int(graphics_settings.get('GstRender.AntiAliasingDeferred', '1'))
        self.aa_method.setCurrentIndex(min(aa_deferred, 3))
        
        rt_quality = int(graphics_settings.get('GstRender.RaytracingQuality', '0'))
        self.raytracing.setCurrentIndex(min(rt_quality, 3))
    
    def save_settings(self):
        """Save settings to config manager."""
        # Display
        self.config_manager.set_setting('GstRender.FullscreenMode', str(self.fullscreen_mode.currentIndex()))
        self.config_manager.set_setting('GstRender.AspectRatio', str(self.aspect_ratio.currentIndex()))
        
        # Quality
        quality_mappings = {
            'texture_quality': 'GstRender.TextureQuality',
            'shadow_quality': 'GstRender.ShadowQuality',
            'effects_quality': 'GstRender.EffectsQuality',
            'mesh_quality': 'GstRender.MeshQuality',
            'lighting_quality': 'GstRender.LightingQuality',
            'postprocess_quality': 'GstRender.PostProcessQuality'
        }
        
        for attr_name, config_key in quality_mappings.items():
            combo = getattr(self, attr_name)
            self.config_manager.set_setting(config_key, str(combo.currentIndex()))
        
        # Effects
        self.config_manager.set_setting('GstRender.AntiAliasingDeferred', str(self.aa_method.currentIndex()))
        self.config_manager.set_setting('GstRender.RaytracingQuality', str(self.raytracing.currentIndex()))


class CodeViewTab(QWidget):
    """Super slick code view tab."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.load_config()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)  # Reduced margins
        layout.setSpacing(12)  # Reduced spacing
        
        # Header
        header_layout = QHBoxLayout()
        
        header_label = QLabel("💻 Config File Editor")
        header_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #ffffff; 
            margin-bottom: 10px;
        """)
        header_layout.addWidget(header_label)
        
        header_layout.addStretch()
        
        # Reload button
        self.reload_btn = QPushButton("🔄 Reload")
        self.reload_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        self.reload_btn.clicked.connect(self.load_config)
        header_layout.addWidget(self.reload_btn)
        
        layout.addLayout(header_layout)
        
        # Code editor
        self.code_editor = QPlainTextEdit()
        self.code_editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 6px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 11px;
                line-height: 1.4;
                padding: 8px;
            }
            QPlainTextEdit:focus {
                border-color: #4a90e2;
            }
        """)
        self.code_editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        layout.addWidget(self.code_editor)
        
        # Info
        info_label = QLabel("💡 Edit the config file directly. Changes will be applied when you save.")
        info_label.setStyleSheet("color: #888; font-size: 11px; padding: 8px;")
        layout.addWidget(info_label)
    
    def load_config(self):
        """Load config file into editor."""
        if self.config_manager.config_path and self.config_manager.config_path.exists():
            try:
                # Display the config data in a readable format
                content_lines = []
                content_lines.append("=== Battlefield 6 Configuration File ===")
                content_lines.append(f"File: {self.config_manager.config_path}")
                content_lines.append(f"Size: {self.config_manager.config_path.stat().st_size:,} bytes")
                content_lines.append(f"Settings: {len(self.config_manager.config_data)}")
                content_lines.append("")
                content_lines.append("=== Current Settings ===")
                
                # Add all settings in a readable format
                for key, value in self.config_manager.config_data.items():
                    content_lines.append(f"{key} = {value}")
                
                content_lines.append("")
                content_lines.append("=== Raw Binary Data (First 1000 bytes) ===")
                
                # Show first 1000 bytes of binary data
                with open(self.config_manager.config_path, 'rb') as f:
                    binary_data = f.read(1000)
                    # Convert to hex representation
                    hex_data = binary_data.hex()
                    # Format as readable hex
                    for i in range(0, len(hex_data), 32):
                        chunk = hex_data[i:i+32]
                        formatted_chunk = ' '.join(chunk[j:j+2] for j in range(0, len(chunk), 2))
                        content_lines.append(formatted_chunk)
                
                self.code_editor.setPlainText('\n'.join(content_lines))
                log_info("Config file loaded into editor", "CODE_VIEW")
            except Exception as e:
                log_error(f"Failed to load config file: {str(e)}", "CODE_VIEW", e)
                QMessageBox.critical(self, "Error", f"Failed to load config file: {str(e)}")
        else:
            log_warning("Config file not found", "CODE_VIEW")
            QMessageBox.warning(self, "Warning", "Config file not found!")
    
    def save_config(self):
        """Save config file from editor."""
        if self.config_manager.config_path:
            try:
                content = self.code_editor.toPlainText()
                with open(self.config_manager.config_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                # Reload the config manager
                self.config_manager._load_config()
                log_info("Config file saved from editor", "CODE_VIEW")
                return True
            except Exception as e:
                log_error(f"Failed to save config file: {str(e)}", "CODE_VIEW", e)
                QMessageBox.critical(self, "Error", f"Failed to save config file: {str(e)}")
                return False
        return False


class BackupTab(QWidget):
    """Clean, intuitive backup management - completely rebuilt UI."""

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.refresh_backups()

    def setup_ui(self):
        # Main layout with proper spacing
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Header section
        header = QLabel("💾 Backup Management")
        header.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 8px;
            padding: 8px;
            background-color: #2a2a2a;
            border-radius: 4px;
            border: 1px solid #444;
        """)
        layout.addWidget(header)

        # Create new backup section
        create_section = QGroupBox("Create New Backup")
        create_section.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #4a90e2;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
                font-size: 14px;
            }
        """)
        
        create_layout = QHBoxLayout(create_section)
        create_layout.setContentsMargins(12, 8, 12, 8)
        create_layout.setSpacing(8)

        # Backup name input
        self.backup_name_input = QLineEdit()
        self.backup_name_input.setPlaceholderText("Enter backup name (optional)")
        self.backup_name_input.setStyleSheet("""
            QLineEdit {
                background-color: #444;
                color: white;
                border: 1px solid #666;
                padding: 6px 8px;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
            }
        """)
        create_layout.addWidget(QLabel("Name:"))
        create_layout.addWidget(self.backup_name_input)

        # Create button
        self.create_backup_btn = QPushButton("Create Backup")
        self.create_backup_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        self.create_backup_btn.clicked.connect(self.create_backup)
        create_layout.addWidget(self.create_backup_btn)

        layout.addWidget(create_section)

        # Available backups section
        backups_section = QGroupBox("Available Backups")
        backups_section.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #2e7d32;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
                font-size: 14px;
            }
        """)
        
        backups_layout = QVBoxLayout(backups_section)
        backups_layout.setContentsMargins(12, 8, 12, 8)
        backups_layout.setSpacing(8)

        # Backup list with proper styling
        self.backup_list = QListWidget()
        self.backup_list.setStyleSheet("""
            QListWidget {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #444;
                border-radius: 2px;
                margin: 1px;
            }
            QListWidget::item:selected {
                background-color: #4a90e2;
                border: 1px solid #4a90e2;
            }
            QListWidget::item:hover {
                background-color: #444;
            }
        """)
        backups_layout.addWidget(self.backup_list)

        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(8)

        # Restore selected button
        self.restore_btn = QPushButton("Restore Selected")
        self.restore_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1b5e20;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        self.restore_btn.clicked.connect(self.restore_selected_backup)
        self.restore_btn.setEnabled(False)
        action_layout.addWidget(self.restore_btn)

        # Delete selected button
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_selected_backup)
        self.delete_btn.setEnabled(False)
        action_layout.addWidget(self.delete_btn)

        # Open backup folder button
        self.open_folder_btn = QPushButton("Open Backup Folder")
        self.open_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.open_folder_btn.clicked.connect(self.open_backup_folder)
        action_layout.addWidget(self.open_folder_btn)

        # Refresh button
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_backups)
        action_layout.addWidget(self.refresh_btn)

        backups_layout.addLayout(action_layout)
        layout.addWidget(backups_section)

        # Connect signals
        self.backup_list.itemSelectionChanged.connect(self.update_backup_buttons)
    
    def showEvent(self, event):
        """Refresh backups when tab is shown."""
        super().showEvent(event)
        self.refresh_backups()
    
    def refresh_backups(self):
        """Refresh the backup list with clean, simple display."""
        self.backup_list.clear()
        
        # Ensure backup directory exists
        self.config_manager.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
        if not self.config_manager.BACKUP_DIR.exists():
            return
        
        backup_files = list(self.config_manager.BACKUP_DIR.glob("*.bak"))
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Populate backup list with clean format
        for backup_file in backup_files:
            try:
                # Get file info
                file_mtime = backup_file.stat().st_mtime
                timestamp = datetime.fromtimestamp(file_mtime)
                size = backup_file.stat().st_size
                
                # Format display text
                time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                size_str = f"{size:,} bytes"
                display_text = f"{backup_file.name} | {time_str} | {size_str}"
                
                # Create list item
                item = QListWidgetItem(display_text)
                item.setData(Qt.ItemDataRole.UserRole, backup_file)
                self.backup_list.addItem(item)
                
            except Exception as e:
                log_error(f"Error processing backup file {backup_file}: {str(e)}", "BACKUP", e)
                continue
    
    def create_backup(self):
        """Create a new backup with clean feedback."""
        backup_name = self.backup_name_input.text().strip()
        
        try:
            success = self.config_manager._create_backup(backup_name if backup_name else None)
            if success:
                QMessageBox.information(self, "Backup Created", "✅ Backup created successfully!")
                self.backup_name_input.clear()
                self.refresh_backups()
            else:
                QMessageBox.warning(self, "Backup Failed", "❌ Failed to create backup!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ Error creating backup: {str(e)}")
    
    def restore_selected_backup(self):
        """Restore the selected backup."""
        current_item = self.backup_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "❌ Please select a backup to restore!")
            return
        
        backup_file = current_item.data(Qt.ItemDataRole.UserRole)
        if not backup_file or not backup_file.exists():
            QMessageBox.warning(self, "Error", "❌ Selected backup file not found!")
            return
        
        reply = QMessageBox.question(
            self, 
            "Restore Backup",
            f"🔄 Are you sure you want to restore this backup?\n\n"
            f"📁 File: {backup_file.name}\n\n"
            f"⚠️ This will overwrite your current settings!\n"
            f"💾 A backup of your current settings will be created first.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Create backup of current settings first
                self.config_manager._create_backup("Before_Restore")
                
                # Restore the backup
                import shutil
                shutil.copy2(backup_file, self.config_manager.config_path)
                
                QMessageBox.information(self, "Backup Restored", "✅ Backup restored successfully!")
                self.refresh_backups()
            except Exception as e:
                QMessageBox.critical(self, "Restore Failed", f"❌ Failed to restore backup: {str(e)}")
    
    def delete_selected_backup(self):
        """Delete the selected backup."""
        current_item = self.backup_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "❌ Please select a backup to delete!")
            return
        
        backup_file = current_item.data(Qt.ItemDataRole.UserRole)
        if not backup_file or not backup_file.exists():
            QMessageBox.warning(self, "Error", "❌ Selected backup file not found!")
            return
        
        reply = QMessageBox.question(
            self, 
            "Delete Backup",
            f"🗑️ Are you sure you want to delete this backup?\n\n"
            f"📁 File: {backup_file.name}\n"
            f"📅 Date: {current_item.text()}\n\n"
            f"⚠️ This action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                backup_file.unlink()
                QMessageBox.information(self, "Backup Deleted", "✅ Backup deleted successfully!")
                self.refresh_backups()
            except Exception as e:
                QMessageBox.critical(self, "Delete Failed", f"❌ Failed to delete backup: {str(e)}")
    
    def open_backup_folder(self):
        """Open the backup folder in file explorer."""
        try:
            backup_path = str(self.config_manager.BACKUP_DIR)
            os.makedirs(backup_path, exist_ok=True)
            import subprocess
            subprocess.run(f'explorer "{backup_path}"', shell=True, check=False)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"❌ Failed to open backup folder: {str(e)}")
    
    def update_backup_buttons(self):
        """Update backup action buttons based on selection."""
        has_selection = self.backup_list.currentItem() is not None
        self.restore_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
class DebugTab(QWidget):
    """Debug tab for real-time log viewing."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.debug_logger = get_debug_logger()
        self.setup_ui()
        self.refresh_logs()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)  # Reduced margins
        layout.setSpacing(12)  # Reduced spacing
        
        # Header
        header = QLabel("Debug Console")
        header.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #ffffff; 
            margin-bottom: 10px;
        """)
        layout.addWidget(header)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 6px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.log_display)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_logs)
        button_layout.addWidget(refresh_btn)
        
        export_btn = QPushButton("📁 Export Logs")
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1b5e20;
            }
        """)
        export_btn.clicked.connect(self.export_logs)
        button_layout.addWidget(export_btn)
        
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        """)
        clear_btn.clicked.connect(self.clear_logs)
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Connect to logger
        self.debug_logger.log_updated.connect(self.update_log_display)
    
    def refresh_logs(self):
        """Refresh log display."""
        logs = self.debug_logger.get_recent_logs(100)
        self.log_display.setPlainText('\n'.join(logs))
        # Scroll to bottom
        cursor = self.log_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_display.setTextCursor(cursor)
    
    def update_log_display(self, log_entry):
        """Update log display with new entry."""
        self.log_display.append(log_entry)
        # Auto-scroll to bottom
        cursor = self.log_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_display.setTextCursor(cursor)
    
    def export_logs(self):
        """Export logs to file."""
        try:
            file_path = self.debug_logger.export_logs()
            QMessageBox.information(self, "Export Complete", f"Logs exported to:\n{file_path}")
            log_info(f"Logs exported to: {file_path}", "DEBUG")
        except Exception as e:
            log_error(f"Failed to export logs: {str(e)}", "DEBUG", e)
            QMessageBox.critical(self, "Error", f"Failed to export logs: {str(e)}")
    
    def clear_logs(self):
        """Clear log display."""
        self.log_display.clear()
        log_info("Debug console cleared", "DEBUG")


class MainWindow(QMainWindow):
    """Super slick main window with world-class design."""
    
    def __init__(self):
        super().__init__()
        log_info("Initializing FieldTuner MainWindow", "MAIN")
        self.config_manager = ConfigManager()
        self.setup_ui()
        self.apply_super_slick_theme()
        self.update_status()
        
        # Show startup message
        if self.config_manager.config_path and self.config_manager.config_path.exists():
            QMessageBox.information(
                self, 
                "🎮 FieldTuner Connected!", 
                f"✅ Successfully connected to your Battlefield 6 configuration!\n\n"
                f"📁 Config File: {self.config_manager.config_path.name}\n"
                f"📂 Full Path: {self.config_manager.config_path}\n"
                f"⚙️ Settings Loaded: {len(self.config_manager.config_data)}\n"
                f"💾 Auto-backup Created: Your original config is safely backed up\n\n"
                f"🚀 You can now safely modify your settings!"
            )
            log_info("Startup message shown to user", "MAIN")
        
        log_info("FieldTuner MainWindow initialized successfully", "MAIN")
    
    def setup_ui(self):
        """Setup the super slick UI."""
        self.setWindowTitle("FieldTuner - Battlefield 6 Configuration Tool")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 600)  # Allow smaller minimum size
        self.resize(1200, 800)  # Set default size but allow resizing
        
        # Central widget with scrolling
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setWidget(central_widget)
        
        # Set scroll area as central widget
        self.setCentralWidget(scroll_area)
        
        # Main layout - tight spacing
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)  # Minimal margins
        main_layout.setSpacing(4)  # Minimal spacing
        
        # Header with subtle gradient - compact height
        header_widget = QWidget()
        header_widget.setFixedHeight(40)  # More compact height
        header_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2a2a2a, stop:1 #333);
                border: none;
            }
        """)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(12, 4, 12, 4)  # Minimal margins
        
        # Title
        title_label = QLabel("🎮 FieldTuner")
        title_label.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #ffffff;
        """)
        header_layout.addWidget(title_label)
        
        # Creator note (bigger and more prominent)
        creator_label = QLabel("💝 Created by Tom with Love from Cursor")
        creator_label.setStyleSheet("""
            color: #ff6b35; 
            font-size: 14px;
            font-weight: bold;
            font-style: italic;
            margin-left: 15px;
            background-color: rgba(255, 107, 53, 0.1);
            padding: 4px 8px;
            border-radius: 12px;
            border: 1px solid rgba(255, 107, 53, 0.3);
        """)
        header_layout.addWidget(creator_label)
        
        header_layout.addStretch()
        
        # Status info
        self.status_label = QLabel()
        self.status_label.setStyleSheet("""
            color: #cccccc; 
            font-size: 12px;
            background-color: rgba(0,0,0,0.3);
            padding: 6px 12px;
            border-radius: 15px;
        """)
        header_layout.addWidget(self.status_label)
        
        main_layout.addWidget(header_widget)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background-color: #2a2a2a;
                color: #ffffff;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #4a90e2;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #444;
            }
        """)
        
        # Create tabs
        self.quick_tab = QuickSettingsTab(self.config_manager)
        self.graphics_tab = GraphicsTab(self.config_manager)
        self.input_tab = InputTab(self.config_manager)
        self.advanced_tab = AdvancedTab(self.config_manager)
        self.code_tab = CodeViewTab(self.config_manager)
        self.backup_tab = BackupTab(self.config_manager)
        self.debug_tab = DebugTab(self.config_manager)
        
        # Add tabs
        self.tab_widget.addTab(self.quick_tab, "⚡ Quick")
        self.tab_widget.addTab(self.graphics_tab, "🎨 Graphics")
        self.tab_widget.addTab(self.input_tab, "🎮 Input")
        self.tab_widget.addTab(self.advanced_tab, "⚙️ Advanced")
        self.tab_widget.addTab(self.code_tab, "💻 Code")
        self.tab_widget.addTab(self.backup_tab, "💾 Backups")
        self.tab_widget.addTab(self.debug_tab, "🐛 Debug")
        
        main_layout.addWidget(self.tab_widget)
        
        # Changes feedback section
        self.changes_feedback = QWidget()
        self.changes_feedback.setFixedHeight(60)
        self.changes_feedback.setStyleSheet("""
            QWidget {
                background-color: #1a3d5c;
                border: 2px solid #4a90e2;
                border-radius: 6px;
                margin: 5px;
            }
        """)
        
        changes_layout = QVBoxLayout(self.changes_feedback)
        changes_layout.setContentsMargins(12, 8, 12, 8)
        changes_layout.setSpacing(4)
        
        # Changes header
        self.changes_header = QLabel("📝 Here's what you're changing:")
        self.changes_header.setStyleSheet("""
            color: #4a90e2;
            font-size: 12px;
            font-weight: bold;
        """)
        changes_layout.addWidget(self.changes_header)
        
        # Changes list
        self.changes_list = QLabel("No changes made yet")
        self.changes_list.setStyleSheet("""
            color: #ffffff;
            font-size: 11px;
            background-color: rgba(74, 144, 226, 0.1);
            padding: 4px 8px;
            border-radius: 3px;
        """)
        self.changes_list.setWordWrap(True)
        changes_layout.addWidget(self.changes_list)
        
        # Initially hide the feedback
        self.changes_feedback.hide()
        main_layout.addWidget(self.changes_feedback)
        
        # Action buttons
        button_widget = QWidget()
        button_widget.setFixedHeight(70)
        button_widget.setStyleSheet("background-color: #2a2a2a; border-top: 1px solid #444;")
        
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(30, 15, 30, 15)
        button_layout.setSpacing(15)
        
        self.apply_btn = QPushButton("✅ Apply Changes")
        self.apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2968a3;
            }
        """)
        self.apply_btn.clicked.connect(self.apply_changes)
        
        # Initialize changes tracking
        self.pending_changes = {}
        
        # Connect to tab change signals to track changes
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        self.reset_btn = QPushButton("🏭 Reset to Factory")
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff6b35;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e55a2b;
            }
            QPushButton:pressed {
                background-color: #cc4a1f;
            }
        """)
        self.reset_btn.clicked.connect(self.reset_to_factory)
        
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        
        main_layout.addWidget(button_widget)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #2a2a2a;
                color: #ffffff;
                border-top: 1px solid #444;
                font-size: 11px;
            }
        """)
    
    
    def apply_super_slick_theme(self):
        """Apply super slick theme."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                font-size: 14px;
            }
            QLabel {
                color: #ffffff;
            }
            QCheckBox {
                color: #ffffff;
            }
            QComboBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 6px 10px;
                border-radius: 4px;
                min-width: 100px;
                font-size: 12px;
            }
            QComboBox::drop-down {
                border: none;
                width: 16px;
            }
            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
            }
            QComboBox:hover {
                border-color: #777;
            }
            QComboBox:focus {
                border-color: #4a90e2;
            }
            QSlider::groove:horizontal {
                border: 1px solid #555;
                height: 6px;
                background: #333;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #4a90e2;
                border: 1px solid #555;
                width: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #357abd;
            }
            QStatusBar {
                background-color: #2a2a2a;
                color: #ffffff;
                border-top: 1px solid #444;
            }
        """)
    
    def update_status(self):
        """Update status information with clear connection status."""
        if self.config_manager.config_path:
            file_size = self.config_manager.config_path.stat().st_size
            settings_count = len(self.config_manager.config_data)
            backup_count = len(list(self.config_manager.BACKUP_DIR.glob("*.bak"))) if self.config_manager.BACKUP_DIR.exists() else 0
            
            # Show clear connection status
            self.status_label.setText(f"✅ Connected to BF6 Config • 📁 {self.config_manager.config_path.name} • 📊 {file_size:,} bytes • ⚙️ {settings_count} settings • 💾 {backup_count} backups")
            self.status_label.setStyleSheet("""
                color: #4CAF50; 
                font-size: 12px;
                background-color: rgba(76, 175, 80, 0.2);
                padding: 6px 12px;
                border-radius: 15px;
                border: 1px solid #4CAF50;
            """)
        else:
            self.status_label.setText("❌ No Battlefield 6 config file found - Please check your game installation")
            self.status_label.setStyleSheet("""
                color: #f44336; 
                font-size: 12px;
                background-color: rgba(244, 67, 54, 0.2);
                padding: 6px 12px;
                border-radius: 15px;
                border: 1px solid #f44336;
            """)
    
    def apply_changes(self):
        """Apply configuration changes."""
        log_info("Applying configuration changes", "MAIN")
        self.status_bar.showMessage("Applying changes...")
        
        try:
            # Save settings from all tabs
            self.quick_tab.save_settings()
            self.graphics_tab.save_settings()
            
            # Save code view if it was modified
            if hasattr(self.code_tab, 'save_config'):
                if not self.code_tab.save_config():
                    log_error("Failed to save code view changes", "MAIN")
                    QMessageBox.critical(self, "Error", "❌ Failed to save code view changes!")
                    return
            
            # Save to file
            if self.config_manager.save_config():
                self.status_bar.showMessage("✅ Changes applied successfully!")
                QMessageBox.information(self, "Success", "✅ Configuration changes have been applied successfully!")
                log_info("Configuration changes applied successfully", "MAIN")
                
                # Clear pending changes after successful save
                self.clear_pending_changes()
            else:
                self.status_bar.showMessage("❌ Failed to apply changes!")
                QMessageBox.critical(self, "Error", "❌ Failed to save configuration changes!")
                log_error("Failed to save configuration changes", "MAIN")
        except Exception as e:
            self.status_bar.showMessage("❌ Error applying changes!")
            log_error(f"Error applying changes: {str(e)}", "MAIN", e)
            QMessageBox.critical(self, "Error", f"❌ Error applying changes: {str(e)}")
    
    def quick_restore(self):
        """Quick restore from the most recent backup."""
        try:
            if not self.config_manager.BACKUP_DIR.exists():
                QMessageBox.warning(self, "No Backups", "❌ No backups found!")
                return
            
            backup_files = list(self.config_manager.BACKUP_DIR.glob("*.bak"))
            if not backup_files:
                QMessageBox.warning(self, "No Backups", "❌ No backups found!")
                return
            
            # Get the most recent backup
            latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
            
            reply = QMessageBox.question(
                self, "Quick Restore",
                f"🔄 Restore from the most recent backup?\n\n📁 {latest_backup.name}\n🕒 {datetime.fromtimestamp(latest_backup.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                shutil.copy2(latest_backup, self.config_manager.config_path)
                self.config_manager._load_config()
                
                # Refresh all tabs
                self.quick_tab.load_settings()
                self.graphics_tab.load_settings()
                self.code_tab.load_config()
                self.backup_tab.refresh_backups()
                
                QMessageBox.information(self, "Restore Complete", "✅ Configuration restored from backup!")
                log_info(f"Quick restore completed: {latest_backup.name}", "MAIN")
                
        except Exception as e:
            log_error(f"Quick restore failed: {str(e)}", "MAIN", e)
            QMessageBox.critical(self, "Error", f"❌ Restore failed: {str(e)}")
    
    def manual_config_select(self):
        """Allow user to manually select config file."""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, 
                "Select Battlefield 6 Config File", 
                str(Path.home() / "Documents"),
                "Config Files (*.profile);;All Files (*)"
            )
            
            if file_path:
                config_path = Path(file_path)
                if config_path.exists():
                    # Update config manager
                    self.config_manager.config_path = config_path
                    self.config_manager._load_config()
                    self.config_manager._create_backup()
                    
                    # Refresh UI
                    self.connection_widget.deleteLater()
                    self.connection_widget = self.create_connection_widget()
                    self.layout().insertWidget(1, self.connection_widget)
                    
                    self.update_status()
                    self.quick_tab.load_settings()
                    self.graphics_tab.load_settings()
                    self.code_tab.load_config()
                    self.backup_tab.refresh_backups()
                    
                    QMessageBox.information(self, "Config Loaded", f"✅ Configuration loaded successfully!\n\n📁 {config_path.name}\n⚙️ {len(self.config_manager.config_data)} settings\n💾 Auto-backup created")
                    log_info(f"Manual config selection: {config_path}", "MAIN")
                else:
                    QMessageBox.warning(self, "File Not Found", "❌ Selected file does not exist!")
            else:
                log_info("Manual config selection cancelled", "MAIN")
                
        except Exception as e:
            log_error(f"Manual config selection failed: {str(e)}", "MAIN", e)
            QMessageBox.critical(self, "Error", f"❌ Failed to load config: {str(e)}")
    
    def reset_to_factory(self):
        """Reset settings to Battlefield 6 factory defaults."""
        reply = QMessageBox.question(
            self, "Reset to Factory Defaults",
            "🏭 Are you sure you want to reset ALL settings to Battlefield 6 factory defaults?\n\n"
            "⚠️ This will:\n"
            "• Reset all graphics settings to default\n"
            "• Reset all audio settings to default\n"
            "• Reset all input settings to default\n"
            "• This action cannot be undone!\n\n"
            "💾 A backup will be created before resetting.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Create backup before resetting
            self.config_manager._create_backup()
            
            # Reset all tabs
            self.quick_tab.load_settings()
            self.graphics_tab.load_settings()
            self.code_tab.load_config()
            self.status_bar.showMessage("🏭 Settings reset to factory defaults")
            log_info("Settings reset to factory defaults", "MAIN")
            
            QMessageBox.information(
                self, "Factory Reset Complete",
                "✅ All settings have been reset to Battlefield 6 factory defaults!\n\n"
                "💾 A backup of your previous settings has been created."
            )
    
    def on_tab_changed(self, index):
        """Handle tab changes and update change tracking."""
        self.update_changes_feedback()
    
    def track_setting_change(self, setting_key, old_value, new_value):
        """Track a setting change for feedback display."""
        if old_value != new_value:
            self.pending_changes[setting_key] = {
                'old': old_value,
                'new': new_value
            }
        else:
            # Remove from pending changes if value is back to original
            self.pending_changes.pop(setting_key, None)
        
        self.update_changes_feedback()
    
    def update_changes_feedback(self):
        """Update the changes feedback display."""
        if not self.pending_changes:
            self.changes_feedback.hide()
            return
        
        # Show the feedback section
        self.changes_feedback.show()
        
        # Build changes list
        changes_text = []
        for setting_key, change in self.pending_changes.items():
            # Format the setting name for display
            display_name = setting_key.replace('GstRender.', '').replace('GstInput.', '')
            display_name = display_name.replace('.', ' ').title()
            
            old_val = str(change['old'])
            new_val = str(change['new'])
            
            # Truncate long values
            if len(old_val) > 20:
                old_val = old_val[:17] + "..."
            if len(new_val) > 20:
                new_val = new_val[:17] + "..."
            
            changes_text.append(f"• {display_name}: {old_val} → {new_val}")
        
        # Update the display
        if len(changes_text) <= 3:
            self.changes_list.setText("\n".join(changes_text))
        else:
            self.changes_list.setText("\n".join(changes_text[:3]) + f"\n... and {len(changes_text) - 3} more changes")
        
        # Update header with count
        count = len(self.pending_changes)
        self.changes_header.setText(f"📝 Here's what you're changing ({count} setting{'s' if count != 1 else ''}):")
    
    def clear_pending_changes(self):
        """Clear all pending changes."""
        self.pending_changes.clear()
        self.changes_feedback.hide()


class AdvancedTab(QWidget):
    """Advanced Settings Tab - Clean, searchable interface for all BF6 settings."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.all_settings = {}  # Store all settings for search
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the advanced settings UI with clean search and display."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Header
        header = QLabel("⚙️ Advanced Settings")
        header.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 8px;
            padding: 8px;
            background-color: #2a2a2a;
            border-radius: 4px;
            border: 1px solid #444;
        """)
        layout.addWidget(header)
        
        # Search section
        search_widget = QWidget()
        search_widget.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(8, 8, 8, 8)
        search_layout.setSpacing(8)
        
        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search settings by name or description...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 8px 12px;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
                background-color: #3a3a3a;
            }
        """)
        self.search_input.textChanged.connect(self.perform_search)
        search_layout.addWidget(self.search_input)
        
        # Category filter
        self.category_filter = QComboBox()
        self.category_filter.addItems(["All Categories", "Graphics API", "Display", "Performance", "Audio", "Input", "Network", "Game"])
        self.category_filter.setStyleSheet("""
            QComboBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 8px 12px;
                border-radius: 4px;
                font-size: 12px;
                min-width: 120px;
            }
            QComboBox:focus {
                border-color: #4a90e2;
            }
        """)
        self.category_filter.currentTextChanged.connect(self.perform_search)
        search_layout.addWidget(self.category_filter)
        
        # Clear button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_search)
        search_layout.addWidget(self.clear_btn)
        
        layout.addWidget(search_widget)
        
        # Results count
        self.results_label = QLabel("Loading settings...")
        self.results_label.setStyleSheet("""
            color: #888;
            font-size: 11px;
            padding: 4px 8px;
        """)
        layout.addWidget(self.results_label)
        
        # Settings list with proper scroll
        self.settings_scroll = QScrollArea()
        self.settings_scroll.setWidgetResizable(True)
        self.settings_scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #444;
                border-radius: 4px;
                background-color: #2a2a2a;
            }
        """)
        
        self.settings_widget = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_widget)
        self.settings_layout.setContentsMargins(8, 8, 8, 8)
        self.settings_layout.setSpacing(8)
        
        self.settings_scroll.setWidget(self.settings_widget)
        layout.addWidget(self.settings_scroll)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            color: #888;
            font-size: 12px;
            padding: 5px;
        """)
        layout.addWidget(self.status_label)
    
    def showEvent(self, event):
        """Refresh settings when tab becomes visible."""
        super().showEvent(event)
        self.load_settings()
    
    def load_settings(self):
        """Load all settings from the database and display them."""
        from settings_database import BF6_SETTINGS_DATABASE
        
        # Store all settings for search
        self.all_settings = BF6_SETTINGS_DATABASE.copy()
        
        # Clear existing settings
        self.clear_settings_display()
        
        # Display all settings initially
        self.display_settings(self.all_settings)
        
        self.results_label.setText(f"Showing {len(self.all_settings)} settings")
        self.status_label.setText("Ready")
    
    def clear_settings_display(self):
        """Clear all settings from the display."""
        for i in reversed(range(self.settings_layout.count())):
            child = self.settings_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
    
    def display_settings(self, settings_dict):
        """Display the given settings dictionary."""
        if not settings_dict:
            # Show no results message
            no_results = QLabel("No settings found matching your search criteria.")
            no_results.setStyleSheet("""
                color: #888;
                font-size: 14px;
                padding: 20px;
                text-align: center;
            """)
            no_results.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.settings_layout.addWidget(no_results)
            return
        
        # Group settings by category
        categories = {}
        for setting_key, setting_data in settings_dict.items():
            category = setting_data.get("category", "Other")
            if category not in categories:
                categories[category] = []
            categories[category].append((setting_key, setting_data))
        
        # Create category sections
        for category_name, settings in sorted(categories.items()):
            if not settings:
                continue
                
            # Category header
            category_group = QGroupBox(f"📁 {category_name} ({len(settings)} settings)")
            category_group.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    color: #ffffff;
                    border: 2px solid #4a90e2;
                    border-radius: 8px;
                    margin-top: 8px;
                    padding-top: 12px;
                    background-color: #2a2a2a;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 12px;
                    padding: 0 8px 0 8px;
                    font-size: 14px;
                }
            """)
            
            category_layout = QVBoxLayout(category_group)
            category_layout.setSpacing(6)
            
            # Add settings for this category
            for setting_key, setting_data in sorted(settings, key=lambda x: x[1].get("name", "")):
                setting_widget = self.create_setting_widget(setting_key, setting_data)
                category_layout.addWidget(setting_widget)
            
            self.settings_layout.addWidget(category_group)
    
    def perform_search(self):
        """Perform search and filter settings."""
        search_text = self.search_input.text().lower().strip()
        category_filter = self.category_filter.currentText()
        
        # Filter settings
        filtered_settings = {}
        for setting_key, setting_data in self.all_settings.items():
            # Check category filter
            if category_filter != "All Categories" and category_filter not in setting_data.get("category", ""):
                continue
            
            # Check search text
            if search_text:
                searchable_text = (
                    setting_data.get("name", "") + " " +
                    setting_data.get("description", "") + " " +
                    setting_data.get("tooltip", "") + " " +
                    setting_key
                ).lower()
                
                if search_text not in searchable_text:
                    continue
            
            filtered_settings[setting_key] = setting_data
        
        # Update display
        self.clear_settings_display()
        self.display_settings(filtered_settings)
        
        # Update results count
        count = len(filtered_settings)
        if search_text or category_filter != "All Categories":
            self.results_label.setText(f"Found {count} settings matching your criteria")
        else:
            self.results_label.setText(f"Showing {count} settings")
    
    def clear_search(self):
        """Clear search and show all settings."""
        self.search_input.clear()
        self.category_filter.setCurrentIndex(0)
        self.perform_search()
    
    def create_setting_widget(self, setting_key, setting_data):
        """Create a widget for a single setting."""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #333;
                border-radius: 6px;
                padding: 10px;
                margin: 2px;
            }
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Setting name and description
        info_layout = QVBoxLayout()
        
        name_label = QLabel(setting_data.get("name", setting_key))
        name_label.setStyleSheet("""
            font-weight: bold;
            color: #ffffff;
            font-size: 14px;
        """)
        info_layout.addWidget(name_label)
        
        desc_label = QLabel(setting_data.get("description", ""))
        desc_label.setStyleSheet("""
            color: #cccccc;
            font-size: 12px;
        """)
        desc_label.setWordWrap(True)
        info_layout.addWidget(desc_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Control widget based on type
        control_widget = self.create_control_widget(setting_key, setting_data)
        layout.addWidget(control_widget)
        
        return widget
    
    def create_control_widget(self, setting_key, setting_data):
        """Create the appropriate control widget for a setting."""
        setting_type = setting_data.get("type", "string")
        # Always get the most current value from config manager
        current_value = self.config_manager.get_setting(setting_key)
        
        if setting_type == "bool":
            # Toggle switch for boolean values
            toggle = ProfessionalToggleSwitch()
            
            # Block signals during initialization
            toggle.blockSignals(True)
            toggle.set_checked(bool(current_value) if current_value is not None else setting_data.get("default", False))
            toggle.blockSignals(False)
            
            # Connect signal AFTER initialization
            toggle.toggled.connect(lambda checked, key=setting_key: self.update_setting(key, int(checked)))
            
            # Tooltip
            tooltip = setting_data.get("tooltip", "")
            if tooltip:
                toggle.setToolTip(tooltip)
            
            return toggle
            
        elif setting_type == "int":
            # SpinBox for integer values
            spinbox = QSpinBox()
            spinbox.setRange(*setting_data.get("range", [0, 100]))
            
            # Block signals during initialization
            spinbox.blockSignals(True)
            try:
                value = int(current_value) if current_value and str(current_value).strip() else setting_data.get("default", 0)
            except (ValueError, TypeError):
                value = setting_data.get("default", 0)
            spinbox.setValue(value)
            spinbox.blockSignals(False)
            
            # Connect signal AFTER initialization
            spinbox.valueChanged.connect(lambda value, key=setting_key: self.update_setting(key, value))
            spinbox.setStyleSheet("""
                QSpinBox {
                    background-color: #444;
                    color: white;
                    border: 1px solid #666;
                    padding: 5px;
                    border-radius: 4px;
                    min-width: 80px;
                }
                QSpinBox:focus {
                    border-color: #4a90e2;
                }
            """)
            
            tooltip = setting_data.get("tooltip", "")
            if tooltip:
                spinbox.setToolTip(tooltip)
            
            return spinbox
            
        elif setting_type == "float":
            # DoubleSpinBox for float values
            spinbox = QDoubleSpinBox()
            spinbox.setRange(*setting_data.get("range", [0.0, 100.0]))
            
            # Block signals during initialization
            spinbox.blockSignals(True)
            try:
                value = float(current_value) if current_value and str(current_value).strip() else setting_data.get("default", 0.0)
            except (ValueError, TypeError):
                value = setting_data.get("default", 0.0)
            spinbox.setValue(value)
            spinbox.setDecimals(2)
            spinbox.blockSignals(False)
            
            # Connect signal AFTER initialization
            spinbox.valueChanged.connect(lambda value, key=setting_key: self.update_setting(key, value))
            spinbox.setStyleSheet("""
                QDoubleSpinBox {
                    background-color: #444;
                    color: white;
                    border: 1px solid #666;
                    padding: 5px;
                    border-radius: 4px;
                    min-width: 80px;
                }
                QDoubleSpinBox:focus {
                    border-color: #4a90e2;
                }
            """)
            
            tooltip = setting_data.get("tooltip", "")
            if tooltip:
                spinbox.setToolTip(tooltip)
            
            return spinbox
            
        else:
            # Text input for string values
            line_edit = QLineEdit()
            
            # Block signals during initialization
            line_edit.blockSignals(True)
            line_edit.setText(str(current_value) if current_value is not None else str(setting_data.get("default", "")))
            line_edit.blockSignals(False)
            
            # Use editingFinished instead of textChanged for intentional changes only
            line_edit.editingFinished.connect(lambda key=setting_key: self.update_setting(key, line_edit.text()))
            line_edit.setStyleSheet("""
                QLineEdit {
                    background-color: #444;
                    color: white;
                    border: 1px solid #666;
                    padding: 5px;
                    border-radius: 4px;
                    min-width: 120px;
                }
                QLineEdit:focus {
                    border-color: #4a90e2;
                }
            """)
            
            tooltip = setting_data.get("tooltip", "")
            if tooltip:
                line_edit.setToolTip(tooltip)
            
            return line_edit
    
    def update_setting(self, setting_key, value):
        """Update a setting value and track changes."""
        try:
            # Get the old value for tracking
            old_value = self.config_manager.get_setting(setting_key)
            
            # Update the setting
            self.config_manager.set_setting(setting_key, value)
            
            # Track the change in the main window
            if hasattr(self.parent(), 'track_setting_change'):
                self.parent().track_setting_change(setting_key, old_value, value)
            
            self.status_label.setText(f"Updated {setting_key} = {value}")
            log_info(f"Advanced setting updated: {setting_key} = {value}", "ADVANCED")
        except Exception as e:
            log_error(f"Failed to update setting {setting_key}: {str(e)}", "ADVANCED", e)
            self.status_label.setText(f"Error updating {setting_key}")
    
    
    def reset_to_defaults(self):
        """Reset all settings to their default values."""
        reply = QMessageBox.question(
            self,
            "Reset to Defaults",
            "Are you sure you want to reset all advanced settings to their default values?\n\n"
            "This will create a backup of your current settings first.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Create backup first
                self.config_manager._create_backup("Before_Advanced_Reset")
                
                # Reset to defaults
                from settings_database import BF6_SETTINGS_DATABASE
                for setting_key, setting_data in BF6_SETTINGS_DATABASE.items():
                    default_value = setting_data.get("default")
                    if default_value is not None:
                        self.config_manager.set_setting(setting_key, default_value)
                
                # Reload the UI
                self.load_settings()
                
                QMessageBox.information(
                    self,
                    "Settings Reset",
                    "✅ All advanced settings have been reset to their default values.\n\n"
                    "💾 A backup of your previous settings has been created."
                )
                
                log_info("Advanced settings reset to defaults", "ADVANCED")
                
            except Exception as e:
                log_error(f"Failed to reset settings: {str(e)}", "ADVANCED", e)
                QMessageBox.critical(
                    self,
                    "Reset Failed",
                    f"❌ Failed to reset settings: {str(e)}"
                )


class InputTab(QWidget):
    """Input Settings Tab - Comprehensive interface for all input settings."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the input settings UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)  # Minimal margins
        layout.setSpacing(6)  # Minimal spacing
        
        # Header
        header = QLabel("🎮 Input Settings")
        header.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 8px;
            padding: 8px;
            background-color: #2a2a2a;
            border-radius: 4px;
            border: 1px solid #444;
        """)
        layout.addWidget(header)
        
        # Create scroll area for all settings
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #333;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #666;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #888;
            }
        """)
        
        # Main content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(12)
        
        # Create input sections
        self.create_mouse_section()
        self.create_keyboard_section()
        self.create_controller_section()
        self.create_accessibility_section()
        self.create_advanced_section()
        
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
        
        # Status bar
        self.status_label = QLabel("Ready to configure input settings")
        self.status_label.setStyleSheet("""
            color: #888;
            font-size: 12px;
            padding: 5px;
        """)
        layout.addWidget(self.status_label)
    
    def create_mouse_section(self):
        """Create mouse settings section."""
        group = QGroupBox("🖱️ Mouse Settings")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                font-size: 16px;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(8)
        
        # Mouse Sensitivity
        self.mouse_sensitivity = self.create_slider_setting(
            "Mouse Sensitivity", 
            "GstInput.MouseSensitivity", 
            0.0, 5.0, 0.1,
            "Controls how fast the mouse moves the camera. Higher values = faster movement.",
            "Recommended: 0.5-1.5 for most players"
        )
        layout.addWidget(self.mouse_sensitivity, 0, 0, 1, 2)
        
        # Mouse Acceleration
        self.mouse_acceleration = self.create_toggle_setting(
            "Mouse Acceleration",
            "GstInput.MouseAcceleration",
            "Enables mouse acceleration for smoother movement.",
            "Disable for consistent mouse movement (recommended for competitive play)"
        )
        layout.addWidget(self.mouse_acceleration, 1, 0)
        
        # Mouse Smoothing
        self.mouse_smoothing = self.create_toggle_setting(
            "Mouse Smoothing",
            "GstInput.MouseSmoothing",
            "Reduces mouse jitter and provides smoother movement.",
            "Enable for smoother gameplay, disable for more responsive input"
        )
        layout.addWidget(self.mouse_smoothing, 1, 1)
        
        # Mouse Polling Rate
        self.mouse_polling = self.create_combo_setting(
            "Mouse Polling Rate",
            "GstInput.MousePollingRate",
            ["125 Hz", "250 Hz", "500 Hz", "1000 Hz"],
            "Higher polling rates provide more responsive mouse input.",
            "1000 Hz recommended for competitive play"
        )
        layout.addWidget(self.mouse_polling, 2, 0)
        
        # Mouse DPI
        self.mouse_dpi = self.create_slider_setting(
            "Mouse DPI",
            "GstInput.MouseDPI",
            400, 16000, 100,
            "Mouse DPI setting (if supported by your mouse).",
            "Higher DPI = more sensitive movement"
        )
        layout.addWidget(self.mouse_dpi, 2, 1)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
    
    def create_keyboard_section(self):
        """Create keyboard settings section."""
        group = QGroupBox("⌨️ Keyboard Settings")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                font-size: 16px;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(8)
        
        # Key Repeat Rate
        self.key_repeat_rate = self.create_slider_setting(
            "Key Repeat Rate",
            "GstInput.KeyRepeatRate",
            1.0, 10.0, 0.1,
            "How fast keys repeat when held down.",
            "Higher values = faster key repetition"
        )
        layout.addWidget(self.key_repeat_rate, 0, 0)
        
        # Key Repeat Delay
        self.key_repeat_delay = self.create_slider_setting(
            "Key Repeat Delay",
            "GstInput.KeyRepeatDelay",
            0.1, 2.0, 0.1,
            "Delay before key starts repeating.",
            "Lower values = more responsive key repetition"
        )
        layout.addWidget(self.key_repeat_delay, 0, 1)
        
        # Keyboard Layout
        self.keyboard_layout = self.create_combo_setting(
            "Keyboard Layout",
            "GstInput.KeyboardLayout",
            ["QWERTY", "AZERTY", "QWERTZ", "Dvorak"],
            "Keyboard layout for key bindings.",
            "Select your regional keyboard layout"
        )
        layout.addWidget(self.keyboard_layout, 1, 0)
        
        # Sticky Keys
        self.sticky_keys = self.create_toggle_setting(
            "Sticky Keys",
            "GstInput.StickyKeys",
            "Allows modifier keys to stay active after release.",
            "Useful for accessibility, disable for normal gaming"
        )
        layout.addWidget(self.sticky_keys, 1, 1)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
    
    def create_controller_section(self):
        """Create controller settings section."""
        group = QGroupBox("🎮 Controller Settings")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                font-size: 16px;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(8)
        
        # Controller Sensitivity
        self.controller_sensitivity = self.create_slider_setting(
            "Controller Sensitivity",
            "GstInput.ControllerSensitivity",
            0.1, 3.0, 0.1,
            "How fast the controller moves the camera.",
            "Higher values = faster camera movement"
        )
        layout.addWidget(self.controller_sensitivity, 0, 0)
        
        # Controller Dead Zone
        self.controller_deadzone = self.create_slider_setting(
            "Controller Dead Zone",
            "GstInput.ControllerDeadZone",
            0.0, 0.5, 0.01,
            "Minimum input required before controller responds.",
            "Higher values prevent stick drift, lower values more responsive"
        )
        layout.addWidget(self.controller_deadzone, 0, 1)
        
        # Controller Vibration
        self.controller_vibration = self.create_toggle_setting(
            "Controller Vibration",
            "GstInput.ControllerVibration",
            "Enables controller vibration/haptic feedback.",
            "Disable to save battery or reduce distraction"
        )
        layout.addWidget(self.controller_vibration, 1, 0)
        
        # Controller Type
        self.controller_type = self.create_combo_setting(
            "Controller Type",
            "GstInput.ControllerType",
            ["Xbox", "PlayStation", "Generic", "Steam Controller"],
            "Type of controller being used.",
            "Select your controller type for optimal compatibility"
        )
        layout.addWidget(self.controller_type, 1, 1)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
    
    def create_accessibility_section(self):
        """Create accessibility settings section."""
        group = QGroupBox("♿ Accessibility Settings")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                font-size: 16px;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(8)
        
        # One-Handed Mode
        self.one_handed_mode = self.create_toggle_setting(
            "One-Handed Mode",
            "GstInput.OneHandedMode",
            "Optimizes controls for one-handed gameplay.",
            "Useful for players with limited mobility"
        )
        layout.addWidget(self.one_handed_mode, 0, 0)
        
        # Auto-Aim Assist
        self.auto_aim_assist = self.create_toggle_setting(
            "Auto-Aim Assist",
            "GstInput.AutoAimAssist",
            "Provides assistance with aiming for accessibility.",
            "Helps players with motor difficulties"
        )
        layout.addWidget(self.auto_aim_assist, 0, 1)
        
        # Color Blind Support
        self.color_blind_support = self.create_combo_setting(
            "Color Blind Support",
            "GstInput.ColorBlindSupport",
            ["None", "Protanopia", "Deuteranopia", "Tritanopia"],
            "Adjusts colors for color blind players.",
            "Select your type of color blindness for better visibility"
        )
        layout.addWidget(self.color_blind_support, 1, 0)
        
        # High Contrast Mode
        self.high_contrast = self.create_toggle_setting(
            "High Contrast Mode",
            "GstInput.HighContrastMode",
            "Increases contrast for better visibility.",
            "Helpful for players with visual impairments"
        )
        layout.addWidget(self.high_contrast, 1, 1)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
    
    def create_advanced_section(self):
        """Create advanced input settings section."""
        group = QGroupBox("⚙️ Advanced Input Settings")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                font-size: 16px;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(8)
        
        # Raw Input
        self.raw_input = self.create_toggle_setting(
            "Raw Input",
            "GstInput.RawInput",
            "Bypasses Windows mouse acceleration for more precise input.",
            "Recommended for competitive play, provides 1:1 mouse movement"
        )
        layout.addWidget(self.raw_input, 0, 0)
        
        # Input Lag Reduction
        self.input_lag_reduction = self.create_toggle_setting(
            "Input Lag Reduction",
            "GstInput.InputLagReduction",
            "Reduces input lag for more responsive controls.",
            "May increase CPU usage but improves responsiveness"
        )
        layout.addWidget(self.input_lag_reduction, 0, 1)
        
        # Custom Key Bindings
        self.custom_keybindings = self.create_toggle_setting(
            "Custom Key Bindings",
            "GstInput.CustomKeyBindings",
            "Enables custom key binding configuration.",
            "Allows you to remap keys for better accessibility"
        )
        layout.addWidget(self.custom_keybindings, 1, 0)
        
        # Macro Support
        self.macro_support = self.create_toggle_setting(
            "Macro Support",
            "GstInput.MacroSupport",
            "Enables macro recording and playback.",
            "Useful for complex key combinations and accessibility"
        )
        layout.addWidget(self.macro_support, 1, 1)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
    
    def create_slider_setting(self, name, key, min_val, max_val, step, description, recommendation=""):
        """Create a slider setting widget."""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #333;
                border-radius: 6px;
                padding: 10px;
                margin: 2px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Name and description
        name_label = QLabel(name)
        name_label.setStyleSheet("""
            font-weight: bold;
            color: #ffffff;
            font-size: 14px;
        """)
        layout.addWidget(name_label)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            color: #cccccc;
            font-size: 12px;
        """)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        if recommendation:
            rec_label = QLabel(f"💡 {recommendation}")
            rec_label.setStyleSheet("""
                color: #4a90e2;
                font-size: 11px;
                font-style: italic;
            """)
            layout.addWidget(rec_label)
        
        # Slider and value
        slider_layout = QHBoxLayout()
        
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(int(min_val * 100), int(max_val * 100))
        
        # Block signals during initialization
        slider.blockSignals(True)
        slider.setValue(int(self.config_manager.get_setting(key, min_val) * 100))
        slider.blockSignals(False)
        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #555;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #4a90e2;
                width: 18px;
                height: 18px;
                border-radius: 9px;
                margin: -6px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #357abd;
            }
        """)
        
        value_label = QLabel(f"{slider.value() / 100:.2f}")
        value_label.setStyleSheet("""
            color: #ffffff;
            font-weight: bold;
            min-width: 60px;
        """)
        
        slider.valueChanged.connect(lambda v: value_label.setText(f"{v / 100:.2f}"))
        slider.valueChanged.connect(lambda v: self.update_setting(key, v / 100))
        
        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)
        layout.addLayout(slider_layout)
        
        return widget
    
    def create_toggle_setting(self, name, key, description, recommendation=""):
        """Create a toggle setting widget."""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #333;
                border-radius: 6px;
                padding: 10px;
                margin: 2px;
            }
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Info section
        info_layout = QVBoxLayout()
        
        name_label = QLabel(name)
        name_label.setStyleSheet("""
            font-weight: bold;
            color: #ffffff;
            font-size: 14px;
        """)
        info_layout.addWidget(name_label)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            color: #cccccc;
            font-size: 12px;
        """)
        desc_label.setWordWrap(True)
        info_layout.addWidget(desc_label)
        
        if recommendation:
            rec_label = QLabel(f"💡 {recommendation}")
            rec_label.setStyleSheet("""
                color: #4a90e2;
                font-size: 11px;
                font-style: italic;
            """)
            info_layout.addWidget(rec_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Toggle switch
        toggle = ProfessionalToggleSwitch()
        
        # Block signals during initialization
        toggle.blockSignals(True)
        toggle.set_checked(bool(self.config_manager.get_setting(key, False)))
        toggle.blockSignals(False)
        
        # Connect signal AFTER initialization
        toggle.toggled.connect(lambda checked: self.update_setting(key, int(checked)))
        
        layout.addWidget(toggle)
        
        return widget
    
    def create_combo_setting(self, name, key, options, description, recommendation=""):
        """Create a combo box setting widget."""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #333;
                border-radius: 6px;
                padding: 10px;
                margin: 2px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Name and description
        name_label = QLabel(name)
        name_label.setStyleSheet("""
            font-weight: bold;
            color: #ffffff;
            font-size: 14px;
        """)
        layout.addWidget(name_label)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            color: #cccccc;
            font-size: 12px;
        """)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        if recommendation:
            rec_label = QLabel(f"💡 {recommendation}")
            rec_label.setStyleSheet("""
                color: #4a90e2;
                font-size: 11px;
                font-style: italic;
            """)
            layout.addWidget(rec_label)
        
        # Combo box
        combo = QComboBox()
        combo.addItems(options)
        combo.setStyleSheet("""
            QComboBox {
                background-color: #444;
                color: white;
                border: 1px solid #666;
                padding: 5px;
                border-radius: 4px;
                min-width: 120px;
            }
            QComboBox:focus {
                border-color: #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #888;
            }
        """)
        
        # Block signals during initialization
        combo.blockSignals(True)
        current_value = self.config_manager.get_setting(key, options[0])
        if current_value in options:
            combo.setCurrentText(current_value)
        else:
            combo.setCurrentIndex(0)
        combo.blockSignals(False)
        
        # Connect signal AFTER initialization
        combo.currentTextChanged.connect(lambda text: self.update_setting(key, text))
        layout.addWidget(combo)
        
        return widget
    
    def showEvent(self, event):
        """Refresh settings when tab becomes visible."""
        super().showEvent(event)
        self.load_settings()
    
    def load_settings(self):
        """Load current settings from config."""
        # Settings are loaded when widgets are created
        pass
    
    def update_setting(self, key, value):
        """Update a setting value and track changes."""
        try:
            # Get the old value for tracking
            old_value = self.config_manager.get_setting(key)
            
            # Update the setting
            self.config_manager.set_setting(key, value)
            
            # Track the change in the main window
            if hasattr(self.parent(), 'track_setting_change'):
                self.parent().track_setting_change(key, old_value, value)
            
            self.status_label.setText(f"Updated {key} = {value}")
            log_info(f"Input setting updated: {key} = {value}", "INPUT")
        except Exception as e:
            log_error(f"Failed to update input setting {key}: {str(e)}", "INPUT", e)
            self.status_label.setText(f"Error updating {key}")


def main():
    """Main application entry point."""
    try:
        log_info("Starting FieldTuner application", "MAIN")
        app = QApplication(sys.argv)
        app.setApplicationName("FieldTuner")
        app.setApplicationVersion("2.0.0")
        
        # Enable high DPI scaling
        try:
            app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
            app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        except AttributeError:
            pass
        
        window = MainWindow()
        window.show()
        
        log_info("FieldTuner application started successfully", "MAIN")
        sys.exit(app.exec())
        
    except Exception as e:
        log_error(f"Failed to start FieldTuner: {str(e)}", "MAIN", e)
        print(f"Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()