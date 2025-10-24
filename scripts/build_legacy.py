#!/usr/bin/env python3
"""
Build script for FieldTuner
Creates a single executable using PyInstaller.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def build_executable():
    """Build the FieldTuner executable."""
    print("Building FieldTuner executable...")
    
    # Clean previous builds
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=FieldTuner",
        "--icon=assets/icon.ico",
        "--add-data=assets;assets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtGui",
        "main.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(f"Executable created: dist/FieldTuner.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def create_installer():
    """Create a simple installer script."""
    installer_content = '''@echo off
echo Installing FieldTuner...
if not exist "%APPDATA%\\FieldTuner" mkdir "%APPDATA%\\FieldTuner"
if not exist "%APPDATA%\\FieldTuner\\backups" mkdir "%APPDATA%\\FieldTuner\\backups"
if not exist "%APPDATA%\\FieldTuner\\logs" mkdir "%APPDATA%\\FieldTuner\\logs"
copy "FieldTuner.exe" "%APPDATA%\\FieldTuner\\"
echo Installation complete!
pause
'''
    
    with open("install.bat", "w") as f:
        f.write(installer_content)
    
    print("Created install.bat")


def main():
    """Main build function."""
    print("FieldTuner Build Script")
    print("=====================")
    
    # Check if PyInstaller is installed
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build executable
    if build_executable():
        create_installer()
        print("\nBuild completed successfully!")
        print("Files created:")
        print("- dist/FieldTuner.exe (main executable)")
        print("- install.bat (installer script)")
    else:
        print("Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
