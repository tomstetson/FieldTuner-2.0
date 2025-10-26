"""
FieldTuner V2.0 - Quick Settings Tab
Provides quick access to essential settings and presets.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal

from debug import log_info, log_error, log_warning
from ui.components.custom_widgets import PresetCard


class QuickSettingsTab(QWidget):
    """Quick settings tab with preset cards and essential controls."""
    
    preset_applied = pyqtSignal(str)
    
    def __init__(self, config_manager, favorites_manager):
        super().__init__()
        self.config_manager = config_manager
        self.favorites_manager = favorites_manager
        self.preset_cards = {}
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the quick settings UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("⚡ Quick Settings")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 16px;
            padding: 8px 0px;
        """)
        layout.addWidget(header)
        
        # Create scroll area for all content
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
            QScrollBar::handle:vertical:hover {
                background-color: #888;
            }
        """)
        
        # Main content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(20)
        
        # Preset cards
        self.create_preset_cards(self.content_layout)
        
        # Favorites section
        self.create_favorites_section(self.content_layout)
        
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
    
    def create_preset_cards(self, layout):
        """Create preset cards for quick access with improved layout."""
        # Preset cards header
        presets_header = QLabel("🎯 Performance Presets")
        presets_header.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 16px;
            padding: 8px 0px;
        """)
        layout.addWidget(presets_header)
        
        # Create scroll area for horizontal scrolling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(False)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFixedHeight(180)  # Fixed height to prevent vertical expansion
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:horizontal {
                background-color: #333;
                height: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background-color: #666;
                border-radius: 6px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #888;
            }
        """)
        
        # Preset cards container with proper spacing
        presets_container = QWidget()
        presets_container.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)
        
        presets_layout = QHBoxLayout(presets_container)
        presets_layout.setSpacing(24)  # Increased spacing between cards
        presets_layout.setContentsMargins(10, 10, 10, 10)
        
        self.preset_cards = {}
        presets = list(self.config_manager.optimal_settings.items())
        
        for preset_key, preset_data in presets:
            card = PresetCard(preset_key, preset_data)
            card.clicked.connect(self.apply_preset)
            self.preset_cards[preset_key] = card
            presets_layout.addWidget(card)
        
        # Set the container size based on content
        presets_container.setMinimumWidth(len(presets) * 300 + (len(presets) - 1) * 24 + 20)  # Card width + spacing + margins
        
        scroll_area.setWidget(presets_container)
        layout.addWidget(scroll_area)
        
        # Add some spacing after preset cards
        layout.addSpacing(20)
    
    def create_favorites_section(self, parent_layout):
        """Create the favorites section."""
        # Favorites header
        favorites_header = QLabel("⭐ Favorite Settings")
        favorites_header.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #ffd700;
            margin-bottom: 16px;
            padding: 8px 0px;
        """)
        parent_layout.addWidget(favorites_header)
        
        # Favorites container with better styling
        self.favorites_container = QVBoxLayout()
        self.favorites_container.setSpacing(12)
        
        # Create a widget to hold favorites
        self.favorites_widget = QWidget()
        self.favorites_widget.setLayout(self.favorites_container)
        self.favorites_widget.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        # Add to parent layout
        parent_layout.addWidget(self.favorites_widget)
        
        # Load initial favorites
        self.refresh_favorites()
    
    def refresh_favorites(self):
        """Refresh the favorites display."""
        try:
            # Clear existing favorites
            while self.favorites_container.count():
                child = self.favorites_container.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            # Add current favorites
            if not self.favorites_manager.favorites:
                no_favorites_label = QLabel("No favorite settings yet. Add some in the Advanced tab!")
                no_favorites_label.setStyleSheet("""
                    color: #888;
                    font-style: italic;
                    padding: 20px;
                """)
                self.favorites_container.addWidget(no_favorites_label)
                return
            
            for setting_key in self.favorites_manager.favorites:
                self.create_favorite_item(setting_key)
                
        except Exception as e:
            log_error(f"Failed to refresh favorites: {str(e)}", "QUICK", e)
    
    def create_favorite_item(self, setting_key):
        """Create a favorite item widget."""
        try:
            # Get setting info from database
            from settings_database import BF6_SETTINGS_DATABASE
            setting_info = BF6_SETTINGS_DATABASE.get(setting_key, {})
            display_name = setting_info.get('name', setting_key)
            description = setting_info.get('description', '')
            
            # Create favorite item widget
            item_widget = QWidget()
            item_widget.setStyleSheet("""
                QWidget {
                    background-color: #2a2a2a;
                    border: 1px solid #444;
                    border-radius: 6px;
                    padding: 8px;
                }
            """)
            
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(8, 8, 8, 8)
            
            # Setting name and description
            text_layout = QVBoxLayout()
            name_label = QLabel(display_name)
            name_label.setStyleSheet("color: #ffffff; font-weight: bold;")
            text_layout.addWidget(name_label)
            
            if description:
                desc_label = QLabel(description)
                desc_label.setStyleSheet("color: #ccc; font-size: 12px;")
                text_layout.addWidget(desc_label)
            
            item_layout.addLayout(text_layout)
            item_layout.addStretch()
            
            # Remove button
            remove_btn = QPushButton("✕")
            remove_btn.setStyleSheet("""
                QPushButton {
                    background: #ff4444;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 4px 8px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background: #ff6666;
                }
            """)
            remove_btn.clicked.connect(lambda: self.remove_favorite_setting(setting_key))
            item_layout.addWidget(remove_btn)
            
            self.favorites_container.addWidget(item_widget)
            
        except Exception as e:
            log_error(f"Failed to create favorite item for {setting_key}: {str(e)}", "QUICK", e)
    
    def remove_favorite_setting(self, setting_key):
        """Remove a setting from favorites."""
        try:
            self.favorites_manager.remove_favorite(setting_key)
            self.refresh_favorites()
            log_info(f"Removed {setting_key} from favorites", "QUICK")
        except Exception as e:
            log_error(f"Failed to remove favorite {setting_key}: {str(e)}", "QUICK", e)
    
    def load_settings(self):
        """Load current settings."""
        try:
            log_info("Loading quick settings", "QUICK")
            self.refresh_favorites()
        except Exception as e:
            log_error(f"Failed to load quick settings: {str(e)}", "QUICK", e)
    
    def apply_preset(self, preset_key):
        """Apply a settings preset."""
        try:
            log_info(f"Applying preset: {preset_key}", "QUICK")
            
            if self.config_manager.apply_optimal_settings(preset_key):
                self.preset_applied.emit(preset_key)
                log_info(f"Successfully applied {preset_key} preset", "QUICK")
            else:
                log_error(f"Failed to apply {preset_key} preset", "QUICK")
                
        except Exception as e:
            log_error(f"Error applying preset {preset_key}: {str(e)}", "QUICK", e)
    
    def _on_apply_preset_clicked(self):
        """Handle apply preset button click for tests."""
        preset_key = self.preset_combo.currentText()
        self.apply_preset(preset_key)
    
    
    def add_favorite_setting(self, setting_key, value):
        """Add a favorite setting to the display."""
        try:
            # Create favorite item
            favorite_widget = QWidget()
            favorite_layout = QHBoxLayout(favorite_widget)
            favorite_layout.setContentsMargins(8, 4, 8, 4)
            
            # Setting name
            name_label = QLabel(setting_key)
            name_label.setStyleSheet("color: #e0e0e0; font-size: 12px;")
            favorite_layout.addWidget(name_label)
            
            favorite_layout.addStretch()
            
            # Value
            value_label = QLabel(str(value))
            value_label.setStyleSheet("color: #4a90e2; font-weight: bold; font-size: 12px;")
            favorite_layout.addWidget(value_label)
            
            # Remove button
            remove_btn = QPushButton("×")
            remove_btn.setFixedSize(20, 20)
            remove_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            remove_btn.clicked.connect(lambda: self.remove_favorite_setting(setting_key))
            favorite_layout.addWidget(remove_btn)
            
            self.favorites_container.addWidget(favorite_widget)
            
        except Exception as e:
            log_error(f"Failed to add favorite setting {setting_key}: {str(e)}", "QUICK", e)
    
    def remove_favorite_setting(self, setting_key):
        """Remove a favorite setting."""
        try:
            self.favorites_manager.remove_favorite(setting_key)
            self.refresh_favorites()
            log_info(f"Removed favorite: {setting_key}", "QUICK")
        except Exception as e:
            log_error(f"Failed to remove favorite {setting_key}: {str(e)}", "QUICK", e)
    
    def save_settings(self):
        """Save quick settings."""
        # Quick settings don't have direct settings to save
        # They work through presets and favorites
        pass
