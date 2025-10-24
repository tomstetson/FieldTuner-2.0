#!/usr/bin/env python3
"""
FieldTuner Release Package Creator
Creates a complete release package ready for distribution
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_release_package():
    """Create a complete release package."""
    print("FieldTuner Release Package Creator")
    print("=" * 40)
    
    # Define paths
    source_dir = Path("releases/FieldTuner_Portable_v1.0")
    release_name = f"FieldTuner_v1.0_{datetime.now().strftime('%Y%m%d')}"
    release_dir = Path(f"releases/{release_name}")
    zip_file = Path(f"releases/{release_name}.zip")
    
    if not source_dir.exists():
        print("Error: Source directory not found!")
        print("Please run the build script first.")
        return False
    
    print(f"Creating release package: {release_name}")
    
    # Copy files to release directory
    if release_dir.exists():
        shutil.rmtree(release_dir)
    
    shutil.copytree(source_dir, release_dir)
    print(f"   Copied files to {release_dir}")
    
    # Create additional release files
    create_release_notes(release_dir)
    create_installation_guide(release_dir)
    
    # Create ZIP package
    print("Creating ZIP package...")
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in release_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(release_dir)
                zipf.write(file_path, arcname)
    
    zip_size = zip_file.stat().st_size / (1024 * 1024)
    print(f"   ZIP package created: {zip_file}")
    print(f"   Package size: {zip_size:.1f} MB")
    
    # Show contents
    print("\nRelease package contents:")
    for item in release_dir.iterdir():
        if item.is_file():
            size = item.stat().st_size
            if size > 1024 * 1024:
                size_str = f"{size / (1024 * 1024):.1f} MB"
            elif size > 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size} bytes"
            print(f"   {item.name} ({size_str})")
    
    print(f"\nRelease package ready: {release_dir}")
    print(f"ZIP package ready: {zip_file}")
    print("Ready for distribution!")
    
    return True

def create_release_notes(release_dir):
    """Create release notes."""
    notes_content = f"""FieldTuner v1.0.0 Release Notes
================================

Release Date: {datetime.now().strftime('%Y-%m-%d')}
Version: 1.0.0
Build: Stable

## 🎉 What's New

This is the initial release of FieldTuner, a comprehensive Battlefield 6 configuration tool.

### ✨ Key Features
- Complete BF6 configuration management
- Automatic config file detection
- Quick settings presets for different playstyles
- Comprehensive graphics settings
- Automatic backup system
- Advanced technical settings
- Real-time debug logging

### 🎮 Quick Start
1. Extract the ZIP file to any location
2. Run "Run_FieldTuner.bat" as administrator
3. FieldTuner will automatically detect your BF6 config
4. Start configuring your settings!

### 🛡️ Safety First
- Always backup your settings before making changes
- FieldTuner creates automatic backups
- Close Battlefield 6 before using FieldTuner
- Run as administrator for full functionality

### 📋 System Requirements
- Windows 10/11 (64-bit)
- 4GB RAM minimum
- Administrator privileges
- Battlefield 6 installed (Steam or Origin)

### 🆘 Support
- Check README.txt for detailed instructions
- Use the Debug tab for troubleshooting
- GitHub repository for updates and support

Created by Tom with Love from Cursor
"""
    
    with open(release_dir / "RELEASE_NOTES.txt", "w", encoding="utf-8") as f:
        f.write(notes_content)

def create_installation_guide(release_dir):
    """Create installation guide."""
    guide_content = """FieldTuner Installation Guide
============================

## 🚀 Quick Installation

### Method 1: Portable (Recommended)
1. Extract the ZIP file to any folder
2. Right-click "Run_FieldTuner.bat"
3. Select "Run as administrator"
4. FieldTuner will start automatically

### Method 2: Direct Execution
1. Extract the ZIP file to any folder
2. Right-click "FieldTuner.exe"
3. Select "Run as administrator"
4. FieldTuner will start

## 📁 Installation Locations

### Portable Installation
- Extract to any folder (e.g., C:\\Tools\\FieldTuner)
- No registry entries
- No system files modified
- Easy to uninstall (just delete the folder)

### Data Storage
- Backups: %APPDATA%\\FieldTuner\\backups\\
- Logs: %APPDATA%\\FieldTuner\\logs\\
- Settings: Stored with the application

## ⚠️ Important Notes

### Administrator Privileges
- FieldTuner requires administrator privileges
- This is needed to modify game configuration files
- Windows will prompt for permission

### Game Requirements
- Battlefield 6 must be installed
- Run the game at least once to create config files
- Close the game before using FieldTuner

### First Run
1. FieldTuner will automatically detect your config file
2. A backup will be created automatically
3. You can start configuring immediately

## 🛠️ Troubleshooting

### FieldTuner Won't Start
- Make sure you're running as administrator
- Check that Python is installed (if running from source)
- Try running "Run_FieldTuner.bat" instead of the .exe

### Can't Find Config File
- Make sure Battlefield 6 is installed
- Run the game at least once
- Check that config files exist in Documents folder

### Permission Errors
- Run as administrator
- Check that the config file isn't read-only
- Make sure no other programs are using the config file

## 📞 Support

- Check README.txt for detailed information
- Use the Debug tab for troubleshooting
- GitHub repository for updates and support

Created by Tom with Love from Cursor
"""
    
    with open(release_dir / "INSTALLATION_GUIDE.txt", "w", encoding="utf-8") as f:
        f.write(guide_content)

if __name__ == "__main__":
    create_release_package()
