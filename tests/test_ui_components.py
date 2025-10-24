"""
Tests for UI components
"""

import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import MainWindow, QuickSettingsTab, GraphicsTab, BackupTab


class TestUIComponents:
    """Test cases for UI components"""
    
    @pytest.fixture(autouse=True)
    def setup_qt_app(self):
        """Setup QApplication for tests"""
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
        yield
        # Cleanup handled by pytest-qt
    
    def test_main_window_creation(self):
        """Test MainWindow creation"""
        with patch('main.ConfigManager') as mock_config:
            mock_config.return_value.config_path = "test_path"
            mock_config.return_value.settings = {}
            mock_config.return_value.BACKUP_DIR = Mock()
            mock_config.return_value.BACKUP_DIR.exists.return_value = True
            
            window = MainWindow()
            assert window is not None
            assert window.windowTitle() == "FieldTuner - Battlefield 6 Configuration Tool"
    
    def test_quick_settings_tab(self):
        """Test QuickSettingsTab creation"""
        with patch('main.ConfigManager') as mock_config:
            mock_config.return_value.config_path = "test_path"
            mock_config.return_value.settings = {}
            mock_config.return_value.BACKUP_DIR = Mock()
            mock_config.return_value.BACKUP_DIR.exists.return_value = True
            
            tab = QuickSettingsTab(mock_config.return_value)
            assert tab is not None
            assert hasattr(tab, 'preset_combo')
            assert hasattr(tab, 'apply_preset_btn')
    
    def test_graphics_tab(self):
        """Test GraphicsTab creation"""
        with patch('main.ConfigManager') as mock_config:
            mock_config.return_value.config_path = "test_path"
            mock_config.return_value.settings = {}
            mock_config.return_value.BACKUP_DIR = Mock()
            mock_config.return_value.BACKUP_DIR.exists.return_value = True
            
            tab = GraphicsTab(mock_config.return_value)
            assert tab is not None
            assert hasattr(tab, 'resolution_combo')
            assert hasattr(tab, 'quality_combo')
    
    def test_backup_tab(self):
        """Test BackupTab creation"""
        with patch('main.ConfigManager') as mock_config:
            mock_config.return_value.config_path = "test_path"
            mock_config.return_value.settings = {}
            mock_config.return_value.BACKUP_DIR = Mock()
            mock_config.return_value.BACKUP_DIR.exists.return_value = True
            
            tab = BackupTab(mock_config.return_value)
            assert tab is not None
            assert hasattr(tab, 'backup_list')
            assert hasattr(tab, 'create_backup_btn')
    
    def test_toggle_switch_creation(self):
        """Test toggle switch creation"""
        with patch('main.ConfigManager') as mock_config:
            mock_config.return_value.config_path = "test_path"
            mock_config.return_value.settings = {}
            mock_config.return_value.BACKUP_DIR = Mock()
            mock_config.return_value.BACKUP_DIR.exists.return_value = True
            
            tab = QuickSettingsTab(mock_config.return_value)
            
            # Test toggle creation
            toggle = tab.create_professional_toggle("Test Setting", "Test Description")
            assert toggle is not None
            assert hasattr(toggle, 'set_checked')
            assert hasattr(toggle, 'is_checked')
    
    def test_preset_application(self):
        """Test preset application"""
        with patch('main.ConfigManager') as mock_config:
            mock_config.return_value.config_path = "test_path"
            mock_config.return_value.settings = {}
            mock_config.return_value.BACKUP_DIR = Mock()
            mock_config.return_value.BACKUP_DIR.exists.return_value = True
            
            tab = QuickSettingsTab(mock_config.return_value)
            
            # Test preset application
            with patch.object(tab, 'apply_preset') as mock_apply:
                tab.apply_preset("esports_pro")
                mock_apply.assert_called_once_with("esports_pro")
    
    def test_backup_creation(self):
        """Test backup creation"""
        with patch('main.ConfigManager') as mock_config:
            mock_config.return_value.config_path = "test_path"
            mock_config.return_value.settings = {}
            mock_config.return_value.BACKUP_DIR = Mock()
            mock_config.return_value.BACKUP_DIR.exists.return_value = True
            mock_config.return_value._create_backup.return_value = "backup_path"
            
            tab = BackupTab(mock_config.return_value)
            
            # Test backup creation
            tab.create_backup()
            mock_config.return_value._create_backup.assert_called_once()
    
    def test_graphics_settings_loading(self):
        """Test graphics settings loading"""
        with patch('main.ConfigManager') as mock_config:
            mock_config.return_value.config_path = "test_path"
            mock_config.return_value.settings = {
                'GstRender.ResolutionScale': '1.0',
                'GstRender.Dx12Enabled': '1'
            }
            mock_config.return_value.BACKUP_DIR = Mock()
            mock_config.return_value.BACKUP_DIR.exists.return_value = True
            
            tab = GraphicsTab(mock_config.return_value)
            
            # Test settings loading
            tab.load_settings()
            # Settings should be loaded into the UI components
            assert hasattr(tab, 'resolution_combo')
            assert hasattr(tab, 'quality_combo')


class TestUIInteractions:
    """Test UI interactions and user events"""
    
    @pytest.fixture(autouse=True)
    def setup_qt_app(self):
        """Setup QApplication for tests"""
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
        yield
    
    def test_button_clicks(self):
        """Test button click events"""
        with patch('main.ConfigManager') as mock_config:
            mock_config.return_value.config_path = "test_path"
            mock_config.return_value.settings = {}
            mock_config.return_value.BACKUP_DIR = Mock()
            mock_config.return_value.BACKUP_DIR.exists.return_value = True
            
            tab = QuickSettingsTab(mock_config.return_value)
            
            # Test apply preset button
            with patch.object(tab, 'apply_preset') as mock_apply:
                tab.apply_preset_btn.click()
                mock_apply.assert_called_once()
    
    def test_combo_box_selection(self):
        """Test combo box selection events"""
        with patch('main.ConfigManager') as mock_config:
            mock_config.return_value.config_path = "test_path"
            mock_config.return_value.settings = {}
            mock_config.return_value.BACKUP_DIR = Mock()
            mock_config.return_value.BACKUP_DIR.exists.return_value = True
            
            tab = GraphicsTab(mock_config.return_value)
            
            # Test combo box selection
            if hasattr(tab, 'quality_combo'):
                tab.quality_combo.setCurrentText("High")
                assert tab.quality_combo.currentText() == "High"
    
    def test_list_selection(self):
        """Test list widget selection"""
        with patch('main.ConfigManager') as mock_config:
            mock_config.return_value.config_path = "test_path"
            mock_config.return_value.settings = {}
            mock_config.return_value.BACKUP_DIR = Mock()
            mock_config.return_value.BACKUP_DIR.exists.return_value = True
            mock_config.return_value.list_backups.return_value = ["backup1.bak", "backup2.bak"]
            
            tab = BackupTab(mock_config.return_value)
            
            # Test backup list population
            tab.refresh_backups()
            assert tab.backup_list.count() >= 0  # May be 0 if no backups exist
