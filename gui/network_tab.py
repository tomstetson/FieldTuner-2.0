"""
Network Settings Tab for FieldTuner
Handles network-related configuration options.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QSlider, QLabel,
    QCheckBox, QComboBox, QGroupBox, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal


class NetworkTab(QWidget):
    """Network settings tab widget."""
    
    setting_changed = pyqtSignal(str, str)  # key, value
    
    def __init__(self, config_manager):
        """Initialize the network tab."""
        super().__init__()
        self.config_manager = config_manager
        self.controls = {}
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Setup the network tab UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Connection Settings
        connection_group = self._create_group_box("Connection Settings")
        connection_layout = QGridLayout()
        
        # Max Ping
        connection_layout.addWidget(QLabel("Max Ping (ms):"), 0, 0)
        self.max_ping = QSpinBox()
        self.max_ping.setRange(50, 500)
        self.max_ping.setValue(150)
        self.max_ping.setSuffix(" ms")
        self.max_ping.setStyleSheet("""
            QSpinBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        connection_layout.addWidget(self.max_ping, 0, 1)
        
        # Network Quality
        connection_layout.addWidget(QLabel("Network Quality:"), 1, 0)
        self.network_quality = QComboBox()
        self.network_quality.addItems(["Low", "Medium", "High", "Ultra"])
        self.network_quality.setStyleSheet("""
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
        connection_layout.addWidget(self.network_quality, 1, 1)
        
        connection_group.setLayout(connection_layout)
        layout.addWidget(connection_group)
        
        # Bandwidth Settings
        bandwidth_group = self._create_group_box("Bandwidth Settings")
        bandwidth_layout = QGridLayout()
        
        # Upload Rate
        bandwidth_layout.addWidget(QLabel("Upload Rate (kbps):"), 0, 0)
        self.upload_rate = QSpinBox()
        self.upload_rate.setRange(32, 10000)
        self.upload_rate.setValue(1000)
        self.upload_rate.setSuffix(" kbps")
        self.upload_rate.setStyleSheet("""
            QSpinBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        bandwidth_layout.addWidget(self.upload_rate, 0, 1)
        
        # Download Rate
        bandwidth_layout.addWidget(QLabel("Download Rate (kbps):"), 1, 0)
        self.download_rate = QSpinBox()
        self.download_rate.setRange(32, 10000)
        self.download_rate.setValue(2000)
        self.download_rate.setSuffix(" kbps")
        self.download_rate.setStyleSheet("""
            QSpinBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        bandwidth_layout.addWidget(self.download_rate, 1, 1)
        
        bandwidth_group.setLayout(bandwidth_layout)
        layout.addWidget(bandwidth_group)
        
        # Network Features
        features_group = self._create_group_box("Network Features")
        features_layout = QGridLayout()
        
        # Packet Loss Compensation
        self.packet_loss_comp = QCheckBox("Packet Loss Compensation")
        self.packet_loss_comp.setStyleSheet("color: #ffffff; font-size: 14px;")
        features_layout.addWidget(self.packet_loss_comp, 0, 0)
        
        # Lag Compensation
        self.lag_compensation = QCheckBox("Lag Compensation")
        self.lag_compensation.setStyleSheet("color: #ffffff; font-size: 14px;")
        features_layout.addWidget(self.lag_compensation, 0, 1)
        
        # Network Smoothing
        self.network_smoothing = QCheckBox("Network Smoothing")
        self.network_smoothing.setStyleSheet("color: #ffffff; font-size: 14px;")
        features_layout.addWidget(self.network_smoothing, 1, 0)
        
        # Auto-adjust Quality
        self.auto_adjust = QCheckBox("Auto-adjust Quality")
        self.auto_adjust.setStyleSheet("color: #ffffff; font-size: 14px;")
        features_layout.addWidget(self.auto_adjust, 1, 1)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        # Advanced Settings
        advanced_group = self._create_group_box("Advanced Settings")
        advanced_layout = QGridLayout()
        
        # Network Buffer Size
        advanced_layout.addWidget(QLabel("Network Buffer Size:"), 0, 0)
        self.buffer_size = QSpinBox()
        self.buffer_size.setRange(64, 2048)
        self.buffer_size.setValue(512)
        self.buffer_size.setSuffix(" KB")
        self.buffer_size.setStyleSheet("""
            QSpinBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        advanced_layout.addWidget(self.buffer_size, 0, 1)
        
        # Connection Timeout
        advanced_layout.addWidget(QLabel("Connection Timeout (s):"), 1, 0)
        self.connection_timeout = QSpinBox()
        self.connection_timeout.setRange(5, 60)
        self.connection_timeout.setValue(30)
        self.connection_timeout.setSuffix(" s")
        self.connection_timeout.setStyleSheet("""
            QSpinBox {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        advanced_layout.addWidget(self.connection_timeout, 1, 1)
        
        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)
        
        # Store controls for easy access
        self.controls = {
            'GstNetwork.MaxPing': self.max_ping,
            'GstNetwork.Quality': self.network_quality,
            'GstNetwork.UploadRate': self.upload_rate,
            'GstNetwork.DownloadRate': self.download_rate,
            'GstNetwork.PacketLossComp': self.packet_loss_comp,
            'GstNetwork.LagCompensation': self.lag_compensation,
            'GstNetwork.Smoothing': self.network_smoothing,
            'GstNetwork.AutoAdjust': self.auto_adjust,
            'GstNetwork.BufferSize': self.buffer_size,
            'GstNetwork.ConnectionTimeout': self.connection_timeout
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
        # Connection settings
        self.max_ping.valueChanged.connect(
            lambda value: self._on_setting_changed('GstNetwork.MaxPing', str(value))
        )
        self.network_quality.currentIndexChanged.connect(
            lambda index: self._on_setting_changed('GstNetwork.Quality', str(index))
        )
        
        # Bandwidth settings
        self.upload_rate.valueChanged.connect(
            lambda value: self._on_setting_changed('GstNetwork.UploadRate', str(value))
        )
        self.download_rate.valueChanged.connect(
            lambda value: self._on_setting_changed('GstNetwork.DownloadRate', str(value))
        )
        
        # Network features
        self.packet_loss_comp.toggled.connect(
            lambda checked: self._on_setting_changed('GstNetwork.PacketLossComp', str(int(checked)))
        )
        self.lag_compensation.toggled.connect(
            lambda checked: self._on_setting_changed('GstNetwork.LagCompensation', str(int(checked)))
        )
        self.network_smoothing.toggled.connect(
            lambda checked: self._on_setting_changed('GstNetwork.Smoothing', str(int(checked)))
        )
        self.auto_adjust.toggled.connect(
            lambda checked: self._on_setting_changed('GstNetwork.AutoAdjust', str(int(checked)))
        )
        
        # Advanced settings
        self.buffer_size.valueChanged.connect(
            lambda value: self._on_setting_changed('GstNetwork.BufferSize', str(value))
        )
        self.connection_timeout.valueChanged.connect(
            lambda value: self._on_setting_changed('GstNetwork.ConnectionTimeout', str(value))
        )
    
    def _on_setting_changed(self, key, value):
        """Handle setting changes."""
        self.setting_changed.emit(key, value)
    
    def update_from_config(self):
        """Update UI from current config."""
        network_settings = self.config_manager.get_network_settings()
        
        # Update connection settings
        max_ping = int(network_settings.get('GstNetwork.MaxPing', '150'))
        self.max_ping.setValue(max_ping)
        
        quality = int(network_settings.get('GstNetwork.Quality', '2'))
        self.network_quality.setCurrentIndex(quality)
        
        # Update bandwidth settings
        upload_rate = int(network_settings.get('GstNetwork.UploadRate', '1000'))
        self.upload_rate.setValue(upload_rate)
        
        download_rate = int(network_settings.get('GstNetwork.DownloadRate', '2000'))
        self.download_rate.setValue(download_rate)
        
        # Update network features
        self.packet_loss_comp.setChecked(network_settings.get('GstNetwork.PacketLossComp', '0') == '1')
        self.lag_compensation.setChecked(network_settings.get('GstNetwork.LagCompensation', '1') == '1')
        self.network_smoothing.setChecked(network_settings.get('GstNetwork.Smoothing', '1') == '1')
        self.auto_adjust.setChecked(network_settings.get('GstNetwork.AutoAdjust', '1') == '1')
        
        # Update advanced settings
        buffer_size = int(network_settings.get('GstNetwork.BufferSize', '512'))
        self.buffer_size.setValue(buffer_size)
        
        timeout = int(network_settings.get('GstNetwork.ConnectionTimeout', '30'))
        self.connection_timeout.setValue(timeout)
    
    def get_changes(self):
        """Get current changes from UI."""
        changes = {}
        
        changes['GstNetwork.MaxPing'] = str(self.max_ping.value())
        changes['GstNetwork.Quality'] = str(self.network_quality.currentIndex())
        changes['GstNetwork.UploadRate'] = str(self.upload_rate.value())
        changes['GstNetwork.DownloadRate'] = str(self.download_rate.value())
        changes['GstNetwork.PacketLossComp'] = str(int(self.packet_loss_comp.isChecked()))
        changes['GstNetwork.LagCompensation'] = str(int(self.lag_compensation.isChecked()))
        changes['GstNetwork.Smoothing'] = str(int(self.network_smoothing.isChecked()))
        changes['GstNetwork.AutoAdjust'] = str(int(self.auto_adjust.isChecked()))
        changes['GstNetwork.BufferSize'] = str(self.buffer_size.value())
        changes['GstNetwork.ConnectionTimeout'] = str(self.connection_timeout.value())
        
        return changes
    
    def reset_to_defaults(self):
        """Reset to default values."""
        self.max_ping.setValue(150)
        self.network_quality.setCurrentIndex(2)  # High
        self.upload_rate.setValue(1000)
        self.download_rate.setValue(2000)
        self.packet_loss_comp.setChecked(True)
        self.lag_compensation.setChecked(True)
        self.network_smoothing.setChecked(True)
        self.auto_adjust.setChecked(True)
        self.buffer_size.setValue(512)
        self.connection_timeout.setValue(30)
