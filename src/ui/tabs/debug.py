"""
FieldTuner V2.0 - Debug Tab
Debug information and system diagnostics.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, 
    QLabel, QScrollArea, QMessageBox, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from pathlib import Path

from debug import log_info, log_error, log_warning


class DebugTab(QWidget):
    """Debug tab for system diagnostics and logging."""
    
    def __init__(self, config_manager, favorites_manager):
        super().__init__()
        self.config_manager = config_manager
        self.favorites_manager = favorites_manager
        self.setup_ui()
        self.load_debug_info()
    
    def setup_ui(self):
        """Setup the debug tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Debug Information")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 16px;
            padding: 8px 0px;
        """)
        layout.addWidget(header)
        
        # System info section
        self.create_system_info_section(layout)
        
        # Config info section
        self.create_config_info_section(layout)
        
        # Log viewer section
        self.create_log_viewer_section(layout)
        
        layout.addStretch()
    
    def create_system_info_section(self, parent_layout):
        """Create system information section."""
        group = QGroupBox("System Information")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # System info labels
        self.system_info = {
            "Python Version": "Python 3.13",
            "PyQt6 Version": "PyQt6 6.5.0",
            "Platform": "Windows 10",
            "Architecture": "x64"
        }
        
        for key, value in self.system_info.items():
            label = QLabel(value)
            label.setStyleSheet("color: #4a90e2; font-weight: bold;")
            layout.addRow(f"{key}:", label)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_config_info_section(self, parent_layout):
        """Create config information section."""
        group = QGroupBox("Config Information")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Config info
        config_path = str(self.config_manager.config_path) if self.config_manager.config_path else "Not found"
        settings_count = len(self.config_manager.config_data) if hasattr(self.config_manager, 'config_data') else 0
        favorites_count = len(self.favorites_manager.favorites) if hasattr(self.favorites_manager, 'favorites') else 0
        
        self.config_info = {
            "Config Path": config_path,
            "Settings Count": str(settings_count),
            "Favorites Count": str(favorites_count),
            "Config Valid": "Yes" if settings_count > 0 else "No"
        }
        
        for key, value in self.config_info.items():
            label = QLabel(value)
            label.setStyleSheet("color: #4a90e2; font-weight: bold;")
            layout.addRow(f"{key}:", label)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_log_viewer_section(self, parent_layout):
        """Create log viewer section."""
        group = QGroupBox("Debug Logs")
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Log viewer
        self.log_viewer = QTextEdit()
        self.log_viewer.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                padding: 10px;
            }
        """)
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setMaximumHeight(200)
        layout.addWidget(self.log_viewer)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Logs")
        refresh_btn.setStyleSheet(self.get_button_style())
        refresh_btn.clicked.connect(self.refresh_logs)
        layout.addWidget(refresh_btn)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
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
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5ba0f2,
                    stop:1 #4a90e2);
            }
        """
    
    def load_debug_info(self):
        """Load debug information."""
        try:
            log_info("Loading debug information", "DEBUG")
            
            # Update config info
            config_path = str(self.config_manager.config_path) if self.config_manager.config_path else "Not found"
            settings_count = len(self.config_manager.config_data) if hasattr(self.config_manager, 'config_data') else 0
            favorites_count = len(self.favorites_manager.favorites) if hasattr(self.favorites_manager, 'favorites') else 0
            
            self.config_info["Config Path"] = config_path
            self.config_info["Settings Count"] = str(settings_count)
            self.config_info["Favorites Count"] = str(favorites_count)
            self.config_info["Config Valid"] = "Yes" if settings_count > 0 else "No"
            
            # Load recent logs
            self.refresh_logs()
            
            log_info("Debug information loaded", "DEBUG")
            
        except Exception as e:
            log_error(f"Failed to load debug information: {str(e)}", "DEBUG", e)
    
    def refresh_logs(self):
        """Refresh the log viewer."""
        try:
            log_info("Refreshing debug logs", "DEBUG")
            
            # Get recent log entries (simplified)
            log_content = "Debug logs will be displayed here...\n"
            log_content += f"Config Manager: {'OK' if self.config_manager else 'ERROR'}\n"
            log_content += f"Favorites Manager: {'OK' if self.favorites_manager else 'ERROR'}\n"
            log_content += f"Settings Count: {len(self.config_manager.config_data) if hasattr(self.config_manager, 'config_data') else 0}\n"
            
            self.log_viewer.setPlainText(log_content)
            
        except Exception as e:
            log_error(f"Failed to refresh logs: {str(e)}", "DEBUG", e)
            self.log_viewer.setPlainText(f"Error loading logs: {str(e)}")
    
    def save_settings(self):
        """Save debug settings (no-op for debug tab)."""
        log_info("Debug tab has no settings to save", "DEBUG")
        pass