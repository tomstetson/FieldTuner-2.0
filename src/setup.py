#!/usr/bin/env python3
"""
Setup script for FieldTuner
Installs dependencies and sets up the application.
"""

import sys
import subprocess
import os
from pathlib import Path


def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False


def create_directories():
    """Create necessary directories."""
    print("Creating application directories...")
    
    # Create directories in user's AppData
    appdata = Path.home() / "AppData" / "Roaming" / "FieldTuner"
    backups = appdata / "backups"
    logs = appdata / "logs"
    
    try:
        backups.mkdir(parents=True, exist_ok=True)
        logs.mkdir(parents=True, exist_ok=True)
        print("✓ Application directories created!")
        return True
    except Exception as e:
        print(f"✗ Failed to create directories: {e}")
        return False


def test_installation():
    """Test the installation."""
    print("Testing installation...")
    try:
        # Test imports
        import PyQt6
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QIcon
        
        print("✓ PyQt6 imports successful")
        
        # Test our modules
        from core.config_manager import ConfigManager
        print("✓ ConfigManager import successful")
        
        from gui.main_window import MainWindow
        print("✓ MainWindow import successful")
        
        print("✓ Installation test passed!")
        return True
        
    except ImportError as e:
        print(f"✗ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Installation test failed: {e}")
        return False


def main():
    """Main setup function."""
    print("FieldTuner Setup")
    print("===============")
    print()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return 1
    
    print(f"Python version: {sys.version}")
    print()
    
    # Install requirements
    if not install_requirements():
        return 1
    
    print()
    
    # Create directories
    if not create_directories():
        return 1
    
    print()
    
    # Test installation
    if not test_installation():
        return 1
    
    print()
    print("Setup completed successfully!")
    print("You can now run FieldTuner using:")
    print("  python main.py")
    print("  or")
    print("  python run.py")
    print("  or")
    print("  run.bat (on Windows)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
