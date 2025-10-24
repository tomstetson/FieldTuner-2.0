"""
Input Settings Tab for FieldTuner
Handles input-related configuration options.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QSlider, QLabel,
    QCheckBox, QComboBox, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal


class InputTab(QWidget):
    """Input settings tab widget."""
    
    setting_changed = pyqtSignal(str, str)  # key, value
    
    def __init__(self, config_manager):
        """Initialize the input tab."""
        super().__init__()
        self.config_manager = config_manager
        self.controls = {}
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the input tab UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Mouse Settings
        mouse_group = self._create_group_box("Mouse Settings")
        mouse_layout = QGridLayout()
        
        # Mouse Sensitivity
        mouse_layout.addWidget(QLabel("Mouse Sensitivity:"), 0, 0)
        self.mouse_sensitivity = QSlider(Qt.Orientation.Horizontal)
        self.mouse_sensitivity.setRange(1, 100)
        self.mouse_sensitivity.setValue(50)
        self.mouse_sensitivity.setStyleSheet("""
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
        mouse_layout.addWidget(self.mouse_sensitivity, 0, 1)
        
        self.mouse_sensitivity_label = QLabel("50")
        self.mouse_sensitivity_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        mouse_layout.addWidget(self.mouse_sensitivity_label, 0, 2)
        
        # Mouse Acceleration
        self.mouse_acceleration = QCheckBox("Mouse Acceleration")
        self.mouse_acceleration.setStyleSheet("color: #ffffff; font-size: 14px;")
        mouse_layout.addWidget(self.mouse_acceleration, 1, 0)
        
        # Raw Input
        self.raw_input = QCheckBox("Raw Input")
        self.raw_input.setStyleSheet("color: #ffffff; font-size: 14px;")
        mouse_layout.addWidget(self.raw_input, 1, 1)
        
        mouse_group.setLayout(mouse_layout)
        layout.addWidget(mouse_group)
        
        # Keyboard Settings
        keyboard_group = self._create_group_box("Keyboard Settings")
        keyboard_layout = QGridLayout()
        
        # Key Repeat Rate
        keyboard_layout.addWidget(QLabel("Key Repeat Rate:"), 0, 0)
        self.key_repeat_rate = QSlider(Qt.Orientation.Horizontal)
        self.key_repeat_rate.setRange(1, 10)
        self.key_repeat_rate.setValue(5)
        self.key_repeat_rate.setStyleSheet("""
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
        keyboard_layout.addWidget(self.key_repeat_rate, 0, 1)
        
        self.key_repeat_label = QLabel("5")
        self.key_repeat_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        keyboard_layout.addWidget(self.key_repeat_label, 0, 2)
        
        # Sticky Keys
        self.sticky_keys = QCheckBox("Sticky Keys")
        self.sticky_keys.setStyleSheet("color: #ffffff; font-size: 14px;")
        keyboard_layout.addWidget(self.sticky_keys, 1, 0)
        
        keyboard_group.setLayout(keyboard_layout)
        layout.addWidget(keyboard_group)
        
        # Gamepad Settings
        gamepad_group = self._create_group_box("Gamepad Settings")
        gamepad_layout = QGridLayout()
        
        # Gamepad Sensitivity
        gamepad_layout.addWidget(QLabel("Gamepad Sensitivity:"), 0, 0)
        self.gamepad_sensitivity = QSlider(Qt.Orientation.Horizontal)
        self.gamepad_sensitivity.setRange(1, 100)
        self.gamepad_sensitivity.setValue(50)
        self.gamepad_sensitivity.setStyleSheet("""
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
        gamepad_layout.addWidget(self.gamepad_sensitivity, 0, 1)
        
        self.gamepad_sensitivity_label = QLabel("50")
        self.gamepad_sensitivity_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        gamepad_layout.addWidget(self.gamepad_sensitivity_label, 0, 2)
        
        # Vibration
        self.vibration = QCheckBox("Vibration")
        self.vibration.setStyleSheet("color: #ffffff; font-size: 14px;")
        gamepad_layout.addWidget(self.vibration, 1, 0)
        
        # Dead Zone
        gamepad_layout.addWidget(QLabel("Dead Zone:"), 2, 0)
        self.dead_zone = QSlider(Qt.Orientation.Horizontal)
        self.dead_zone.setRange(0, 50)
        self.dead_zone.setValue(10)
        self.dead_zone.setStyleSheet("""
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
        gamepad_layout.addWidget(self.dead_zone, 2, 1)
        
        self.dead_zone_label = QLabel("10")
        self.dead_zone_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        gamepad_layout.addWidget(self.dead_zone_label, 2, 2)
        
        gamepad_group.setLayout(gamepad_layout)
        layout.addWidget(gamepad_group)
        
        # Store controls for easy access
        self.controls = {
            'GstInput.MouseSensitivity': self.mouse_sensitivity,
            'GstInput.MouseAcceleration': self.mouse_acceleration,
            'GstInput.RawInput': self.raw_input,
            'GstInput.KeyRepeatRate': self.key_repeat_rate,
            'GstInput.StickyKeys': self.sticky_keys,
            'GstInput.GamepadSensitivity': self.gamepad_sensitivity,
            'GstInput.Vibration': self.vibration,
            'GstInput.DeadZone': self.dead_zone
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
        # Mouse sensitivity
        self.mouse_sensitivity.valueChanged.connect(self._on_mouse_sensitivity_changed)
        
        # Mouse settings
        self.mouse_acceleration.toggled.connect(
            lambda checked: self._on_setting_changed('GstInput.MouseAcceleration', str(int(checked)))
        )
        self.raw_input.toggled.connect(
            lambda checked: self._on_setting_changed('GstInput.RawInput', str(int(checked)))
        )
        
        # Key repeat rate
        self.key_repeat_rate.valueChanged.connect(self._on_key_repeat_changed)
        
        # Sticky keys
        self.sticky_keys.toggled.connect(
            lambda checked: self._on_setting_changed('GstInput.StickyKeys', str(int(checked)))
        )
        
        # Gamepad sensitivity
        self.gamepad_sensitivity.valueChanged.connect(self._on_gamepad_sensitivity_changed)
        
        # Vibration
        self.vibration.toggled.connect(
            lambda checked: self._on_setting_changed('GstInput.Vibration', str(int(checked)))
        )
        
        # Dead zone
        self.dead_zone.valueChanged.connect(self._on_dead_zone_changed)
    
    def _on_mouse_sensitivity_changed(self, value):
        """Handle mouse sensitivity changes."""
        self.mouse_sensitivity_label.setText(str(value))
        self._on_setting_changed('GstInput.MouseSensitivity', str(value))
    
    def _on_key_repeat_changed(self, value):
        """Handle key repeat rate changes."""
        self.key_repeat_label.setText(str(value))
        self._on_setting_changed('GstInput.KeyRepeatRate', str(value))
    
    def _on_gamepad_sensitivity_changed(self, value):
        """Handle gamepad sensitivity changes."""
        self.gamepad_sensitivity_label.setText(str(value))
        self._on_setting_changed('GstInput.GamepadSensitivity', str(value))
    
    def _on_dead_zone_changed(self, value):
        """Handle dead zone changes."""
        self.dead_zone_label.setText(str(value))
        self._on_setting_changed('GstInput.DeadZone', str(value))
    
    def _on_setting_changed(self, key, value):
        """Handle setting changes."""
        self.setting_changed.emit(key, value)
    
    def update_from_config(self):
        """Update UI from current config."""
        input_settings = self.config_manager.get_input_settings()
        
        # Update mouse settings
        mouse_sens = int(input_settings.get('GstInput.MouseSensitivity', '50'))
        self.mouse_sensitivity.setValue(mouse_sens)
        self.mouse_sensitivity_label.setText(str(mouse_sens))
        
        self.mouse_acceleration.setChecked(input_settings.get('GstInput.MouseAcceleration', '0') == '1')
        self.raw_input.setChecked(input_settings.get('GstInput.RawInput', '0') == '1')
        
        # Update keyboard settings
        key_repeat = int(input_settings.get('GstInput.KeyRepeatRate', '5'))
        self.key_repeat_rate.setValue(key_repeat)
        self.key_repeat_label.setText(str(key_repeat))
        
        self.sticky_keys.setChecked(input_settings.get('GstInput.StickyKeys', '0') == '1')
        
        # Update gamepad settings
        gamepad_sens = int(input_settings.get('GstInput.GamepadSensitivity', '50'))
        self.gamepad_sensitivity.setValue(gamepad_sens)
        self.gamepad_sensitivity_label.setText(str(gamepad_sens))
        
        self.vibration.setChecked(input_settings.get('GstInput.Vibration', '0') == '1')
        
        dead_zone = int(input_settings.get('GstInput.DeadZone', '10'))
        self.dead_zone.setValue(dead_zone)
        self.dead_zone_label.setText(str(dead_zone))
    
    def get_changes(self):
        """Get current changes from UI."""
        changes = {}
        
        changes['GstInput.MouseSensitivity'] = str(self.mouse_sensitivity.value())
        changes['GstInput.MouseAcceleration'] = str(int(self.mouse_acceleration.isChecked()))
        changes['GstInput.RawInput'] = str(int(self.raw_input.isChecked()))
        changes['GstInput.KeyRepeatRate'] = str(self.key_repeat_rate.value())
        changes['GstInput.StickyKeys'] = str(int(self.sticky_keys.isChecked()))
        changes['GstInput.GamepadSensitivity'] = str(self.gamepad_sensitivity.value())
        changes['GstInput.Vibration'] = str(int(self.vibration.isChecked()))
        changes['GstInput.DeadZone'] = str(self.dead_zone.value())
        
        return changes
    
    def reset_to_defaults(self):
        """Reset to default values."""
        self.mouse_sensitivity.setValue(50)
        self.mouse_sensitivity_label.setText("50")
        self.mouse_acceleration.setChecked(False)
        self.raw_input.setChecked(True)
        
        self.key_repeat_rate.setValue(5)
        self.key_repeat_label.setText("5")
        self.sticky_keys.setChecked(False)
        
        self.gamepad_sensitivity.setValue(50)
        self.gamepad_sensitivity_label.setText("50")
        self.vibration.setChecked(True)
        self.dead_zone.setValue(10)
        self.dead_zone_label.setText("10")
