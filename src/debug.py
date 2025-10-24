#!/usr/bin/env python3
"""
FieldTuner Debug System
Comprehensive logging and debugging for FieldTuner application
"""

import sys
import os
import logging
import traceback
import json
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal


class DebugLogger(QObject):
    """Advanced debug logger with GUI integration."""
    
    log_updated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_logging()
        self.log_buffer = []
        self.max_buffer_size = 1000
    
    def setup_logging(self):
        """Setup comprehensive logging system."""
        # Create logs directory
        self.logs_dir = Path.home() / "AppData" / "Roaming" / "FieldTuner" / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.logs_dir / f"fieldtuner_{timestamp}.log"
        
        # Create dedicated testing log file
        self.testing_log_file = self.logs_dir / "fieldtuner_testing.log"
        
        # Setup logging configuration
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger('FieldTuner')
        self.logger.info("FieldTuner Debug System Initialized")
        self.logger.info("Created by Tom with Love from Cursor - Debug System Ready!")
        
        # Log to testing file
        self.log_to_testing_file("FieldTuner Debug System Initialized")
        self.log_to_testing_file("Created by Tom with Love from Cursor - Debug System Ready!")
    
    def log_to_testing_file(self, message):
        """Log message to dedicated testing log file."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.testing_log_file, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} - {message}\n")
        except Exception as e:
            print(f"Failed to write to testing log: {e}")
    
    def log_info(self, message, category="GENERAL"):
        """Log info message."""
        formatted_msg = f"[{category}] {message}"
        self.logger.info(formatted_msg)
        self.add_to_buffer("INFO", formatted_msg)
        self.log_to_testing_file(f"INFO - {formatted_msg}")
    
    def log_warning(self, message, category="GENERAL"):
        """Log warning message."""
        formatted_msg = f"[{category}] {message}"
        self.logger.warning(formatted_msg)
        self.add_to_buffer("WARNING", formatted_msg)
        self.log_to_testing_file(f"WARNING - {formatted_msg}")
    
    def log_error(self, message, category="GENERAL", exception=None):
        """Log error message with optional exception."""
        formatted_msg = f"[{category}] {message}"
        self.logger.error(formatted_msg)
        
        if exception:
            self.logger.error(f"Exception: {str(exception)}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
        
        self.add_to_buffer("ERROR", formatted_msg)
        self.log_to_testing_file(f"ERROR - {formatted_msg}")
    
    def log_debug(self, message, category="GENERAL"):
        """Log debug message."""
        formatted_msg = f"[{category}] {message}"
        self.logger.debug(formatted_msg)
        self.add_to_buffer("DEBUG", formatted_msg)
    
    def add_to_buffer(self, level, message):
        """Add message to buffer and emit signal."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        
        self.log_buffer.append(log_entry)
        
        # Keep buffer size manageable
        if len(self.log_buffer) > self.max_buffer_size:
            self.log_buffer = self.log_buffer[-self.max_buffer_size:]
        
        # Emit signal for GUI updates
        self.log_updated.emit(log_entry)
    
    def get_recent_logs(self, count=50):
        """Get recent log entries."""
        return self.log_buffer[-count:] if self.log_buffer else []
    
    def export_logs(self, file_path=None):
        """Export logs to file."""
        if not file_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = self.logs_dir / f"export_{timestamp}.json"
        
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "log_file": str(self.log_file),
            "entries": self.log_buffer,
            "system_info": self.get_system_info()
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        return file_path
    
    def get_system_info(self):
        """Get system information for debugging."""
        import platform
        import sys
        
        return {
            "python_version": sys.version,
            "platform": platform.platform(),
            "architecture": platform.architecture(),
            "processor": platform.processor(),
            "working_directory": str(Path.cwd()),
            "environment_variables": dict(os.environ)
        }


class DebugWindow:
    """Debug window for real-time log viewing."""
    
    def __init__(self, debug_logger):
        self.debug_logger = debug_logger
        self.window = None
    
    def show_debug_window(self):
        """Show debug window."""
        if self.window is None:
            self.create_debug_window()
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()
    
    def create_debug_window(self):
        """Create debug window."""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
        
        self.window = QDialog()
        self.window.setWindowTitle("FieldTuner Debug Console")
        self.window.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout(self.window)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.log_display)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_logs)
        button_layout.addWidget(refresh_btn)
        
        export_btn = QPushButton("📁 Export Logs")
        export_btn.clicked.connect(self.export_logs)
        button_layout.addWidget(export_btn)
        
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.clicked.connect(self.clear_logs)
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Connect to logger
        self.debug_logger.log_updated.connect(self.update_log_display)
        self.refresh_logs()
    
    def refresh_logs(self):
        """Refresh log display."""
        logs = self.debug_logger.get_recent_logs(100)
        self.log_display.setPlainText('\n'.join(logs))
        # Scroll to bottom
        cursor = self.log_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_display.setTextCursor(cursor)
    
    def update_log_display(self, log_entry):
        """Update log display with new entry."""
        self.log_display.append(log_entry)
        # Auto-scroll to bottom
        cursor = self.log_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_display.setTextCursor(cursor)
    
    def export_logs(self):
        """Export logs to file."""
        file_path = self.debug_logger.export_logs()
        QMessageBox.information(self.window, "Export Complete", f"Logs exported to:\n{file_path}")
    
    def clear_logs(self):
        """Clear log display."""
        self.log_display.clear()


# Global debug logger instance
debug_logger = DebugLogger()


def log_info(message, category="GENERAL"):
    """Log info message."""
    debug_logger.log_info(message, category)


def log_warning(message, category="GENERAL"):
    """Log warning message."""
    debug_logger.log_warning(message, category)


def log_error(message, category="GENERAL", exception=None):
    """Log error message."""
    debug_logger.log_error(message, category, exception)


def log_debug(message, category="GENERAL"):
    """Log debug message."""
    debug_logger.log_debug(message, category)


def get_debug_logger():
    """Get debug logger instance."""
    return debug_logger
