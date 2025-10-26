"""
FieldTuner V2.0 - BF6 Features Tab
Advanced Battlefield 6 specific features and optimizations.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QGridLayout, QProgressBar, QTextEdit, QScrollArea,
    QFrame, QSplitter, QTabWidget, QComboBox, QSpinBox, QCheckBox,
    QSlider, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor

from debug import log_info, log_error, log_warning, log_debug


class BF6FeaturesTab(QWidget):
    """Advanced BF6-specific features and optimizations tab."""
    
    # Signals
    settings_applied = pyqtSignal(str, dict)
    system_info_updated = pyqtSignal(dict)
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.bf6_features = config_manager.bf6_features
        self.setup_ui()
        self.setup_timers()
        
    def setup_ui(self):
        """Setup the BF6 features UI."""
        log_info("Setting up BF6 Features UI", "BF6_FEATURES_UI")
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Clean header
        header = self.create_clean_header()
        main_layout.addWidget(header)
        
        # Main content area
        content_widget = QWidget()
        content_widget.setStyleSheet("""
            QWidget {
                background: #1e1e1e;
                border: none;
            }
        """)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Left panel - Compact system info
        left_panel = self.create_compact_system_panel()
        content_layout.addWidget(left_panel, 1)
        
        # Right panel - Clean features
        right_panel = self.create_clean_features_panel()
        content_layout.addWidget(right_panel, 2)
        
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)
        
        # Status bar with config path
        status_bar = self.create_status_bar()
        main_layout.addWidget(status_bar)
        
        self.setLayout(main_layout)
        
    def create_clean_header(self):
        """Create a clean, minimal header."""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: #2d2d2d;
                border-bottom: 1px solid #404040;
                padding: 15px 20px;
            }
        """)
        header_frame.setFixedHeight(60)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Clean title
        title = QLabel("BF6 Advanced Features")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #ffffff;
        """)
        
        # Status indicator
        self.status_indicator = QLabel("System Ready")
        self.status_indicator.setStyleSheet("""
            font-size: 12px;
            color: #4caf50;
            font-weight: 500;
        """)
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(self.status_indicator)
        
        header_frame.setLayout(layout)
        return header_frame
    
    def create_compact_system_panel(self):
        """Create a compact system information panel."""
        panel = QWidget()
        panel.setStyleSheet("""
            QWidget {
                background: #252525;
                border: 1px solid #404040;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # System Status
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background: #1a1a1a;
                border: 1px solid #333;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(8, 8, 8, 8)
        
        # Process Status
        self.process_status = QLabel("Checking BF6 process...")
        self.process_status.setStyleSheet("""
            color: #cccccc;
            font-size: 13px;
            font-weight: 500;
        """)
        status_layout.addWidget(self.process_status)
        
        # System Info
        self.system_info_label = QLabel("System: Windows 10")
        self.system_info_label.setStyleSheet("""
            color: #888888;
            font-size: 11px;
        """)
        status_layout.addWidget(self.system_info_label)
        
        status_frame.setLayout(status_layout)
        layout.addWidget(status_frame)
        
        # Quick Actions
        actions_frame = QFrame()
        actions_frame.setStyleSheet("""
            QFrame {
                background: #1a1a1a;
                border: 1px solid #333;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        actions_layout = QVBoxLayout()
        actions_layout.setContentsMargins(8, 8, 8, 8)
        
        # Apply All Button
        apply_all_btn = QPushButton("Apply All Optimizations")
        apply_all_btn.setStyleSheet(self.get_primary_button_style())
        apply_all_btn.clicked.connect(self.apply_all_optimizations)
        actions_layout.addWidget(apply_all_btn)
        
        # Refresh Button
        refresh_btn = QPushButton("Refresh Status")
        refresh_btn.setStyleSheet(self.get_secondary_button_style())
        refresh_btn.clicked.connect(self.refresh_system_info)
        actions_layout.addWidget(refresh_btn)
        
        actions_frame.setLayout(actions_layout)
        layout.addWidget(actions_frame)
        
        layout.addStretch()
        panel.setLayout(layout)
        return panel
    
    def create_clean_features_panel(self):
        """Create a clean, functional features panel."""
        panel = QWidget()
        panel.setStyleSheet("""
            QWidget {
                background: #252525;
                border: 1px solid #404040;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Clean Features Tabs
        self.features_tabs = QTabWidget()
        self.features_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #404040;
                border-radius: 6px;
                background: #1a1a1a;
            }
            QTabBar::tab {
                background: #333333;
                color: #cccccc;
                padding: 8px 16px;
                margin-right: 1px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 12px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background: #0078d4;
                color: white;
            }
            QTabBar::tab:hover {
                background: #404040;
            }
        """)
        
        # Audio Features Tab (REAL BF6 settings only)
        audio_tab = self.create_clean_audio_tab()
        self.features_tabs.addTab(audio_tab, "Audio")
        
        # Note: Most other settings don't exist in BF6 config
        # Only audio settings are available in the main config file
        
        layout.addWidget(self.features_tabs)
        panel.setLayout(layout)
        return panel
    
    def create_status_bar(self):
        """Create a status bar with config file path."""
        status_bar = QFrame()
        status_bar.setStyleSheet("""
            QFrame {
                background: #1a1a1a;
                border-top: 1px solid #404040;
                padding: 8px 20px;
            }
        """)
        status_bar.setFixedHeight(35)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Config file path
        self.config_path_label = QLabel("Config: Loading...")
        self.config_path_label.setStyleSheet("""
            color: #888888;
            font-size: 11px;
            font-family: 'Consolas', monospace;
        """)
        
        # Last updated
        self.last_updated_label = QLabel("")
        self.last_updated_label.setStyleSheet("""
            color: #666666;
            font-size: 10px;
        """)
        
        layout.addWidget(self.config_path_label)
        layout.addStretch()
        layout.addWidget(self.last_updated_label)
        
        status_bar.setLayout(layout)
        return status_bar
    
    def create_clean_audio_tab(self):
        """Create a clean, functional audio tab."""
        tab = QWidget()
        tab.setStyleSheet("""
            QWidget {
                background: #1a1a1a;
                border: none;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Audio Quality Section (REAL BF6 settings only)
        quality_frame = QFrame()
        quality_frame.setStyleSheet("""
            QFrame {
                background: #252525;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        quality_layout = QVBoxLayout()
        quality_layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        quality_title = QLabel("Audio Quality (Real BF6 Settings)")
        quality_title.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
        """)
        quality_layout.addWidget(quality_title)
        
        # Quality settings grid
        quality_grid = QGridLayout()
        quality_grid.setSpacing(10)
        
        # Audio Quality (REAL setting)
        quality_grid.addWidget(QLabel("Audio Quality:"), 0, 0)
        self.audio_quality_combo = QComboBox()
        self.audio_quality_combo.addItems(["Low", "Medium", "High", "Ultra"])
        self.audio_quality_combo.setCurrentText("High")
        self.audio_quality_combo.setStyleSheet(self.get_combo_style())
        quality_grid.addWidget(self.audio_quality_combo, 0, 1)
        
        # Sound System Size (REAL setting)
        quality_grid.addWidget(QLabel("Sound System Size:"), 1, 0)
        self.sound_system_size_spin = QSpinBox()
        self.sound_system_size_spin.setRange(1, 100)
        self.sound_system_size_spin.setValue(20)
        self.sound_system_size_spin.setStyleSheet(self.get_spinbox_style())
        quality_grid.addWidget(self.sound_system_size_spin, 1, 1)
        
        # Speaker Configuration (REAL setting)
        quality_grid.addWidget(QLabel("Speaker Config:"), 2, 0)
        self.speaker_config_combo = QComboBox()
        self.speaker_config_combo.addItems(["Stereo", "Surround", "5.1", "7.1"])
        self.speaker_config_combo.setCurrentText("Surround")
        self.speaker_config_combo.setStyleSheet(self.get_combo_style())
        quality_grid.addWidget(self.speaker_config_combo, 2, 1)
        
        quality_layout.addLayout(quality_grid)
        quality_frame.setLayout(quality_layout)
        layout.addWidget(quality_frame)
        
        # Competitive Audio Section (REAL BF6 settings only)
        competitive_frame = QFrame()
        competitive_frame.setStyleSheet("""
            QFrame {
                background: #252525;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        competitive_layout = QVBoxLayout()
        competitive_layout.setContentsMargins(0, 0, 0, 0)
        
        # Section title
        competitive_title = QLabel("Competitive Audio (Real BF6 Settings)")
        competitive_title.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
        """)
        competitive_layout.addWidget(competitive_title)
        
        # Competitive settings
        competitive_grid = QGridLayout()
        competitive_grid.setSpacing(10)
        
        # Hit Indicator Sound (REAL setting)
        self.hit_indicator_check = QCheckBox("Hit Indicator Sound")
        self.hit_indicator_check.setChecked(True)
        self.hit_indicator_check.setStyleSheet(self.get_checkbox_style())
        competitive_grid.addWidget(self.hit_indicator_check, 0, 0, 1, 2)
        
        # In-Game Announcer (REAL setting)
        self.announcer_check = QCheckBox("In-Game Announcer")
        self.announcer_check.setChecked(True)
        self.announcer_check.setStyleSheet(self.get_checkbox_style())
        competitive_grid.addWidget(self.announcer_check, 1, 0, 1, 2)
        
        # Subtitles for Enemies (REAL setting)
        self.subtitles_enemies_check = QCheckBox("Enemy Subtitles")
        self.subtitles_enemies_check.setChecked(True)
        self.subtitles_enemies_check.setStyleSheet(self.get_checkbox_style())
        competitive_grid.addWidget(self.subtitles_enemies_check, 2, 0, 1, 2)
        
        # Subtitles for Friendlies (REAL setting)
        self.subtitles_friendlies_check = QCheckBox("Friendly Subtitles")
        self.subtitles_friendlies_check.setChecked(True)
        self.subtitles_friendlies_check.setStyleSheet(self.get_checkbox_style())
        competitive_grid.addWidget(self.subtitles_friendlies_check, 3, 0, 1, 2)
        
        # Subtitles for Squad (REAL setting)
        self.subtitles_squad_check = QCheckBox("Squad Subtitles")
        self.subtitles_squad_check.setChecked(True)
        self.subtitles_squad_check.setStyleSheet(self.get_checkbox_style())
        competitive_grid.addWidget(self.subtitles_squad_check, 4, 0, 1, 2)
        
        competitive_layout.addLayout(competitive_grid)
        competitive_frame.setLayout(competitive_layout)
        layout.addWidget(competitive_frame)
        
        # Apply Button
        apply_btn = QPushButton("Apply Audio Settings")
        apply_btn.setStyleSheet(self.get_primary_button_style())
        apply_btn.clicked.connect(self.apply_audio_settings)
        layout.addWidget(apply_btn)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_clean_network_tab(self):
        """Create a clean network tab."""
        tab = QWidget()
        tab.setStyleSheet("""
            QWidget {
                background: #1a1a1a;
                border: none;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Network Performance Section
        perf_frame = QFrame()
        perf_frame.setStyleSheet("""
            QFrame {
                background: #252525;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        perf_layout = QVBoxLayout()
        perf_layout.setContentsMargins(0, 0, 0, 0)
        
        perf_title = QLabel("Network Performance")
        perf_title.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
        """)
        perf_layout.addWidget(perf_title)
        
        perf_grid = QGridLayout()
        perf_grid.setSpacing(10)
        
        # Bandwidth
        perf_grid.addWidget(QLabel("Bandwidth (Mbps):"), 0, 0)
        self.bandwidth_spin = QSpinBox()
        self.bandwidth_spin.setRange(1, 1000)
        self.bandwidth_spin.setValue(1000)
        self.bandwidth_spin.setStyleSheet(self.get_spinbox_style())
        perf_grid.addWidget(self.bandwidth_spin, 0, 1)
        
        # Packet Size
        perf_grid.addWidget(QLabel("Packet Size:"), 1, 0)
        self.packet_size_combo = QComboBox()
        self.packet_size_combo.addItems(["1200", "1500", "9000"])
        self.packet_size_combo.setCurrentText("1500")
        self.packet_size_combo.setStyleSheet(self.get_combo_style())
        perf_grid.addWidget(self.packet_size_combo, 1, 1)
        
        # Send Rate
        perf_grid.addWidget(QLabel("Send Rate (Hz):"), 2, 0)
        self.send_rate_spin = QSpinBox()
        self.send_rate_spin.setRange(30, 120)
        self.send_rate_spin.setValue(60)
        self.send_rate_spin.setStyleSheet(self.get_spinbox_style())
        perf_grid.addWidget(self.send_rate_spin, 2, 1)
        
        perf_layout.addLayout(perf_grid)
        perf_frame.setLayout(perf_layout)
        layout.addWidget(perf_frame)
        
        # Latency Optimization Section
        latency_frame = QFrame()
        latency_frame.setStyleSheet("""
            QFrame {
                background: #252525;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        latency_layout = QVBoxLayout()
        latency_layout.setContentsMargins(0, 0, 0, 0)
        
        latency_title = QLabel("Latency Optimization")
        latency_title.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
        """)
        latency_layout.addWidget(latency_title)
        
        # Optimization checkboxes
        self.ping_optimization_check = QCheckBox("Ping Optimization")
        self.ping_optimization_check.setChecked(True)
        self.ping_optimization_check.setStyleSheet(self.get_checkbox_style())
        latency_layout.addWidget(self.ping_optimization_check)
        
        self.jitter_buffer_check = QCheckBox("Jitter Buffer")
        self.jitter_buffer_check.setChecked(True)
        self.jitter_buffer_check.setStyleSheet(self.get_checkbox_style())
        latency_layout.addWidget(self.jitter_buffer_check)
        
        self.packet_loss_recovery_check = QCheckBox("Packet Loss Recovery")
        self.packet_loss_recovery_check.setChecked(True)
        self.packet_loss_recovery_check.setStyleSheet(self.get_checkbox_style())
        latency_layout.addWidget(self.packet_loss_recovery_check)
        
        self.adaptive_bitrate_check = QCheckBox("Adaptive Bitrate")
        self.adaptive_bitrate_check.setChecked(True)
        self.adaptive_bitrate_check.setStyleSheet(self.get_checkbox_style())
        latency_layout.addWidget(self.adaptive_bitrate_check)
        
        latency_frame.setLayout(latency_layout)
        layout.addWidget(latency_frame)
        
        # Apply Button
        apply_btn = QPushButton("Apply Network Settings")
        apply_btn.setStyleSheet(self.get_primary_button_style())
        apply_btn.clicked.connect(self.apply_network_settings)
        layout.addWidget(apply_btn)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_clean_input_tab(self):
        """Create a clean input tab."""
        tab = QWidget()
        tab.setStyleSheet("""
            QWidget {
                background: #1a1a1a;
                border: none;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Mouse Settings Section
        mouse_frame = QFrame()
        mouse_frame.setStyleSheet("""
            QFrame {
                background: #252525;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        mouse_layout = QVBoxLayout()
        mouse_layout.setContentsMargins(0, 0, 0, 0)
        
        mouse_title = QLabel("Mouse Settings")
        mouse_title.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
        """)
        mouse_layout.addWidget(mouse_title)
        
        mouse_grid = QGridLayout()
        mouse_grid.setSpacing(10)
        
        # Mouse Sensitivity
        mouse_grid.addWidget(QLabel("Sensitivity:"), 0, 0)
        self.mouse_sensitivity_slider = QSlider(Qt.Orientation.Horizontal)
        self.mouse_sensitivity_slider.setRange(1, 100)
        self.mouse_sensitivity_slider.setValue(50)
        self.mouse_sensitivity_slider.setStyleSheet(self.get_slider_style())
        mouse_grid.addWidget(self.mouse_sensitivity_slider, 0, 1)
        
        # Polling Rate
        mouse_grid.addWidget(QLabel("Polling Rate (Hz):"), 1, 0)
        self.polling_rate_combo = QComboBox()
        self.polling_rate_combo.addItems(["125", "250", "500", "1000"])
        self.polling_rate_combo.setCurrentText("1000")
        self.polling_rate_combo.setStyleSheet(self.get_combo_style())
        mouse_grid.addWidget(self.polling_rate_combo, 1, 1)
        
        # Mouse options
        self.mouse_acceleration_check = QCheckBox("Mouse Acceleration")
        self.mouse_acceleration_check.setChecked(False)
        self.mouse_acceleration_check.setStyleSheet(self.get_checkbox_style())
        mouse_grid.addWidget(self.mouse_acceleration_check, 2, 0, 1, 2)
        
        self.raw_input_check = QCheckBox("Raw Input")
        self.raw_input_check.setChecked(True)
        self.raw_input_check.setStyleSheet(self.get_checkbox_style())
        mouse_grid.addWidget(self.raw_input_check, 3, 0, 1, 2)
        
        mouse_layout.addLayout(mouse_grid)
        mouse_frame.setLayout(mouse_layout)
        layout.addWidget(mouse_frame)
        
        # Controller Settings Section
        controller_frame = QFrame()
        controller_frame.setStyleSheet("""
            QFrame {
                background: #252525;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        controller_layout = QVBoxLayout()
        controller_layout.setContentsMargins(0, 0, 0, 0)
        
        controller_title = QLabel("Controller Settings")
        controller_title.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
        """)
        controller_layout.addWidget(controller_title)
        
        controller_grid = QGridLayout()
        controller_grid.setSpacing(10)
        
        # Controller Sensitivity
        controller_grid.addWidget(QLabel("Sensitivity:"), 0, 0)
        self.controller_sensitivity_slider = QSlider(Qt.Orientation.Horizontal)
        self.controller_sensitivity_slider.setRange(1, 100)
        self.controller_sensitivity_slider.setValue(50)
        self.controller_sensitivity_slider.setStyleSheet(self.get_slider_style())
        controller_grid.addWidget(self.controller_sensitivity_slider, 0, 1)
        
        # Deadzone
        controller_grid.addWidget(QLabel("Deadzone:"), 1, 0)
        self.deadzone_slider = QSlider(Qt.Orientation.Horizontal)
        self.deadzone_slider.setRange(0, 50)
        self.deadzone_slider.setValue(15)
        self.deadzone_slider.setStyleSheet(self.get_slider_style())
        controller_grid.addWidget(self.deadzone_slider, 1, 1)
        
        # Vibration
        self.vibration_check = QCheckBox("Controller Vibration")
        self.vibration_check.setChecked(True)
        self.vibration_check.setStyleSheet(self.get_checkbox_style())
        controller_grid.addWidget(self.vibration_check, 2, 0, 1, 2)
        
        controller_layout.addLayout(controller_grid)
        controller_frame.setLayout(controller_layout)
        layout.addWidget(controller_frame)
        
        # Apply Button
        apply_btn = QPushButton("Apply Input Settings")
        apply_btn.setStyleSheet(self.get_primary_button_style())
        apply_btn.clicked.connect(self.apply_input_settings)
        layout.addWidget(apply_btn)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_clean_competitive_tab(self):
        """Create a clean competitive tab."""
        tab = QWidget()
        tab.setStyleSheet("""
            QWidget {
                background: #1a1a1a;
                border: none;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # HUD Settings Section
        hud_frame = QFrame()
        hud_frame.setStyleSheet("""
            QFrame {
                background: #252525;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        hud_layout = QVBoxLayout()
        hud_layout.setContentsMargins(0, 0, 0, 0)
        
        hud_title = QLabel("HUD Settings")
        hud_title.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
        """)
        hud_layout.addWidget(hud_title)
        
        hud_grid = QGridLayout()
        hud_grid.setSpacing(10)
        
        # HUD Scale
        hud_grid.addWidget(QLabel("HUD Scale:"), 0, 0)
        self.hud_scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.hud_scale_slider.setRange(50, 150)
        self.hud_scale_slider.setValue(100)
        self.hud_scale_slider.setStyleSheet(self.get_slider_style())
        hud_grid.addWidget(self.hud_scale_slider, 0, 1)
        
        # Minimap Size
        hud_grid.addWidget(QLabel("Minimap Size:"), 1, 0)
        self.minimap_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.minimap_size_slider.setRange(50, 200)
        self.minimap_size_slider.setValue(120)
        self.minimap_size_slider.setStyleSheet(self.get_slider_style())
        hud_grid.addWidget(self.minimap_size_slider, 1, 1)
        
        # Crosshair Size
        hud_grid.addWidget(QLabel("Crosshair Size:"), 2, 0)
        self.crosshair_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.crosshair_size_slider.setRange(50, 150)
        self.crosshair_size_slider.setValue(80)
        self.crosshair_size_slider.setStyleSheet(self.get_slider_style())
        hud_grid.addWidget(self.crosshair_size_slider, 2, 1)
        
        hud_layout.addLayout(hud_grid)
        hud_frame.setLayout(hud_layout)
        layout.addWidget(hud_frame)
        
        # Competitive Features Section
        competitive_frame = QFrame()
        competitive_frame.setStyleSheet("""
            QFrame {
                background: #252525;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        competitive_layout = QVBoxLayout()
        competitive_layout.setContentsMargins(0, 0, 0, 0)
        
        competitive_title = QLabel("Competitive Features")
        competitive_title.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 10px;
        """)
        competitive_layout.addWidget(competitive_title)
        
        # Feature checkboxes
        self.hit_marker_check = QCheckBox("Hit Marker")
        self.hit_marker_check.setChecked(True)
        self.hit_marker_check.setStyleSheet(self.get_checkbox_style())
        competitive_layout.addWidget(self.hit_marker_check)
        
        self.damage_numbers_check = QCheckBox("Damage Numbers")
        self.damage_numbers_check.setChecked(True)
        self.damage_numbers_check.setStyleSheet(self.get_checkbox_style())
        competitive_layout.addWidget(self.damage_numbers_check)
        
        self.kill_feed_check = QCheckBox("Kill Feed")
        self.kill_feed_check.setChecked(True)
        self.kill_feed_check.setStyleSheet(self.get_checkbox_style())
        competitive_layout.addWidget(self.kill_feed_check)
        
        self.fps_counter_check = QCheckBox("FPS Counter")
        self.fps_counter_check.setChecked(True)
        self.fps_counter_check.setStyleSheet(self.get_checkbox_style())
        competitive_layout.addWidget(self.fps_counter_check)
        
        self.ping_display_check = QCheckBox("Ping Display")
        self.ping_display_check.setChecked(True)
        self.ping_display_check.setStyleSheet(self.get_checkbox_style())
        competitive_layout.addWidget(self.ping_display_check)
        
        competitive_frame.setLayout(competitive_layout)
        layout.addWidget(competitive_frame)
        
        # Apply Button
        apply_btn = QPushButton("Apply Competitive Settings")
        apply_btn.setStyleSheet(self.get_primary_button_style())
        apply_btn.clicked.connect(self.apply_competitive_settings)
        layout.addWidget(apply_btn)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_network_features_tab(self):
        """Create the network features tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Network Performance Settings
        performance_group = QGroupBox("⚡ Network Performance")
        performance_group.setStyleSheet(self.get_group_style())
        performance_layout = QGridLayout()
        
        # Max Bandwidth
        performance_layout.addWidget(QLabel("Max Bandwidth (Mbps):"), 0, 0)
        self.bandwidth_spin = QSpinBox()
        self.bandwidth_spin.setRange(1, 1000)
        self.bandwidth_spin.setValue(1000)
        performance_layout.addWidget(self.bandwidth_spin, 0, 1)
        
        # Packet Size
        performance_layout.addWidget(QLabel("Packet Size:"), 1, 0)
        self.packet_size_combo = QComboBox()
        self.packet_size_combo.addItems(["1200", "1500", "9000"])
        self.packet_size_combo.setCurrentText("1500")
        performance_layout.addWidget(self.packet_size_combo, 1, 1)
        
        # Send/Receive Rate
        performance_layout.addWidget(QLabel("Send Rate (Hz):"), 2, 0)
        self.send_rate_spin = QSpinBox()
        self.send_rate_spin.setRange(30, 120)
        self.send_rate_spin.setValue(60)
        performance_layout.addWidget(self.send_rate_spin, 2, 1)
        
        performance_group.setLayout(performance_layout)
        layout.addWidget(performance_group)
        
        # Latency Optimization
        latency_group = QGroupBox("🏃 Latency Optimization")
        latency_group.setStyleSheet(self.get_group_style())
        latency_layout = QVBoxLayout()
        
        # Optimization checkboxes
        self.ping_optimization_check = QCheckBox("Ping Optimization")
        self.ping_optimization_check.setChecked(True)
        latency_layout.addWidget(self.ping_optimization_check)
        
        self.jitter_buffer_check = QCheckBox("Jitter Buffer")
        self.jitter_buffer_check.setChecked(True)
        latency_layout.addWidget(self.jitter_buffer_check)
        
        self.packet_loss_recovery_check = QCheckBox("Packet Loss Recovery")
        self.packet_loss_recovery_check.setChecked(True)
        latency_layout.addWidget(self.packet_loss_recovery_check)
        
        self.adaptive_bitrate_check = QCheckBox("Adaptive Bitrate")
        self.adaptive_bitrate_check.setChecked(True)
        latency_layout.addWidget(self.adaptive_bitrate_check)
        
        latency_group.setLayout(latency_layout)
        layout.addWidget(latency_group)
        
        # Apply Network Settings Button
        apply_network_btn = QPushButton("🌐 Apply Network Settings")
        apply_network_btn.setStyleSheet(self.get_button_style())
        apply_network_btn.clicked.connect(self.apply_network_settings)
        layout.addWidget(apply_network_btn)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_input_features_tab(self):
        """Create the input features tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Mouse Settings
        mouse_group = QGroupBox("🖱️ Mouse Settings")
        mouse_group.setStyleSheet(self.get_group_style())
        mouse_layout = QGridLayout()
        
        # Mouse Sensitivity
        mouse_layout.addWidget(QLabel("Mouse Sensitivity:"), 0, 0)
        self.mouse_sensitivity_slider = QSlider(Qt.Orientation.Horizontal)
        self.mouse_sensitivity_slider.setRange(1, 100)
        self.mouse_sensitivity_slider.setValue(50)
        mouse_layout.addWidget(self.mouse_sensitivity_slider, 0, 1)
        
        # Mouse Acceleration
        self.mouse_acceleration_check = QCheckBox("Mouse Acceleration")
        self.mouse_acceleration_check.setChecked(False)
        mouse_layout.addWidget(self.mouse_acceleration_check, 1, 0, 1, 2)
        
        # Raw Input
        self.raw_input_check = QCheckBox("Raw Input")
        self.raw_input_check.setChecked(True)
        mouse_layout.addWidget(self.raw_input_check, 2, 0, 1, 2)
        
        # Polling Rate
        mouse_layout.addWidget(QLabel("Polling Rate (Hz):"), 3, 0)
        self.polling_rate_combo = QComboBox()
        self.polling_rate_combo.addItems(["125", "250", "500", "1000"])
        self.polling_rate_combo.setCurrentText("1000")
        mouse_layout.addWidget(self.polling_rate_combo, 3, 1)
        
        mouse_group.setLayout(mouse_layout)
        layout.addWidget(mouse_group)
        
        # Controller Settings
        controller_group = QGroupBox("🎮 Controller Settings")
        controller_group.setStyleSheet(self.get_group_style())
        controller_layout = QGridLayout()
        
        # Controller Sensitivity
        controller_layout.addWidget(QLabel("Controller Sensitivity:"), 0, 0)
        self.controller_sensitivity_slider = QSlider(Qt.Orientation.Horizontal)
        self.controller_sensitivity_slider.setRange(1, 100)
        self.controller_sensitivity_slider.setValue(50)
        controller_layout.addWidget(self.controller_sensitivity_slider, 0, 1)
        
        # Deadzone
        controller_layout.addWidget(QLabel("Deadzone:"), 1, 0)
        self.deadzone_slider = QSlider(Qt.Orientation.Horizontal)
        self.deadzone_slider.setRange(0, 50)
        self.deadzone_slider.setValue(15)
        controller_layout.addWidget(self.deadzone_slider, 1, 1)
        
        # Vibration
        self.vibration_check = QCheckBox("Controller Vibration")
        self.vibration_check.setChecked(True)
        controller_layout.addWidget(self.vibration_check, 2, 0, 1, 2)
        
        controller_group.setLayout(controller_layout)
        layout.addWidget(controller_group)
        
        # Apply Input Settings Button
        apply_input_btn = QPushButton("🎮 Apply Input Settings")
        apply_input_btn.setStyleSheet(self.get_button_style())
        apply_input_btn.clicked.connect(self.apply_input_settings)
        layout.addWidget(apply_input_btn)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_competitive_features_tab(self):
        """Create the competitive features tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # HUD Settings
        hud_group = QGroupBox("📊 HUD Settings")
        hud_group.setStyleSheet(self.get_group_style())
        hud_layout = QGridLayout()
        
        # HUD Scale
        hud_layout.addWidget(QLabel("HUD Scale:"), 0, 0)
        self.hud_scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.hud_scale_slider.setRange(50, 150)
        self.hud_scale_slider.setValue(100)
        hud_layout.addWidget(self.hud_scale_slider, 0, 1)
        
        # Minimap Size
        hud_layout.addWidget(QLabel("Minimap Size:"), 1, 0)
        self.minimap_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.minimap_size_slider.setRange(50, 200)
        self.minimap_size_slider.setValue(120)
        hud_layout.addWidget(self.minimap_size_slider, 1, 1)
        
        # Crosshair Size
        hud_layout.addWidget(QLabel("Crosshair Size:"), 2, 0)
        self.crosshair_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.crosshair_size_slider.setRange(50, 150)
        self.crosshair_size_slider.setValue(80)
        hud_layout.addWidget(self.crosshair_size_slider, 2, 1)
        
        hud_group.setLayout(hud_layout)
        layout.addWidget(hud_group)
        
        # Competitive Features
        competitive_group = QGroupBox("⚔️ Competitive Features")
        competitive_group.setStyleSheet(self.get_group_style())
        competitive_layout = QVBoxLayout()
        
        # Feature checkboxes
        self.hit_marker_check = QCheckBox("Hit Marker")
        self.hit_marker_check.setChecked(True)
        competitive_layout.addWidget(self.hit_marker_check)
        
        self.damage_numbers_check = QCheckBox("Damage Numbers")
        self.damage_numbers_check.setChecked(True)
        competitive_layout.addWidget(self.damage_numbers_check)
        
        self.kill_feed_check = QCheckBox("Kill Feed")
        self.kill_feed_check.setChecked(True)
        competitive_layout.addWidget(self.kill_feed_check)
        
        self.fps_counter_check = QCheckBox("FPS Counter")
        self.fps_counter_check.setChecked(True)
        competitive_layout.addWidget(self.fps_counter_check)
        
        self.ping_display_check = QCheckBox("Ping Display")
        self.ping_display_check.setChecked(True)
        competitive_layout.addWidget(self.ping_display_check)
        
        competitive_group.setLayout(competitive_layout)
        layout.addWidget(competitive_group)
        
        # Apply Competitive Settings Button
        apply_competitive_btn = QPushButton("⚔️ Apply Competitive Settings")
        apply_competitive_btn.setStyleSheet(self.get_button_style())
        apply_competitive_btn.clicked.connect(self.apply_competitive_settings)
        layout.addWidget(apply_competitive_btn)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def setup_timers(self):
        """Setup refresh timers."""
        # System info refresh timer
        self.system_timer = QTimer()
        self.system_timer.timeout.connect(self.refresh_system_info)
        self.system_timer.start(5000)  # Refresh every 5 seconds
        
        # Initial refresh
        self.refresh_system_info()
    
    def refresh_system_info(self):
        """Refresh system information."""
        try:
            system_info = self.config_manager.get_bf6_system_info()
            
            # Update process status
            process_info = system_info['process_info']
            if process_info['running']:
                self.process_status.setText(f"BF6 Running - {process_info['status']}")
                self.status_indicator.setText("BF6 Active")
            else:
                self.process_status.setText("BF6 Not Running")
                self.status_indicator.setText("BF6 Inactive")
            
            # Update system info
            system_info_text = f"{system_info['system_info']['os']} {system_info['system_info']['architecture']}"
            self.system_info_label.setText(f"System: {system_info_text}")
            
            # Update config path
            if self.config_manager.config_path:
                config_path = str(self.config_manager.config_path)
                self.config_path_label.setText(f"Config: {config_path}")
            else:
                self.config_path_label.setText("Config: Not detected")
            
            # Update last updated time
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M:%S")
            self.last_updated_label.setText(f"Updated: {current_time}")
            
        except Exception as e:
            log_error(f"Failed to refresh system info: {e}", "BF6_FEATURES_UI")
    
    def apply_audio_settings(self):
        """Apply audio settings (REAL BF6 settings only)."""
        try:
            settings = {
                # REAL BF6 Audio Settings
                'GstAudio.AudioQuality': str(self.audio_quality_combo.currentIndex() + 1),
                'GstAudio.SoundSystemSize': str(self.sound_system_size_spin.value()),
                'GstAudio.SpeakerConfiguration': str(self.speaker_config_combo.currentIndex() + 1),
                'GstAudio.HitIndicatorSound': '1' if self.hit_indicator_check.isChecked() else '0',
                'GstAudio.InGameAnnouncer_OnOff': '1' if self.announcer_check.isChecked() else '0',
                'GstAudio.SubtitlesEnemies': '1' if self.subtitles_enemies_check.isChecked() else '0',
                'GstAudio.SubtitlesFriendlies': '1' if self.subtitles_friendlies_check.isChecked() else '0',
                'GstAudio.SubtitlesSquad': '1' if self.subtitles_squad_check.isChecked() else '0',
            }
            
            # Apply settings
            for key, value in settings.items():
                self.config_manager.config_data[key] = value
            
            self.config_manager.save_config()
            self.settings_applied.emit("audio", settings)
            
            QMessageBox.information(self, "Audio Settings Applied", 
                                  "BF6 audio settings have been applied successfully!\n\n"
                                  "Only REAL BF6 config settings were used.")
            
        except Exception as e:
            log_error(f"Failed to apply audio settings: {e}", "BF6_FEATURES_UI")
            QMessageBox.critical(self, "Error", f"Failed to apply audio settings: {e}")
    
    def apply_network_settings(self):
        """Apply network settings."""
        try:
            settings = {
                'GstNetwork.MaxBandwidth': str(self.bandwidth_spin.value() * 1000),  # Convert to Kbps
                'GstNetwork.PacketSize': self.packet_size_combo.currentText(),
                'GstNetwork.SendRate': str(self.send_rate_spin.value()),
                'GstNetwork.PingOptimization': '1' if self.ping_optimization_check.isChecked() else '0',
                'GstNetwork.JitterBuffer': '1' if self.jitter_buffer_check.isChecked() else '0',
                'GstNetwork.PacketLossRecovery': '1' if self.packet_loss_recovery_check.isChecked() else '0',
                'GstNetwork.AdaptiveBitrate': '1' if self.adaptive_bitrate_check.isChecked() else '0',
            }
            
            # Apply settings
            for key, value in settings.items():
                self.config_manager.config_data[key] = value
            
            self.config_manager.save_config()
            self.settings_applied.emit("network", settings)
            
            QMessageBox.information(self, "Network Settings Applied", 
                                  "BF6 network settings have been applied successfully!")
            
        except Exception as e:
            log_error(f"Failed to apply network settings: {e}", "BF6_FEATURES_UI")
            QMessageBox.critical(self, "Error", f"Failed to apply network settings: {e}")
    
    def apply_input_settings(self):
        """Apply input settings."""
        try:
            settings = {
                'GstInput.MouseSensitivity': str(self.mouse_sensitivity_slider.value() / 50.0),
                'GstInput.MouseAcceleration': '1' if self.mouse_acceleration_check.isChecked() else '0',
                'GstInput.MouseRawInput': '1' if self.raw_input_check.isChecked() else '0',
                'GstInput.MousePollingRate': self.polling_rate_combo.currentText(),
                'GstInput.ControllerSensitivity': str(self.controller_sensitivity_slider.value() / 50.0),
                'GstInput.ControllerDeadzone': str(self.deadzone_slider.value() / 100.0),
                'GstInput.ControllerVibration': '1' if self.vibration_check.isChecked() else '0',
            }
            
            # Apply settings
            for key, value in settings.items():
                self.config_manager.config_data[key] = value
            
            self.config_manager.save_config()
            self.settings_applied.emit("input", settings)
            
            QMessageBox.information(self, "Input Settings Applied", 
                                  "BF6 input settings have been applied successfully!")
            
        except Exception as e:
            log_error(f"Failed to apply input settings: {e}", "BF6_FEATURES_UI")
            QMessageBox.critical(self, "Error", f"Failed to apply input settings: {e}")
    
    def apply_competitive_settings(self):
        """Apply competitive settings."""
        try:
            settings = {
                'GstUI.HUDScale': str(self.hud_scale_slider.value() / 100.0),
                'GstUI.MinimapSize': str(self.minimap_size_slider.value() / 100.0),
                'GstUI.CrosshairSize': str(self.crosshair_size_slider.value() / 100.0),
                'GstUI.HitMarker': '1' if self.hit_marker_check.isChecked() else '0',
                'GstUI.DamageNumbers': '1' if self.damage_numbers_check.isChecked() else '0',
                'GstUI.KillFeed': '1' if self.kill_feed_check.isChecked() else '0',
                'GstUI.FPSCounter': '1' if self.fps_counter_check.isChecked() else '0',
                'GstUI.PingDisplay': '1' if self.ping_display_check.isChecked() else '0',
            }
            
            # Apply settings
            for key, value in settings.items():
                self.config_manager.config_data[key] = value
            
            self.config_manager.save_config()
            self.settings_applied.emit("competitive", settings)
            
            QMessageBox.information(self, "Competitive Settings Applied", 
                                  "BF6 competitive settings have been applied successfully!")
            
        except Exception as e:
            log_error(f"Failed to apply competitive settings: {e}", "BF6_FEATURES_UI")
            QMessageBox.critical(self, "Error", f"Failed to apply competitive settings: {e}")
    
    def apply_all_optimizations(self):
        """Apply all BF6 optimizations."""
        try:
            # Get all current settings from UI
            all_settings = {}
            
            # Audio settings
            all_settings.update({
                'GstAudio.SampleRate': self.sample_rate_combo.currentText(),
                'GstAudio.BitDepth': self.bit_depth_combo.currentText(),
                'GstAudio.AudioQuality': str(self.audio_quality_combo.currentIndex() + 1),
                'GstAudio.FootstepVolume': str(self.footstep_slider.value() / 100.0),
                'GstAudio.WeaponVolume': str(self.weapon_slider.value() / 100.0),
                'GstAudio.SpatialAudio': '1' if self.spatial_audio_check.isChecked() else '0',
            })
            
            # Network settings
            all_settings.update({
                'GstNetwork.MaxBandwidth': str(self.bandwidth_spin.value() * 1000),
                'GstNetwork.PacketSize': self.packet_size_combo.currentText(),
                'GstNetwork.SendRate': str(self.send_rate_spin.value()),
                'GstNetwork.PingOptimization': '1' if self.ping_optimization_check.isChecked() else '0',
                'GstNetwork.JitterBuffer': '1' if self.jitter_buffer_check.isChecked() else '0',
                'GstNetwork.PacketLossRecovery': '1' if self.packet_loss_recovery_check.isChecked() else '0',
                'GstNetwork.AdaptiveBitrate': '1' if self.adaptive_bitrate_check.isChecked() else '0',
            })
            
            # Input settings
            all_settings.update({
                'GstInput.MouseSensitivity': str(self.mouse_sensitivity_slider.value() / 50.0),
                'GstInput.MouseAcceleration': '1' if self.mouse_acceleration_check.isChecked() else '0',
                'GstInput.MouseRawInput': '1' if self.raw_input_check.isChecked() else '0',
                'GstInput.MousePollingRate': self.polling_rate_combo.currentText(),
                'GstInput.ControllerSensitivity': str(self.controller_sensitivity_slider.value() / 50.0),
                'GstInput.ControllerDeadzone': str(self.deadzone_slider.value() / 100.0),
                'GstInput.ControllerVibration': '1' if self.vibration_check.isChecked() else '0',
            })
            
            # Competitive settings
            all_settings.update({
                'GstUI.HUDScale': str(self.hud_scale_slider.value() / 100.0),
                'GstUI.MinimapSize': str(self.minimap_size_slider.value() / 100.0),
                'GstUI.CrosshairSize': str(self.crosshair_size_slider.value() / 100.0),
                'GstUI.HitMarker': '1' if self.hit_marker_check.isChecked() else '0',
                'GstUI.DamageNumbers': '1' if self.damage_numbers_check.isChecked() else '0',
                'GstUI.KillFeed': '1' if self.kill_feed_check.isChecked() else '0',
                'GstUI.FPSCounter': '1' if self.fps_counter_check.isChecked() else '0',
                'GstUI.PingDisplay': '1' if self.ping_display_check.isChecked() else '0',
            })
            
            # Apply all settings
            for key, value in all_settings.items():
                self.config_manager.config_data[key] = value
            
            self.config_manager.save_config()
            self.settings_applied.emit("all", all_settings)
            
            QMessageBox.information(self, "All Optimizations Applied", 
                                  f"All BF6 optimizations have been applied successfully!\n\n"
                                  f"Applied {len(all_settings)} settings across all categories.")
            
        except Exception as e:
            log_error(f"Failed to apply all optimizations: {e}", "BF6_FEATURES_UI")
            QMessageBox.critical(self, "Error", f"Failed to apply all optimizations: {e}")
    
    def get_group_style(self):
        """Get the group box style."""
        return """
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #ecf0f1;
                border: 2px solid #7f8c8d;
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
    
    def get_button_style(self):
        """Get the button style."""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #1f618d);
            }
        """
    
    def get_primary_button_style(self):
        """Get the primary button style."""
        return """
            QPushButton {
                background: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background: #106ebe;
            }
            QPushButton:pressed {
                background: #005a9e;
            }
        """
    
    def get_secondary_button_style(self):
        """Get the secondary button style."""
        return """
            QPushButton {
                background: #404040;
                color: #cccccc;
                border: 1px solid #666666;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #4a4a4a;
                border-color: #888888;
            }
            QPushButton:pressed {
                background: #333333;
            }
        """
    
    def get_combo_style(self):
        """Get the combo box style."""
        return """
            QComboBox {
                background: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 12px;
            }
            QComboBox:hover {
                border-color: #777777;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #cccccc;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                selection-background-color: #0078d4;
            }
        """
    
    def get_slider_style(self):
        """Get the slider style."""
        return """
            QSlider::groove:horizontal {
                border: 1px solid #555555;
                height: 6px;
                background: #333333;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #0078d4;
                border: 1px solid #555555;
                width: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #106ebe;
            }
            QSlider::sub-page:horizontal {
                background: #0078d4;
                border-radius: 3px;
            }
        """
    
    def get_checkbox_style(self):
        """Get the checkbox style."""
        return """
            QCheckBox {
                color: #cccccc;
                font-size: 12px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #555555;
                border-radius: 3px;
                background: #333333;
            }
            QCheckBox::indicator:checked {
                background: #0078d4;
                border-color: #0078d4;
            }
            QCheckBox::indicator:checked:hover {
                background: #106ebe;
            }
        """
    
    def get_spinbox_style(self):
        """Get the spinbox style."""
        return """
            QSpinBox {
                background: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 12px;
            }
            QSpinBox:hover {
                border-color: #777777;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background: #404040;
                border: 1px solid #555555;
                width: 16px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background: #4a4a4a;
            }
        """
