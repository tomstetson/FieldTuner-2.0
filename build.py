#!/usr/bin/env python3
"""
FieldTuner Build Script
Builds a portable executable using PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    """Build the FieldTuner portable executable."""
    print("Building FieldTuner...")
    
    # Clean previous builds
    try:
        if Path("dist").exists():
            shutil.rmtree("dist")
        if Path("build").exists():
            shutil.rmtree("build")
    except PermissionError:
        print("Warning: Could not clean previous builds (files may be in use)")
        print("Continuing with build...")
    
    # Build command
    cmd = [
        "python", "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=FieldTuner",
        "--icon=assets/icon.ico",
        "--add-data=assets;assets",
        "src/main.py"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(f"Executable: dist/FieldTuner.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
