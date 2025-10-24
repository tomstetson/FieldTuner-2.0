#!/usr/bin/env python3
"""
Simple FieldTuner Portable Executable Builder
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    print("FieldTuner Portable Executable Builder")
    print("=" * 50)
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
        print("PyInstaller found")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        try:
            import PyInstaller
            print("PyInstaller installed successfully")
        except ImportError:
            print("Failed to install PyInstaller")
            return False
    
    # Clean previous builds
    print("Cleaning previous builds...")
    for dir_name in ["build", "dist", "__pycache__"]:
        if Path(dir_name).exists():
            try:
                shutil.rmtree(dir_name)
                print(f"   Cleaned {dir_name}")
            except PermissionError:
                print(f"   Warning: Could not clean {dir_name} (permission denied)")
            except Exception as e:
                print(f"   Warning: Could not clean {dir_name}: {e}")
    
    # Create releases directory
    releases_dir = Path("releases")
    releases_dir.mkdir(exist_ok=True)
    
    # Build the executable
    print("Building executable...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed", 
        "--name=FieldTuner",
        "--distpath=dist",
        "--workpath=build",
        "--clean",
        "--noconfirm",
        "--add-data=src;src",
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=PyQt6.QtWidgets",
        "src/main.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("Executable built successfully!")
        else:
            print(f"Build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"Build error: {e}")
        return False
    
    # Create portable package
    print("Creating portable package...")
    
    package_dir = releases_dir / "FieldTuner_Portable_v1.0"
    package_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_src = Path("dist/FieldTuner.exe")
    exe_dst = package_dir / "FieldTuner.exe"
    
    if exe_src.exists():
        shutil.copy2(exe_src, exe_dst)
        print(f"   Copied executable to {exe_dst}")
    else:
        print("Executable not found!")
        return False
    
    # Create README
    readme_content = f"""# FieldTuner Portable v1.0

## 🚀 Quick Start

1. **Run as Administrator**: Right-click `FieldTuner.exe` and select "Run as administrator"
2. **Auto-Detection**: FieldTuner will automatically find your Battlefield 6 config file
3. **Backup Created**: Your current settings will be backed up automatically
4. **Start Configuring**: Use the tabs to adjust your settings

## 📁 File Locations

- **Config File**: Automatically detected in your Documents folder
- **Backups**: Stored in `%APPDATA%\\FieldTuner\\backups\\`
- **Logs**: Stored in `%APPDATA%\\FieldTuner\\logs\\`

## 🎮 Features

- **Quick Settings**: Preset configurations for different playstyles
- **Graphics**: Comprehensive graphics settings management  
- **Backup System**: Automatic backups with easy restore
- **Advanced**: Technical settings with user-friendly descriptions
- **Debug**: Real-time logging and troubleshooting

## ⚠️ Important Notes

- **Admin Required**: FieldTuner needs administrator privileges to modify game files
- **Backup First**: Always backup your settings before making changes
- **Game Closed**: Close Battlefield 6 before using FieldTuner
- **Steam/Origin**: Works with both Steam and Origin versions

## 🆘 Troubleshooting

If FieldTuner can't find your config file:
1. Make sure Battlefield 6 is installed
2. Run the game at least once to create config files
3. Check that the config file exists in your Documents folder

## 📞 Support

Created by Tom with Love from Cursor
For support, check the GitHub repository.

---
**Version**: 1.0.0
**Build Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Compatible**: Windows 10/11
"""
    
    with open(package_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Create batch file for easy launching
    batch_content = """@echo off
echo Starting FieldTuner...
echo.
echo FieldTuner - Battlefield 6 Configuration Tool
echo Created by Tom with Love from Cursor
echo.
echo Checking for administrator privileges...

net session >nul 2>&1
if %errorLevel% == 0 (
    echo Administrator privileges confirmed.
    echo.
    start "" "FieldTuner.exe"
) else (
    echo Administrator privileges required.
    echo Please run this batch file as administrator.
    echo.
    pause
    exit /b 1
)
"""
    
    with open(package_dir / "Run_FieldTuner.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    print(f"   Portable package created in {package_dir}")
    
    # Show file sizes
    exe_size = exe_dst.stat().st_size / (1024 * 1024)
    print(f"   Executable size: {exe_size:.1f} MB")
    
    print("\nBuild completed successfully!")
    print(f"Portable package: {package_dir}")
    print("Ready to ship!")
    
    return True

if __name__ == "__main__":
    main()
