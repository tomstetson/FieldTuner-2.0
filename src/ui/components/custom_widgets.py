"""
FieldTuner V2.0 - Enhanced Custom Widgets
Modern, accessible custom widgets with consistent theming and improved UX.
"""

from PyQt6.QtWidgets import (
    QWidget, QSlider, QDoubleSpinBox, QComboBox, QLabel, QPushButton, 
    QVBoxLayout, QHBoxLayout, QProgressBar, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QPainter, QColor, QFont, QLinearGradient, QBrush, QPalette

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from debug import log_info, log_error, log_warning
from ui.theme import theme_manager


class FocusAwareSlider(QSlider):
    """Enhanced slider that only responds to scroll wheel when focused."""
    
    def __init__(self, orientation=Qt.Orientation.Horizontal):
        super().__init__(orientation)
        self._scroll_enabled = False
        self._setup_style()
        
    def _setup_style(self):
        """Setup the slider styling using theme manager."""
        self.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: {theme_manager.get_color('bg_tertiary')};
                height: 6px;
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {theme_manager.get_color('primary')};
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin: -7px 0;
                border: 2px solid {theme_manager.get_color('bg_primary')};
            }}
            QSlider::handle:horizontal:hover {{
                background: {theme_manager.get_color('primary_hover')};
            }}
            QSlider::handle:horizontal:pressed {{
                background: {theme_manager.get_color('primary_pressed')};
            }}
            QSlider::sub-page:horizontal {{
                background: {theme_manager.get_color('primary')};
                border-radius: 3px;
            }}
        """)
        
    def wheelEvent(self, event):
        """Only respond to scroll wheel when the slider is focused."""
        if self._scroll_enabled and self.hasFocus():
            super().wheelEvent(event)
    
    def focusInEvent(self, event):
        """Enable scroll wheel when focused."""
        super().focusInEvent(event)
        self._scroll_enabled = True
        # Add focus indicator
        self.setStyleSheet(self.styleSheet() + f"""
            QSlider::handle:horizontal {{
                border: 3px solid {theme_manager.get_color('border_focus')};
            }}
        """)
    
    def focusOutEvent(self, event):
        """Disable scroll wheel when not focused."""
        super().focusOutEvent(event)
        self._scroll_enabled = False
        # Remove focus indicator
        self.setStyleSheet(self.styleSheet().replace(f"""
            QSlider::handle:horizontal {{
                border: 3px solid {theme_manager.get_color('border_focus')};
            }}
        """, ""))


class FocusAwareSpinBox(QDoubleSpinBox):
    """Enhanced spinbox that only responds to scroll wheel when focused."""
    
    def __init__(self):
        super().__init__()
        self._scroll_enabled = False
        self._setup_style()
        
    def _setup_style(self):
        """Setup the spinbox styling using theme manager."""
        self.setStyleSheet(theme_manager.get_input_style())
        
    def wheelEvent(self, event):
        """Only respond to scroll wheel when the spinbox is focused."""
        if self._scroll_enabled and self.hasFocus():
            super().wheelEvent(event)
    
    def focusInEvent(self, event):
        """Enable scroll wheel when focused."""
        super().focusInEvent(event)
        self._scroll_enabled = True
    
    def focusOutEvent(self, event):
        """Disable scroll wheel when not focused."""
        super().focusOutEvent(event)
        self._scroll_enabled = False


class FocusAwareComboBox(QComboBox):
    """Enhanced combobox that only responds to scroll wheel when focused."""
    
    def __init__(self):
        super().__init__()
        self._scroll_enabled = False
        self._setup_style()
        
    def _setup_style(self):
        """Setup the combobox styling using theme manager."""
        self.setStyleSheet(theme_manager.get_input_style())
        
    def wheelEvent(self, event):
        """Only respond to scroll wheel when the combobox is focused."""
        if self._scroll_enabled and self.hasFocus():
            super().wheelEvent(event)
    
    def focusInEvent(self, event):
        """Enable scroll wheel when focused."""
        super().focusInEvent(event)
        self._scroll_enabled = True
    
    def focusOutEvent(self, event):
        """Disable scroll wheel when not focused."""
        super().focusOutEvent(event)
        self._scroll_enabled = False


class ProfessionalToggleSwitch(QWidget):
    """Enhanced toggle switch with modern design and smooth animations."""
    
    toggled = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(52, 28)
        self.is_on = False
        self._setup_style()
        
    def _setup_style(self):
        """Setup the toggle switch styling."""
        self.update_style()
        
    def mousePressEvent(self, event):
        self.toggle()
        super().mousePressEvent(event)
    
    def toggle(self):
        self.is_on = not self.is_on
        self.update_style()
        self.toggled.emit(self.is_on)
    
    def set_checked(self, checked):
        self.is_on = checked
        self.update_style()
    
    def is_checked(self):
        return self.is_on
    
    def update_style(self):
        """Update toggle switch styling based on state."""
        if self.is_on:
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: {theme_manager.get_color('primary')};
                    border: 2px solid {theme_manager.get_color('primary')};
                    border-radius: 14px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: {theme_manager.get_color('bg_tertiary')};
                    border: 2px solid {theme_manager.get_color('border_primary')};
                    border-radius: 14px;
                }}
            """)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        if self.is_on:
            painter.setBrush(QColor(theme_manager.get_color('primary')))
            painter.setPen(QColor(theme_manager.get_color('primary')))
        else:
            painter.setBrush(QColor(theme_manager.get_color('bg_tertiary')))
            painter.setPen(QColor(theme_manager.get_color('border_primary')))
        
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 14, 14)
        
        # Draw toggle button
        painter.setBrush(QColor(theme_manager.get_color('text_primary')))
        painter.setPen(QColor(theme_manager.get_color('text_primary')))
        
        if self.is_on:
            button_x = self.width() - 22
        else:
            button_x = 2
        
        button_y = 2
        painter.drawEllipse(button_x, button_y, 20, 20)


class ModernPresetCard(QWidget):
    """Modern, consistent preset card with enhanced UX."""
    
    clicked = pyqtSignal(str)
    hovered = pyqtSignal(str)
    
    def __init__(self, preset_key, preset_data, parent=None):
        super().__init__(parent)
        self.preset_key = preset_key
        self.preset_data = preset_data
        self.is_selected = False
        self.setFixedSize(280, 180)  # Consistent size
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """Setup the modern preset card UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Header with icon and title
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        # Icon with background
        icon_label = QLabel(self._get_preset_icon())
        icon_label.setStyleSheet(f"""
            font-size: 32px;
            color: {self._get_preset_color()};
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: {theme_manager.get_border_radius('lg')};
            padding: 8px;
        """)
        icon_label.setFixedSize(48, 48)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(icon_label)
        
        # Title and description
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        title_label = QLabel(self.preset_data.get('name', 'Unknown'))
        title_label.setStyleSheet(f"""
            font-size: {theme_manager.get_font('secondary_size')};
            font-weight: bold;
            color: {theme_manager.get_color('text_primary')};
        """)
        title_label.setWordWrap(True)
        text_layout.addWidget(title_label)
        
        # Description
        desc_text = self.preset_data.get('description', '')
        if not desc_text:
            desc_text = self._get_default_description()
        
        desc_label = QLabel(desc_text)
        desc_label.setStyleSheet(f"""
            font-size: {theme_manager.get_font('small_size')};
            color: {theme_manager.get_color('text_secondary')};
            line-height: 1.3;
        """)
        desc_label.setWordWrap(True)
        desc_label.setMaximumHeight(32)
        text_layout.addWidget(desc_label)
        
        header_layout.addLayout(text_layout)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Performance indicator
        perf_layout = QHBoxLayout()
        perf_layout.setSpacing(8)
        
        perf_label = QLabel("Performance:")
        perf_label.setStyleSheet(f"""
            font-size: {theme_manager.get_font('small_size')};
            color: {theme_manager.get_color('text_tertiary')};
            font-weight: 500;
        """)
        perf_layout.addWidget(perf_label)
        
        # Performance bar
        self.perf_bar = QProgressBar()
        self.perf_bar.setFixedHeight(6)
        self.perf_bar.setRange(0, 100)
        self.perf_bar.setValue(self._get_performance_value())
        self.perf_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {theme_manager.get_color('bg_tertiary')};
                border: 1px solid {theme_manager.get_color('border_primary')};
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self._get_preset_color()}, stop:1 {self._get_darker_color()});
                border-radius: 2px;
            }}
        """)
        perf_layout.addWidget(self.perf_bar)
        
        layout.addLayout(perf_layout)
        
        # Spacer to push button to bottom
        layout.addStretch()
        
        # Apply button
        apply_btn = QPushButton("Apply Preset")
        apply_btn.setFixedHeight(32)
        apply_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._get_preset_color()};
                color: {theme_manager.get_color('text_primary')};
                border: none;
                border-radius: {theme_manager.get_border_radius('md')};
                font-weight: bold;
                font-size: {theme_manager.get_font('secondary_size')};
            }}
            QPushButton:hover {{
                background-color: {self._get_darker_color()};
            }}
            QPushButton:pressed {{
                background-color: {theme_manager.get_color('primary_pressed')};
            }}
        """)
        apply_btn.clicked.connect(lambda: self.clicked.emit(self.preset_key))
        layout.addWidget(apply_btn)
        
        # Set card styling
        self.update_style()
    
    def setup_animations(self):
        """Setup hover and selection animations."""
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(150)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def update_style(self):
        """Update card styling based on state."""
        color = self._get_preset_color()
        if self.is_selected:
            self.setStyleSheet(f"""
                QWidget {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1a3a5c, stop:1 #0f2a4a);
                    border: 2px solid {color};
                    border-radius: {theme_manager.get_border_radius('lg')};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: {theme_manager.get_color('bg_card')};
                    border: 1px solid {theme_manager.get_color('border_primary')};
                    border-radius: {theme_manager.get_border_radius('lg')};
                }}
                QWidget:hover {{
                    background-color: {theme_manager.get_color('bg_tertiary')};
                    border: 2px solid {color};
                }}
            """)
    
    def set_selected(self, selected):
        """Set the selected state of the card."""
        self.is_selected = selected
        self.update_style()
    
    def enterEvent(self, event):
        """Handle mouse enter event."""
        self.hovered.emit(self.preset_key)
        super().enterEvent(event)
    
    def mousePressEvent(self, event):
        """Handle mouse press event."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.preset_key)
        super().mousePressEvent(event)
    
    def _get_preset_icon(self):
        """Get the appropriate icon for the preset."""
        icon_map = {
            'esports': '🏆',
            'competitive': '⚔️',
            'balanced': '⚖️',
            'quality': '🎨',
            'performance': '🚀'
        }
        return icon_map.get(self.preset_key, '⚙️')
    
    def _get_preset_color(self):
        """Get the primary color for the preset."""
        color_map = {
            'esports': theme_manager.get_color('accent_gold'),
            'competitive': theme_manager.get_color('accent_red'),
            'balanced': theme_manager.get_color('accent_green'),
            'quality': theme_manager.get_color('accent_blue'),
            'performance': theme_manager.get_color('accent_purple')
        }
        return color_map.get(self.preset_key, theme_manager.get_color('primary'))
    
    def _get_darker_color(self):
        """Get a darker version of the preset color."""
        darker_map = {
            'esports': '#b8860b',
            'competitive': '#e74c3c',
            'balanced': '#26a69a',
            'quality': '#2980b9',
            'performance': '#7fb069'
        }
        return darker_map.get(self.preset_key, theme_manager.get_color('primary_pressed'))
    
    def _get_default_description(self):
        """Get default description for preset."""
        desc_map = {
            'esports': 'Maximum performance for competitive gaming',
            'competitive': 'High performance with balanced settings',
            'balanced': 'Optimal balance between quality and performance',
            'quality': 'High visual quality with good performance',
            'performance': 'Maximum performance with minimal quality loss'
        }
        return desc_map.get(self.preset_key, 'Optimized settings for better gaming')
    
    def _get_performance_value(self):
        """Get performance value for this preset."""
        performance_map = {
            'esports': 95,
            'competitive': 85,
            'balanced': 70,
            'quality': 45,
            'performance': 25
        }
        return performance_map.get(self.preset_key, 50)


class LoadingOverlay(QWidget):
    """Enhanced loading overlay with modern animations."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.hide()
        
    def setup_ui(self):
        """Setup the loading overlay UI."""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(0, 0, 0, 180);
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Loading spinner
        self.spinner = QLabel("⏳")
        self.spinner.setStyleSheet(f"""
            font-size: 48px;
            color: {theme_manager.get_color('primary')};
        """)
        self.spinner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.spinner)
        
        # Loading text
        self.loading_text = QLabel("Loading...")
        self.loading_text.setStyleSheet(f"""
            font-size: {theme_manager.get_font('subheader_size')};
            color: {theme_manager.get_color('text_primary')};
            font-weight: bold;
        """)
        self.loading_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loading_text)
        
        # Setup spinner animation
        self.setup_spinner_animation()
    
    def setup_spinner_animation(self):
        """Setup the spinner rotation animation."""
        self.spinner_animation = QPropertyAnimation(self.spinner, b"rotation")
        self.spinner_animation.setDuration(1000)
        self.spinner_animation.setStartValue(0)
        self.spinner_animation.setEndValue(360)
        self.spinner_animation.setLoopCount(-1)  # Infinite loop
    
    def show_loading(self, text="Loading..."):
        """Show the loading overlay with custom text."""
        self.loading_text.setText(text)
        self.show()
        self.spinner_animation.start()
        self.raise_()
    
    def hide_loading(self):
        """Hide the loading overlay."""
        self.spinner_animation.stop()
        self.hide()


# Backward compatibility
PresetCard = ModernPresetCard
