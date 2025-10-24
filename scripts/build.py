#!/usr/bin/env python3
"""
Build script for FieldTuner GUI
Creates a single executable using PyInstaller.
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path

def build_gui_executable():
    """Build the FieldTuner GUI executable."""
    print("Building FieldTuner GUI executable...")
    
    # Clean previous builds
    for dir_name in ["dist", "build"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}/")
    
    # PyInstaller command for GUI
    cmd = [
        "python", "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=FieldTuner_GUI",
        "--icon=assets/icon.ico" if Path("assets/icon.ico").exists() else "",
        "gui_main.py"
    ]
    
    # Remove empty icon parameter if icon doesn't exist
    if not Path("assets/icon.ico").exists():
        cmd = [item for item in cmd if item != "--icon=assets/icon.ico"]
    
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(f"Executable created: dist/FieldTuner_GUI.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def main():
    """Main build function."""
    print("FieldTuner GUI Build Script")
    print("==========================")
    print()
    
    if build_gui_executable():
        print("\nSUCCESS: Build completed!")
        print("Files created:")
        print("- dist/FieldTuner_GUI.exe (main GUI executable)")
        print("- FieldTuner_GUI.bat (launcher script)")
        print()
        print("You can now run FieldTuner_GUI.exe or FieldTuner_GUI.bat")
    else:
        print("Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
