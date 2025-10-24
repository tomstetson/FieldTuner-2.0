"""
Game Settings Tab for FieldTuner
Handles game-related configuration options.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QSlider, QLabel,
    QCheckBox, QComboBox, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal


class GameTab(QWidget):
    """Game settings tab widget."""
    
    setting_changed = pyqtSignal(str, str)  # key, value
    
    def __init__(self, config_manager):
        """Initialize the game tab."""
        super().__init__()
        self.config_manager = config_manager
        self.controls = {}
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the game tab UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Gameplay Settings
        gameplay_group = self._create_group_box("Gameplay Settings")
        gameplay_layout = QGridLayout()
        
        # Difficulty
        gameplay_layout.addWidget(QLabel("Difficulty:"), 0, 0)
        self.difficulty = QComboBox()
        self.difficulty.addItems(["Easy", "Normal", "Hard", "Expert"])
        self.difficulty.setStyleSheet("""
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
        gameplay_layout.addWidget(self.difficulty, 0, 1)
        
        # Auto-aim
        self.auto_aim = QCheckBox("Auto-aim")
        self.auto_aim.setStyleSheet("color: #ffffff; font-size: 14px;")
        gameplay_layout.addWidget(self.auto_aim, 1, 0)
        
        # Auto-heal
        self.auto_heal = QCheckBox("Auto-heal")
        self.auto_heal.setStyleSheet("color: #ffffff; font-size: 14px;")
        gameplay_layout.addWidget(self.auto_heal, 1, 1)
        
        gameplay_group.setLayout(gameplay_layout)
        layout.addWidget(gameplay_group)
        
        # HUD Settings
        hud_group = self._create_group_box("HUD Settings")
        hud_layout = QGridLayout()
        
        # HUD Scale
        hud_layout.addWidget(QLabel("HUD Scale:"), 0, 0)
        self.hud_scale = QSlider(Qt.Orientation.Horizontal)
        self.hud_scale.setRange(50, 200)
        self.hud_scale.setValue(100)
        self.hud_scale.setStyleSheet("""
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
        hud_layout.addWidget(self.hud_scale, 0, 1)
        
        self.hud_scale_label = QLabel("100%")
        self.hud_scale_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        hud_layout.addWidget(self.hud_scale_label, 0, 2)
        
        # Minimap
        self.minimap = QCheckBox("Show Minimap")
        self.minimap.setStyleSheet("color: #ffffff; font-size: 14px;")
        hud_layout.addWidget(self.minimap, 1, 0)
        
        # Crosshair
        self.crosshair = QCheckBox("Show Crosshair")
        self.crosshair.setStyleSheet("color: #ffffff; font-size: 14px;")
        hud_layout.addWidget(self.crosshair, 1, 1)
        
        # Health Bar
        self.health_bar = QCheckBox("Show Health Bar")
        self.health_bar.setStyleSheet("color: #ffffff; font-size: 14px;")
        hud_layout.addWidget(self.health_bar, 2, 0)
        
        hud_group.setLayout(hud_layout)
        layout.addWidget(hud_group)
        
        # Chat Settings
        chat_group = self._create_group_box("Chat Settings")
        chat_layout = QGridLayout()
        
        # Chat Scale
        chat_layout.addWidget(QLabel("Chat Scale:"), 0, 0)
        self.chat_scale = QSlider(Qt.Orientation.Horizontal)
        self.chat_scale.setRange(50, 200)
        self.chat_scale.setValue(100)
        self.chat_scale.setStyleSheet("""
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
        chat_layout.addWidget(self.chat_scale, 0, 1)
        
        self.chat_scale_label = QLabel("100%")
        self.chat_scale_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        chat_layout.addWidget(self.chat_scale_label, 0, 2)
        
        # Chat Filter
        self.chat_filter = QCheckBox("Chat Filter")
        self.chat_filter.setStyleSheet("color: #ffffff; font-size: 14px;")
        chat_layout.addWidget(self.chat_filter, 1, 0)
        
        chat_group.setLayout(chat_layout)
        layout.addWidget(chat_group)
        
        # Store controls for easy access
        self.controls = {
            'GstGame.Difficulty': self.difficulty,
            'GstGame.AutoAim': self.auto_aim,
            'GstGame.AutoHeal': self.auto_heal,
            'GstGame.HUDScale': self.hud_scale,
            'GstGame.Minimap': self.minimap,
            'GstGame.Crosshair': self.crosshair,
            'GstGame.HealthBar': self.health_bar,
            'GstGame.ChatScale': self.chat_scale,
            'GstGame.ChatFilter': self.chat_filter
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
        # Difficulty
        self.difficulty.currentIndexChanged.connect(
            lambda index: self._on_setting_changed('GstGame.Difficulty', str(index))
        )
        
        # Gameplay settings
        self.auto_aim.toggled.connect(
            lambda checked: self._on_setting_changed('GstGame.AutoAim', str(int(checked)))
        )
        self.auto_heal.toggled.connect(
            lambda checked: self._on_setting_changed('GstGame.AutoHeal', str(int(checked)))
        )
        
        # HUD scale
        self.hud_scale.valueChanged.connect(self._on_hud_scale_changed)
        
        # HUD elements
        self.minimap.toggled.connect(
            lambda checked: self._on_setting_changed('GstGame.Minimap', str(int(checked)))
        )
        self.crosshair.toggled.connect(
            lambda checked: self._on_setting_changed('GstGame.Crosshair', str(int(checked)))
        )
        self.health_bar.toggled.connect(
            lambda checked: self._on_setting_changed('GstGame.HealthBar', str(int(checked)))
        )
        
        # Chat scale
        self.chat_scale.valueChanged.connect(self._on_chat_scale_changed)
        
        # Chat filter
        self.chat_filter.toggled.connect(
            lambda checked: self._on_setting_changed('GstGame.ChatFilter', str(int(checked)))
        )
    
    def _on_hud_scale_changed(self, value):
        """Handle HUD scale changes."""
        self.hud_scale_label.setText(f"{value}%")
        self._on_setting_changed('GstGame.HUDScale', str(value))
    
    def _on_chat_scale_changed(self, value):
        """Handle chat scale changes."""
        self.chat_scale_label.setText(f"{value}%")
        self._on_setting_changed('GstGame.ChatScale', str(value))
    
    def _on_setting_changed(self, key, value):
        """Handle setting changes."""
        self.setting_changed.emit(key, value)
    
    def update_from_config(self):
        """Update UI from current config."""
        game_settings = self.config_manager.get_game_settings()
        
        # Update gameplay settings
        difficulty = int(game_settings.get('GstGame.Difficulty', '1'))
        self.difficulty.setCurrentIndex(difficulty)
        
        self.auto_aim.setChecked(game_settings.get('GstGame.AutoAim', '0') == '1')
        self.auto_heal.setChecked(game_settings.get('GstGame.AutoHeal', '0') == '1')
        
        # Update HUD settings
        hud_scale = int(game_settings.get('GstGame.HUDScale', '100'))
        self.hud_scale.setValue(hud_scale)
        self.hud_scale_label.setText(f"{hud_scale}%")
        
        self.minimap.setChecked(game_settings.get('GstGame.Minimap', '1') == '1')
        self.crosshair.setChecked(game_settings.get('GstGame.Crosshair', '1') == '1')
        self.health_bar.setChecked(game_settings.get('GstGame.HealthBar', '1') == '1')
        
        # Update chat settings
        chat_scale = int(game_settings.get('GstGame.ChatScale', '100'))
        self.chat_scale.setValue(chat_scale)
        self.chat_scale_label.setText(f"{chat_scale}%")
        
        self.chat_filter.setChecked(game_settings.get('GstGame.ChatFilter', '0') == '1')
    
    def get_changes(self):
        """Get current changes from UI."""
        changes = {}
        
        changes['GstGame.Difficulty'] = str(self.difficulty.currentIndex())
        changes['GstGame.AutoAim'] = str(int(self.auto_aim.isChecked()))
        changes['GstGame.AutoHeal'] = str(int(self.auto_heal.isChecked()))
        changes['GstGame.HUDScale'] = str(self.hud_scale.value())
        changes['GstGame.Minimap'] = str(int(self.minimap.isChecked()))
        changes['GstGame.Crosshair'] = str(int(self.crosshair.isChecked()))
        changes['GstGame.HealthBar'] = str(int(self.health_bar.isChecked()))
        changes['GstGame.ChatScale'] = str(self.chat_scale.value())
        changes['GstGame.ChatFilter'] = str(int(self.chat_filter.isChecked()))
        
        return changes
    
    def reset_to_defaults(self):
        """Reset to default values."""
        self.difficulty.setCurrentIndex(1)  # Normal
        self.auto_aim.setChecked(False)
        self.auto_heal.setChecked(True)
        
        self.hud_scale.setValue(100)
        self.hud_scale_label.setText("100%")
        self.minimap.setChecked(True)
        self.crosshair.setChecked(True)
        self.health_bar.setChecked(True)
        
        self.chat_scale.setValue(100)
        self.chat_scale_label.setText("100%")
        self.chat_filter.setChecked(False)
