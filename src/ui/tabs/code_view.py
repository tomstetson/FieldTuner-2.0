"""
FieldTuner V2.0 - Code View Tab
Raw config file viewer and editor.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, 
    QLabel, QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from debug import log_info, log_error, log_warning


class CodeViewTab(QWidget):
    """Code view tab for raw config file viewing."""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, config_manager, favorites_manager):
        super().__init__()
        self.config_manager = config_manager
        self.favorites_manager = favorites_manager
        self.setup_ui()
        self.load_config()
    
    def setup_ui(self):
        """Setup the code view tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Raw Config Viewer")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 16px;
            padding: 8px 0px;
        """)
        layout.addWidget(header)
        
        # Warning label
        warning_label = QLabel("WARNING: This is a read-only view of your raw config file. Do not edit directly!")
        warning_label.setStyleSheet("""
            color: #ff6b6b;
            font-size: 14px;
            font-weight: bold;
            padding: 10px;
            background-color: #2a1a1a;
            border: 1px solid #ff6b6b;
            border-radius: 4px;
        """)
        layout.addWidget(warning_label)
        
        # Text editor
        self.text_editor = QTextEdit()
        self.text_editor.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """)
        self.text_editor.setReadOnly(True)
        layout.addWidget(self.text_editor)
        
        # Status label
        self.status_label = QLabel("Ready to display config")
        self.status_label.setStyleSheet("""
            color: #888;
            font-size: 12px;
            padding: 5px;
        """)
        layout.addWidget(self.status_label)
    
    def load_config(self):
        """Load config file content."""
        try:
            log_info("Loading config for code view", "CODEVIEW")
            
            if not self.config_manager.config_path or not self.config_manager.config_path.exists():
                self.text_editor.setPlainText("Config file not found or not accessible.")
                self.status_label.setText("Config file not found")
                return
            
            # Read config file as text
            try:
                with open(self.config_manager.config_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if content.strip():
                    self.text_editor.setPlainText(content)
                    self.status_label.setText(f"Loaded config: {self.config_manager.config_path.name}")
                else:
                    self.text_editor.setPlainText("Config file is empty or contains no readable text.")
                    self.status_label.setText("Config file is empty")
                    
            except Exception as e:
                # Try reading as binary and show hex
                try:
                    with open(self.config_manager.config_path, 'rb') as f:
                        binary_data = f.read()
                    
                    # Show first 1000 bytes as hex
                    hex_content = binary_data[:1000].hex()
                    formatted_hex = ' '.join(hex_content[i:i+2] for i in range(0, len(hex_content), 2))
                    self.text_editor.setPlainText(f"Binary config file (first 1000 bytes):\n{formatted_hex}")
                    self.status_label.setText("Binary config file (hex view)")
                    
                except Exception as e2:
                    self.text_editor.setPlainText(f"Failed to read config file: {str(e2)}")
                    self.status_label.setText("Failed to read config")
            
            log_info("Config loaded for code view", "CODEVIEW")
            
        except Exception as e:
            log_error(f"Failed to load config for code view: {str(e)}", "CODEVIEW", e)
            self.text_editor.setPlainText(f"Error loading config: {str(e)}")
            self.status_label.setText("Error loading config")
    
    def save_settings(self):
        """Save code view settings (read-only, no-op)."""
        log_info("Code view is read-only, no settings to save", "CODEVIEW")
        pass