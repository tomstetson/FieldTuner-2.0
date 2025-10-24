"""
Audio Settings Tab for FieldTuner
Handles audio-related configuration options.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QSlider, QLabel,
    QCheckBox, QComboBox, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal


class AudioTab(QWidget):
    """Audio settings tab widget."""
    
    setting_changed = pyqtSignal(str, str)  # key, value
    
    def __init__(self, config_manager):
        """Initialize the audio tab."""
        super().__init__()
        self.config_manager = config_manager
        self.controls = {}
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the audio tab UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Master Volume
        volume_group = self._create_group_box("Volume Settings")
        volume_layout = QGridLayout()
        
        # Master Volume
        volume_layout.addWidget(QLabel("Master Volume:"), 0, 0)
        self.master_volume = QSlider(Qt.Orientation.Horizontal)
        self.master_volume.setRange(0, 100)
        self.master_volume.setValue(100)
        self.master_volume.setStyleSheet("""
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
        volume_layout.addWidget(self.master_volume, 0, 1)
        
        self.master_volume_label = QLabel("100%")
        self.master_volume_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        volume_layout.addWidget(self.master_volume_label, 0, 2)
        
        # Music Volume
        volume_layout.addWidget(QLabel("Music Volume:"), 1, 0)
        self.music_volume = QSlider(Qt.Orientation.Horizontal)
        self.music_volume.setRange(0, 100)
        self.music_volume.setValue(80)
        self.music_volume.setStyleSheet("""
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
        volume_layout.addWidget(self.music_volume, 1, 1)
        
        self.music_volume_label = QLabel("80%")
        self.music_volume_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        volume_layout.addWidget(self.music_volume_label, 1, 2)
        
        # SFX Volume
        volume_layout.addWidget(QLabel("SFX Volume:"), 2, 0)
        self.sfx_volume = QSlider(Qt.Orientation.Horizontal)
        self.sfx_volume.setRange(0, 100)
        self.sfx_volume.setValue(100)
        self.sfx_volume.setStyleSheet("""
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
        volume_layout.addWidget(self.sfx_volume, 2, 1)
        
        self.sfx_volume_label = QLabel("100%")
        self.sfx_volume_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        volume_layout.addWidget(self.sfx_volume_label, 2, 2)
        
        volume_group.setLayout(volume_layout)
        layout.addWidget(volume_group)
        
        # Audio Quality
        quality_group = self._create_group_box("Audio Quality")
        quality_layout = QGridLayout()
        
        # Audio Quality
        quality_layout.addWidget(QLabel("Audio Quality:"), 0, 0)
        self.audio_quality = QComboBox()
        self.audio_quality.addItems(["Low", "Medium", "High", "Ultra"])
        self.audio_quality.setStyleSheet("""
            QComboBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
        """)
        quality_layout.addWidget(self.audio_quality, 0, 1)
        
        # Audio Channels
        quality_layout.addWidget(QLabel("Audio Channels:"), 1, 0)
        self.audio_channels = QComboBox()
        self.audio_channels.addItems(["Stereo", "5.1 Surround", "7.1 Surround"])
        self.audio_channels.setStyleSheet("""
            QComboBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
        """)
        quality_layout.addWidget(self.audio_channels, 1, 1)
        
        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)
        
        # Audio Features
        features_group = self._create_group_box("Audio Features")
        features_layout = QGridLayout()
        
        self.audio_3d = QCheckBox("3D Audio")
        self.audio_3d.setStyleSheet("color: #ffffff; font-size: 14px;")
        features_layout.addWidget(self.audio_3d, 0, 0)
        
        self.audio_compression = QCheckBox("Audio Compression")
        self.audio_compression.setStyleSheet("color: #ffffff; font-size: 14px;")
        features_layout.addWidget(self.audio_compression, 0, 1)
        
        self.audio_enhancement = QCheckBox("Audio Enhancement")
        self.audio_enhancement.setStyleSheet("color: #ffffff; font-size: 14px;")
        features_layout.addWidget(self.audio_enhancement, 1, 0)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        # Store controls for easy access
        self.controls = {
            'GstAudio.MasterVolume': self.master_volume,
            'GstAudio.MusicVolume': self.music_volume,
            'GstAudio.SFXVolume': self.sfx_volume,
            'GstAudio.Quality': self.audio_quality,
            'GstAudio.Channels': self.audio_channels,
            'GstAudio.3DEnabled': self.audio_3d,
            'GstAudio.CompressionEnabled': self.audio_compression,
            'GstAudio.EnhancementEnabled': self.audio_enhancement
        }
        
        layout.addStretch()
    
    def _create_group_box(self, title):
        """Create a styled group box."""
        group = QGroupBox(title)
        group.setStyleSheet("""
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
        """)
        return group
    
    def _connect_signals(self):
        """Connect UI signals."""
        # Volume sliders
        self.master_volume.valueChanged.connect(self._on_master_volume_changed)
        self.music_volume.valueChanged.connect(self._on_music_volume_changed)
        self.sfx_volume.valueChanged.connect(self._on_sfx_volume_changed)
        
        # Combo boxes
        self.audio_quality.currentIndexChanged.connect(
            lambda index: self._on_setting_changed('GstAudio.Quality', str(index))
        )
        self.audio_channels.currentIndexChanged.connect(
            lambda index: self._on_setting_changed('GstAudio.Channels', str(index))
        )
        
        # Check boxes
        self.audio_3d.toggled.connect(
            lambda checked: self._on_setting_changed('GstAudio.3DEnabled', str(int(checked)))
        )
        self.audio_compression.toggled.connect(
            lambda checked: self._on_setting_changed('GstAudio.CompressionEnabled', str(int(checked)))
        )
        self.audio_enhancement.toggled.connect(
            lambda checked: self._on_setting_changed('GstAudio.EnhancementEnabled', str(int(checked)))
        )
    
    def _on_master_volume_changed(self, value):
        """Handle master volume changes."""
        self.master_volume_label.setText(f"{value}%")
        self._on_setting_changed('GstAudio.MasterVolume', str(value))
    
    def _on_music_volume_changed(self, value):
        """Handle music volume changes."""
        self.music_volume_label.setText(f"{value}%")
        self._on_setting_changed('GstAudio.MusicVolume', str(value))
    
    def _on_sfx_volume_changed(self, value):
        """Handle SFX volume changes."""
        self.sfx_volume_label.setText(f"{value}%")
        self._on_setting_changed('GstAudio.SFXVolume', str(value))
    
    def _on_setting_changed(self, key, value):
        """Handle setting changes."""
        self.setting_changed.emit(key, value)
    
    def update_from_config(self):
        """Update UI from current config."""
        audio_settings = self.config_manager.get_audio_settings()
        
        # Update volume settings
        master_vol = int(audio_settings.get('GstAudio.MasterVolume', '100'))
        self.master_volume.setValue(master_vol)
        self.master_volume_label.setText(f"{master_vol}%")
        
        music_vol = int(audio_settings.get('GstAudio.MusicVolume', '80'))
        self.music_volume.setValue(music_vol)
        self.music_volume_label.setText(f"{music_vol}%")
        
        sfx_vol = int(audio_settings.get('GstAudio.SFXVolume', '100'))
        self.sfx_volume.setValue(sfx_vol)
        self.sfx_volume_label.setText(f"{sfx_vol}%")
        
        # Update quality settings
        quality = int(audio_settings.get('GstAudio.Quality', '2'))
        self.audio_quality.setCurrentIndex(quality)
        
        channels = int(audio_settings.get('GstAudio.Channels', '0'))
        self.audio_channels.setCurrentIndex(channels)
        
        # Update features
        self.audio_3d.setChecked(audio_settings.get('GstAudio.3DEnabled', '0') == '1')
        self.audio_compression.setChecked(audio_settings.get('GstAudio.CompressionEnabled', '0') == '1')
        self.audio_enhancement.setChecked(audio_settings.get('GstAudio.EnhancementEnabled', '0') == '1')
    
    def get_changes(self):
        """Get current changes from UI."""
        changes = {}
        
        changes['GstAudio.MasterVolume'] = str(self.master_volume.value())
        changes['GstAudio.MusicVolume'] = str(self.music_volume.value())
        changes['GstAudio.SFXVolume'] = str(self.sfx_volume.value())
        changes['GstAudio.Quality'] = str(self.audio_quality.currentIndex())
        changes['GstAudio.Channels'] = str(self.audio_channels.currentIndex())
        changes['GstAudio.3DEnabled'] = str(int(self.audio_3d.isChecked()))
        changes['GstAudio.CompressionEnabled'] = str(int(self.audio_compression.isChecked()))
        changes['GstAudio.EnhancementEnabled'] = str(int(self.audio_enhancement.isChecked()))
        
        return changes
    
    def reset_to_defaults(self):
        """Reset to default values."""
        self.master_volume.setValue(100)
        self.master_volume_label.setText("100%")
        self.music_volume.setValue(80)
        self.music_volume_label.setText("80%")
        self.sfx_volume.setValue(100)
        self.sfx_volume_label.setText("100%")
        self.audio_quality.setCurrentIndex(2)  # High
        self.audio_channels.setCurrentIndex(0)  # Stereo
        self.audio_3d.setChecked(True)
        self.audio_compression.setChecked(False)
        self.audio_enhancement.setChecked(True)
