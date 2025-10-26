"""
FieldTuner V2.0 - Enhanced Error Handling System
Comprehensive error handling with user-friendly feedback and recovery options.
"""

from PyQt6.QtWidgets import (
    QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QScrollArea, QWidget, QCheckBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from debug import log_info, log_error, log_warning
from ui.theme import theme_manager
from typing import Optional, Dict, Any, List
import traceback
import sys
from datetime import datetime


class ErrorSeverity:
    """Error severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorCategory:
    """Error categories for better organization."""
    CONFIG = "configuration"
    FILE = "file_operation"
    NETWORK = "network"
    UI = "user_interface"
    SYSTEM = "system"
    VALIDATION = "validation"
    PERMISSION = "permission"


class FieldTunerError(Exception):
    """Base exception for FieldTuner with enhanced error information."""
    
    def __init__(self, message: str, category: str = ErrorCategory.SYSTEM, 
                 severity: str = ErrorSeverity.ERROR, details: Optional[Dict[str, Any]] = None,
                 recovery_action: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.category = category
        self.severity = severity
        self.details = details or {}
        self.recovery_action = recovery_action
        self.timestamp = datetime.now()
        self.traceback = traceback.format_exc()


class ErrorDialog(QDialog):
    """Enhanced error dialog with detailed information and recovery options."""
    
    def __init__(self, error: FieldTunerError, parent=None):
        super().__init__(parent)
        self.error = error
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup the error dialog UI."""
        self.setWindowTitle(f"FieldTuner Error - {self.error.category.title()}")
        self.setModal(True)
        self.setMinimumSize(500, 400)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(theme_manager.get_spacing('md'))
        layout.setContentsMargins(
            int(theme_manager.get_spacing('lg').replace('px', '')),
            int(theme_manager.get_spacing('lg').replace('px', '')),
            int(theme_manager.get_spacing('lg').replace('px', '')),
            int(theme_manager.get_spacing('lg').replace('px', ''))
        )
        
        # Header
        self.create_header(layout)
        
        # Error message
        self.create_message_section(layout)
        
        # Details section (collapsible)
        self.create_details_section(layout)
        
        # Recovery section
        if self.error.recovery_action:
            self.create_recovery_section(layout)
        
        # Action buttons
        self.create_action_buttons(layout)
        
        # Apply theme
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme_manager.get_color('bg_primary')};
                color: {theme_manager.get_color('text_primary')};
            }}
        """)
    
    def create_header(self, layout):
        """Create the error dialog header."""
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self._get_severity_color()};
                border-radius: {theme_manager.get_border_radius('md')};
                padding: {theme_manager.get_spacing('md')};
            }}
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setSpacing(theme_manager.get_spacing('md'))
        
        # Error icon
        icon_label = QLabel(self._get_severity_icon())
        icon_label.setStyleSheet(f"""
            font-size: 32px;
            color: {theme_manager.get_color('text_primary')};
        """)
        header_layout.addWidget(icon_label)
        
        # Error info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        title_label = QLabel(f"{self.error.severity.title()} Error")
        title_label.setStyleSheet(f"""
            font-size: {theme_manager.get_font('subheader_size')};
            font-weight: bold;
            color: {theme_manager.get_color('text_primary')};
        """)
        info_layout.addWidget(title_label)
        
        category_label = QLabel(f"Category: {self.error.category.title()}")
        category_label.setStyleSheet(f"""
            font-size: {theme_manager.get_font('secondary_size')};
            color: {theme_manager.get_color('text_secondary')};
        """)
        info_layout.addWidget(category_label)
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_message_section(self, layout):
        """Create the error message section."""
        message_label = QLabel(self.error.message)
        message_label.setStyleSheet(f"""
            font-size: {theme_manager.get_font('primary_size')};
            color: {theme_manager.get_color('text_primary')};
            padding: {theme_manager.get_spacing('md')};
            background-color: {theme_manager.get_color('bg_secondary')};
            border-radius: {theme_manager.get_border_radius('md')};
            border-left: 4px solid {self._get_severity_color()};
        """)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
    
    def create_details_section(self, layout):
        """Create the collapsible details section."""
        # Details toggle
        self.details_toggle = QCheckBox("Show Technical Details")
        self.details_toggle.setStyleSheet(f"""
            QCheckBox {{
                font-size: {theme_manager.get_font('secondary_size')};
                color: {theme_manager.get_color('text_secondary')};
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
            }}
        """)
        self.details_toggle.toggled.connect(self.toggle_details)
        layout.addWidget(self.details_toggle)
        
        # Details container
        self.details_container = QWidget()
        self.details_container.hide()
        details_layout = QVBoxLayout(self.details_container)
        details_layout.setSpacing(theme_manager.get_spacing('sm'))
        
        # Error details
        if self.error.details:
            details_text = "Error Details:\n"
            for key, value in self.error.details.items():
                details_text += f"• {key}: {value}\n"
            
            details_label = QLabel(details_text)
            details_label.setStyleSheet(f"""
                font-size: {theme_manager.get_font('small_size')};
                color: {theme_manager.get_color('text_tertiary')};
                font-family: {theme_manager.get_font('monospace')};
                background-color: {theme_manager.get_color('bg_tertiary')};
                padding: {theme_manager.get_spacing('sm')};
                border-radius: {theme_manager.get_border_radius('sm')};
            """)
            details_label.setWordWrap(True)
            details_layout.addWidget(details_label)
        
        # Traceback
        traceback_text = QTextEdit()
        traceback_text.setPlainText(self.error.traceback)
        traceback_text.setReadOnly(True)
        traceback_text.setMaximumHeight(150)
        traceback_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {theme_manager.get_color('bg_tertiary')};
                color: {theme_manager.get_color('text_tertiary')};
                border: 1px solid {theme_manager.get_color('border_primary')};
                border-radius: {theme_manager.get_border_radius('sm')};
                font-family: {theme_manager.get_font('monospace')};
                font-size: {theme_manager.get_font('small_size')};
            }}
        """)
        details_layout.addWidget(traceback_text)
        
        layout.addWidget(self.details_container)
    
    def create_recovery_section(self, layout):
        """Create the recovery section."""
        recovery_frame = QFrame()
        recovery_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {theme_manager.get_color('bg_secondary')};
                border: 1px solid {theme_manager.get_color('border_primary')};
                border-radius: {theme_manager.get_border_radius('md')};
                padding: {theme_manager.get_spacing('md')};
            }}
        """)
        
        recovery_layout = QVBoxLayout(recovery_frame)
        recovery_layout.setSpacing(theme_manager.get_spacing('sm'))
        
        recovery_title = QLabel("💡 Recovery Suggestion")
        recovery_title.setStyleSheet(f"""
            font-size: {theme_manager.get_font('secondary_size')};
            font-weight: bold;
            color: {theme_manager.get_color('info')};
        """)
        recovery_layout.addWidget(recovery_title)
        
        recovery_text = QLabel(self.error.recovery_action)
        recovery_text.setStyleSheet(f"""
            font-size: {theme_manager.get_font('primary_size')};
            color: {theme_manager.get_color('text_primary')};
        """)
        recovery_text.setWordWrap(True)
        recovery_layout.addWidget(recovery_text)
        
        layout.addWidget(recovery_frame)
    
    def create_action_buttons(self, layout):
        """Create the action buttons."""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(theme_manager.get_spacing('md'))
        
        # Copy error button
        copy_btn = QPushButton("📋 Copy Error Details")
        copy_btn.setStyleSheet(theme_manager.get_button_style("default", "sm"))
        copy_btn.clicked.connect(self.copy_error_details)
        button_layout.addWidget(copy_btn)
        
        button_layout.addStretch()
        
        # Report button (for critical errors)
        if self.error.severity == ErrorSeverity.CRITICAL:
            report_btn = QPushButton("🐛 Report Bug")
            report_btn.setStyleSheet(theme_manager.get_button_style("warning", "sm"))
            report_btn.clicked.connect(self.report_bug)
            button_layout.addWidget(report_btn)
        
        # OK button
        ok_btn = QPushButton("OK")
        ok_btn.setStyleSheet(theme_manager.get_button_style("primary", "md"))
        ok_btn.clicked.connect(self.accept)
        ok_btn.setDefault(True)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
    
    def setup_connections(self):
        """Setup signal connections."""
        pass
    
    def toggle_details(self, checked):
        """Toggle the details section visibility."""
        self.details_container.setVisible(checked)
        self.adjustSize()
    
    def copy_error_details(self):
        """Copy error details to clipboard."""
        details = f"""
FieldTuner Error Report
======================

Severity: {self.error.severity.title()}
Category: {self.error.category.title()}
Message: {self.error.message}
Timestamp: {self.error.timestamp}

Details:
{self.error.details}

Traceback:
{self.error.traceback}
        """.strip()
        
        # Copy to clipboard
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(details)
        
        # Show confirmation
        QMessageBox.information(self, "Copied", "Error details copied to clipboard!")
    
    def report_bug(self):
        """Open bug report dialog."""
        # This would open a bug report dialog or redirect to GitHub issues
        QMessageBox.information(
            self,
            "Report Bug",
            "Please visit our GitHub repository to report this bug:\n\n"
            "https://github.com/sneakytom/FieldTuner/issues\n\n"
            "The error details have been copied to your clipboard."
        )
    
    def _get_severity_color(self):
        """Get the color for the error severity."""
        color_map = {
            ErrorSeverity.INFO: theme_manager.get_color('info'),
            ErrorSeverity.WARNING: theme_manager.get_color('warning'),
            ErrorSeverity.ERROR: theme_manager.get_color('error'),
            ErrorSeverity.CRITICAL: theme_manager.get_color('error')
        }
        return color_map.get(self.error.severity, theme_manager.get_color('error'))
    
    def _get_severity_icon(self):
        """Get the icon for the error severity."""
        icon_map = {
            ErrorSeverity.INFO: "ℹ️",
            ErrorSeverity.WARNING: "⚠️",
            ErrorSeverity.ERROR: "❌",
            ErrorSeverity.CRITICAL: "🚨"
        }
        return icon_map.get(self.error.severity, "❌")


class ErrorHandler:
    """Centralized error handling system."""
    
    def __init__(self):
        self.error_log: List[FieldTunerError] = []
        self.max_log_size = 100
    
    def handle_error(self, error: Exception, context: str = "", 
                    category: str = ErrorCategory.SYSTEM,
                    severity: str = ErrorSeverity.ERROR,
                    details: Optional[Dict[str, Any]] = None,
                    recovery_action: Optional[str] = None,
                    show_dialog: bool = True) -> bool:
        """
        Handle an error with comprehensive logging and user feedback.
        
        Returns:
            bool: True if error was handled successfully, False otherwise
        """
        try:
            # Convert to FieldTunerError if needed
            if not isinstance(error, FieldTunerError):
                error = FieldTunerError(
                    message=str(error),
                    category=category,
                    severity=severity,
                    details=details or {},
                    recovery_action=recovery_action
                )
            
            # Add context to details
            if context:
                error.details['context'] = context
            
            # Log the error
            self.log_error(error)
            
            # Show dialog if requested
            if show_dialog:
                self.show_error_dialog(error)
            
            return True
            
        except Exception as e:
            # Fallback error handling
            log_error(f"Failed to handle error: {str(e)}", "ERROR_HANDLER", e)
            return False
    
    def log_error(self, error: FieldTunerError):
        """Log the error to the internal log."""
        self.error_log.append(error)
        
        # Maintain log size
        if len(self.error_log) > self.max_log_size:
            self.error_log.pop(0)
        
        # Log to debug system
        if error.severity == ErrorSeverity.CRITICAL:
            log_error(f"[{error.category}] {error.message}", "ERROR_HANDLER", error)
        elif error.severity == ErrorSeverity.ERROR:
            log_error(f"[{error.category}] {error.message}", "ERROR_HANDLER", error)
        elif error.severity == ErrorSeverity.WARNING:
            log_warning(f"[{error.category}] {error.message}", "ERROR_HANDLER")
        else:
            log_info(f"[{error.category}] {error.message}", "ERROR_HANDLER")
    
    def show_error_dialog(self, error: FieldTunerError):
        """Show the error dialog."""
        try:
            dialog = ErrorDialog(error)
            dialog.exec()
        except Exception as e:
            # Fallback to simple message box
            QMessageBox.critical(
                None,
                "FieldTuner Error",
                f"An error occurred:\n\n{error.message}\n\n"
                f"Category: {error.category}\n"
                f"Severity: {error.severity}"
            )
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get a summary of recent errors."""
        if not self.error_log:
            return {"total": 0, "by_severity": {}, "by_category": {}}
        
        summary = {
            "total": len(self.error_log),
            "by_severity": {},
            "by_category": {},
            "recent": []
        }
        
        # Count by severity and category
        for error in self.error_log:
            summary["by_severity"][error.severity] = summary["by_severity"].get(error.severity, 0) + 1
            summary["by_category"][error.category] = summary["by_category"].get(error.category, 0) + 1
        
        # Recent errors (last 5)
        summary["recent"] = [
            {
                "message": error.message,
                "severity": error.severity,
                "category": error.category,
                "timestamp": error.timestamp
            }
            for error in self.error_log[-5:]
        ]
        
        return summary
    
    def clear_error_log(self):
        """Clear the error log."""
        self.error_log.clear()
        log_info("Error log cleared", "ERROR_HANDLER")


# Global error handler instance
error_handler = ErrorHandler()


def handle_error(error: Exception, context: str = "", 
                category: str = ErrorCategory.SYSTEM,
                severity: str = ErrorSeverity.ERROR,
                details: Optional[Dict[str, Any]] = None,
                recovery_action: Optional[str] = None,
                show_dialog: bool = True) -> bool:
    """
    Convenience function to handle errors using the global error handler.
    
    Args:
        error: The exception to handle
        context: Additional context about where the error occurred
        category: Error category (from ErrorCategory)
        severity: Error severity (from ErrorSeverity)
        details: Additional error details
        recovery_action: Suggested recovery action
        show_dialog: Whether to show the error dialog
    
    Returns:
        bool: True if error was handled successfully
    """
    return error_handler.handle_error(
        error, context, category, severity, details, recovery_action, show_dialog
    )


def safe_execute(func, *args, context: str = "", 
                category: str = ErrorCategory.SYSTEM,
                severity: str = ErrorSeverity.ERROR,
                **kwargs):
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        *args: Function arguments
        context: Context for error reporting
        category: Error category
        severity: Error severity
        **kwargs: Additional keyword arguments
    
    Returns:
        Tuple of (success: bool, result: Any, error: Exception or None)
    """
    try:
        result = func(*args, **kwargs)
        return True, result, None
    except Exception as e:
        error_handler.handle_error(
            e, context, category, severity, show_dialog=False
        )
        return False, None, e
