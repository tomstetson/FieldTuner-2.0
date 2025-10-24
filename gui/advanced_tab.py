"""
Advanced Settings Tab for FieldTuner
Handles advanced configuration options like DirectX 12, Ray Tracing, etc.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QSlider, QLabel,
    QCheckBox, QComboBox, QGroupBox, QSpinBox, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal


class AdvancedTab(QWidget):
    """Advanced settings tab widget."""
    
    setting_changed = pyqtSignal(str, str)  # key, value
    
    def __init__(self, config_manager):
        """Initialize the advanced tab."""
        super().__init__()
        self.config_manager = config_manager
        self.controls = {}
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the advanced tab UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # DirectX 12 Advanced Settings
        dx12_group = self._create_group_box("DirectX 12 Advanced Settings")
        dx12_layout = QGridLayout()
        
        # Async Compute
        self.async_compute = QCheckBox("Async Compute")
        self.async_compute.setStyleSheet("color: #ffffff; font-size: 14px;")
        dx12_layout.addWidget(self.async_compute, 0, 0)
        
        # Multi-GPU
        self.multi_gpu = QCheckBox("Multi-GPU Support")
        self.multi_gpu.setStyleSheet("color: #ffffff; font-size: 14px;")
        dx12_layout.addWidget(self.multi_gpu, 0, 1)
        
        # Variable Rate Shading
        self.vrs = QCheckBox("Variable Rate Shading")
        self.vrs.setStyleSheet("color: #ffffff; font-size: 14px;")
        dx12_layout.addWidget(self.vrs, 1, 0)
        
        # Mesh Shaders
        self.mesh_shaders = QCheckBox("Mesh Shaders")
        self.mesh_shaders.setStyleSheet("color: #ffffff; font-size: 14px;")
        dx12_layout.addWidget(self.mesh_shaders, 1, 1)
        
        dx12_group.setLayout(dx12_layout)
        layout.addWidget(dx12_group)
        
        # Ray Tracing Settings
        rt_group = self._create_group_box("Ray Tracing Settings")
        rt_layout = QGridLayout()
        
        # Ray Tracing Quality
        rt_layout.addWidget(QLabel("Ray Tracing Quality:"), 0, 0)
        self.rt_quality = QComboBox()
        self.rt_quality.addItems(["Off", "Low", "Medium", "High", "Ultra"])
        self.rt_quality.setStyleSheet("""
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
        rt_layout.addWidget(self.rt_quality, 0, 1)
        
        # Ray Tracing Reflections
        self.rt_reflections = QCheckBox("RT Reflections")
        self.rt_reflections.setStyleSheet("color: #ffffff; font-size: 14px;")
        rt_layout.addWidget(self.rt_reflections, 1, 0)
        
        # Ray Tracing Shadows
        self.rt_shadows = QCheckBox("RT Shadows")
        self.rt_shadows.setStyleSheet("color: #ffffff; font-size: 14px;")
        rt_layout.addWidget(self.rt_shadows, 1, 1)
        
        # Ray Tracing Global Illumination
        self.rt_gi = QCheckBox("RT Global Illumination")
        self.rt_gi.setStyleSheet("color: #ffffff; font-size: 14px;")
        rt_layout.addWidget(self.rt_gi, 2, 0)
        
        rt_group.setLayout(rt_layout)
        layout.addWidget(rt_group)
        
        # Performance Settings
        perf_group = self._create_group_box("Performance Settings")
        perf_layout = QGridLayout()
        
        # Frame Rate Limit
        perf_layout.addWidget(QLabel("Frame Rate Limit:"), 0, 0)
        self.frame_rate_limit = QSpinBox()
        self.frame_rate_limit.setRange(30, 300)
        self.frame_rate_limit.setValue(0)  # Unlimited
        self.frame_rate_limit.setSpecialValueText("Unlimited")
        self.frame_rate_limit.setSuffix(" FPS")
        self.frame_rate_limit.setStyleSheet("""
            QSpinBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        perf_layout.addWidget(self.frame_rate_limit, 0, 1)
        
        # CPU Thread Count
        perf_layout.addWidget(QLabel("CPU Thread Count:"), 1, 0)
        self.cpu_threads = QSpinBox()
        self.cpu_threads.setRange(1, 32)
        self.cpu_threads.setValue(0)  # Auto
        self.cpu_threads.setSpecialValueText("Auto")
        self.cpu_threads.setStyleSheet("""
            QSpinBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        perf_layout.addWidget(self.cpu_threads, 1, 1)
        
        # GPU Memory Limit
        perf_layout.addWidget(QLabel("GPU Memory Limit (MB):"), 2, 0)
        self.gpu_memory_limit = QSpinBox()
        self.gpu_memory_limit.setRange(1024, 16384)
        self.gpu_memory_limit.setValue(8192)
        self.gpu_memory_limit.setSuffix(" MB")
        self.gpu_memory_limit.setStyleSheet("""
            QSpinBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        perf_layout.addWidget(self.gpu_memory_limit, 2, 1)
        
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)
        
        # Debug Settings
        debug_group = self._create_group_box("Debug Settings")
        debug_layout = QGridLayout()
        
        # Debug Overlay
        self.debug_overlay = QCheckBox("Debug Overlay")
        self.debug_overlay.setStyleSheet("color: #ffffff; font-size: 14px;")
        debug_layout.addWidget(self.debug_overlay, 0, 0)
        
        # Performance Monitor
        self.perf_monitor = QCheckBox("Performance Monitor")
        self.perf_monitor.setStyleSheet("color: #ffffff; font-size: 14px;")
        debug_layout.addWidget(self.perf_monitor, 0, 1)
        
        # Log Level
        debug_layout.addWidget(QLabel("Log Level:"), 1, 0)
        self.log_level = QComboBox()
        self.log_level.addItems(["Off", "Error", "Warning", "Info", "Debug"])
        self.log_level.setStyleSheet("""
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
        debug_layout.addWidget(self.log_level, 1, 1)
        
        debug_group.setLayout(debug_layout)
        layout.addWidget(debug_group)
        
        # Custom Settings
        custom_group = self._create_group_box("Custom Settings")
        custom_layout = QVBoxLayout()
        
        # Custom settings text area
        self.custom_settings = QTextEdit()
        self.custom_settings.setPlaceholderText("Enter custom settings here (one per line, format: Key=Value)")
        self.custom_settings.setMaximumHeight(100)
        self.custom_settings.setStyleSheet("""
            QTextEdit {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
                font-family: monospace;
            }
        """)
        custom_layout.addWidget(self.custom_settings)
        
        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)
        
        # Store controls for easy access
        self.controls = {
            'GstRender.AsyncCompute': self.async_compute,
            'GstRender.MultiGPU': self.multi_gpu,
            'GstRender.VRS': self.vrs,
            'GstRender.MeshShaders': self.mesh_shaders,
            'GstRender.RTQuality': self.rt_quality,
            'GstRender.RTReflections': self.rt_reflections,
            'GstRender.RTShadows': self.rt_shadows,
            'GstRender.RTGI': self.rt_gi,
            'GstRender.FrameRateLimit': self.frame_rate_limit,
            'GstRender.CPUThreads': self.cpu_threads,
            'GstRender.GPUMemoryLimit': self.gpu_memory_limit,
            'GstRender.DebugOverlay': self.debug_overlay,
            'GstRender.PerfMonitor': self.perf_monitor,
            'GstRender.LogLevel': self.log_level
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
        # DirectX 12 settings
        self.async_compute.toggled.connect(
            lambda checked: self._on_setting_changed('GstRender.AsyncCompute', str(int(checked)))
        )
        self.multi_gpu.toggled.connect(
            lambda checked: self._on_setting_changed('GstRender.MultiGPU', str(int(checked)))
        )
        self.vrs.toggled.connect(
            lambda checked: self._on_setting_changed('GstRender.VRS', str(int(checked)))
        )
        self.mesh_shaders.toggled.connect(
            lambda checked: self._on_setting_changed('GstRender.MeshShaders', str(int(checked)))
        )
        
        # Ray Tracing settings
        self.rt_quality.currentIndexChanged.connect(
            lambda index: self._on_setting_changed('GstRender.RTQuality', str(index))
        )
        self.rt_reflections.toggled.connect(
            lambda checked: self._on_setting_changed('GstRender.RTReflections', str(int(checked)))
        )
        self.rt_shadows.toggled.connect(
            lambda checked: self._on_setting_changed('GstRender.RTShadows', str(int(checked)))
        )
        self.rt_gi.toggled.connect(
            lambda checked: self._on_setting_changed('GstRender.RTGI', str(int(checked)))
        )
        
        # Performance settings
        self.frame_rate_limit.valueChanged.connect(
            lambda value: self._on_setting_changed('GstRender.FrameRateLimit', str(value))
        )
        self.cpu_threads.valueChanged.connect(
            lambda value: self._on_setting_changed('GstRender.CPUThreads', str(value))
        )
        self.gpu_memory_limit.valueChanged.connect(
            lambda value: self._on_setting_changed('GstRender.GPUMemoryLimit', str(value))
        )
        
        # Debug settings
        self.debug_overlay.toggled.connect(
            lambda checked: self._on_setting_changed('GstRender.DebugOverlay', str(int(checked)))
        )
        self.perf_monitor.toggled.connect(
            lambda checked: self._on_setting_changed('GstRender.PerfMonitor', str(int(checked)))
        )
        self.log_level.currentIndexChanged.connect(
            lambda index: self._on_setting_changed('GstRender.LogLevel', str(index))
        )
    
    def _on_setting_changed(self, key, value):
        """Handle setting changes."""
        self.setting_changed.emit(key, value)
    
    def update_from_config(self):
        """Update UI from current config."""
        # Get all settings for advanced tab
        all_settings = self.config_manager.config_data
        
        # Update DirectX 12 settings
        self.async_compute.setChecked(all_settings.get('GstRender.AsyncCompute', '0') == '1')
        self.multi_gpu.setChecked(all_settings.get('GstRender.MultiGPU', '0') == '1')
        self.vrs.setChecked(all_settings.get('GstRender.VRS', '0') == '1')
        self.mesh_shaders.setChecked(all_settings.get('GstRender.MeshShaders', '0') == '1')
        
        # Update Ray Tracing settings
        rt_quality = int(all_settings.get('GstRender.RTQuality', '0'))
        self.rt_quality.setCurrentIndex(rt_quality)
        
        self.rt_reflections.setChecked(all_settings.get('GstRender.RTReflections', '0') == '1')
        self.rt_shadows.setChecked(all_settings.get('GstRender.RTShadows', '0') == '1')
        self.rt_gi.setChecked(all_settings.get('GstRender.RTGI', '0') == '1')
        
        # Update Performance settings
        frame_limit = int(all_settings.get('GstRender.FrameRateLimit', '0'))
        self.frame_rate_limit.setValue(frame_limit)
        
        cpu_threads = int(all_settings.get('GstRender.CPUThreads', '0'))
        self.cpu_threads.setValue(cpu_threads)
        
        gpu_memory = int(all_settings.get('GstRender.GPUMemoryLimit', '8192'))
        self.gpu_memory_limit.setValue(gpu_memory)
        
        # Update Debug settings
        self.debug_overlay.setChecked(all_settings.get('GstRender.DebugOverlay', '0') == '1')
        self.perf_monitor.setChecked(all_settings.get('GstRender.PerfMonitor', '0') == '1')
        
        log_level = int(all_settings.get('GstRender.LogLevel', '2'))
        self.log_level.setCurrentIndex(log_level)
    
    def get_changes(self):
        """Get current changes from UI."""
        changes = {}
        
        # DirectX 12 settings
        changes['GstRender.AsyncCompute'] = str(int(self.async_compute.isChecked()))
        changes['GstRender.MultiGPU'] = str(int(self.multi_gpu.isChecked()))
        changes['GstRender.VRS'] = str(int(self.vrs.isChecked()))
        changes['GstRender.MeshShaders'] = str(int(self.mesh_shaders.isChecked()))
        
        # Ray Tracing settings
        changes['GstRender.RTQuality'] = str(self.rt_quality.currentIndex())
        changes['GstRender.RTReflections'] = str(int(self.rt_reflections.isChecked()))
        changes['GstRender.RTShadows'] = str(int(self.rt_shadows.isChecked()))
        changes['GstRender.RTGI'] = str(int(self.rt_gi.isChecked()))
        
        # Performance settings
        changes['GstRender.FrameRateLimit'] = str(self.frame_rate_limit.value())
        changes['GstRender.CPUThreads'] = str(self.cpu_threads.value())
        changes['GstRender.GPUMemoryLimit'] = str(self.gpu_memory_limit.value())
        
        # Debug settings
        changes['GstRender.DebugOverlay'] = str(int(self.debug_overlay.isChecked()))
        changes['GstRender.PerfMonitor'] = str(int(self.perf_monitor.isChecked()))
        changes['GstRender.LogLevel'] = str(self.log_level.currentIndex())
        
        # Custom settings
        custom_text = self.custom_settings.toPlainText().strip()
        if custom_text:
            for line in custom_text.split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    changes[key.strip()] = value.strip()
        
        return changes
    
    def reset_to_defaults(self):
        """Reset to default values."""
        # DirectX 12 settings
        self.async_compute.setChecked(True)
        self.multi_gpu.setChecked(False)
        self.vrs.setChecked(False)
        self.mesh_shaders.setChecked(False)
        
        # Ray Tracing settings
        self.rt_quality.setCurrentIndex(0)  # Off
        self.rt_reflections.setChecked(False)
        self.rt_shadows.setChecked(False)
        self.rt_gi.setChecked(False)
        
        # Performance settings
        self.frame_rate_limit.setValue(0)  # Unlimited
        self.cpu_threads.setValue(0)  # Auto
        self.gpu_memory_limit.setValue(8192)
        
        # Debug settings
        self.debug_overlay.setChecked(False)
        self.perf_monitor.setChecked(False)
        self.log_level.setCurrentIndex(2)  # Info
        
        # Clear custom settings
        self.custom_settings.clear()
