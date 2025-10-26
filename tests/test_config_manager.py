"""
Tests for ConfigManager class
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "PROFSAVE_profile"
        self.backup_dir = Path(self.temp_dir) / "backups"
        
        # Create a mock config file
        self.config_path.write_bytes(b"mock_config_data")
    
    def teardown_method(self):
        """Cleanup after each test method"""
        if hasattr(self, 'temp_dir') and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_init_with_valid_config(self):
        """Test ConfigManager initialization with valid config"""
        with patch.object(ConfigManager, '_parse_config_data', return_value={}):
            manager = ConfigManager(self.config_path)
            assert manager.config_path == self.config_path
            assert manager.BACKUP_DIR.exists()
    
    def test_detect_config_file(self):
        """Test config file detection"""
        # Test with existing file
        manager = ConfigManager(self.config_path)
        assert manager.config_path == self.config_path
        
        # Test with non-existent file
        non_existent = Path(self.temp_dir) / "non_existent"
        with pytest.raises(FileNotFoundError):
            ConfigManager(non_existent)
    
    def test_create_backup(self):
        """Test backup creation"""
        with patch.object(ConfigManager, '_parse_config_data', return_value={}):
            manager = ConfigManager(self.config_path)
            
            # Test backup creation
            backup_path = manager._create_backup("test_backup")
            assert backup_path is not None
            assert backup_path.exists()
            assert "test_backup" in backup_path.name
    
    def test_list_backups(self):
        """Test backup listing"""
        with patch.object(ConfigManager, '_parse_config_data', return_value={}):
            manager = ConfigManager(self.config_path)
            
            # Get initial backup count (should be 1 from automatic backup during init)
            initial_backups = manager.list_backups()
            initial_count = len(initial_backups)
            
            # Create some test backups
            manager._create_backup("backup1")
            manager._create_backup("backup2")
            
            backups = manager.list_backups()
            assert len(backups) == initial_count + 2
            assert all(backup.endswith('.bak') for backup in backups)
    
    def test_save_config(self):
        """Test config saving"""
        with patch.object(ConfigManager, '_parse_config_data', return_value={}):
            manager = ConfigManager(self.config_path)
            
            # Test saving config
            result = manager.save_config()
            assert result is True
            assert self.config_path.exists()
    
    def test_parse_config_data(self):
        """Test config data parsing"""
        # Create a mock binary config
        mock_data = b"mock_binary_data"
        self.config_path.write_bytes(mock_data)
        
        manager = ConfigManager(self.config_path)
        
        # Test that parsing doesn't crash
        # Note: This is a basic test - real parsing would need actual BF6 config data
        assert hasattr(manager, 'settings')
    
    def test_backup_directory_creation(self):
        """Test backup directory creation"""
        with patch.object(ConfigManager, '_parse_config_data', return_value={}):
            # Test with non-existent backup directory
            backup_path = Path(self.temp_dir) / "new_backup_dir"
            manager = ConfigManager(self.config_path)
            
            # Backup directory should be created
            assert manager.BACKUP_DIR.exists()
    
    def test_error_handling(self):
        """Test error handling in various scenarios"""
        with patch.object(ConfigManager, '_parse_config_data', return_value={}):
            manager = ConfigManager(self.config_path)
            
            # Test with invalid backup name
            backup_path = manager._create_backup("")
            assert backup_path is not None
            
            # Test with None backup name
            backup_path = manager._create_backup(None)
            assert backup_path is not None


class TestConfigManagerIntegration:
    """Integration tests for ConfigManager"""
    
    def setup_method(self):
        """Setup for integration tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "PROFSAVE_profile"
        
        # Create a more realistic mock config
        self.config_path.write_bytes(b"mock_battlefield_config_data")
    
    def teardown_method(self):
        """Cleanup after integration tests"""
        shutil.rmtree(self.temp_dir)
    
    def test_full_workflow(self):
        """Test complete workflow: load -> backup -> modify -> save"""
        with patch.object(ConfigManager, '_parse_config_data', return_value={}):
            manager = ConfigManager(self.config_path)
            
            # Create backup
            backup_path = manager._create_backup("workflow_test")
            assert backup_path.exists()
            
            # Save config
            result = manager.save_config()
            assert result is True
            
            # Verify original file still exists
            assert self.config_path.exists()
    
    def test_multiple_backups(self):
        """Test creating and managing multiple backups"""
        with patch.object(ConfigManager, '_parse_config_data', return_value={}):
            manager = ConfigManager(self.config_path)
            
            # Get initial backup count (should be 1 from automatic backup during init)
            initial_backups = manager.list_backups()
            initial_count = len(initial_backups)
            
            # Create multiple backups
            backup1 = manager._create_backup("backup1")
            backup2 = manager._create_backup("backup2")
            backup3 = manager._create_backup("backup3")
            
            # All backups should exist
            assert backup1.exists()
            assert backup2.exists()
            assert backup3.exists()
            
            # List backups
            backups = manager.list_backups()
            assert len(backups) == initial_count + 3
