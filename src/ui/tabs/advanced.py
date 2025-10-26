"""
FieldTuner V2.0 - Advanced Tab
Advanced settings with search and favorites functionality.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, 
    QLabel, QLineEdit, QComboBox, QScrollArea, QPushButton, QSpinBox, QDoubleSpinBox, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

from debug import log_info, log_error, log_warning
from ui.components.custom_widgets import FocusAwareSlider, FocusAwareSpinBox, ProfessionalToggleSwitch
from settings_database import BF6_SETTINGS_DATABASE


class AdvancedTab(QWidget):
    """Advanced settings tab with search and favorites functionality."""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, config_manager, favorites_manager):
        super().__init__()
        self.config_manager = config_manager
        self.favorites_manager = favorites_manager
        self.all_settings = {}
        self.settings_loaded = False
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the advanced tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Advanced Settings")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 16px;
            padding: 8px 0px;
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
        self.search_input.setPlaceholderText("Search settings by name or description...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: #444;
                color: white;
                border: 2px solid #666;
                padding: 12px 16px;
                border-radius: 8px;
                font-size: 14px;
                min-width: 300px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
            }
        """)
        self.search_input.textChanged.connect(self.perform_search)
        search_layout.addWidget(self.search_input)
        
        # Category filter
        self.category_filter = QComboBox()
        self.category_filter.addItems(["All Categories", "Graphics", "Input", "Audio", "Network", "Game"])
        self.category_filter.setStyleSheet("""
            QComboBox {
                background: #444;
                color: white;
                border: 2px solid #666;
                padding: 12px 16px;
                border-radius: 8px;
                font-size: 14px;
                min-width: 160px;
            }
            QComboBox:focus {
                border-color: #4a90e2;
            }
        """)
        self.category_filter.currentTextChanged.connect(self.perform_search)
        search_layout.addWidget(self.category_filter)
        
        layout.addWidget(search_widget)
        
        # Settings display area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
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
        """)
        
        self.settings_widget = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_widget)
        self.settings_layout.setSpacing(12)
        
        self.scroll_area.setWidget(self.settings_widget)
        layout.addWidget(self.scroll_area)
        
        # Status label
        self.status_label = QLabel("Ready to load advanced settings")
        self.status_label.setStyleSheet("""
            color: #888;
            font-size: 12px;
            padding: 5px;
        """)
        layout.addWidget(self.status_label)
    
    def showEvent(self, event):
        """Load settings when tab is first shown."""
        super().showEvent(event)
        if not self.settings_loaded:
            QTimer.singleShot(100, self.load_settings)
    
    def load_settings(self):
        """Load advanced settings from config."""
        try:
            log_info("Loading advanced settings", "ADVANCED")
            self.status_label.setText("Loading settings...")
            
            # Clear existing settings
            while self.settings_layout.count():
                child = self.settings_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            # Create a simple settings display
            self.create_sample_settings()
            
            self.settings_loaded = True
            self.status_label.setText(f"Loaded {len(self.all_settings)} settings")
            log_info("Advanced settings loaded successfully", "ADVANCED")
            
        except Exception as e:
            log_error(f"Failed to load advanced settings: {str(e)}", "ADVANCED", e)
            self.status_label.setText("Failed to load settings")
    
    def create_sample_settings(self):
        """Create settings from the full BF6 settings database."""
        try:
            # Group settings by category
            categories = {}
            for setting_key, setting_info in BF6_SETTINGS_DATABASE.items():
                category = setting_info.get('category', 'Other')
                if category not in categories:
                    categories[category] = []
                categories[category].append((setting_key, setting_info))
            
            # Create groups for each category
            for category_name, settings in categories.items():
                if not settings:  # Skip empty categories
                    continue
                    
                group = QGroupBox(category_name)
                group.setStyleSheet(self.get_group_style())
                
                layout = QFormLayout()
                layout.setSpacing(8)
                layout.setContentsMargins(16, 16, 16, 16)
                
                for setting_key, setting_info in settings:
                    # Get current value from config
                    current_value = self.config_manager.config_data.get(setting_key, str(setting_info.get('default', '0')))
                    
                    # Create appropriate control based on setting type
                    control = self.create_control_for_setting(setting_key, setting_info, current_value)
                    
                    # Store reference
                    setattr(self, f"control_{setting_key.replace('.', '_')}", control)
                    self.all_settings[setting_key] = {
                        'control': control,
                        'display_name': setting_info.get('name', setting_key),
                        'description': setting_info.get('description', ''),
                        'tooltip': setting_info.get('tooltip', ''),
                        'group': category_name,
                        'setting_info': setting_info
                    }
                    
                    # Add tooltip if available
                    if setting_info.get('tooltip'):
                        control.setToolTip(setting_info['tooltip'])
                    
                    # Create star button for favorites
                    star_button = QPushButton("☆")
                    star_button.setStyleSheet("""
                        QPushButton {
                            background: transparent;
                            border: none;
                            color: #666;
                            font-size: 16px;
                            padding: 2px;
                            min-width: 20px;
                            max-width: 20px;
                        }
                        QPushButton:hover {
                            color: #ffd700;
                        }
                        QPushButton:pressed {
                            color: #ffd700;
                        }
                    """)
                    star_button.setCheckable(True)
                    star_button.clicked.connect(lambda checked, key=setting_key: self.toggle_favorite_setting(key, checked))
                    
                    # Check if this setting is already a favorite
                    if setting_key in self.favorites_manager.favorites:
                        star_button.setChecked(True)
                        star_button.setText("★")
                        star_button.setStyleSheet("""
                            QPushButton {
                                background: transparent;
                                border: none;
                                color: #ffd700;
                                font-size: 16px;
                                padding: 2px;
                                min-width: 20px;
                                max-width: 20px;
                            }
                        """)
                    
                    # Create horizontal layout for control and star
                    control_layout = QHBoxLayout()
                    control_layout.addWidget(control)
                    control_layout.addWidget(star_button)
                    control_layout.addStretch()
                    
                    layout.addRow(f"{setting_info.get('name', setting_key)}:", control_layout)
                
                group.setLayout(layout)
                self.settings_layout.addWidget(group)
            
            self.settings_layout.addStretch()
            
        except Exception as e:
            log_error(f"Failed to create settings from database: {str(e)}", "ADVANCED", e)
            # Fallback to simple display
            self.create_fallback_settings()
    
    def create_control_for_setting(self, setting_key, setting_info, current_value):
        """Create appropriate control for a setting based on its type."""
        setting_type = setting_info.get('type', 'string')
        
        try:
            if setting_type == 'bool':
                control = ProfessionalToggleSwitch()
                control.set_checked(float(current_value) > 0.5)
                return control
                
            elif setting_type == 'int':
                control = FocusAwareSpinBox()
                range_vals = setting_info.get('range', [0, 100])
                control.setRange(range_vals[0], range_vals[1])
                control.setValue(int(float(current_value)))
                return control
                
            elif setting_type == 'float':
                control = FocusAwareSpinBox()
                range_vals = setting_info.get('range', [0.0, 100.0])
                control.setRange(range_vals[0], range_vals[1])
                control.setDecimals(2)
                control.setSingleStep(0.1)
                control.setValue(float(current_value))
                return control
                
            else:  # string or unknown
                control = FocusAwareSpinBox()
                control.setRange(0, 100)
                try:
                    control.setValue(int(float(current_value) * 100))
                except (ValueError, TypeError):
                    control.setValue(50)
                return control
                
        except Exception as e:
            log_error(f"Failed to create control for {setting_key}: {str(e)}", "ADVANCED", e)
            # Fallback control
            control = FocusAwareSpinBox()
            control.setRange(0, 100)
            control.setValue(50)
            return control
    
    def create_fallback_settings(self):
        """Create fallback settings if database fails."""
        group = QGroupBox("Basic Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Add a few basic settings
        basic_settings = [
            ("GstRender.Dx12Enabled", "DirectX 12"),
            ("GstRender.VSyncMode", "V-Sync"),
            ("GstRender.ResolutionScale", "Resolution Scale"),
        ]
        
        for setting_key, display_name in basic_settings:
            current_value = self.config_manager.config_data.get(setting_key, '0')
            control = ProfessionalToggleSwitch()
            try:
                control.set_checked(float(current_value) > 0.5)
            except (ValueError, TypeError):
                control.set_checked(False)
            
            setattr(self, f"control_{setting_key.replace('.', '_')}", control)
            self.all_settings[setting_key] = {
                'control': control,
                'display_name': display_name,
                'description': '',
                'group': 'Basic'
            }
            
            layout.addRow(f"{display_name}:", control)
        
        group.setLayout(layout)
        self.settings_layout.addWidget(group)
    
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
    
    def perform_search(self):
        """Perform search and filter settings with optimized search."""
        try:
            search_text = self.search_input.text().lower()
            category = self.category_filter.currentText()
            
            # Use optimized search from config manager
            search_results = self.config_manager.search_settings(search_text, category)
            
            # Hide/show groups based on search results
            for i in range(self.settings_layout.count()):
                item = self.settings_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    if isinstance(widget, QGroupBox):
                        # Check if any settings in this group match the search
                        group_visible = False
                        if not search_text:  # Show all if no search
                            group_visible = True
                        else:
                            # Check if any settings in this group match
                            for setting_key, setting_info in self.all_settings.items():
                                if setting_info.get('group') == widget.title():
                                    if any(result['key'] == setting_key for result in search_results):
                                        group_visible = True
                                        break
                        
                        widget.setVisible(group_visible)
            
            log_info(f"Search performed: '{search_text}' in category '{category}' - {len(search_results)} results", "ADVANCED")
            
        except Exception as e:
            log_error(f"Failed to perform search: {str(e)}", "ADVANCED", e)
    
    def save_settings(self):
        """Save advanced settings to config."""
        try:
            log_info("Saving advanced settings", "ADVANCED")
            
            # Save all settings
            for setting_key, setting_info in self.all_settings.items():
                control = setting_info['control']
                setting_data = setting_info.get('setting_info', {})
                setting_type = setting_data.get('type', 'string')
                
                if isinstance(control, ProfessionalToggleSwitch):
                    value = '1' if control.is_checked() else '0'
                elif setting_type == 'float':
                    value = str(control.value())
                elif setting_type == 'int':
                    value = str(int(control.value()))
                else:
                    # Default handling for unknown types
                    value = str(control.value())
                
                self.config_manager.config_data[setting_key] = value
            
            self.settings_changed.emit()
            log_info("Advanced settings saved successfully", "ADVANCED")
            
        except Exception as e:
            log_error(f"Failed to save advanced settings: {str(e)}", "ADVANCED", e)
    
    def toggle_favorite_setting(self, setting_key, is_favorite):
        """Toggle a setting as favorite."""
        try:
            if is_favorite:
                self.favorites_manager.add_favorite(setting_key)
                log_info(f"Added {setting_key} to favorites", "ADVANCED")
            else:
                self.favorites_manager.remove_favorite(setting_key)
                log_info(f"Removed {setting_key} from favorites", "ADVANCED")
            
            # Emit signal to update other tabs
            self.settings_changed.emit()
            
        except Exception as e:
            log_error(f"Failed to toggle favorite for {setting_key}: {str(e)}", "ADVANCED", e)
