"""
FieldTuner V2.0 - Preferences Tab
User preferences and application settings.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, 
    QLabel, QPushButton, QCheckBox, QSpinBox, QComboBox, QSlider, QScrollArea,
    QFileDialog, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from pathlib import Path

from debug import log_info, log_error, log_warning


class PreferencesTab(QWidget):
    """User preferences and application settings tab."""
    
    preferences_changed = pyqtSignal()
    
    def __init__(self, config_manager, favorites_manager, user_preferences):
        super().__init__()
        self.config_manager = config_manager
        self.favorites_manager = favorites_manager
        self.user_preferences = user_preferences
        self.setup_ui()
        self.load_preferences()
    
    def setup_ui(self):
        """Setup the preferences tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("⚙️ Preferences")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 16px;
            padding: 8px 0px;
        """)
        layout.addWidget(header)
        
        # Create scroll area for all preferences
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
        """)
        
        # Main content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(20)
        
        # Create preference sections
        self.create_profile_section()
        self.create_ui_section()
        self.create_performance_section()
        self.create_backup_section()
        self.create_advanced_section()
        
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
        
        # Action buttons
        self.create_action_buttons(layout)
    
    def create_profile_section(self):
        """Create profile selection section."""
        group = QGroupBox("Profile Selection")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Current profile path
        self.current_profile_label = QLabel("Current Profile:")
        self.current_profile_label.setStyleSheet("color: #e0e0e0; font-weight: bold;")
        
        self.current_profile_path = QLineEdit()
        self.current_profile_path.setReadOnly(True)
        self.current_profile_path.setStyleSheet(self.get_lineedit_style())
        layout.addRow(self.current_profile_label, self.current_profile_path)
        
        # Profile selection buttons
        button_layout = QHBoxLayout()
        
        self.browse_profile_btn = QPushButton("Browse Profile")
        self.browse_profile_btn.setStyleSheet(self.get_button_style())
        self.browse_profile_btn.clicked.connect(self.browse_profile)
        button_layout.addWidget(self.browse_profile_btn)
        
        self.auto_detect_btn = QPushButton("Auto Detect")
        self.auto_detect_btn.setStyleSheet(self.get_secondary_button_style())
        self.auto_detect_btn.clicked.connect(self.auto_detect_profile)
        button_layout.addWidget(self.auto_detect_btn)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet(self.get_secondary_button_style())
        self.refresh_btn.clicked.connect(self.refresh_profile_info)
        button_layout.addWidget(self.refresh_btn)
        
        layout.addRow("Actions:", button_layout)
        
        # Profile info
        self.profile_info_label = QLabel("Profile Information:")
        self.profile_info_label.setStyleSheet("color: #e0e0e0; font-weight: bold;")
        
        self.profile_info_text = QLabel("No profile selected")
        self.profile_info_text.setStyleSheet("color: #b0b0b0; font-size: 12px;")
        self.profile_info_text.setWordWrap(True)
        layout.addRow(self.profile_info_label, self.profile_info_text)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
        
        # Load current profile info
        self.refresh_profile_info()
    
    def create_ui_section(self):
        """Create UI preferences section."""
        group = QGroupBox("User Interface")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Auto"])
        self.theme_combo.setStyleSheet(self.get_combo_style())
        layout.addRow("Theme:", self.theme_combo)
        
        # Show tooltips
        self.show_tooltips = QCheckBox()
        self.show_tooltips.setStyleSheet(self.get_checkbox_style())
        layout.addRow("Show Tooltips:", self.show_tooltips)
        
        # Show status messages
        self.show_status_messages = QCheckBox()
        self.show_status_messages.setStyleSheet(self.get_checkbox_style())
        layout.addRow("Show Status Messages:", self.show_status_messages)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
    
    def create_performance_section(self):
        """Create performance preferences section."""
        group = QGroupBox("Performance")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Cache settings
        self.cache_settings = QCheckBox()
        self.cache_settings.setStyleSheet(self.get_checkbox_style())
        layout.addRow("Cache Settings:", self.cache_settings)
        
        # Lazy load tabs
        self.lazy_load_tabs = QCheckBox()
        self.lazy_load_tabs.setStyleSheet(self.get_checkbox_style())
        layout.addRow("Lazy Load Tabs:", self.lazy_load_tabs)
        
        # Search debounce
        self.search_debounce = QSpinBox()
        self.search_debounce.setRange(100, 1000)
        self.search_debounce.setSuffix(" ms")
        self.search_debounce.setStyleSheet(self.get_spinbox_style())
        layout.addRow("Search Debounce:", self.search_debounce)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
    
    def create_backup_section(self):
        """Create backup preferences section."""
        group = QGroupBox("Backup Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Auto backup
        self.auto_backup = QCheckBox()
        self.auto_backup.setStyleSheet(self.get_checkbox_style())
        layout.addRow("Auto Backup:", self.auto_backup)
        
        # Max backups
        self.max_backups = QSpinBox()
        self.max_backups.setRange(10, 200)
        self.max_backups.setStyleSheet(self.get_spinbox_style())
        layout.addRow("Max Backups:", self.max_backups)
        
        # Backup before save
        self.backup_before_save = QCheckBox()
        self.backup_before_save.setStyleSheet(self.get_checkbox_style())
        layout.addRow("Backup Before Save:", self.backup_before_save)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
    
    def create_advanced_section(self):
        """Create advanced preferences section."""
        group = QGroupBox("Advanced")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Show technical names
        self.show_technical_names = QCheckBox()
        self.show_technical_names.setStyleSheet(self.get_checkbox_style())
        layout.addRow("Show Technical Names:", self.show_technical_names)
        
        # Group by category
        self.group_by_category = QCheckBox()
        self.group_by_category.setStyleSheet(self.get_checkbox_style())
        layout.addRow("Group by Category:", self.group_by_category)
        
        # Show descriptions
        self.show_descriptions = QCheckBox()
        self.show_descriptions.setStyleSheet(self.get_checkbox_style())
        layout.addRow("Show Descriptions:", self.show_descriptions)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)
    
    def create_action_buttons(self, parent_layout):
        """Create action buttons."""
        button_layout = QHBoxLayout()
        
        # Save preferences button
        self.save_btn = QPushButton("Save Preferences")
        self.save_btn.setStyleSheet(self.get_button_style())
        self.save_btn.clicked.connect(self.save_preferences)
        button_layout.addWidget(self.save_btn)
        
        # Reset to defaults button
        self.reset_btn = QPushButton("Reset to Defaults")
        self.reset_btn.setStyleSheet(self.get_reset_button_style())
        self.reset_btn.clicked.connect(self.reset_preferences)
        button_layout.addWidget(self.reset_btn)
        
        button_layout.addStretch()
        parent_layout.addLayout(button_layout)
    
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
    
    def get_combo_style(self):
        """Get combo box styling."""
        return """
            QComboBox {
                background-color: #444;
                color: white;
                border: 1px solid #666;
                border-radius: 4px;
                padding: 5px;
                min-width: 120px;
            }
            QComboBox:focus {
                border: 2px solid #4a90e2;
            }
        """
    
    def get_checkbox_style(self):
        """Get checkbox styling."""
        return """
            QCheckBox {
                color: #e0e0e0;
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #666;
                border-radius: 3px;
                background-color: #333;
            }
            QCheckBox::indicator:checked {
                background-color: #4a90e2;
                border-color: #4a90e2;
            }
        """
    
    def get_spinbox_style(self):
        """Get spinbox styling."""
        return """
            QSpinBox {
                background-color: #444;
                color: white;
                border: 1px solid #666;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
            QSpinBox:focus {
                border: 2px solid #4a90e2;
            }
        """
    
    def get_button_style(self):
        """Get button styling."""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2,
                    stop:1 #357abd);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5ba0f2,
                    stop:1 #4a90e2);
            }
        """
    
    def get_reset_button_style(self):
        """Get reset button styling."""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff6b6b,
                    stop:1 #ee5a52);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff7b7b,
                    stop:1 #ff6b6b);
            }
        """
    
    def get_lineedit_style(self):
        """Get line edit styling."""
        return """
            QLineEdit {
                background-color: #444;
                color: white;
                border: 1px solid #666;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #4a90e2;
            }
        """
    
    def get_secondary_button_style(self):
        """Get secondary button styling."""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #666,
                    stop:1 #555);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #777,
                    stop:1 #666);
            }
        """
    
    def load_preferences(self):
        """Load preferences into the UI."""
        try:
            if not self.user_preferences:
                log_warning("No user preferences available", "PREFERENCES")
                return
            
            # Load UI preferences
            self.theme_combo.setCurrentText(self.user_preferences.get("ui.theme", "Dark"))
            self.show_tooltips.setChecked(self.user_preferences.get("ui.show_tooltips", True))
            self.show_status_messages.setChecked(self.user_preferences.get("ui.show_status_messages", True))
            
            # Load performance preferences
            self.cache_settings.setChecked(self.user_preferences.get("performance.cache_settings", True))
            self.lazy_load_tabs.setChecked(self.user_preferences.get("performance.lazy_load_tabs", True))
            self.search_debounce.setValue(self.user_preferences.get("performance.search_debounce_ms", 300))
            
            # Load backup preferences
            self.auto_backup.setChecked(self.user_preferences.get("backup.auto_backup", True))
            self.max_backups.setValue(self.user_preferences.get("backup.max_backups", 50))
            self.backup_before_save.setChecked(self.user_preferences.get("backup.backup_before_save", True))
            
            # Load advanced preferences
            self.show_technical_names.setChecked(self.user_preferences.get("advanced.show_technical_names", False))
            self.group_by_category.setChecked(self.user_preferences.get("advanced.group_by_category", True))
            self.show_descriptions.setChecked(self.user_preferences.get("advanced.show_descriptions", True))
            
            log_info("Preferences loaded successfully", "PREFERENCES")
            
        except Exception as e:
            log_error(f"Failed to load preferences: {str(e)}", "PREFERENCES", e)
    
    def save_preferences(self):
        """Save preferences from the UI."""
        try:
            if not self.user_preferences:
                log_warning("No user preferences available", "PREFERENCES")
                return
            
            # Save UI preferences
            self.user_preferences.set("ui.theme", self.theme_combo.currentText().lower())
            self.user_preferences.set("ui.show_tooltips", self.show_tooltips.isChecked())
            self.user_preferences.set("ui.show_status_messages", self.show_status_messages.isChecked())
            
            # Save performance preferences
            self.user_preferences.set("performance.cache_settings", self.cache_settings.isChecked())
            self.user_preferences.set("performance.lazy_load_tabs", self.lazy_load_tabs.isChecked())
            self.user_preferences.set("performance.search_debounce_ms", self.search_debounce.value())
            
            # Save backup preferences
            self.user_preferences.set("backup.auto_backup", self.auto_backup.isChecked())
            self.user_preferences.set("backup.max_backups", self.max_backups.value())
            self.user_preferences.set("backup.backup_before_save", self.backup_before_save.isChecked())
            
            # Save advanced preferences
            self.user_preferences.set("advanced.show_technical_names", self.show_technical_names.isChecked())
            self.user_preferences.set("advanced.group_by_category", self.group_by_category.isChecked())
            self.user_preferences.set("advanced.show_descriptions", self.show_descriptions.isChecked())
            
            # Save to file
            if self.user_preferences.save_preferences():
                self.preferences_changed.emit()
                log_info("Preferences saved successfully", "PREFERENCES")
            else:
                log_error("Failed to save preferences", "PREFERENCES")
            
        except Exception as e:
            log_error(f"Failed to save preferences: {str(e)}", "PREFERENCES", e)
    
    def reset_preferences(self):
        """Reset preferences to defaults."""
        try:
            if not self.user_preferences:
                log_warning("No user preferences available", "PREFERENCES")
                return
            
            if self.user_preferences.reset_to_defaults():
                self.load_preferences()
                self.preferences_changed.emit()
                log_info("Preferences reset to defaults", "PREFERENCES")
            else:
                log_error("Failed to reset preferences", "PREFERENCES")
            
        except Exception as e:
            log_error(f"Failed to reset preferences: {str(e)}", "PREFERENCES", e)
    
    def browse_profile(self):
        """Browse for a profile file."""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Battlefield 6 Profile File",
                str(Path.home() / "Documents"),
                "Profile Files (*.profile);;All Files (*)"
            )
            
            if file_path:
                profile_path = Path(file_path)
                if self._validate_profile_file(profile_path):
                    self._load_profile(profile_path)
                    log_info(f"Profile selected: {profile_path}", "PREFERENCES")
                else:
                    QMessageBox.warning(
                        self,
                        "Invalid Profile",
                        "❌ Selected file is not a valid Battlefield 6 profile file.\n\n"
                        "Please select a PROFSAVE_profile file from your Battlefield 6 settings directory."
                    )
            else:
                log_info("Profile selection cancelled", "PREFERENCES")
                
        except Exception as e:
            log_error(f"Profile selection failed: {str(e)}", "PREFERENCES", e)
            QMessageBox.critical(
                self,
                "Error",
                f"❌ Failed to select profile: {str(e)}"
            )
    
    def auto_detect_profile(self):
        """Auto-detect profile using config manager."""
        try:
            log_info("Attempting auto-detection of profile", "PREFERENCES")
            
            # Create a temporary config manager for detection
            from core.config_manager import ConfigManager
            
            # Try to detect config file
            temp_manager = ConfigManager()
            if temp_manager.config_path and temp_manager.config_path.exists():
                self._load_profile(temp_manager.config_path)
                QMessageBox.information(
                    self,
                    "Profile Detected",
                    f"✅ Profile auto-detected successfully!\n\n"
                    f"📁 {temp_manager.config_path.name}\n"
                    f"📂 {temp_manager.config_path.parent}\n"
                    f"⚙️ {len(temp_manager.config_data)} settings loaded"
                )
                log_info(f"Profile auto-detected: {temp_manager.config_path}", "PREFERENCES")
            else:
                QMessageBox.warning(
                    self,
                    "No Profile Found",
                    "❌ No Battlefield 6 profile found automatically.\n\n"
                    "Please use 'Browse Profile' to manually select your profile file."
                )
                log_warning("Auto-detection failed - no profile found", "PREFERENCES")
                
        except Exception as e:
            log_error(f"Auto-detection failed: {str(e)}", "PREFERENCES", e)
            QMessageBox.critical(
                self,
                "Auto-Detection Error",
                f"❌ Auto-detection failed: {str(e)}\n\n"
                "Please use 'Browse Profile' to manually select your profile file."
            )
    
    def refresh_profile_info(self):
        """Refresh profile information display."""
        try:
            if self.config_manager and self.config_manager.config_path:
                profile_path = self.config_manager.config_path
                self.current_profile_path.setText(str(profile_path))
                
                # Get profile info
                if profile_path.exists():
                    file_size = profile_path.stat().st_size
                    settings_count = len(self.config_manager.config_data)
                    
                    info_text = (
                        f"📁 File: {profile_path.name}\n"
                        f"📂 Path: {profile_path.parent}\n"
                        f"📊 Size: {file_size:,} bytes\n"
                        f"⚙️ Settings: {settings_count}\n"
                        f"✅ Status: Loaded and ready"
                    )
                else:
                    info_text = "❌ Profile file not found"
            else:
                self.current_profile_path.setText("No profile selected")
                info_text = "No profile selected - use Browse or Auto Detect"
            
            self.profile_info_text.setText(info_text)
            log_info("Profile info refreshed", "PREFERENCES")
            
        except Exception as e:
            log_error(f"Failed to refresh profile info: {str(e)}", "PREFERENCES", e)
            self.current_profile_path.setText("Error loading profile info")
            self.profile_info_text.setText(f"❌ Error: {str(e)}")
    
    def _validate_profile_file(self, profile_path: Path) -> bool:
        """Validate that a file is a valid Battlefield 6 profile."""
        try:
            if not profile_path.exists() or not profile_path.is_file():
                return False
            
            # Check file size
            file_size = profile_path.stat().st_size
            if file_size < 100 or file_size > 10 * 1024 * 1024:  # 100 bytes to 10MB
                return False
            
            # Check for Battlefield 6 signatures
            with open(profile_path, 'rb') as f:
                header = f.read(1024)
                
                bf6_signatures = [
                    b'PROFSAVE',
                    b'Battlefield',
                    b'GstRender',
                    b'GstInput',
                    b'GstAudio',
                ]
                
                for signature in bf6_signatures:
                    if signature in header:
                        return True
                
                # Check text content
                try:
                    text_content = header.decode('utf-8', errors='ignore')
                    if any(keyword in text_content for keyword in ['GstRender', 'GstInput', 'GstAudio', 'PROFSAVE']):
                        return True
                except:
                    pass
            
            return False
            
        except Exception as e:
            log_error(f"Profile validation error: {str(e)}", "PREFERENCES", e)
            return False
    
    def _load_profile(self, profile_path: Path):
        """Load a profile file into the config manager."""
        try:
            # Update config manager
            self.config_manager.config_path = profile_path
            self.config_manager._load_config()
            self.config_manager._create_backup()
            
            # Refresh profile info
            self.refresh_profile_info()
            
            # Emit signal to notify other components
            self.preferences_changed.emit()
            
            log_info(f"Profile loaded successfully: {profile_path}", "PREFERENCES")
            
        except Exception as e:
            log_error(f"Failed to load profile: {str(e)}", "PREFERENCES", e)
            raise
