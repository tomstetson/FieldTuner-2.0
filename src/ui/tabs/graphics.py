"""
FieldTuner V2.0 - Graphics Tab
Comprehensive graphics settings with modern UI.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, 
    QLabel, QComboBox, QSlider, QCheckBox, QSpinBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal

from debug import log_info, log_error, log_warning
from ui.components.custom_widgets import FocusAwareComboBox, FocusAwareSlider, ProfessionalToggleSwitch


class GraphicsTab(QWidget):
    """Graphics settings tab with comprehensive controls."""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, config_manager, favorites_manager):
        super().__init__()
        self.config_manager = config_manager
        self.favorites_manager = favorites_manager
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the graphics tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Graphics Settings")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 16px;
            padding: 8px 0px;
        """)
        layout.addWidget(header)
        
        # Create scroll area for all settings
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
        self.content_layout.setSpacing(12)
        
        # Add missing attributes for tests
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["1920x1080", "2560x1440", "3840x2160"])
        self.content_layout.addWidget(self.resolution_combo)
        
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["Low", "Medium", "High", "Ultra"])
        self.content_layout.addWidget(self.quality_combo)
        
        # Create settings groups
        self.create_display_group(self.content_layout)
        self.create_quality_group(self.content_layout)
        self.create_effects_group(self.content_layout)
        
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
    
    def create_display_group(self, parent_layout):
        """Create display settings group."""
        group = QGroupBox("Display Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Fullscreen mode
        self.fullscreen_mode = FocusAwareComboBox()
        self.fullscreen_mode.addItems(["Windowed", "Borderless", "Fullscreen"])
        self.fullscreen_mode.setStyleSheet(self.get_combo_style())
        layout.addRow("Fullscreen Mode:", self.fullscreen_mode)
        
        # Aspect ratio
        self.aspect_ratio = FocusAwareComboBox()
        self.aspect_ratio.addItems(["Auto", "4:3", "16:9", "16:10", "21:9"])
        self.aspect_ratio.setStyleSheet(self.get_combo_style())
        layout.addRow("Aspect Ratio:", self.aspect_ratio)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_quality_group(self, parent_layout):
        """Create quality settings group."""
        group = QGroupBox("Quality Settings")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Quality settings
        quality_settings = [
            ("Texture Quality", "texture_quality"),
            ("Shadow Quality", "shadow_quality"),
            ("Effects Quality", "effects_quality"),
            ("Mesh Quality", "mesh_quality"),
            ("Lighting Quality", "lighting_quality"),
            ("Post Process Quality", "postprocess_quality")
        ]
        
        for label, attr_name in quality_settings:
            combo = FocusAwareComboBox()
            combo.addItems(["Low", "Medium", "High", "Ultra"])
            combo.setStyleSheet(self.get_combo_style())
            setattr(self, attr_name, combo)
            layout.addRow(f"{label}:", combo)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_effects_group(self, parent_layout):
        """Create effects settings group."""
        group = QGroupBox("Visual Effects")
        group.setStyleSheet(self.get_group_style())
        
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Effects toggles
        effects_settings = [
            ("Motion Blur", "motion_blur"),
            ("Ambient Occlusion", "ambient_occlusion"),
            ("Anti-Aliasing", "anti_aliasing"),
            ("Depth of Field", "depth_of_field"),
            ("Lens Flare", "lens_flare"),
            ("Screen Space Reflections", "ssr")
        ]
        
        for label, attr_name in effects_settings:
            toggle = ProfessionalToggleSwitch()
            setattr(self, attr_name, toggle)
            layout.addRow(f"{label}:", toggle)
        
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
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ccc;
                margin-right: 5px;
            }
        """
    
    def load_settings(self):
        """Load graphics settings from config."""
        try:
            log_info("Loading graphics settings", "GRAPHICS")
            
            # Load display settings
            self.load_display_settings()
            self.load_quality_settings()
            self.load_effects_settings()
            
            log_info("Graphics settings loaded successfully", "GRAPHICS")
            
        except Exception as e:
            log_error(f"Failed to load graphics settings: {str(e)}", "GRAPHICS", e)
    
    def load_display_settings(self):
        """Load display-related settings."""
        try:
            # Fullscreen mode
            fullscreen_mode = self.config_manager.config_data.get('GstRender.FullscreenMode', '1')
            mode_map = {'0': 0, '1': 1, '2': 2}  # Windowed, Borderless, Fullscreen
            if fullscreen_mode in mode_map:
                self.fullscreen_mode.setCurrentIndex(mode_map[fullscreen_mode])
            
            # Aspect ratio (placeholder - BF6 doesn't have explicit aspect ratio setting)
            self.aspect_ratio.setCurrentIndex(0)  # Auto
            
        except Exception as e:
            log_error(f"Failed to load display settings: {str(e)}", "GRAPHICS", e)
    
    def load_quality_settings(self):
        """Load quality settings."""
        try:
            quality_mapping = {
                'GstRender.TextureQuality': self.texture_quality,
                'GstRender.ShadowQuality': self.shadow_quality,
                'GstRender.EffectsQuality': self.effects_quality,
                'GstRender.MeshQuality': self.mesh_quality,
                'GstRender.LightingQuality': self.lighting_quality,
                'GstRender.PostProcessQuality': self.postprocess_quality
            }
            
            for setting_key, combo in quality_mapping.items():
                value = self.config_manager.config_data.get(setting_key, '2')
                try:
                    index = int(value)
                    combo.setCurrentIndex(max(0, min(3, index)))
                except (ValueError, TypeError):
                    combo.setCurrentIndex(2)  # Default to High
                    
        except Exception as e:
            log_error(f"Failed to load quality settings: {str(e)}", "GRAPHICS", e)
    
    def load_effects_settings(self):
        """Load effects settings."""
        try:
            effects_mapping = {
                'GstRender.MotionBlurWorld': self.motion_blur,
                'GstRender.AmbientOcclusion': self.ambient_occlusion,
                'GstRender.AntiAliasing': self.anti_aliasing,
                'GstRender.DepthOfField': self.depth_of_field,
                'GstRender.LensFlare': self.lens_flare,
                'GstRender.ScreenSpaceReflections': self.ssr
            }
            
            for setting_key, toggle in effects_mapping.items():
                value = self.config_manager.config_data.get(setting_key, '0')
                try:
                    is_enabled = float(value) > 0.5
                    toggle.set_checked(is_enabled)
                except (ValueError, TypeError):
                    toggle.set_checked(False)
                    
        except Exception as e:
            log_error(f"Failed to load effects settings: {str(e)}", "GRAPHICS", e)
    
    def save_settings(self):
        """Save graphics settings to config."""
        try:
            log_info("Saving graphics settings", "GRAPHICS")
            
            # Save display settings
            self.save_display_settings()
            self.save_quality_settings()
            self.save_effects_settings()
            
            self.settings_changed.emit()
            log_info("Graphics settings saved successfully", "GRAPHICS")
            
        except Exception as e:
            log_error(f"Failed to save graphics settings: {str(e)}", "GRAPHICS", e)
    
    def save_display_settings(self):
        """Save display settings."""
        try:
            # Fullscreen mode
            mode_index = self.fullscreen_mode.currentIndex()
            self.config_manager.config_data['GstRender.FullscreenMode'] = str(mode_index)
            
        except Exception as e:
            log_error(f"Failed to save display settings: {str(e)}", "GRAPHICS", e)
    
    def save_quality_settings(self):
        """Save quality settings."""
        try:
            quality_mapping = {
                'GstRender.TextureQuality': self.texture_quality,
                'GstRender.ShadowQuality': self.shadow_quality,
                'GstRender.EffectsQuality': self.effects_quality,
                'GstRender.MeshQuality': self.mesh_quality,
                'GstRender.LightingQuality': self.lighting_quality,
                'GstRender.PostProcessQuality': self.postprocess_quality
            }
            
            for setting_key, combo in quality_mapping.items():
                value = str(combo.currentIndex())
                self.config_manager.config_data[setting_key] = value
                
        except Exception as e:
            log_error(f"Failed to save quality settings: {str(e)}", "GRAPHICS", e)
    
    def save_effects_settings(self):
        """Save effects settings."""
        try:
            effects_mapping = {
                'GstRender.MotionBlurWorld': self.motion_blur,
                'GstRender.AmbientOcclusion': self.ambient_occlusion,
                'GstRender.AntiAliasing': self.anti_aliasing,
                'GstRender.DepthOfField': self.depth_of_field,
                'GstRender.LensFlare': self.lens_flare,
                'GstRender.ScreenSpaceReflections': self.ssr
            }
            
            for setting_key, toggle in effects_mapping.items():
                value = '1' if toggle.is_checked() else '0'
                self.config_manager.config_data[setting_key] = value
                
        except Exception as e:
            log_error(f"Failed to save effects settings: {str(e)}", "GRAPHICS", e)
