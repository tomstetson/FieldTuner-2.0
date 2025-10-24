#!/usr/bin/env python3
"""
FieldTuner - Completely Overhauled GUI
Clean, intuitive interface with code view and optimal settings recommendations
"""

import sys
import os
import re
import shutil
import json
from pathlib import Path
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QLabel, QPushButton, QSlider, QCheckBox, QComboBox,
    QSpinBox, QDoubleSpinBox, QGroupBox, QGridLayout, QTextEdit,
    QMessageBox, QFileDialog, QStatusBar, QProgressBar, QSplitter,
    QListWidget, QListWidgetItem, QFrame, QScrollArea, QPlainTextEdit,
    QPushButton, QLineEdit, QFormLayout, QButtonGroup, QRadioButton
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QTextCursor


class ConfigManager:
    """Enhanced config manager with optimal settings recommendations."""
    
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
        
        # Optimal settings recommendations
        self.optimal_settings = {
            'competitive': {
                'GstRender.Dx12Enabled': '1',
                'GstRender.FullscreenMode': '1',
                'GstRender.VSyncMode': '0',
                'GstRender.FutureFrameRendering': '1',
                'GstRender.MotionBlurWorld': '0',
                'GstRender.WeaponDOF': '0',
                'GstRender.ChromaticAberration': '0',
                'GstRender.VolumetricQuality': '0',
                'GstRender.AmbientOcclusion': '0',
                'GstRender.AntiAliasingDeferred': '1',
                'GstRender.AntiAliasingPost': '0',
                'GstRender.TerrainQuality': '0',
                'GstRender.VegetationQuality': '0',
                'GstRender.EffectsQuality': '0',
                'GstRender.MeshQuality': '0',
                'GstRender.TextureQuality': '1',
                'GstRender.LightingQuality': '0',
                'GstRender.PostProcessQuality': '0',
                'GstRender.ShadowQuality': '0',
                'GstRender.UnderwaterQuality': '0',
                'GstRender.UndergrowthQuality': '0'
            },
            'balanced': {
                'GstRender.Dx12Enabled': '1',
                'GstRender.FullscreenMode': '1',
                'GstRender.VSyncMode': '0',
                'GstRender.FutureFrameRendering': '1',
                'GstRender.MotionBlurWorld': '0.5',
                'GstRender.WeaponDOF': '1',
                'GstRender.ChromaticAberration': '1',
                'GstRender.VolumetricQuality': '1',
                'GstRender.AmbientOcclusion': '1',
                'GstRender.AntiAliasingDeferred': '2',
                'GstRender.AntiAliasingPost': '1',
                'GstRender.TerrainQuality': '1',
                'GstRender.VegetationQuality': '1',
                'GstRender.EffectsQuality': '1',
                'GstRender.MeshQuality': '1',
                'GstRender.TextureQuality': '2',
                'GstRender.LightingQuality': '1',
                'GstRender.PostProcessQuality': '1',
                'GstRender.ShadowQuality': '1',
                'GstRender.UnderwaterQuality': '1',
                'GstRender.UndergrowthQuality': '1'
            },
            'quality': {
                'GstRender.Dx12Enabled': '1',
                'GstRender.FullscreenMode': '1',
                'GstRender.VSyncMode': '1',
                'GstRender.FutureFrameRendering': '1',
                'GstRender.MotionBlurWorld': '1',
                'GstRender.WeaponDOF': '1',
                'GstRender.ChromaticAberration': '1',
                'GstRender.VolumetricQuality': '2',
                'GstRender.AmbientOcclusion': '2',
                'GstRender.AntiAliasingDeferred': '3',
                'GstRender.AntiAliasingPost': '2',
                'GstRender.TerrainQuality': '2',
                'GstRender.VegetationQuality': '2',
                'GstRender.EffectsQuality': '2',
                'GstRender.MeshQuality': '2',
                'GstRender.TextureQuality': '3',
                'GstRender.LightingQuality': '2',
                'GstRender.PostProcessQuality': '2',
                'GstRender.ShadowQuality': '2',
                'GstRender.UnderwaterQuality': '2',
                'GstRender.UndergrowthQuality': '2'
            }
        }
        
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
    
    def apply_optimal_settings(self, preset):
        """Apply optimal settings preset."""
        if preset in self.optimal_settings:
            for key, value in self.optimal_settings[preset].items():
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


class QuickSettingsTab(QWidget):
    """Quick settings tab with presets and common options."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Quick Settings")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #ff6b35; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Preset Buttons
        preset_group = QGroupBox("Performance Presets")
        preset_layout = QHBoxLayout()
        
        self.competitive_btn = QPushButton("Competitive")
        self.competitive_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        """)
        self.competitive_btn.clicked.connect(lambda: self.apply_preset('competitive'))
        
        self.balanced_btn = QPushButton("Balanced")
        self.balanced_btn.setStyleSheet("""
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
        """)
        self.balanced_btn.clicked.connect(lambda: self.apply_preset('balanced'))
        
        self.quality_btn = QPushButton("Quality")
        self.quality_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1b5e20;
            }
        """)
        self.quality_btn.clicked.connect(lambda: self.apply_preset('quality'))
        
        preset_layout.addWidget(self.competitive_btn)
        preset_layout.addWidget(self.balanced_btn)
        preset_layout.addWidget(self.quality_btn)
        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)
        
        # Quick Toggles
        toggles_group = QGroupBox("Quick Toggles")
        toggles_layout = QGridLayout()
        
        self.dx12_toggle = QCheckBox("DirectX 12")
        self.dx12_toggle.setStyleSheet("color: white; font-size: 12px;")
        toggles_layout.addWidget(self.dx12_toggle, 0, 0)
        
        self.vsync_toggle = QCheckBox("VSync")
        self.vsync_toggle.setStyleSheet("color: white; font-size: 12px;")
        toggles_layout.addWidget(self.vsync_toggle, 0, 1)
        
        self.motion_blur_toggle = QCheckBox("Motion Blur")
        self.motion_blur_toggle.setStyleSheet("color: white; font-size: 12px;")
        toggles_layout.addWidget(self.motion_blur_toggle, 1, 0)
        
        self.ao_toggle = QCheckBox("Ambient Occlusion")
        self.ao_toggle.setStyleSheet("color: white; font-size: 12px;")
        toggles_layout.addWidget(self.ao_toggle, 1, 1)
        
        toggles_group.setLayout(toggles_layout)
        layout.addWidget(toggles_group)
        
        # Resolution Scale
        scale_group = QGroupBox("Resolution Scale")
        scale_layout = QHBoxLayout()
        
        self.resolution_scale = QSlider(Qt.Orientation.Horizontal)
        self.resolution_scale.setRange(50, 200)
        self.resolution_scale.setValue(100)
        self.resolution_scale.setStyleSheet("""
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
        """)
        
        self.scale_label = QLabel("100%")
        self.scale_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; min-width: 50px;")
        
        scale_layout.addWidget(QLabel("Scale:"))
        scale_layout.addWidget(self.resolution_scale)
        scale_layout.addWidget(self.scale_label)
        scale_group.setLayout(scale_layout)
        layout.addWidget(scale_group)
        
        # Connect signals
        self.resolution_scale.valueChanged.connect(self.on_scale_changed)
        
        layout.addStretch()
    
    def on_scale_changed(self, value):
        self.scale_label.setText(f"{value}%")
    
    def apply_preset(self, preset):
        """Apply a settings preset."""
        if self.config_manager.apply_optimal_settings(preset):
            self.load_settings()
            QMessageBox.information(self, "Preset Applied", f"{preset.title()} preset has been applied!")
        else:
            QMessageBox.warning(self, "Error", "Failed to apply preset!")
    
    def load_settings(self):
        """Load settings from config manager."""
        graphics_settings = self.config_manager.get_graphics_settings()
        
        # Toggles
        self.dx12_toggle.setChecked(graphics_settings.get('GstRender.Dx12Enabled', '0') == '1')
        self.vsync_toggle.setChecked(graphics_settings.get('GstRender.VSyncMode', '0') != '0')
        self.motion_blur_toggle.setChecked(graphics_settings.get('GstRender.MotionBlurWorld', '0') != '0')
        self.ao_toggle.setChecked(graphics_settings.get('GstRender.AmbientOcclusion', '0') != '0')
        
        # Resolution scale
        scale = float(graphics_settings.get('GstRender.ResolutionScale', '1.0'))
        self.resolution_scale.setValue(int(scale * 100))
        self.scale_label.setText(f"{int(scale * 100)}%")
    
    def save_settings(self):
        """Save settings to config manager."""
        # Toggles
        self.config_manager.set_setting('GstRender.Dx12Enabled', str(int(self.dx12_toggle.isChecked())))
        self.config_manager.set_setting('GstRender.VSyncMode', str(1 if self.vsync_toggle.isChecked() else 0))
        self.config_manager.set_setting('GstRender.MotionBlurWorld', str(0.5 if self.motion_blur_toggle.isChecked() else 0))
        self.config_manager.set_setting('GstRender.AmbientOcclusion', str(1 if self.ao_toggle.isChecked() else 0))
        
        # Resolution scale
        scale = self.resolution_scale.value() / 100.0
        self.config_manager.set_setting('GstRender.ResolutionScale', str(scale))


class GraphicsTab(QWidget):
    """Clean graphics settings tab."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Display Settings
        display_group = QGroupBox("Display Settings")
        display_layout = QFormLayout()
        
        self.fullscreen_mode = QComboBox()
        self.fullscreen_mode.addItems(["Windowed", "Borderless", "Fullscreen"])
        display_layout.addRow("Fullscreen Mode:", self.fullscreen_mode)
        
        self.aspect_ratio = QComboBox()
        self.aspect_ratio.addItems(["Auto", "4:3", "16:9", "16:10", "21:9"])
        display_layout.addRow("Aspect Ratio:", self.aspect_ratio)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # Quality Settings
        quality_group = QGroupBox("Quality Settings")
        quality_layout = QFormLayout()
        
        self.texture_quality = QComboBox()
        self.texture_quality.addItems(["Low", "Medium", "High", "Ultra"])
        quality_layout.addRow("Texture Quality:", self.texture_quality)
        
        self.shadow_quality = QComboBox()
        self.shadow_quality.addItems(["Low", "Medium", "High", "Ultra"])
        quality_layout.addRow("Shadow Quality:", self.shadow_quality)
        
        self.effects_quality = QComboBox()
        self.effects_quality.addItems(["Low", "Medium", "High", "Ultra"])
        quality_layout.addRow("Effects Quality:", self.effects_quality)
        
        self.mesh_quality = QComboBox()
        self.mesh_quality.addItems(["Low", "Medium", "High", "Ultra"])
        quality_layout.addRow("Mesh Quality:", self.mesh_quality)
        
        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)
        
        # Anti-Aliasing
        aa_group = QGroupBox("Anti-Aliasing")
        aa_layout = QFormLayout()
        
        self.aa_method = QComboBox()
        self.aa_method.addItems(["Off", "FXAA", "TAA", "TAA High"])
        aa_layout.addRow("Method:", self.aa_method)
        
        aa_group.setLayout(aa_layout)
        layout.addWidget(aa_group)
        
        layout.addStretch()
    
    def load_settings(self):
        """Load settings from config manager."""
        graphics_settings = self.config_manager.get_graphics_settings()
        
        # Display
        fullscreen_mode = int(graphics_settings.get('GstRender.FullscreenMode', '0'))
        self.fullscreen_mode.setCurrentIndex(min(fullscreen_mode, 2))
        
        aspect_ratio = int(graphics_settings.get('GstRender.AspectRatio', '0'))
        self.aspect_ratio.setCurrentIndex(min(aspect_ratio, 4))
        
        # Quality
        texture_quality = int(graphics_settings.get('GstRender.TextureQuality', '1'))
        self.texture_quality.setCurrentIndex(min(texture_quality, 3))
        
        shadow_quality = int(graphics_settings.get('GstRender.ShadowQuality', '1'))
        self.shadow_quality.setCurrentIndex(min(shadow_quality, 3))
        
        effects_quality = int(graphics_settings.get('GstRender.EffectsQuality', '1'))
        self.effects_quality.setCurrentIndex(min(effects_quality, 3))
        
        mesh_quality = int(graphics_settings.get('GstRender.MeshQuality', '1'))
        self.mesh_quality.setCurrentIndex(min(mesh_quality, 3))
        
        # Anti-aliasing
        aa_deferred = int(graphics_settings.get('GstRender.AntiAliasingDeferred', '1'))
        self.aa_method.setCurrentIndex(min(aa_deferred, 3))
    
    def save_settings(self):
        """Save settings to config manager."""
        # Display
        self.config_manager.set_setting('GstRender.FullscreenMode', str(self.fullscreen_mode.currentIndex()))
        self.config_manager.set_setting('GstRender.AspectRatio', str(self.aspect_ratio.currentIndex()))
        
        # Quality
        self.config_manager.set_setting('GstRender.TextureQuality', str(self.texture_quality.currentIndex()))
        self.config_manager.set_setting('GstRender.ShadowQuality', str(self.shadow_quality.currentIndex()))
        self.config_manager.set_setting('GstRender.EffectsQuality', str(self.effects_quality.currentIndex()))
        self.config_manager.set_setting('GstRender.MeshQuality', str(self.mesh_quality.currentIndex()))
        
        # Anti-aliasing
        self.config_manager.set_setting('GstRender.AntiAliasingDeferred', str(self.aa_method.currentIndex()))


class CodeViewTab(QWidget):
    """Code view tab for direct config editing."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.load_config()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        
        header_label = QLabel("Config File Editor")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ff6b35;")
        header_layout.addWidget(header_label)
        
        header_layout.addStretch()
        
        self.reload_btn = QPushButton("Reload")
        self.reload_btn.setStyleSheet("""
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
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                line-height: 1.4;
            }
        """)
        self.code_editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        layout.addWidget(self.code_editor)
        
        # Info
        info_label = QLabel("Edit the config file directly. Changes will be applied when you save.")
        info_label.setStyleSheet("color: #888; font-size: 11px; padding: 5px;")
        layout.addWidget(info_label)
    
    def load_config(self):
        """Load config file into editor."""
        if self.config_manager.config_path and self.config_manager.config_path.exists():
            try:
                with open(self.config_manager.config_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                self.code_editor.setPlainText(content)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load config file: {str(e)}")
        else:
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
                return True
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save config file: {str(e)}")
                return False
        return False


class BackupTab(QWidget):
    """Clean backup management tab."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.refresh_backups()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("Backup Management")
        header.setStyleSheet("font-size: 16px; font-weight: bold; color: #ff6b35;")
        layout.addWidget(header)
        
        # Backup actions
        actions_layout = QHBoxLayout()
        
        self.create_backup_btn = QPushButton("Create Backup")
        self.create_backup_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        self.create_backup_btn.clicked.connect(self.create_backup)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_backups)
        
        actions_layout.addWidget(self.create_backup_btn)
        actions_layout.addWidget(self.refresh_btn)
        actions_layout.addStretch()
        
        layout.addLayout(actions_layout)
        
        # Backup list
        self.backup_list = QListWidget()
        self.backup_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #444;
            }
            QListWidget::item:selected {
                background-color: #ff6b35;
            }
        """)
        layout.addWidget(self.backup_list)
        
        # Backup actions
        backup_actions_layout = QHBoxLayout()
        
        self.restore_btn = QPushButton("Restore Selected")
        self.restore_btn.setStyleSheet("""
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
        self.restore_btn.clicked.connect(self.restore_backup)
        
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setStyleSheet("""
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
        self.delete_btn.clicked.connect(self.delete_backup)
        
        backup_actions_layout.addWidget(self.restore_btn)
        backup_actions_layout.addWidget(self.delete_btn)
        backup_actions_layout.addStretch()
        
        layout.addLayout(backup_actions_layout)
    
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
            item_text = f"{backup_file.name} - {timestamp.strftime('%Y-%m-%d %H:%M:%S')} ({size:,} bytes)"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, backup_file)
            self.backup_list.addItem(item)
    
    def restore_backup(self):
        """Restore selected backup."""
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
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to restore backup: {str(e)}")
    
    def delete_backup(self):
        """Delete selected backup."""
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


class MainWindow(QMainWindow):
    """Completely overhauled main window."""
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.setup_ui()
        self.apply_clean_theme()
        self.update_status()
    
    def setup_ui(self):
        """Setup the clean UI."""
        self.setWindowTitle("FieldTuner - Battlefield 6 Configuration Tool")
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("FieldTuner")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ff6b35;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Status info
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #888; font-size: 12px;")
        header_layout.addWidget(self.status_label)
        
        main_layout.addLayout(header_layout)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #444;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #333;
                color: #fff;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #ff6b35;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #444;
            }
        """)
        
        # Create tabs
        self.quick_tab = QuickSettingsTab(self.config_manager)
        self.graphics_tab = GraphicsTab(self.config_manager)
        self.code_tab = CodeViewTab(self.config_manager)
        self.backup_tab = BackupTab(self.config_manager)
        
        # Add tabs
        self.tab_widget.addTab(self.quick_tab, "Quick Settings")
        self.tab_widget.addTab(self.graphics_tab, "Graphics")
        self.tab_widget.addTab(self.code_tab, "Code View")
        self.tab_widget.addTab(self.backup_tab, "Backups")
        
        main_layout.addWidget(self.tab_widget)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.apply_btn = QPushButton("Apply Changes")
        self.apply_btn.setStyleSheet("""
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
        """)
        self.apply_btn.clicked.connect(self.apply_changes)
        
        self.reset_btn = QPushButton("Reset to Defaults")
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def apply_clean_theme(self):
        """Apply clean, modern theme."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QGroupBox {
                font-weight: bold;
                color: #ff6b35;
                border: 2px solid #444;
                border-radius: 8px;
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
                padding: 6px;
                border-radius: 4px;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
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
            self.status_label.setText(f"Config: {self.config_manager.config_path.name} | {file_size:,} bytes | {settings_count} settings")
        else:
            self.status_label.setText("No Battlefield 6 config file found")
    
    def apply_changes(self):
        """Apply configuration changes."""
        self.status_bar.showMessage("Applying changes...")
        
        try:
            # Save settings from all tabs
            self.quick_tab.save_settings()
            self.graphics_tab.save_settings()
            
            # Save code view if it was modified
            if hasattr(self.code_tab, 'save_config'):
                if not self.code_tab.save_config():
                    QMessageBox.critical(self, "Error", "Failed to save code view changes!")
                    return
            
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
            self.quick_tab.load_settings()
            self.graphics_tab.load_settings()
            self.code_tab.load_config()
            self.status_bar.showMessage("Settings reset to defaults")


def main():
    """Main application entry point."""
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
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
