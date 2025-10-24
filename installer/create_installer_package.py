#!/usr/bin/env python3
"""
FieldTuner Installer Package Creator
Creates a complete installer package with all necessary files
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_installer_package():
    """Create a complete installer package."""
    print("FieldTuner Installer Package Creator")
    print("=" * 40)
    
    # Create installer package directory
    package_dir = Path("releases/FieldTuner_Installer_v1.0")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy portable release files
    portable_dir = Path("releases/FieldTuner_Portable_v1.0")
    if not portable_dir.exists():
        print("Error: Portable release not found. Please run build_simple.py first.")
        return False
    
    print("Copying portable release files...")
    for item in portable_dir.iterdir():
        if item.is_file():
            shutil.copy2(item, package_dir / item.name)
            print(f"   Copied {item.name}")
    
    # Copy installer files
    installer_files = [
        "install.bat",
        "install_fieldtuner.py",
        "FieldTuner.nsi"
    ]
    
    for file_name in installer_files:
        src = Path(f"installer/{file_name}")
        if src.exists():
            shutil.copy2(src, package_dir / file_name)
            print(f"   Copied {file_name}")
    
    # Create installer README
    installer_readme = """# FieldTuner Installer Package

## Installation Options

### Option 1: Simple Installation (Recommended)
1. Run `install.bat` as administrator
2. Follow the on-screen instructions
3. FieldTuner will be installed to Program Files

### Option 2: Python Installer
1. Run `python install_fieldtuner.py` as administrator
2. Follow the on-screen instructions

### Option 3: Portable Version
1. Simply run `FieldTuner.exe` directly
2. No installation required

## Features
- Professional Windows installer
- Desktop and Start Menu shortcuts
- Automatic uninstaller creation
- Administrator privilege handling
- Registry entries for proper uninstallation

## System Requirements
- Windows 10/11 (64-bit)
- Administrator privileges for installation
- Battlefield 6 installed

## Uninstallation
- Use the uninstaller in the installation directory
- Or use Windows "Add or Remove Programs"

## Support
- GitHub: https://github.com/tomstetson/FieldTuner
- Issues: https://github.com/tomstetson/FieldTuner/issues
"""
    
    with open(package_dir / "INSTALLER_README.txt", "w", encoding="utf-8") as f:
        f.write(installer_readme)
    
    print("   Created INSTALLER_README.txt")
    
    # Create installation guide
    installation_guide = """# FieldTuner Installation Guide

## Quick Start

### For End Users (Recommended)
1. **Download** the latest FieldTuner installer package
2. **Extract** the ZIP file to any folder
3. **Run** `install.bat` as administrator
4. **Launch** FieldTuner from Start Menu or Desktop

### For Developers
1. **Clone** the repository: `git clone https://github.com/tomstetson/FieldTuner.git`
2. **Install** dependencies: `pip install -r requirements.txt`
3. **Run** the application: `python src/main.py`

## Installation Methods

### Method 1: Windows Installer (Recommended)
- **File**: `install.bat`
- **Requirements**: Administrator privileges
- **Features**: 
  - Installs to Program Files
  - Creates desktop shortcut
  - Creates Start Menu entry
  - Creates uninstaller
  - Registry entries

### Method 2: Python Installer
- **File**: `install_fieldtuner.py`
- **Requirements**: Python 3.8+, Administrator privileges
- **Features**: Same as Windows installer

### Method 3: Portable Version
- **File**: `FieldTuner.exe`
- **Requirements**: None (runs anywhere)
- **Features**: No installation required

## System Requirements

### Minimum Requirements
- **OS**: Windows 10 (64-bit) or Windows 11
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 100 MB free space
- **Game**: Battlefield 6 (Steam or Origin)

### Recommended Requirements
- **OS**: Windows 11 (64-bit)
- **RAM**: 16 GB or more
- **Storage**: 1 GB free space
- **CPU**: Modern multi-core processor
- **Graphics**: DirectX 12 compatible graphics card

## Troubleshooting

### Installation Issues
- **"Access Denied"**: Run installer as administrator
- **"File Not Found"**: Ensure all files are in the same directory
- **"Permission Denied"**: Check antivirus settings

### Runtime Issues
- **"Config file not found"**: Ensure Battlefield 6 is installed and has been launched
- **"Permission denied"**: Run FieldTuner as administrator
- **"Application won't start"**: Check system requirements

### Uninstallation
- **Windows Installer**: Use the uninstaller in Program Files
- **Portable Version**: Simply delete the folder
- **Python Version**: Delete the installation directory

## Support
- **GitHub**: https://github.com/tomstetson/FieldTuner
- **Issues**: https://github.com/tomstetson/FieldTuner/issues
- **Documentation**: https://github.com/tomstetson/FieldTuner/wiki
"""
    
    with open(package_dir / "INSTALLATION_GUIDE.txt", "w", encoding="utf-8") as f:
        f.write(installation_guide)
    
    print("   Created INSTALLATION_GUIDE.txt")
    
    # Create ZIP package
    timestamp = datetime.now().strftime("%Y%m%d")
    zip_name = f"FieldTuner_Installer_v1.0_{timestamp}.zip"
    zip_path = Path("releases") / zip_name
    
    print(f"Creating ZIP package: {zip_name}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
    
    print(f"   Created {zip_name}")
    
    # Show package contents
    print("\nInstaller package contents:")
    for item in sorted(package_dir.iterdir()):
        if item.is_file():
            size_kb = item.stat().st_size / 1024
            print(f"   {item.name} ({size_kb:.1f} KB)")
    
    # Show ZIP size
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"\nZIP package size: {zip_size_mb:.1f} MB")
    
    print(f"\nInstaller package created successfully!")
    print(f"Package directory: {package_dir}")
    print(f"ZIP package: {zip_path}")
    print("Ready for distribution!")
    
    return True

def main():
    """Main function."""
    try:
        return create_installer_package()
    except Exception as e:
        print(f"Error creating installer package: {e}")
        return False

if __name__ == "__main__":
    main()
