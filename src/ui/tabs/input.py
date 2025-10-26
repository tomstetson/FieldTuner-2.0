"""
FieldTuner V2.0 - Input Tab
Comprehensive input settings with modern UI.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, 
    QLabel, QSlider, QSpinBox, QCheckBox, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal

from debug import log_info, log_error, log_warning
from ui.components.custom_widgets import FocusAwareSlider, FocusAwareSpinBox, ProfessionalToggleSwitch


class InputTab(QWidget):
    """Input settings tab with comprehensive controls."""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, config_manager, favorites_manager):
        super().__init__()
        self.config_manager = config_manager
        self.favorites_manager = favorites_manager
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the input tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Input Settings")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 16px;
            padding: 8px 0px;
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
        group = QGroupBox("Mouse Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QGridLayout()
        layout.setSpacing(8)
        
        # Mouse Sensitivity
        self.mouse_sensitivity = FocusAwareSlider(Qt.Orientation.Horizontal)
        self.mouse_sensitivity.setRange(0, 100)
        self.mouse_sensitivity.setValue(50)
        self.mouse_sensitivity.setStyleSheet(self.get_slider_style())
        
        self.mouse_sensitivity_label = QLabel("50%")
        self.mouse_sensitivity_label.setStyleSheet("color: #4a90e2; font-weight: bold; min-width: 40px;")
        self.mouse_sensitivity.valueChanged.connect(
            lambda v: self.mouse_sensitivity_label.setText(f"{v}%")
        )
        
        layout.addWidget(QLabel("Mouse Sensitivity:"), 0, 0)
        layout.addWidget(self.mouse_sensitivity, 0, 1)
        layout.addWidget(self.mouse_sensitivity_label, 0, 2)
        
        # Mouse Smoothing
        self.mouse_smoothing = FocusAwareSlider(Qt.Orientation.Horizontal)
        self.mouse_smoothing.setRange(0, 100)
        self.mouse_smoothing.setValue(0)
        self.mouse_smoothing.setStyleSheet(self.get_slider_style())
        
        self.mouse_smoothing_label = QLabel("0%")
        self.mouse_smoothing_label.setStyleSheet("color: #4a90e2; font-weight: bold; min-width: 40px;")
        self.mouse_smoothing.valueChanged.connect(
            lambda v: self.mouse_smoothing_label.setText(f"{v}%")
        )
        
        layout.addWidget(QLabel("Mouse Smoothing:"), 1, 0)
        layout.addWidget(self.mouse_smoothing, 1, 1)
        layout.addWidget(self.mouse_smoothing_label, 1, 2)
        
        # Mouse Acceleration
        self.mouse_acceleration = ProfessionalToggleSwitch()
        layout.addWidget(QLabel("Mouse Acceleration:"), 2, 0)
        layout.addWidget(self.mouse_acceleration, 2, 1)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
    
    def create_keyboard_section(self):
        """Create keyboard settings section."""
        group = QGroupBox("Keyboard Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Key repeat rate
        self.key_repeat_rate = FocusAwareSlider(Qt.Orientation.Horizontal)
        self.key_repeat_rate.setRange(0, 100)
        self.key_repeat_rate.setValue(50)
        self.key_repeat_rate.setStyleSheet(self.get_slider_style())
        
        layout.addRow("Key Repeat Rate:", self.key_repeat_rate)
        
        # Sticky keys
        self.sticky_keys = ProfessionalToggleSwitch()
        layout.addRow("Sticky Keys:", self.sticky_keys)
        
        # Filter keys
        self.filter_keys = ProfessionalToggleSwitch()
        layout.addRow("Filter Keys:", self.filter_keys)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
    
    def create_controller_section(self):
        """Create controller settings section."""
        group = QGroupBox("Controller Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Controller sensitivity
        self.controller_sensitivity = FocusAwareSlider(Qt.Orientation.Horizontal)
        self.controller_sensitivity.setRange(0, 100)
        self.controller_sensitivity.setValue(50)
        self.controller_sensitivity.setStyleSheet(self.get_slider_style())
        
        layout.addRow("Controller Sensitivity:", self.controller_sensitivity)
        
        # Vibration
        self.vibration = ProfessionalToggleSwitch()
        layout.addRow("Vibration:", self.vibration)
        
        # Auto-aim
        self.auto_aim = ProfessionalToggleSwitch()
        layout.addRow("Auto-Aim:", self.auto_aim)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
    
    def get_group_style(self):
        """Get group box styling."""
        return """
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #e0e0e0;
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
        """
    
    def get_slider_style(self):
        """Get slider styling."""
        return """
            QSlider::groove:horizontal {
                border: 1px solid #666;
                height: 8px;
                background: #333;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #4a90e2;
                border: 1px solid #4a90e2;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #357abd;
            }
        """
    
    def load_settings(self):
        """Load input settings from config."""
        try:
            log_info("Loading input settings", "INPUT")
            
            # Load mouse settings
            self.load_mouse_settings()
            self.load_keyboard_settings()
            self.load_controller_settings()
            
            log_info("Input settings loaded successfully", "INPUT")
            
        except Exception as e:
            log_error(f"Failed to load input settings: {str(e)}", "INPUT", e)
    
    def load_mouse_settings(self):
        """Load mouse-related settings."""
        try:
            # Mouse sensitivity
            sensitivity = self.config_manager.config_data.get('GstInput.MouseSensitivity', '0.5')
            try:
                sensitivity_value = int(float(sensitivity) * 100)
                self.mouse_sensitivity.setValue(max(0, min(100, sensitivity_value)))
            except (ValueError, TypeError):
                self.mouse_sensitivity.setValue(50)
            
            # Mouse smoothing
            smoothing = self.config_manager.config_data.get('GstInput.MouseSmoothing', '0')
            try:
                smoothing_value = int(float(smoothing) * 100)
                self.mouse_smoothing.setValue(max(0, min(100, smoothing_value)))
            except (ValueError, TypeError):
                self.mouse_smoothing.setValue(0)
            
            # Mouse acceleration
            acceleration = self.config_manager.config_data.get('GstInput.MouseAcceleration', '0')
            try:
                self.mouse_acceleration.set_checked(float(acceleration) > 0.5)
            except (ValueError, TypeError):
                self.mouse_acceleration.set_checked(False)
                
        except Exception as e:
            log_error(f"Failed to load mouse settings: {str(e)}", "INPUT", e)
    
    def load_keyboard_settings(self):
        """Load keyboard settings."""
        try:
            # Key repeat rate
            repeat_rate = self.config_manager.config_data.get('GstInput.KeyRepeatRate', '0.5')
            try:
                repeat_value = int(float(repeat_rate) * 100)
                self.key_repeat_rate.setValue(max(0, min(100, repeat_value)))
            except (ValueError, TypeError):
                self.key_repeat_rate.setValue(50)
            
            # Sticky keys
            sticky = self.config_manager.config_data.get('GstInput.StickyKeys', '0')
            try:
                self.sticky_keys.set_checked(float(sticky) > 0.5)
            except (ValueError, TypeError):
                self.sticky_keys.set_checked(False)
            
            # Filter keys
            filter_keys = self.config_manager.config_data.get('GstInput.FilterKeys', '0')
            try:
                self.filter_keys.set_checked(float(filter_keys) > 0.5)
            except (ValueError, TypeError):
                self.filter_keys.set_checked(False)
                
        except Exception as e:
            log_error(f"Failed to load keyboard settings: {str(e)}", "INPUT", e)
    
    def load_controller_settings(self):
        """Load controller settings."""
        try:
            # Controller sensitivity
            controller_sens = self.config_manager.config_data.get('GstInput.ControllerSensitivity', '0.5')
            try:
                controller_value = int(float(controller_sens) * 100)
                self.controller_sensitivity.setValue(max(0, min(100, controller_value)))
            except (ValueError, TypeError):
                self.controller_sensitivity.setValue(50)
            
            # Vibration
            vibration = self.config_manager.config_data.get('GstInput.Vibration', '1')
            try:
                self.vibration.set_checked(float(vibration) > 0.5)
            except (ValueError, TypeError):
                self.vibration.set_checked(True)
            
            # Auto-aim
            auto_aim = self.config_manager.config_data.get('GstInput.AutoAim', '1')
            try:
                self.auto_aim.set_checked(float(auto_aim) > 0.5)
            except (ValueError, TypeError):
                self.auto_aim.set_checked(True)
                
        except Exception as e:
            log_error(f"Failed to load controller settings: {str(e)}", "INPUT", e)
    
    def save_settings(self):
        """Save input settings to config."""
        try:
            log_info("Saving input settings", "INPUT")
            
            # Save mouse settings
            self.save_mouse_settings()
            self.save_keyboard_settings()
            self.save_controller_settings()
            
            self.settings_changed.emit()
            log_info("Input settings saved successfully", "INPUT")
            
        except Exception as e:
            log_error(f"Failed to save input settings: {str(e)}", "INPUT", e)
    
    def save_mouse_settings(self):
        """Save mouse settings."""
        try:
            # Mouse sensitivity
            sensitivity = self.mouse_sensitivity.value() / 100.0
            self.config_manager.config_data['GstInput.MouseSensitivity'] = str(sensitivity)
            
            # Mouse smoothing
            smoothing = self.mouse_smoothing.value() / 100.0
            self.config_manager.config_data['GstInput.MouseSmoothing'] = str(smoothing)
            
            # Mouse acceleration
            acceleration = '1' if self.mouse_acceleration.is_checked() else '0'
            self.config_manager.config_data['GstInput.MouseAcceleration'] = acceleration
            
        except Exception as e:
            log_error(f"Failed to save mouse settings: {str(e)}", "INPUT", e)
    
    def save_keyboard_settings(self):
        """Save keyboard settings."""
        try:
            # Key repeat rate
            repeat_rate = self.key_repeat_rate.value() / 100.0
            self.config_manager.config_data['GstInput.KeyRepeatRate'] = str(repeat_rate)
            
            # Sticky keys
            sticky = '1' if self.sticky_keys.is_checked() else '0'
            self.config_manager.config_data['GstInput.StickyKeys'] = sticky
            
            # Filter keys
            filter_keys = '1' if self.filter_keys.is_checked() else '0'
            self.config_manager.config_data['GstInput.FilterKeys'] = filter_keys
            
        except Exception as e:
            log_error(f"Failed to save keyboard settings: {str(e)}", "INPUT", e)
    
    def save_controller_settings(self):
        """Save controller settings."""
        try:
            # Controller sensitivity
            controller_sens = self.controller_sensitivity.value() / 100.0
            self.config_manager.config_data['GstInput.ControllerSensitivity'] = str(controller_sens)
            
            # Vibration
            vibration = '1' if self.vibration.is_checked() else '0'
            self.config_manager.config_data['GstInput.Vibration'] = vibration
            
            # Auto-aim
            auto_aim = '1' if self.auto_aim.is_checked() else '0'
            self.config_manager.config_data['GstInput.AutoAim'] = auto_aim
            
        except Exception as e:
            log_error(f"Failed to save controller settings: {str(e)}", "INPUT", e)
