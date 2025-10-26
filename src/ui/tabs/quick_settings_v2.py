"""
FieldTuner V2.0 - Enhanced Quick Settings Tab
Modern, extensible quick settings with improved UX and performance.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QFrame, QGridLayout, QSpacerItem, QSizePolicy, QButtonGroup, QRadioButton,
    QSlider, QSpinBox, QComboBox, QCheckBox, QGroupBox, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QLinearGradient, QBrush

from debug import log_info, log_error, log_warning
from ui.components.custom_widgets import ModernPresetCard, ProfessionalToggleSwitch
from ui.theme import theme_manager


# ModernPresetCard is now imported from custom_widgets.py


class QuickSettingsWidget(QWidget):
    """Enhanced quick settings widget with modern design."""
    
    settings_changed = pyqtSignal()
    preset_applied = pyqtSignal(str)
    
    def __init__(self, config_manager, favorites_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.favorites_manager = favorites_manager
        self.preset_cards = {}
        self.current_preset = None
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the enhanced quick settings UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)
        
        # Header section
        self.create_header_section(layout)
        
        # Quick actions section
        self.create_quick_actions_section(layout)
        
        # Preset cards section
        self.create_preset_cards_section(layout)
        
        # Favorites section
        self.create_favorites_section(layout)
        
        # Status section
        self.create_status_section(layout)
    
    def create_header_section(self, parent_layout):
        """Create the header section with title and status."""
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90e2, stop:1 #357abd);
                border-radius: 12px;
                padding: 16px;
            }
        """)
        
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(8)
        
        # Title
        title_label = QLabel("⚡ Quick Settings")
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
        """)
        header_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Optimize your Battlefield 6 experience with one click")
        subtitle_label.setStyleSheet("""
            font-size: 14px;
            color: rgba(255, 255, 255, 0.9);
        """)
        header_layout.addWidget(subtitle_label)
        
        parent_layout.addWidget(header_widget)
    
    def create_quick_actions_section(self, parent_layout):
        """Create quick actions section."""
        actions_widget = QWidget()
        actions_widget.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        actions_layout = QVBoxLayout(actions_widget)
        actions_layout.setSpacing(12)
        
        # Section title
        title_label = QLabel("🚀 Quick Actions")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #ffffff;
        """)
        actions_layout.addWidget(title_label)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        # Reset to defaults
        self.reset_btn = QPushButton("🔄 Reset to Defaults")
        self.reset_btn.setFixedHeight(40)
        self.reset_btn.setStyleSheet(self.get_action_button_style("#e74c3c"))
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        buttons_layout.addWidget(self.reset_btn)
        
        # Apply current settings
        self.apply_btn = QPushButton("💾 Apply Current Settings")
        self.apply_btn.setFixedHeight(40)
        self.apply_btn.setStyleSheet(self.get_action_button_style("#27ae60"))
        self.apply_btn.clicked.connect(self.apply_current_settings)
        buttons_layout.addWidget(self.apply_btn)
        
        # Backup settings
        self.backup_btn = QPushButton("💾 Create Backup")
        self.backup_btn.setFixedHeight(40)
        self.backup_btn.setStyleSheet(self.get_action_button_style("#f39c12"))
        self.backup_btn.clicked.connect(self.create_backup)
        buttons_layout.addWidget(self.backup_btn)
        
        buttons_layout.addStretch()
        actions_layout.addLayout(buttons_layout)
        
        parent_layout.addWidget(actions_widget)
    
    def create_preset_cards_section(self, parent_layout):
        """Create Performance Presets section with proper spacing and layout."""
        # Section container with adequate space
        section_widget = QWidget()
        section_widget.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        section_layout = QVBoxLayout(section_widget)
        section_layout.setSpacing(20)
        
        # Header with icon and title
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        title_icon = QLabel("🎯")
        title_icon.setStyleSheet("font-size: 24px;")
        
        title_label = QLabel("Performance Presets")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #ffffff;
        """)
        
        header_layout.addWidget(title_icon)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        section_layout.addLayout(header_layout)
        
        # Create scrollable preset cards area
        self.create_scrollable_preset_cards(section_layout)
        
        parent_layout.addWidget(section_widget)
    
    def create_scrollable_preset_cards(self, parent_layout):
        """Create scrollable preset cards with proper spacing and layout."""
        self.preset_cards = {}
        log_info(f"Creating scrollable preset cards for {len(self.config_manager.optimal_settings)} presets", "QUICK")
        
        # Create scroll area for horizontal scrolling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(False)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFixedHeight(200)  # Fixed height to prevent vertical expansion
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            QScrollBar:horizontal {{
                background-color: {theme_manager.get_color('bg_tertiary')};
                height: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {theme_manager.get_color('border_secondary')};
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {theme_manager.get_color('text_tertiary')};
            }}
        """)
        
        # Create cards container widget
        cards_container = QWidget()
        cards_layout = QHBoxLayout(cards_container)
        cards_layout.setSpacing(int(theme_manager.get_spacing('xl').replace('px', '')))  # Use theme spacing
        cards_layout.setContentsMargins(
            int(theme_manager.get_spacing('md').replace('px', '')),
            int(theme_manager.get_spacing('md').replace('px', '')),
            int(theme_manager.get_spacing('md').replace('px', '')),
            int(theme_manager.get_spacing('md').replace('px', ''))
        )
        
        presets = list(self.config_manager.optimal_settings.items())
        
        for preset_key, preset_data in presets:
            log_info(f"Creating card for preset: {preset_key}", "QUICK")
            
            # Create a modern preset card using the theme system
            card = ModernPresetCard(preset_key, preset_data)
            card.clicked.connect(self.apply_preset)
            self.preset_cards[preset_key] = card
            
            # Add to horizontal layout
            cards_layout.addWidget(card)
            log_info(f"Added card for {preset_key}", "QUICK")
        
        # Set the container size based on content
        card_width = 280  # ModernPresetCard width
        spacing = int(theme_manager.get_spacing('xl').replace('px', ''))
        margins = int(theme_manager.get_spacing('md').replace('px', '')) * 2
        cards_container.setMinimumWidth(len(presets) * card_width + (len(presets) - 1) * spacing + margins)
        
        scroll_area.setWidget(cards_container)
        parent_layout.addWidget(scroll_area)
        
        log_info(f"Created {len(self.preset_cards)} scrollable preset cards", "QUICK")
    
    def create_optimized_preset_card(self, preset_key, preset_data):
        """Create an optimized preset card with proper sizing and layout."""
        card = ModernPresetCard(preset_key, preset_data)
        return card
    
    def create_simple_preset_card(self, preset_key, preset_data):
        """Create a simple preset card with adequate space."""
        card = ModernPresetCard(preset_key, preset_data)
        return card
    
    def get_action_button_style(self, color):
        """Get style for action buttons."""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color}, stop:1 #2c3e50);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2c3e50, stop:1 {color});
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34495e, stop:1 #2c3e50);
            }}
        """
    
    def reset_to_defaults(self):
        """Reset settings to defaults."""
        log_info("Resetting settings to defaults", "QUICK")
        # Implementation for resetting to defaults
        pass
    
    def apply_current_settings(self):
        """Apply current settings."""
        log_info("Applying current settings", "QUICK")
        # Implementation for applying current settings
        pass
    
    def create_backup(self):
        """Create a backup of current settings."""
        log_info("Creating backup", "QUICK")
        # Implementation for creating backup
        pass
    
    def apply_preset(self, preset_key):
        """Apply a preset to the configuration."""
        log_info(f"Applying preset: {preset_key}", "QUICK")
        try:
            success = self.config_manager.apply_optimal_settings(preset_key)
            if success:
                log_info(f"Successfully applied preset: {preset_key}", "QUICK")
                self.preset_applied.emit(preset_key)
            else:
                log_error(f"Failed to apply preset: {preset_key}", "QUICK")
        except Exception as e:
            log_error(f"Error applying preset {preset_key}: {e}", "QUICK")
    
    def on_preset_hovered(self, preset_key):
        """Handle preset hover events."""
        log_info(f"Hovering over preset: {preset_key}", "QUICK")
        # Update status or show preview
        pass
    
    def create_favorites_section(self, parent_layout):
        """Create the favorites section."""
        favorites_widget = QWidget()
        favorites_widget.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        favorites_layout = QVBoxLayout(favorites_widget)
        favorites_layout.setSpacing(12)
        
        # Section title
        title_label = QLabel("⭐ Favorite Settings")
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #ffffff;
        """)
        favorites_layout.addWidget(title_label)
        
        # Favorites content
        favorites_content = QLabel("No favorite settings yet. Add some in the Advanced tab!")
        favorites_content.setStyleSheet("""
            font-size: 12px;
            color: #aaaaaa;
            padding: 20px;
            background-color: #252525;
            border-radius: 6px;
        """)
        favorites_layout.addWidget(favorites_content)
        
        parent_layout.addWidget(favorites_widget)
    
    def create_status_section(self, parent_layout):
        """Create the current status section."""
        status_widget = QWidget()
        status_widget.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        status_layout = QVBoxLayout(status_widget)
        status_layout.setSpacing(12)
        
        # Section title
        title_label = QLabel("📊 Current Status")
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #ffffff;
        """)
        status_layout.addWidget(title_label)
        
        # Status content
        self.status_content = QLabel("Ready to optimize your Battlefield 6 experience!")
        self.status_content.setStyleSheet("""
            font-size: 12px;
            color: #4caf50;
            padding: 20px;
            background-color: #252525;
            border-radius: 6px;
            border-left: 4px solid #4caf50;
        """)
        status_layout.addWidget(self.status_content)
        
        parent_layout.addWidget(status_widget)
    
    def load_settings(self):
        """Load current settings."""
        log_info("Loading quick settings", "QUICK")
        # Implementation for loading settings
        pass


class OptimizedPresetCard(QWidget):
    """Optimized preset card designed for proper horizontal layout without smooshing."""
    
    clicked = pyqtSignal(str)
    
    def __init__(self, preset_key, preset_data, parent=None):
        super().__init__(parent)
        self.preset_key = preset_key
        self.preset_data = preset_data
        self.setFixedSize(240, 160)  # Consistent size for all cards
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the optimized preset card UI."""
        # Main layout with proper margins
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Header with icon and title
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        # Icon
        icon_label = QLabel(self._get_preset_icon())
        icon_label.setStyleSheet(f"""
            font-size: 28px;
            color: {self._get_preset_color()};
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 8px;
        """)
        icon_label.setFixedSize(44, 44)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(self.preset_data.get('name', 'Unknown'))
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #ffffff;
        """)
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label)
        
        layout.addLayout(header_layout)
        
        # Description
        desc_text = self.preset_data.get('description', '')
        if not desc_text:
            desc_text = self._get_default_description()
        
        desc_label = QLabel(desc_text)
        desc_label.setStyleSheet("""
            font-size: 12px;
            color: #cccccc;
            line-height: 1.3;
        """)
        desc_label.setWordWrap(True)
        desc_label.setMaximumHeight(40)  # Limit height for consistency
        layout.addWidget(desc_label)
        
        # Performance indicator
        perf_layout = QHBoxLayout()
        perf_layout.setSpacing(8)
        
        perf_label = QLabel("Performance:")
        perf_label.setStyleSheet("font-size: 11px; color: #888888; font-weight: 500;")
        perf_layout.addWidget(perf_label)
        
        perf_bar = QProgressBar()
        perf_bar.setFixedHeight(6)
        perf_bar.setRange(0, 100)
        perf_bar.setValue(self._get_performance_value())
        perf_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #2a2a2a;
                border: 1px solid #404040;
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background-color: {self._get_preset_color()};
                border-radius: 2px;
            }}
        """)
        perf_layout.addWidget(perf_bar)
        layout.addLayout(perf_layout)
        
        # Apply button
        apply_btn = QPushButton("Apply Preset")
        apply_btn.setFixedHeight(32)
        apply_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._get_preset_color()};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {self._get_darker_color()};
            }}
            QPushButton:pressed {{
                background-color: #2c5aa0;
            }}
        """)
        apply_btn.clicked.connect(lambda: self.clicked.emit(self.preset_key))
        layout.addWidget(apply_btn)
        
        # Set card styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #2a2a2a;
                border: 2px solid #404040;
                border-radius: 12px;
                margin: 4px;
            }}
            QWidget:hover {{
                background-color: #333333;
                border: 2px solid {self._get_preset_color()};
            }}
        """)
    
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
            'esports': '#ffd700',
            'competitive': '#ff6b6b',
            'balanced': '#4ecdc4',
            'quality': '#45b7d1',
            'performance': '#96ceb4'
        }
        return color_map.get(self.preset_key, '#4a90e2')
    
    def _get_darker_color(self):
        """Get a darker version of the preset color."""
        darker_map = {
            'esports': '#b8860b',
            'competitive': '#e74c3c',
            'balanced': '#26a69a',
            'quality': '#2980b9',
            'performance': '#7fb069'
        }
        return darker_map.get(self.preset_key, '#357abd')
    
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


# Backward compatibility
QuickSettingsTab = QuickSettingsWidget
