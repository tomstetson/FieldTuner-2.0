"""
Main Window for FieldTuner
The primary interface for the Battlefield 6 configuration tool.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QLabel, QStatusBar, QMessageBox,
    QMenuBar, QMenu, QFileDialog, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QIcon, QFont

from .graphics_tab import GraphicsTab
from .audio_tab import AudioTab
from .input_tab import InputTab
from .game_tab import GameTab
from .network_tab import NetworkTab
from .advanced_tab import AdvancedTab


class MainWindow(QMainWindow):
    """Main window for FieldTuner application."""
    
    def __init__(self, config_manager):
        """Initialize the main window."""
        super().__init__()
        self.config_manager = config_manager
        self.unsaved_changes = False
        
        self._setup_ui()
        self._setup_menu()
        self._setup_status_bar()
        self._connect_signals()
        
        # Update UI with current config
        self._update_ui_from_config()
    
    def _setup_ui(self):
        """Setup the main UI components."""
        self.setWindowTitle("FieldTuner - Battlefield 6 Configuration Tool")
        self.setGeometry(100, 100, 1000, 700)
        
        # Apply dark theme
        self._apply_theme()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Config info label
        self.info_label = QLabel()
        self.info_label.setStyleSheet("color: #888; font-size: 12px;")
        main_layout.addWidget(self.info_label)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        # Create tabs
        self.graphics_tab = GraphicsTab(self.config_manager)
        self.audio_tab = AudioTab(self.config_manager)
        self.input_tab = InputTab(self.config_manager)
        self.game_tab = GameTab(self.config_manager)
        self.network_tab = NetworkTab(self.config_manager)
        self.advanced_tab = AdvancedTab(self.config_manager)
        
        # Add tabs to widget
        self.tab_widget.addTab(self.graphics_tab, "Graphics")
        self.tab_widget.addTab(self.audio_tab, "Audio")
        self.tab_widget.addTab(self.input_tab, "Input")
        self.tab_widget.addTab(self.game_tab, "Game")
        self.tab_widget.addTab(self.network_tab, "Network")
        self.tab_widget.addTab(self.advanced_tab, "Advanced")
        
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
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        
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
        
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.backup_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
    
    def _setup_menu(self):
        """Setup the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open Config File", self)
        open_action.triggered.connect(self._open_config_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save Config", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save_config)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("Export Profile", self)
        export_action.triggered.connect(self._export_profile)
        file_menu.addAction(export_action)
        
        import_action = QAction("Import Profile", self)
        import_action.triggered.connect(self._import_profile)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        validate_action = QAction("Validate Settings", self)
        validate_action.triggered.connect(self._validate_settings)
        tools_menu.addAction(validate_action)
        
        backup_action = QAction("Create Backup", self)
        backup_action.triggered.connect(self._create_backup)
        tools_menu.addAction(backup_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_status_bar(self):
        """Setup the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def _connect_signals(self):
        """Connect UI signals."""
        self.apply_button.clicked.connect(self._apply_changes)
        self.reset_button.clicked.connect(self._reset_to_defaults)
        self.backup_button.clicked.connect(self._restore_backup)
        
        # Connect tab change signals
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
    
    def _apply_theme(self):
        """Apply the dark theme to the application."""
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
            QLabel {
                color: #ffffff;
            }
            QStatusBar {
                background-color: #2d2d2d;
                color: #ffffff;
                border-top: 1px solid #444;
            }
        """)
    
    def _update_ui_from_config(self):
        """Update UI elements with current config values."""
        # Update info label
        config_info = self.config_manager.get_config_info()
        info_text = f"Config: {config_info['config_path']} | Settings: {config_info['settings_count']}"
        self.info_label.setText(info_text)
        
        # Update all tabs
        self.graphics_tab.update_from_config()
        self.audio_tab.update_from_config()
        self.input_tab.update_from_config()
        self.game_tab.update_from_config()
        self.network_tab.update_from_config()
        self.advanced_tab.update_from_config()
    
    def _on_tab_changed(self, index):
        """Handle tab change events."""
        # Update the current tab
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'update_from_config'):
            current_tab.update_from_config()
    
    def _apply_changes(self):
        """Apply configuration changes."""
        self.status_label.setText("Applying changes...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        try:
            # Collect changes from all tabs
            changes = {}
            
            # Get changes from each tab
            for i in range(self.tab_widget.count()):
                tab = self.tab_widget.widget(i)
                if hasattr(tab, 'get_changes'):
                    changes.update(tab.get_changes())
            
            # Apply changes to config manager
            for key, value in changes.items():
                self.config_manager.set_setting(key, value)
            
            # Save config
            if self.config_manager.save_config():
                self.status_label.setText("Changes applied successfully!")
                self.unsaved_changes = False
                self.apply_button.setEnabled(False)
            else:
                self.status_label.setText("Failed to apply changes!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply changes: {str(e)}")
            self.status_label.setText("Error applying changes")
        
        finally:
            self.progress_bar.setVisible(False)
    
    def _reset_to_defaults(self):
        """Reset settings to defaults."""
        reply = QMessageBox.question(
            self, "Reset to Defaults",
            "Are you sure you want to reset all settings to their default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Reset all tabs
            for i in range(self.tab_widget.count()):
                tab = self.tab_widget.widget(i)
                if hasattr(tab, 'reset_to_defaults'):
                    tab.reset_to_defaults()
            
            self.unsaved_changes = True
            self.apply_button.setEnabled(True)
            self.status_label.setText("Settings reset to defaults")
    
    def _restore_backup(self):
        """Restore from backup."""
        reply = QMessageBox.question(
            self, "Restore Backup",
            "Are you sure you want to restore from backup? This will overwrite current settings.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.config_manager.restore_backup():
                self._update_ui_from_config()
                self.status_label.setText("Backup restored successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to restore backup!")
    
    def _open_config_file(self):
        """Open a different config file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Config File", "", "PROFSAVE files (*.PROFSAVE_profile);;All files (*.*)"
        )
        
        if file_path:
            # TODO: Implement config file switching
            self.status_label.setText("Config file switching not yet implemented")
    
    def _save_config(self):
        """Save the current configuration."""
        self._apply_changes()
    
    def _export_profile(self):
        """Export current profile."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Profile", "", "JSON files (*.json);;All files (*.*)"
        )
        
        if file_path:
            # TODO: Implement profile export
            self.status_label.setText("Profile export not yet implemented")
    
    def _import_profile(self):
        """Import a profile."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Profile", "", "JSON files (*.json);;All files (*.*)"
        )
        
        if file_path:
            # TODO: Implement profile import
            self.status_label.setText("Profile import not yet implemented")
    
    def _validate_settings(self):
        """Validate current settings."""
        # TODO: Implement settings validation
        self.status_label.setText("Settings validation not yet implemented")
    
    def _create_backup(self):
        """Create a new backup."""
        if self.config_manager._create_backup():
            self.status_label.setText("Backup created successfully!")
        else:
            QMessageBox.critical(self, "Error", "Failed to create backup!")
    
    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self, "About FieldTuner",
            "FieldTuner v1.0.0\n\n"
            "A modern Windows GUI tool for managing Battlefield 6 configuration files.\n\n"
            "Features:\n"
            "• Auto-detection of Steam vs EA App installations\n"
            "• Safe configuration editing with backup/restore\n"
            "• Modern dark theme interface\n"
            "• Comprehensive settings management\n\n"
            "Built with PyQt6"
        )
    
    def closeEvent(self, event):
        """Handle application close event."""
        if self.unsaved_changes:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Do you want to save before closing?",
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                self._apply_changes()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
