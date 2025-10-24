#!/usr/bin/env python3
"""
FieldTuner - Enhanced GUI Version
Modern Windows GUI for Battlefield 6 Configuration with Settings Management
"""

import sys
import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QLabel, QPushButton, QSlider, QCheckBox, QComboBox,
    QSpinBox, QDoubleSpinBox, QGroupBox, QGridLayout, QTextEdit,
    QMessageBox, QFileDialog, QStatusBar, QProgressBar, QSplitter,
    QListWidget, QListWidgetItem, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor


class ConfigManager:
    """Manages Battlefield 6 configuration files and settings."""
    
    def __init__(self):
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
        
        self.BACKUP_DIR = Path.home() / "AppData" / "Roaming" / "FieldTuner" / "backups"
        self.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
        self._detect_config_file()
        if self.config_path and self.config_path.exists():
            self._load_config()
            self._create_backup()
    
    def _detect_config_file(self):
        """Auto-detect the Battlefield 6 config file."""
        for path in self.CONFIG_PATHS:
            if path.exists():
                self.config_path = path
                return True
        return False
    
    def _load_config(self):
        """Load configuration from the detected file."""
        if not self.config_path or not self.config_path.exists():
            return False
        
        try:
            with open(self.config_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.original_data = f.read()
            
            self.config_data = self._parse_config_data(self.original_data)
            return True
        except Exception as e:
            print(f"Failed to load config: {e}")
            return False
    
    def _parse_config_data(self, data):
        """Parse configuration data into key-value pairs."""
        config = {}
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
    
    def _create_backup(self):
        """Create a backup of the original config file."""
        if not self.config_path or not self.config_path.exists():
            return False
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"PROFSAVE_profile_backup_{timestamp}.bak"
            self.backup_path = self.BACKUP_DIR / backup_name
            shutil.copy2(self.config_path, self.backup_path)
            return True
        except Exception as e:
            print(f"Failed to create backup: {e}")
            return False
    
    def get_setting(self, key, default=""):
        """Get a configuration setting value."""
        return self.config_data.get(key, default)
    
    def set_setting(self, key, value):
        """Set a configuration setting value."""
        self.config_data[key] = str(value)
    
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
        """Save configuration changes to file."""
        if not self.config_path:
            return False
        
        try:
            new_data = self._generate_config_content()
            with open(self.config_path, 'w', encoding='utf-8') as f:
                f.write(new_data)
            return True
        except Exception as e:
            print(f"Failed to save config: {e}")
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


class GraphicsTab(QWidget):
    """Graphics settings tab."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # DirectX 12 Settings
        dx12_group = QGroupBox("DirectX 12 Settings")
        dx12_layout = QGridLayout()
        
        self.dx12_enabled = QCheckBox("Enable DirectX 12")
        dx12_layout.addWidget(self.dx12_enabled, 0, 0)
        
        self.raytracing_enabled = QCheckBox("Enable Ray Tracing")
        dx12_layout.addWidget(self.raytracing_enabled, 0, 1)
        
        dx12_group.setLayout(dx12_layout)
        layout.addWidget(dx12_group)
        
        # Display Settings
        display_group = QGroupBox("Display Settings")
        display_layout = QGridLayout()
        
        display_layout.addWidget(QLabel("Fullscreen Mode:"), 0, 0)
        self.fullscreen_mode = QComboBox()
        self.fullscreen_mode.addItems(["Windowed", "Borderless", "Fullscreen"])
        display_layout.addWidget(self.fullscreen_mode, 0, 1)
        
        display_layout.addWidget(QLabel("Resolution Scale:"), 1, 0)
        self.resolution_scale = QSlider(Qt.Orientation.Horizontal)
        self.resolution_scale.setRange(50, 200)
        self.resolution_scale.setValue(100)
        display_layout.addWidget(self.resolution_scale, 1, 1)
        
        self.resolution_scale_label = QLabel("100%")
        display_layout.addWidget(self.resolution_scale_label, 1, 2)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # Visual Effects
        effects_group = QGroupBox("Visual Effects")
        effects_layout = QGridLayout()
        
        self.motion_blur = QCheckBox("Motion Blur")
        effects_layout.addWidget(self.motion_blur, 0, 0)
        
        self.depth_of_field = QCheckBox("Depth of Field")
        effects_layout.addWidget(self.depth_of_field, 0, 1)
        
        self.ambient_occlusion = QCheckBox("Ambient Occlusion")
        effects_layout.addWidget(self.ambient_occlusion, 1, 0)
        
        self.volumetric_lighting = QCheckBox("Volumetric Lighting")
        effects_layout.addWidget(self.volumetric_lighting, 1, 1)
        
        effects_group.setLayout(effects_layout)
        layout.addWidget(effects_group)
        
        # Performance
        perf_group = QGroupBox("Performance Settings")
        perf_layout = QGridLayout()
        
        self.vsync = QCheckBox("Vertical Sync")
        perf_layout.addWidget(self.vsync, 0, 0)
        
        self.future_frame_rendering = QCheckBox("Future Frame Rendering")
        perf_layout.addWidget(self.future_frame_rendering, 0, 1)
        
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)
        
        # Connect signals
        self.resolution_scale.valueChanged.connect(self.on_resolution_scale_changed)
    
    def on_resolution_scale_changed(self, value):
        self.resolution_scale_label.setText(f"{value}%")
    
    def load_settings(self):
        """Load settings from config manager."""
        graphics_settings = self.config_manager.get_graphics_settings()
        
        # DirectX 12 settings
        self.dx12_enabled.setChecked(graphics_settings.get('GstRender.Dx12Enabled', '0') == '1')
        self.raytracing_enabled.setChecked(graphics_settings.get('GstRender.RaytracingAmbientOcclusion', '0') == '1')
        
        # Display settings
        fullscreen_mode = int(graphics_settings.get('GstRender.FullscreenMode', '0'))
        self.fullscreen_mode.setCurrentIndex(min(fullscreen_mode, 2))
        
        resolution_scale = float(graphics_settings.get('GstRender.ResolutionScale', '1.0'))
        self.resolution_scale.setValue(int(resolution_scale * 100))
        self.resolution_scale_label.setText(f"{int(resolution_scale * 100)}%")
        
        # Visual effects
        self.motion_blur.setChecked(graphics_settings.get('GstRender.MotionBlurWorld', '0') != '0')
        self.depth_of_field.setChecked(graphics_settings.get('GstRender.WeaponDOF', '0') == '1')
        self.ambient_occlusion.setChecked(graphics_settings.get('GstRender.AmbientOcclusion', '0') == '1')
        self.volumetric_lighting.setChecked(graphics_settings.get('GstRender.VolumetricQuality', '0') != '0')
        
        # Performance settings
        self.vsync.setChecked(graphics_settings.get('GstRender.VSyncMode', '0') != '0')
        self.future_frame_rendering.setChecked(graphics_settings.get('GstRender.FutureFrameRendering', '0') == '1')
    
    def save_settings(self):
        """Save settings to config manager."""
        # DirectX 12 settings
        self.config_manager.set_setting('GstRender.Dx12Enabled', str(int(self.dx12_enabled.isChecked())))
        self.config_manager.set_setting('GstRender.RaytracingAmbientOcclusion', str(int(self.raytracing_enabled.isChecked())))
        
        # Display settings
        self.config_manager.set_setting('GstRender.FullscreenMode', str(self.fullscreen_mode.currentIndex()))
        
        resolution_scale = self.resolution_scale.value() / 100.0
        self.config_manager.set_setting('GstRender.ResolutionScale', str(resolution_scale))
        
        # Visual effects
        self.config_manager.set_setting('GstRender.MotionBlurWorld', str(0.5 if self.motion_blur.isChecked() else 0))
        self.config_manager.set_setting('GstRender.WeaponDOF', str(int(self.depth_of_field.isChecked())))
        self.config_manager.set_setting('GstRender.AmbientOcclusion', str(int(self.ambient_occlusion.isChecked())))
        self.config_manager.set_setting('GstRender.VolumetricQuality', str(1 if self.volumetric_lighting.isChecked() else 0))
        
        # Performance settings
        self.config_manager.set_setting('GstRender.VSyncMode', str(1 if self.vsync.isChecked() else 0))
        self.config_manager.set_setting('GstRender.FutureFrameRendering', str(int(self.future_frame_rendering.isChecked())))


class AudioTab(QWidget):
    """Audio settings tab."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Volume Settings
        volume_group = QGroupBox("Volume Settings")
        volume_layout = QGridLayout()
        
        volume_layout.addWidget(QLabel("Master Volume:"), 0, 0)
        self.master_volume = QSlider(Qt.Orientation.Horizontal)
        self.master_volume.setRange(0, 100)
        self.master_volume.setValue(100)
        volume_layout.addWidget(self.master_volume, 0, 1)
        
        self.master_volume_label = QLabel("100%")
        volume_layout.addWidget(self.master_volume_label, 0, 2)
        
        volume_layout.addWidget(QLabel("Music Volume:"), 1, 0)
        self.music_volume = QSlider(Qt.Orientation.Horizontal)
        self.music_volume.setRange(0, 100)
        self.music_volume.setValue(80)
        volume_layout.addWidget(self.music_volume, 1, 1)
        
        self.music_volume_label = QLabel("80%")
        volume_layout.addWidget(self.music_volume_label, 1, 2)
        
        volume_group.setLayout(volume_layout)
        layout.addWidget(volume_group)
        
        # Audio Quality
        quality_group = QGroupBox("Audio Quality")
        quality_layout = QGridLayout()
        
        quality_layout.addWidget(QLabel("Audio Quality:"), 0, 0)
        self.audio_quality = QComboBox()
        self.audio_quality.addItems(["Low", "Medium", "High", "Ultra"])
        quality_layout.addWidget(self.audio_quality, 0, 1)
        
        quality_layout.addWidget(QLabel("Speaker Configuration:"), 1, 0)
        self.speaker_config = QComboBox()
        self.speaker_config.addItems(["Stereo", "5.1 Surround", "7.1 Surround"])
        quality_layout.addWidget(self.speaker_config, 1, 1)
        
        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)
        
        # Audio Features
        features_group = QGroupBox("Audio Features")
        features_layout = QGridLayout()
        
        self.audio_3d = QCheckBox("3D Audio")
        features_layout.addWidget(self.audio_3d, 0, 0)
        
        self.subtitles = QCheckBox("Subtitles")
        features_layout.addWidget(self.subtitles, 0, 1)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        # Connect signals
        self.master_volume.valueChanged.connect(self.on_master_volume_changed)
        self.music_volume.valueChanged.connect(self.on_music_volume_changed)
    
    def on_master_volume_changed(self, value):
        self.master_volume_label.setText(f"{value}%")
    
    def on_music_volume_changed(self, value):
        self.music_volume_label.setText(f"{value}%")
    
    def load_settings(self):
        """Load settings from config manager."""
        audio_settings = self.config_manager.get_audio_settings()
        
        # Volume settings
        master_vol = int(float(audio_settings.get('GstAudio.Volume', '1.0')) * 100)
        self.master_volume.setValue(master_vol)
        self.master_volume_label.setText(f"{master_vol}%")
        
        music_vol = int(float(audio_settings.get('GstAudio.Volume_Music', '1.0')) * 100)
        self.music_volume.setValue(music_vol)
        self.music_volume_label.setText(f"{music_vol}%")
        
        # Audio quality
        quality = int(audio_settings.get('GstAudio.AudioQuality', '1'))
        self.audio_quality.setCurrentIndex(quality)
        
        speaker_config = int(audio_settings.get('GstAudio.SpeakerConfiguration', '2'))
        self.speaker_config.setCurrentIndex(speaker_config - 2)
        
        # Audio features
        self.audio_3d.setChecked(audio_settings.get('GstAudio.3dEnabled', '0') == '1')
        self.subtitles.setChecked(audio_settings.get('GstAudio.SubtitlesCommander', '0') == '1')
    
    def save_settings(self):
        """Save settings to config manager."""
        # Volume settings
        self.config_manager.set_setting('GstAudio.Volume', str(self.master_volume.value() / 100.0))
        self.config_manager.set_setting('GstAudio.Volume_Music', str(self.music_volume.value() / 100.0))
        
        # Audio quality
        self.config_manager.set_setting('GstAudio.AudioQuality', str(self.audio_quality.currentIndex()))
        self.config_manager.set_setting('GstAudio.SpeakerConfiguration', str(self.speaker_config.currentIndex() + 2))
        
        # Audio features
        self.config_manager.set_setting('GstAudio.3dEnabled', str(int(self.audio_3d.isChecked())))
        self.config_manager.set_setting('GstAudio.SubtitlesCommander', str(int(self.subtitles.isChecked())))


class InputTab(QWidget):
    """Input settings tab."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Mouse Settings
        mouse_group = QGroupBox("Mouse Settings")
        mouse_layout = QGridLayout()
        
        mouse_layout.addWidget(QLabel("Mouse Sensitivity:"), 0, 0)
        self.mouse_sensitivity = QSlider(Qt.Orientation.Horizontal)
        self.mouse_sensitivity.setRange(1, 100)
        self.mouse_sensitivity.setValue(50)
        mouse_layout.addWidget(self.mouse_sensitivity, 0, 1)
        
        self.mouse_sensitivity_label = QLabel("50")
        mouse_layout.addWidget(self.mouse_sensitivity_label, 0, 2)
        
        self.raw_input = QCheckBox("Raw Input")
        mouse_layout.addWidget(self.raw_input, 1, 0)
        
        mouse_group.setLayout(mouse_layout)
        layout.addWidget(mouse_group)
        
        # Gamepad Settings
        gamepad_group = QGroupBox("Gamepad Settings")
        gamepad_layout = QGridLayout()
        
        gamepad_layout.addWidget(QLabel("Gamepad Sensitivity:"), 0, 0)
        self.gamepad_sensitivity = QSlider(Qt.Orientation.Horizontal)
        self.gamepad_sensitivity.setRange(1, 100)
        self.gamepad_sensitivity.setValue(50)
        gamepad_layout.addWidget(self.gamepad_sensitivity, 0, 1)
        
        self.gamepad_sensitivity_label = QLabel("50")
        gamepad_layout.addWidget(self.gamepad_sensitivity_label, 0, 2)
        
        self.vibration = QCheckBox("Vibration")
        gamepad_layout.addWidget(self.vibration, 1, 0)
        
        gamepad_group.setLayout(gamepad_layout)
        layout.addWidget(gamepad_group)
        
        # Connect signals
        self.mouse_sensitivity.valueChanged.connect(self.on_mouse_sensitivity_changed)
        self.gamepad_sensitivity.valueChanged.connect(self.on_gamepad_sensitivity_changed)
    
    def on_mouse_sensitivity_changed(self, value):
        self.mouse_sensitivity_label.setText(str(value))
    
    def on_gamepad_sensitivity_changed(self, value):
        self.gamepad_sensitivity_label.setText(str(value))
    
    def load_settings(self):
        """Load settings from config manager."""
        input_settings = self.config_manager.get_input_settings()
        
        # Mouse settings
        mouse_sens = int(float(input_settings.get('GstInput.MouseSensitivity', '0.025500')) * 1000)
        self.mouse_sensitivity.setValue(mouse_sens)
        self.mouse_sensitivity_label.setText(str(mouse_sens))
        
        self.raw_input.setChecked(input_settings.get('GstInput.MouseRawInput', '0') == '1')
        
        # Gamepad settings
        gamepad_sens = int(float(input_settings.get('GstInput.JoystickSensitivity', '1.750000')) * 20)
        self.gamepad_sensitivity.setValue(gamepad_sens)
        self.gamepad_sensitivity_label.setText(str(gamepad_sens))
        
        self.vibration.setChecked(input_settings.get('GstInput.Vibration', '0') == '1')
    
    def save_settings(self):
        """Save settings to config manager."""
        # Mouse settings
        mouse_sens = self.mouse_sensitivity.value() / 1000.0
        self.config_manager.set_setting('GstInput.MouseSensitivity', str(mouse_sens))
        self.config_manager.set_setting('GstInput.MouseRawInput', str(int(self.raw_input.isChecked())))
        
        # Gamepad settings
        gamepad_sens = self.gamepad_sensitivity.value() / 20.0
        self.config_manager.set_setting('GstInput.JoystickSensitivity', str(gamepad_sens))
        self.config_manager.set_setting('GstInput.Vibration', str(int(self.vibration.isChecked())))


class SettingsTab(QWidget):
    """Settings management tab."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Config File Info
        config_group = QGroupBox("Configuration File")
        config_layout = QVBoxLayout()
        
        self.config_path_label = QLabel("Config Path: Not found")
        self.config_path_label.setWordWrap(True)
        config_layout.addWidget(self.config_path_label)
        
        self.config_size_label = QLabel("File Size: Unknown")
        config_layout.addWidget(self.config_size_label)
        
        self.config_settings_label = QLabel("Settings Count: Unknown")
        config_layout.addWidget(self.config_settings_label)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Backup Management
        backup_group = QGroupBox("Backup Management")
        backup_layout = QVBoxLayout()
        
        # Backup buttons
        backup_buttons_layout = QHBoxLayout()
        
        self.create_backup_button = QPushButton("Create New Backup")
        self.create_backup_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        self.create_backup_button.clicked.connect(self.create_backup)
        
        self.refresh_backups_button = QPushButton("Refresh Backups")
        self.refresh_backups_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        self.refresh_backups_button.clicked.connect(self.refresh_backups)
        
        backup_buttons_layout.addWidget(self.create_backup_button)
        backup_buttons_layout.addWidget(self.refresh_backups_button)
        backup_buttons_layout.addStretch()
        
        backup_layout.addLayout(backup_buttons_layout)
        
        # Backup list
        self.backup_list = QListWidget()
        self.backup_list.setMaximumHeight(150)
        backup_layout.addWidget(QLabel("Available Backups:"))
        backup_layout.addWidget(self.backup_list)
        
        # Backup actions
        backup_actions_layout = QHBoxLayout()
        
        self.restore_backup_button = QPushButton("Restore Selected")
        self.restore_backup_button.setStyleSheet("""
            QPushButton {
                background-color: #ff6b35;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e55a2b;
            }
        """)
        self.restore_backup_button.clicked.connect(self.restore_selected_backup)
        
        self.delete_backup_button = QPushButton("Delete Selected")
        self.delete_backup_button.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        """)
        self.delete_backup_button.clicked.connect(self.delete_selected_backup)
        
        backup_actions_layout.addWidget(self.restore_backup_button)
        backup_actions_layout.addWidget(self.delete_backup_button)
        backup_actions_layout.addStretch()
        
        backup_layout.addLayout(backup_actions_layout)
        
        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)
        
        # Settings Overview
        overview_group = QGroupBox("Settings Overview")
        overview_layout = QVBoxLayout()
        
        # Settings categories
        self.settings_overview = QTextEdit()
        self.settings_overview.setMaximumHeight(200)
        self.settings_overview.setReadOnly(True)
        self.settings_overview.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                font-family: monospace;
                font-size: 11px;
            }
        """)
        overview_layout.addWidget(QLabel("Current Settings Summary:"))
        overview_layout.addWidget(self.settings_overview)
        
        # Refresh overview button
        refresh_overview_button = QPushButton("Refresh Overview")
        refresh_overview_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        refresh_overview_button.clicked.connect(self.refresh_overview)
        overview_layout.addWidget(refresh_overview_button)
        
        overview_group.setLayout(overview_layout)
        layout.addWidget(overview_group)
        
        # File Operations
        file_group = QGroupBox("File Operations")
        file_layout = QHBoxLayout()
        
        self.open_config_button = QPushButton("Open Config File")
        self.open_config_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        self.open_config_button.clicked.connect(self.open_config_file)
        
        self.open_backup_folder_button = QPushButton("Open Backup Folder")
        self.open_backup_folder_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        self.open_backup_folder_button.clicked.connect(self.open_backup_folder)
        
        file_layout.addWidget(self.open_config_button)
        file_layout.addWidget(self.open_backup_folder_button)
        file_layout.addStretch()
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
    
    def refresh_data(self):
        """Refresh all data in the settings tab."""
        self.update_config_info()
        self.refresh_backups()
        self.refresh_overview()
    
    def update_config_info(self):
        """Update configuration file information."""
        if self.config_manager.config_path and self.config_manager.config_path.exists():
            file_size = self.config_manager.config_path.stat().st_size
            settings_count = len(self.config_manager.config_data)
            
            self.config_path_label.setText(f"Config Path: {self.config_manager.config_path}")
            self.config_size_label.setText(f"File Size: {file_size:,} bytes")
            self.config_settings_label.setText(f"Settings Count: {settings_count}")
        else:
            self.config_path_label.setText("Config Path: Not found")
            self.config_size_label.setText("File Size: Unknown")
            self.config_settings_label.setText("Settings Count: Unknown")
    
    def refresh_backups(self):
        """Refresh the backup list."""
        self.backup_list.clear()
        
        if not self.config_manager.BACKUP_DIR.exists():
            return
        
        backup_files = list(self.config_manager.BACKUP_DIR.glob("*.bak"))
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        for backup_file in backup_files:
            timestamp = datetime.fromtimestamp(backup_file.stat().st_mtime)
            size = backup_file.stat().st_size
            item_text = f"{backup_file.name} ({timestamp.strftime('%Y-%m-%d %H:%M:%S')}) - {size:,} bytes"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, backup_file)
            self.backup_list.addItem(item)
    
    def refresh_overview(self):
        """Refresh the settings overview."""
        if not self.config_manager.config_data:
            self.settings_overview.setText("No settings loaded")
            return
        
        overview_text = "SETTINGS OVERVIEW\n"
        overview_text += "=" * 50 + "\n\n"
        
        # Graphics settings
        graphics_settings = self.config_manager.get_graphics_settings()
        overview_text += f"GRAPHICS SETTINGS ({len(graphics_settings)})\n"
        overview_text += "-" * 30 + "\n"
        for key, value in list(graphics_settings.items())[:10]:  # Show first 10
            overview_text += f"{key} = {value}\n"
        if len(graphics_settings) > 10:
            overview_text += f"... and {len(graphics_settings) - 10} more\n"
        overview_text += "\n"
        
        # Audio settings
        audio_settings = self.config_manager.get_audio_settings()
        overview_text += f"AUDIO SETTINGS ({len(audio_settings)})\n"
        overview_text += "-" * 30 + "\n"
        for key, value in list(audio_settings.items())[:5]:  # Show first 5
            overview_text += f"{key} = {value}\n"
        if len(audio_settings) > 5:
            overview_text += f"... and {len(audio_settings) - 5} more\n"
        overview_text += "\n"
        
        # Input settings
        input_settings = self.config_manager.get_input_settings()
        overview_text += f"INPUT SETTINGS ({len(input_settings)})\n"
        overview_text += "-" * 30 + "\n"
        for key, value in list(input_settings.items())[:5]:  # Show first 5
            overview_text += f"{key} = {value}\n"
        if len(input_settings) > 5:
            overview_text += f"... and {len(input_settings) - 5} more\n"
        
        self.settings_overview.setText(overview_text)
    
    def create_backup(self):
        """Create a new backup."""
        try:
            if self.config_manager._create_backup():
                QMessageBox.information(self, "Success", "Backup created successfully!")
                self.refresh_backups()
            else:
                QMessageBox.warning(self, "Warning", "Failed to create backup!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create backup: {str(e)}")
    
    def restore_selected_backup(self):
        """Restore the selected backup."""
        current_item = self.backup_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a backup to restore!")
            return
        
        backup_file = current_item.data(Qt.ItemDataRole.UserRole)
        if not backup_file or not backup_file.exists():
            QMessageBox.warning(self, "Warning", "Selected backup file not found!")
            return
        
        reply = QMessageBox.question(
            self, "Restore Backup",
            f"Are you sure you want to restore from backup?\n\n{backup_file.name}\n\nThis will overwrite current settings.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                shutil.copy2(backup_file, self.config_manager.config_path)
                self.config_manager._load_config()
                QMessageBox.information(self, "Success", "Backup restored successfully!")
                self.refresh_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to restore backup: {str(e)}")
    
    def delete_selected_backup(self):
        """Delete the selected backup."""
        current_item = self.backup_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a backup to delete!")
            return
        
        backup_file = current_item.data(Qt.ItemDataRole.UserRole)
        if not backup_file or not backup_file.exists():
            QMessageBox.warning(self, "Warning", "Selected backup file not found!")
            return
        
        reply = QMessageBox.question(
            self, "Delete Backup",
            f"Are you sure you want to delete this backup?\n\n{backup_file.name}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                backup_file.unlink()
                QMessageBox.information(self, "Success", "Backup deleted successfully!")
                self.refresh_backups()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete backup: {str(e)}")
    
    def open_config_file(self):
        """Open the config file in default editor."""
        if self.config_manager.config_path and self.config_manager.config_path.exists():
            try:
                os.startfile(self.config_manager.config_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open config file: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "Config file not found!")
    
    def open_backup_folder(self):
        """Open the backup folder in file explorer."""
        try:
            os.startfile(self.config_manager.BACKUP_DIR)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open backup folder: {str(e)}")


class MainWindow(QMainWindow):
    """Main window for FieldTuner."""
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.setup_ui()
        self.apply_dark_theme()
        self.update_status()
    
    def setup_ui(self):
        """Setup the main UI."""
        self.setWindowTitle("FieldTuner - Battlefield 6 Configuration Tool")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Config info
        self.info_label = QLabel()
        self.info_label.setStyleSheet("color: #888; font-size: 12px; padding: 5px;")
        main_layout.addWidget(self.info_label)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.graphics_tab = GraphicsTab(self.config_manager)
        self.audio_tab = AudioTab(self.config_manager)
        self.input_tab = InputTab(self.config_manager)
        self.settings_tab = SettingsTab(self.config_manager)
        
        # Add tabs
        self.tab_widget.addTab(self.graphics_tab, "Graphics")
        self.tab_widget.addTab(self.audio_tab, "Audio")
        self.tab_widget.addTab(self.input_tab, "Input")
        self.tab_widget.addTab(self.settings_tab, "Settings")
        
        main_layout.addWidget(self.tab_widget)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.apply_button = QPushButton("Apply Changes")
        self.apply_button.setStyleSheet("""
            QPushButton {
                background-color: #ff6b35;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e55a2b;
            }
        """)
        self.apply_button.clicked.connect(self.apply_changes)
        
        self.reset_button = QPushButton("Reset to Defaults")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        self.reset_button.clicked.connect(self.reset_to_defaults)
        
        self.backup_button = QPushButton("Restore Backup")
        self.backup_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        self.backup_button.clicked.connect(self.restore_backup)
        
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.backup_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def apply_dark_theme(self):
        """Apply dark theme to the application."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #333;
                color: #fff;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #ff6b35;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #444;
            }
            QGroupBox {
                font-weight: bold;
                color: #ff6b35;
                border: 2px solid #444;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
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
                padding: 5px;
                border-radius: 3px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #555;
                height: 8px;
                background: #333;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #ff6b35;
                border: 1px solid #555;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QStatusBar {
                background-color: #2d2d2d;
                color: #ffffff;
                border-top: 1px solid #444;
            }
        """)
    
    def update_status(self):
        """Update status information."""
        if self.config_manager.config_path:
            file_size = self.config_manager.config_path.stat().st_size
            settings_count = len(self.config_manager.config_data)
            info_text = f"Config: {self.config_manager.config_path.name} | Size: {file_size:,} bytes | Settings: {settings_count}"
            self.info_label.setText(info_text)
        else:
            self.info_label.setText("No Battlefield 6 config file found")
    
    def apply_changes(self):
        """Apply configuration changes."""
        self.status_bar.showMessage("Applying changes...")
        
        try:
            # Save settings from all tabs
            self.graphics_tab.save_settings()
            self.audio_tab.save_settings()
            self.input_tab.save_settings()
            
            # Save to file
            if self.config_manager.save_config():
                self.status_bar.showMessage("Changes applied successfully!")
                QMessageBox.information(self, "Success", "Configuration changes have been applied successfully!")
            else:
                self.status_bar.showMessage("Failed to apply changes!")
                QMessageBox.critical(self, "Error", "Failed to save configuration changes!")
        except Exception as e:
            self.status_bar.showMessage("Error applying changes!")
            QMessageBox.critical(self, "Error", f"Error applying changes: {str(e)}")
    
    def reset_to_defaults(self):
        """Reset settings to defaults."""
        reply = QMessageBox.question(
            self, "Reset to Defaults",
            "Are you sure you want to reset all settings to their default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Reset all tabs
            self.graphics_tab.load_settings()
            self.audio_tab.load_settings()
            self.input_tab.load_settings()
            self.status_bar.showMessage("Settings reset to defaults")
    
    def restore_backup(self):
        """Restore from backup."""
        if not self.config_manager.backup_path or not self.config_manager.backup_path.exists():
            QMessageBox.warning(self, "No Backup", "No backup file available!")
            return
        
        reply = QMessageBox.question(
            self, "Restore Backup",
            "Are you sure you want to restore from backup? This will overwrite current settings.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                shutil.copy2(self.config_manager.backup_path, self.config_manager.config_path)
                self.config_manager._load_config()
                self.graphics_tab.load_settings()
                self.audio_tab.load_settings()
                self.input_tab.load_settings()
                self.settings_tab.refresh_data()
                self.status_bar.showMessage("Backup restored successfully!")
                QMessageBox.information(self, "Success", "Backup restored successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to restore backup: {str(e)}")


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("FieldTuner")
    app.setApplicationVersion("1.0.0")
    
    # Enable high DPI scaling
    try:
        app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    except AttributeError:
        # PyQt6 doesn't have these attributes, skip them
        pass
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
