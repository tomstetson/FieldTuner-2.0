#!/usr/bin/env python3
"""
Test script for FieldTuner
Tests basic functionality without requiring actual Battlefield 6 config files.
"""

import sys
import os
import tempfile
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config_manager import ConfigManager


def create_test_config():
    """Create a test configuration file."""
    test_config = """GstRender.Dx12Enabled 1
GstRender.MotionBlurEnable 1
GstRender.DepthOfFieldEnable 1
GstRender.AntiAliasingDeferred 2
GstRender.ResolutionScale 1.0
GstRender.FullscreenMode 1
GstRender.VSyncEnable 0
GstAudio.MasterVolume 100
GstAudio.MusicVolume 80
GstAudio.SFXVolume 100
GstInput.MouseSensitivity 50
GstInput.MouseAcceleration 0
GstInput.RawInput 1
GstGame.Difficulty 1
GstGame.AutoAim 0
GstGame.AutoHeal 1
GstNetwork.MaxPing 150
GstNetwork.Quality 2
GstNetwork.UploadRate 1000
GstNetwork.DownloadRate 2000
"""
    return test_config


def test_config_manager():
    """Test the ConfigManager class."""
    print("Testing ConfigManager...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test config file
        config_file = temp_path / "PROFSAVE_profile"
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(create_test_config())
        
        # Create a mock config manager
        config_manager = ConfigManager()
        
        # Override the config path for testing
        config_manager.config_path = config_file
        config_manager.BACKUP_DIR = temp_path / "backups"
        config_manager.LOG_DIR = temp_path / "logs"
        
        # Create directories
        config_manager.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        config_manager.LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        # Test loading config
        print("  Testing config loading...")
        if config_manager._load_config():
            print("  ✓ Config loaded successfully")
        else:
            print("  ✗ Failed to load config")
            return False
        
        # Test getting settings
        print("  Testing setting retrieval...")
        dx12 = config_manager.get_setting('GstRender.Dx12Enabled')
        if dx12 == '1':
            print("  ✓ DirectX 12 setting retrieved correctly")
        else:
            print(f"  ✗ DirectX 12 setting incorrect: {dx12}")
            return False
        
        # Test setting a value
        print("  Testing setting modification...")
        config_manager.set_setting('GstRender.Dx12Enabled', '0')
        dx12_after = config_manager.get_setting('GstRender.Dx12Enabled')
        if dx12_after == '0':
            print("  ✓ Setting modification successful")
        else:
            print(f"  ✗ Setting modification failed: {dx12_after}")
            return False
        
        # Test validation
        print("  Testing setting validation...")
        valid, error = config_manager.validate_setting('GstRender.ResolutionScale', '1.5')
        if valid:
            print("  ✓ Valid setting accepted")
        else:
            print(f"  ✗ Valid setting rejected: {error}")
            return False
        
        invalid, error = config_manager.validate_setting('GstRender.ResolutionScale', '5.0')
        if not invalid:
            print("  ✓ Invalid setting rejected")
        else:
            print(f"  ✗ Invalid setting accepted: {error}")
            return False
        
        # Test saving config
        print("  Testing config saving...")
        if config_manager.save_config():
            print("  ✓ Config saved successfully")
        else:
            print("  ✗ Failed to save config")
            return False
        
        # Test backup creation
        print("  Testing backup creation...")
        if config_manager._create_backup():
            print("  ✓ Backup created successfully")
        else:
            print("  ✗ Failed to create backup")
            return False
        
        print("  ✓ All ConfigManager tests passed!")
        return True


def test_gui_imports():
    """Test that GUI components can be imported."""
    print("Testing GUI imports...")
    
    try:
        from gui.main_window import MainWindow
        print("  ✓ MainWindow imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import MainWindow: {e}")
        return False
    
    try:
        from gui.graphics_tab import GraphicsTab
        print("  ✓ GraphicsTab imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import GraphicsTab: {e}")
        return False
    
    try:
        from gui.audio_tab import AudioTab
        print("  ✓ AudioTab imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import AudioTab: {e}")
        return False
    
    try:
        from gui.input_tab import InputTab
        print("  ✓ InputTab imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import InputTab: {e}")
        return False
    
    try:
        from gui.game_tab import GameTab
        print("  ✓ GameTab imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import GameTab: {e}")
        return False
    
    try:
        from gui.network_tab import NetworkTab
        print("  ✓ NetworkTab imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import NetworkTab: {e}")
        return False
    
    try:
        from gui.advanced_tab import AdvancedTab
        print("  ✓ AdvancedTab imported successfully")
    except ImportError as e:
        print(f"  ✗ Failed to import AdvancedTab: {e}")
        return False
    
    print("  ✓ All GUI imports successful!")
    return True


def test_dependencies():
    """Test that required dependencies are available."""
    print("Testing dependencies...")
    
    try:
        import PyQt6
        print("  ✓ PyQt6 available")
    except ImportError:
        print("  ✗ PyQt6 not available")
        return False
    
    try:
        from PyQt6.QtWidgets import QApplication
        print("  ✓ PyQt6.QtWidgets available")
    except ImportError:
        print("  ✗ PyQt6.QtWidgets not available")
        return False
    
    try:
        from PyQt6.QtCore import Qt
        print("  ✓ PyQt6.QtCore available")
    except ImportError:
        print("  ✗ PyQt6.QtCore not available")
        return False
    
    try:
        from PyQt6.QtGui import QIcon
        print("  ✓ PyQt6.QtGui available")
    except ImportError:
        print("  ✗ PyQt6.QtGui not available")
        return False
    
    print("  ✓ All dependencies available!")
    return True


def main():
    """Run all tests."""
    print("FieldTuner Test Suite")
    print("===================")
    print()
    
    all_passed = True
    
    # Test dependencies
    if not test_dependencies():
        all_passed = False
        print()
    
    # Test GUI imports
    if not test_gui_imports():
        all_passed = False
        print()
    
    # Test config manager
    if not test_config_manager():
        all_passed = False
        print()
    
    print("Test Results")
    print("============")
    if all_passed:
        print("✓ All tests passed! FieldTuner is ready to use.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
