"""
FieldTuner V2.0 - Theme System
Centralized theme management for consistent UI/UX across the application.
"""

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication
from typing import Dict, Any
import json
from pathlib import Path

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from debug import log_info, log_error


class ThemeManager(QObject):
    """Centralized theme management system."""
    
    theme_changed = pyqtSignal(str)  # Emitted when theme changes
    
    def __init__(self):
        super().__init__()
        self.current_theme = "dark"
        self.themes = self._load_themes()
        self._apply_theme(self.current_theme)
    
    def _load_themes(self) -> Dict[str, Dict[str, Any]]:
        """Load all available themes."""
        return {
            "dark": {
                "name": "Dark Theme",
                "description": "Modern dark theme optimized for gaming",
                "colors": {
                    # Primary colors
                    "primary": "#4a90e2",
                    "primary_hover": "#357abd",
                    "primary_pressed": "#2c5aa0",
                    
                    # Background colors
                    "bg_primary": "#1a1a1a",
                    "bg_secondary": "#2a2a2a",
                    "bg_tertiary": "#3a3a3a",
                    "bg_card": "#2a2a2a",
                    "bg_header": "#1a1a1a",
                    
                    # Text colors
                    "text_primary": "#ffffff",
                    "text_secondary": "#cccccc",
                    "text_tertiary": "#888888",
                    "text_disabled": "#666666",
                    
                    # Border colors
                    "border_primary": "#404040",
                    "border_secondary": "#555555",
                    "border_focus": "#4a90e2",
                    
                    # Status colors
                    "success": "#27ae60",
                    "warning": "#f39c12",
                    "error": "#e74c3c",
                    "info": "#3498db",
                    
                    # Accent colors
                    "accent_gold": "#ffd700",
                    "accent_red": "#ff6b6b",
                    "accent_green": "#4ecdc4",
                    "accent_blue": "#45b7d1",
                    "accent_purple": "#96ceb4",
                },
                "fonts": {
                    "primary_size": "14px",
                    "secondary_size": "12px",
                    "header_size": "28px",
                    "subheader_size": "20px",
                    "small_size": "11px",
                    "family": "Segoe UI, Arial, sans-serif",
                    "monospace": "Consolas, 'Courier New', monospace"
                },
                "spacing": {
                    "xs": "4px",
                    "sm": "8px",
                    "md": "12px",
                    "lg": "16px",
                    "xl": "20px",
                    "xxl": "24px",
                    "xxxl": "32px"
                },
                "border_radius": {
                    "sm": "4px",
                    "md": "6px",
                    "lg": "8px",
                    "xl": "12px",
                    "round": "50%"
                },
                "shadows": {
                    "light": "0 2px 4px rgba(0, 0, 0, 0.1)",
                    "medium": "0 4px 8px rgba(0, 0, 0, 0.2)",
                    "heavy": "0 8px 16px rgba(0, 0, 0, 0.3)"
                }
            },
            "light": {
                "name": "Light Theme",
                "description": "Clean light theme for better visibility",
                "colors": {
                    # Primary colors
                    "primary": "#0078d4",
                    "primary_hover": "#106ebe",
                    "primary_pressed": "#005a9e",
                    
                    # Background colors
                    "bg_primary": "#ffffff",
                    "bg_secondary": "#f8f9fa",
                    "bg_tertiary": "#e9ecef",
                    "bg_card": "#ffffff",
                    "bg_header": "#f8f9fa",
                    
                    # Text colors
                    "text_primary": "#212529",
                    "text_secondary": "#495057",
                    "text_tertiary": "#6c757d",
                    "text_disabled": "#adb5bd",
                    
                    # Border colors
                    "border_primary": "#dee2e6",
                    "border_secondary": "#ced4da",
                    "border_focus": "#0078d4",
                    
                    # Status colors
                    "success": "#28a745",
                    "warning": "#ffc107",
                    "error": "#dc3545",
                    "info": "#17a2b8",
                    
                    # Accent colors
                    "accent_gold": "#ffc107",
                    "accent_red": "#dc3545",
                    "accent_green": "#28a745",
                    "accent_blue": "#007bff",
                    "accent_purple": "#6f42c1",
                },
                "fonts": {
                    "primary_size": "14px",
                    "secondary_size": "12px",
                    "header_size": "28px",
                    "subheader_size": "20px",
                    "small_size": "11px",
                    "family": "Segoe UI, Arial, sans-serif",
                    "monospace": "Consolas, 'Courier New', monospace"
                },
                "spacing": {
                    "xs": "4px",
                    "sm": "8px",
                    "md": "12px",
                    "lg": "16px",
                    "xl": "20px",
                    "xxl": "24px",
                    "xxxl": "32px"
                },
                "border_radius": {
                    "sm": "4px",
                    "md": "6px",
                    "lg": "8px",
                    "xl": "12px",
                    "round": "50%"
                },
                "shadows": {
                    "light": "0 2px 4px rgba(0, 0, 0, 0.1)",
                    "medium": "0 4px 8px rgba(0, 0, 0, 0.15)",
                    "heavy": "0 8px 16px rgba(0, 0, 0, 0.2)"
                }
            }
        }
    
    def get_color(self, color_name: str) -> str:
        """Get a color value from the current theme."""
        return self.themes[self.current_theme]["colors"].get(color_name, "#000000")
    
    def get_font(self, font_name: str) -> str:
        """Get a font value from the current theme."""
        return self.themes[self.current_theme]["fonts"].get(font_name, "14px")
    
    def get_spacing(self, spacing_name: str) -> str:
        """Get a spacing value from the current theme."""
        return self.themes[self.current_theme]["spacing"].get(spacing_name, "8px")
    
    def get_border_radius(self, radius_name: str) -> str:
        """Get a border radius value from the current theme."""
        return self.themes[self.current_theme]["border_radius"].get(radius_name, "4px")
    
    def get_shadow(self, shadow_name: str) -> str:
        """Get a shadow value from the current theme."""
        return self.themes[self.current_theme]["shadows"].get(shadow_name, "none")
    
    def get_theme(self) -> str:
        """Get the current theme name."""
        return self.current_theme
    
    def set_theme(self, theme_name: str):
        """Set the current theme."""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self._apply_theme(theme_name)
            self.theme_changed.emit(theme_name)
            log_info(f"Theme changed to: {theme_name}", "THEME")
        else:
            log_error(f"Theme '{theme_name}' not found", "THEME")
    
    def _apply_theme(self, theme_name: str):
        """Apply theme to the application."""
        try:
            theme = self.themes[theme_name]
            colors = theme["colors"]
            
            # Apply to QApplication palette
            app = QApplication.instance()
            if app:
                palette = QPalette()
                
                # Set color roles
                palette.setColor(QPalette.ColorRole.Window, QColor(colors["bg_primary"]))
                palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["text_primary"]))
                palette.setColor(QPalette.ColorRole.Base, QColor(colors["bg_secondary"]))
                palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["bg_tertiary"]))
                palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["bg_card"]))
                palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["text_primary"]))
                palette.setColor(QPalette.ColorRole.Text, QColor(colors["text_primary"]))
                palette.setColor(QPalette.ColorRole.Button, QColor(colors["bg_tertiary"]))
                palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["text_primary"]))
                palette.setColor(QPalette.ColorRole.BrightText, QColor(colors["text_primary"]))
                palette.setColor(QPalette.ColorRole.Link, QColor(colors["primary"]))
                palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["primary"]))
                palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors["text_primary"]))
                
                app.setPalette(palette)
                
        except Exception as e:
            log_error(f"Failed to apply theme {theme_name}: {str(e)}", "THEME", e)
    
    def get_available_themes(self) -> Dict[str, str]:
        """Get available themes with their descriptions."""
        return {name: theme["description"] for name, theme in self.themes.items()}
    
    def get_button_style(self, variant: str = "primary", size: str = "md") -> str:
        """Get standardized button styles."""
        colors = self.themes[self.current_theme]["colors"]
        spacing = self.themes[self.current_theme]["spacing"]
        radius = self.themes[self.current_theme]["border_radius"]
        
        if variant == "primary":
            bg_color = colors["primary"]
            hover_color = colors["primary_hover"]
            pressed_color = colors["primary_pressed"]
        elif variant == "success":
            bg_color = colors["success"]
            hover_color = "#2ecc71"
            pressed_color = "#229954"
        elif variant == "warning":
            bg_color = colors["warning"]
            hover_color = "#e67e22"
            pressed_color = "#d35400"
        elif variant == "error":
            bg_color = colors["error"]
            hover_color = "#ff6666"
            pressed_color = "#c0392b"
        else:
            bg_color = colors["bg_tertiary"]
            hover_color = colors["border_secondary"]
            pressed_color = colors["border_primary"]
        
        padding = spacing["lg"] if size == "lg" else spacing["md"] if size == "md" else spacing["sm"]
        
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {colors["text_primary"]};
                border: none;
                border-radius: {radius["md"]};
                padding: {padding};
                font-weight: bold;
                font-size: {self.get_font("primary_size")};
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
            QPushButton:disabled {{
                background-color: {colors["text_disabled"]};
                color: {colors["text_tertiary"]};
            }}
        """
    
    def get_input_style(self, variant: str = "default") -> str:
        """Get standardized input field styles."""
        colors = self.themes[self.current_theme]["colors"]
        radius = self.themes[self.current_theme]["border_radius"]
        
        return f"""
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
                background-color: {colors["bg_secondary"]};
                color: {colors["text_primary"]};
                border: 2px solid {colors["border_primary"]};
                border-radius: {radius["md"]};
                padding: {self.get_spacing("md")};
                font-size: {self.get_font("primary_size")};
            }}
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
                border-color: {colors["border_focus"]};
                background-color: {colors["bg_tertiary"]};
            }}
            QComboBox::drop-down {{
                border: none;
                background-color: {colors["bg_tertiary"]};
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {colors["text_secondary"]};
                margin-right: {self.get_spacing("sm")};
            }}
        """
    
    def get_group_style(self) -> str:
        """Get standardized group box styles."""
        colors = self.themes[self.current_theme]["colors"]
        radius = self.themes[self.current_theme]["border_radius"]
        
        return f"""
            QGroupBox {{
                background-color: {colors["bg_card"]};
                border: 1px solid {colors["border_primary"]};
                border-radius: {radius["lg"]};
                margin-top: {self.get_spacing("lg")};
                padding-top: {self.get_spacing("lg")};
                font-weight: bold;
                color: {colors["text_primary"]};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: {self.get_spacing("lg")};
                padding: 0 {self.get_spacing("sm")} 0 {self.get_spacing("sm")};
                color: {colors["text_primary"]};
                font-size: {self.get_font("secondary_size")};
            }}
        """
    
    def get_card_style(self, variant: str = "default") -> str:
        """Get standardized card styles."""
        colors = self.themes[self.current_theme]["colors"]
        radius = self.themes[self.current_theme]["border_radius"]
        shadow = self.themes[self.current_theme]["shadows"]
        
        if variant == "elevated":
            shadow_style = f"box-shadow: {shadow['medium']};"
        elif variant == "highlighted":
            shadow_style = f"box-shadow: {shadow['heavy']};"
        else:
            shadow_style = f"box-shadow: {shadow['light']};"
        
        return f"""
            QWidget {{
                background-color: {colors["bg_card"]};
                border: 1px solid {colors["border_primary"]};
                border-radius: {radius["lg"]};
                {shadow_style}
            }}
            QWidget:hover {{
                background-color: {colors["bg_tertiary"]};
                border-color: {colors["border_focus"]};
            }}
        """


# Global theme manager instance
theme_manager = ThemeManager()
