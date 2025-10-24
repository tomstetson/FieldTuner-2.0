"""
Graphics Settings Tab for FieldTuner
Handles graphics-related configuration options.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QCheckBox, QSlider, QLabel, QSpinBox, QComboBox,
    QGroupBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal


class GraphicsTab(QWidget):
    """Graphics settings tab widget."""
    
    setting_changed = pyqtSignal(str, str)  # key, value
    
    def __init__(self, config_manager):
        """Initialize the graphics tab."""
        super().__init__()
        self.config_manager = config_manager
        self.controls = {}
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the graphics tab UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # DirectX 12 Settings
        dx12_group = self._create_group_box("DirectX 12 Settings")
        dx12_layout = QGridLayout()
        
        self.dx12_enabled = QCheckBox("Enable DirectX 12")
        self.dx12_enabled.setStyleSheet("color: #ffffff; font-size: 14px;")
        dx12_layout.addWidget(self.dx12_enabled, 0, 0)
        
        self.raytracing_enabled = QCheckBox("Enable Ray Tracing")
        self.raytracing_enabled.setStyleSheet("color: #ffffff; font-size: 14px;")
        dx12_layout.addWidget(self.raytracing_enabled, 1, 0)
        
        dx12_group.setLayout(dx12_layout)
        layout.addWidget(dx12_group)
        
        # Display Settings
        display_group = self._create_group_box("Display Settings")
        display_layout = QGridLayout()
        
        # Fullscreen Mode
        display_layout.addWidget(QLabel("Fullscreen Mode:"), 0, 0)
        self.fullscreen_mode = QComboBox()
        self.fullscreen_mode.addItems(["Windowed", "Fullscreen"])
        self.fullscreen_mode.setStyleSheet("""
            QComboBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
        """)
        display_layout.addWidget(self.fullscreen_mode, 0, 1)
        
        # Resolution Scale
        display_layout.addWidget(QLabel("Resolution Scale:"), 1, 0)
        self.resolution_scale = QSlider(Qt.Orientation.Horizontal)
        self.resolution_scale.setRange(50, 200)  # 0.5 to 2.0
        self.resolution_scale.setValue(100)  # Default 1.0
        self.resolution_scale.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #555;
                height: 8px;
                background: #333;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #ff6b35;
                border: 1px solid #555;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """)
        display_layout.addWidget(self.resolution_scale, 1, 1)
        
        self.resolution_scale_label = QLabel("100%")
        self.resolution_scale_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        display_layout.addWidget(self.resolution_scale_label, 1, 2)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # Visual Effects
        effects_group = self._create_group_box("Visual Effects")
        effects_layout = QGridLayout()
        
        self.motion_blur = QCheckBox("Motion Blur")
        self.motion_blur.setStyleSheet("color: #ffffff; font-size: 14px;")
        effects_layout.addWidget(self.motion_blur, 0, 0)
        
        self.depth_of_field = QCheckBox("Depth of Field")
        self.depth_of_field.setStyleSheet("color: #ffffff; font-size: 14px;")
        effects_layout.addWidget(self.depth_of_field, 0, 1)
        
        self.ambient_occlusion = QCheckBox("Ambient Occlusion")
        self.ambient_occlusion.setStyleSheet("color: #ffffff; font-size: 14px;")
        effects_layout.addWidget(self.ambient_occlusion, 1, 0)
        
        self.volumetric_lighting = QCheckBox("Volumetric Lighting")
        self.volumetric_lighting.setStyleSheet("color: #ffffff; font-size: 14px;")
        effects_layout.addWidget(self.volumetric_lighting, 1, 1)
        
        effects_group.setLayout(effects_layout)
        layout.addWidget(effects_group)
        
        # Anti-Aliasing
        aa_group = self._create_group_box("Anti-Aliasing")
        aa_layout = QGridLayout()
        
        aa_layout.addWidget(QLabel("Anti-Aliasing Level:"), 0, 0)
        self.anti_aliasing = QComboBox()
        self.anti_aliasing.addItems(["Off", "Low", "Medium", "High", "Ultra"])
        self.anti_aliasing.setStyleSheet("""
            QComboBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
        """)
        aa_layout.addWidget(self.anti_aliasing, 0, 1)
        
        aa_group.setLayout(aa_layout)
        layout.addWidget(aa_group)
        
        # Performance
        perf_group = self._create_group_box("Performance Settings")
        perf_layout = QGridLayout()
        
        self.vsync = QCheckBox("Vertical Sync")
        self.vsync.setStyleSheet("color: #ffffff; font-size: 14px;")
        perf_layout.addWidget(self.vsync, 0, 0)
        
        self.future_frame_rendering = QCheckBox("Future Frame Rendering")
        self.future_frame_rendering.setStyleSheet("color: #ffffff; font-size: 14px;")
        perf_layout.addWidget(self.future_frame_rendering, 0, 1)
        
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)
        
        # Store controls for easy access
        self.controls = {
            'GstRender.Dx12Enabled': self.dx12_enabled,
            'GstRender.RayTracingEnabled': self.raytracing_enabled,
            'GstRender.FullscreenMode': self.fullscreen_mode,
            'GstRender.ResolutionScale': self.resolution_scale,
            'GstRender.MotionBlurEnable': self.motion_blur,
            'GstRender.DepthOfFieldEnable': self.depth_of_field,
            'GstRender.AmbientOcclusionEnable': self.ambient_occlusion,
            'GstRender.VolumetricLightingEnable': self.volumetric_lighting,
            'GstRender.AntiAliasingDeferred': self.anti_aliasing,
            'GstRender.VSyncEnable': self.vsync,
            'GstRender.FutureFrameRenderingEnable': self.future_frame_rendering
        }
        
        layout.addStretch()
    
    def _create_group_box(self, title):
        """Create a styled group box."""
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ff6b35;
                border: 2px solid #444;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        return group
    
    def _connect_signals(self):
        """Connect UI signals."""
        # Connect all controls to change handler
        for key, control in self.controls.items():
            if isinstance(control, QCheckBox):
                control.toggled.connect(lambda checked, k=key: self._on_setting_changed(k, str(int(checked))))
            elif isinstance(control, QComboBox):
                control.currentIndexChanged.connect(lambda index, k=key: self._on_combo_changed(k, index))
            elif isinstance(control, QSlider):
                control.valueChanged.connect(lambda value, k=key: self._on_slider_changed(k, value))
        
        # Special handling for resolution scale
        self.resolution_scale.valueChanged.connect(self._on_resolution_scale_changed)
    
    def _on_setting_changed(self, key, value):
        """Handle setting changes."""
        self.setting_changed.emit(key, value)
    
    def _on_combo_changed(self, key, index):
        """Handle combo box changes."""
        if key == 'GstRender.FullscreenMode':
            value = str(index)
        elif key == 'GstRender.AntiAliasingDeferred':
            value = str(index)
        else:
            value = str(index)
        
        self.setting_changed.emit(key, value)
    
    def _on_slider_changed(self, key, value):
        """Handle slider changes."""
        if key == 'GstRender.ResolutionScale':
            scale_value = value / 100.0
            self.resolution_scale_label.setText(f"{value}%")
            self.setting_changed.emit(key, str(scale_value))
    
    def _on_resolution_scale_changed(self, value):
        """Handle resolution scale slider changes."""
        scale_value = value / 100.0
        self.resolution_scale_label.setText(f"{value}%")
        self.setting_changed.emit('GstRender.ResolutionScale', str(scale_value))
    
    def update_from_config(self):
        """Update UI from current config."""
        graphics_settings = self.config_manager.get_graphics_settings()
        
        # Update DirectX 12 settings
        self.dx12_enabled.setChecked(graphics_settings.get('GstRender.Dx12Enabled', '0') == '1')
        self.raytracing_enabled.setChecked(graphics_settings.get('GstRender.RayTracingEnabled', '0') == '1')
        
        # Update display settings
        fullscreen_mode = int(graphics_settings.get('GstRender.FullscreenMode', '0'))
        self.fullscreen_mode.setCurrentIndex(fullscreen_mode)
        
        resolution_scale = float(graphics_settings.get('GstRender.ResolutionScale', '1.0'))
        self.resolution_scale.setValue(int(resolution_scale * 100))
        self.resolution_scale_label.setText(f"{int(resolution_scale * 100)}%")
        
        # Update visual effects
        self.motion_blur.setChecked(graphics_settings.get('GstRender.MotionBlurEnable', '0') == '1')
        self.depth_of_field.setChecked(graphics_settings.get('GstRender.DepthOfFieldEnable', '0') == '1')
        self.ambient_occlusion.setChecked(graphics_settings.get('GstRender.AmbientOcclusionEnable', '0') == '1')
        self.volumetric_lighting.setChecked(graphics_settings.get('GstRender.VolumetricLightingEnable', '0') == '1')
        
        # Update anti-aliasing
        aa_level = int(graphics_settings.get('GstRender.AntiAliasingDeferred', '0'))
        self.anti_aliasing.setCurrentIndex(aa_level)
        
        # Update performance settings
        self.vsync.setChecked(graphics_settings.get('GstRender.VSyncEnable', '0') == '1')
        self.future_frame_rendering.setChecked(graphics_settings.get('GstRender.FutureFrameRenderingEnable', '0') == '1')
    
    def get_changes(self):
        """Get current changes from UI."""
        changes = {}
        
        # DirectX 12 settings
        changes['GstRender.Dx12Enabled'] = str(int(self.dx12_enabled.isChecked()))
        changes['GstRender.RayTracingEnabled'] = str(int(self.raytracing_enabled.isChecked()))
        
        # Display settings
        changes['GstRender.FullscreenMode'] = str(self.fullscreen_mode.currentIndex())
        
        resolution_scale = self.resolution_scale.value() / 100.0
        changes['GstRender.ResolutionScale'] = str(resolution_scale)
        
        # Visual effects
        changes['GstRender.MotionBlurEnable'] = str(int(self.motion_blur.isChecked()))
        changes['GstRender.DepthOfFieldEnable'] = str(int(self.depth_of_field.isChecked()))
        changes['GstRender.AmbientOcclusionEnable'] = str(int(self.ambient_occlusion.isChecked()))
        changes['GstRender.VolumetricLightingEnable'] = str(int(self.volumetric_lighting.isChecked()))
        
        # Anti-aliasing
        changes['GstRender.AntiAliasingDeferred'] = str(self.anti_aliasing.currentIndex())
        
        # Performance settings
        changes['GstRender.VSyncEnable'] = str(int(self.vsync.isChecked()))
        changes['GstRender.FutureFrameRenderingEnable'] = str(int(self.future_frame_rendering.isChecked()))
        
        return changes
    
    def reset_to_defaults(self):
        """Reset to default values."""
        # DirectX 12 settings
        self.dx12_enabled.setChecked(True)
        self.raytracing_enabled.setChecked(False)
        
        # Display settings
        self.fullscreen_mode.setCurrentIndex(1)  # Fullscreen
        self.resolution_scale.setValue(100)  # 100%
        self.resolution_scale_label.setText("100%")
        
        # Visual effects
        self.motion_blur.setChecked(True)
        self.depth_of_field.setChecked(True)
        self.ambient_occlusion.setChecked(True)
        self.volumetric_lighting.setChecked(True)
        
        # Anti-aliasing
        self.anti_aliasing.setCurrentIndex(2)  # Medium
        
        # Performance settings
        self.vsync.setChecked(False)
        self.future_frame_rendering.setChecked(True)
