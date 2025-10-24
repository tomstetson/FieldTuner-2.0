#!/usr/bin/env python3
"""
FieldTuner Simple Installer
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def install_fieldtuner():
    """Install FieldTuner to Program Files."""
    print("FieldTuner Installer")
    print("=" * 20)
    
    # Check for admin privileges
    try:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("Error: Administrator privileges required!")
            print("Please run this installer as administrator.")
            input("Press Enter to exit...")
            return False
    except:
        print("Warning: Could not verify administrator privileges")
    
    # Installation directory
    install_dir = Path("C:/Program Files/FieldTuner")
    
    print(f"Installing to: {install_dir}")
    
    # Create installation directory
    install_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy files
    source_dir = Path(".")
    files_to_install = [
        "FieldTuner.exe",
        "Run_FieldTuner.bat",
        "README.txt",
        "LICENSE.txt"
    ]
    
    for file_name in files_to_install:
        src = source_dir / file_name
        dst = install_dir / file_name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"Installed {file_name}")
        else:
            print(f"Warning: {file_name} not found")
    
    # Create desktop shortcut
    desktop = Path.home() / "Desktop"
    shortcut_path = desktop / "FieldTuner.lnk"
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Targetpath = str(install_dir / "FieldTuner.exe")
        shortcut.WorkingDirectory = str(install_dir)
        shortcut.IconLocation = str(install_dir / "FieldTuner.exe")
        shortcut.save()
        print("Created desktop shortcut")
    except ImportError:
        print("Warning: Could not create desktop shortcut (winshell not available)")
    except Exception as e:
        print(f"Warning: Could not create desktop shortcut: {e}")
    
    # Create Start Menu shortcut
    start_menu = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
    start_menu.mkdir(parents=True, exist_ok=True)
    
    try:
        shortcut_path = start_menu / "FieldTuner.lnk"
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Targetpath = str(install_dir / "FieldTuner.exe")
        shortcut.WorkingDirectory = str(install_dir)
        shortcut.IconLocation = str(install_dir / "FieldTuner.exe")
        shortcut.save()
        print("Created Start Menu shortcut")
    except Exception as e:
        print(f"Warning: Could not create Start Menu shortcut: {e}")
    
    print("\nInstallation completed successfully!")
    print(f"FieldTuner installed to: {install_dir}")
    print("You can now run FieldTuner from the Start Menu or Desktop shortcut.")
    
    input("Press Enter to exit...")
    return True

if __name__ == "__main__":
    install_fieldtuner()
