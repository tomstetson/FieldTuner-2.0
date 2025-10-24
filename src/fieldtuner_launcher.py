#!/usr/bin/env python3
"""
FieldTuner - Simple Launcher
Works with or without PyQt6 dependencies
"""

import sys
import os
import re
from pathlib import Path

def find_config_file():
    """Find Battlefield 6 config file."""
    config_paths = [
        Path.home() / "Documents" / "Battlefield 6" / "settings" / "steam" / "PROFSAVE_profile",
        Path.home() / "Documents" / "Battlefield 6" / "settings" / "PROFSAVE_profile"
    ]
    
    for path in config_paths:
        if path.exists():
            return path
    return None

def parse_config(data):
    """Parse config data into key-value pairs."""
    config = {}
    patterns = [
        r'(GstRender\.\w+)\s+(\S+)',
        r'(GstAudio\.\w+)\s+(\S+)',
        r'(GstInput\.\w+)\s+(\S+)',
        r'(GstGame\.\w+)\s+(\S+)',
        r'(GstNetwork\.\w+)\s+(\S+)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, data)
        for key, value in matches:
            config[key] = value
    
    return config

def main():
    """Main launcher function."""
    print("FieldTuner - Battlefield 6 Configuration Tool")
    print("=============================================")
    print()
    
    # Find config file
    config_path = find_config_file()
    if not config_path:
        print("ERROR: Battlefield 6 config file not found!")
        print()
        print("Expected locations:")
        print("  Steam: %USERPROFILE%\\Documents\\Battlefield 6\\settings\\steam\\PROFSAVE_profile")
        print("  EA App: %USERPROFILE%\\Documents\\Battlefield 6\\settings\\PROFSAVE_profile")
        print()
        print("Make sure Battlefield 6 is installed and has been run at least once.")
        return 1
    
    print(f"SUCCESS: Found config: {config_path}")
    
    # Show file info
    file_size = config_path.stat().st_size
    print(f"File size: {file_size:,} bytes")
    print()
    
    # Try to read and show settings
    try:
        with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Parse settings
        config = parse_config(content)
        
        print(f"Loaded {len(config)} settings")
        print()
        
        # Show graphics settings
        graphics_settings = {k: v for k, v in config.items() if k.startswith('GstRender.')}
        if graphics_settings:
            print("Graphics Settings:")
            for key, value in graphics_settings.items():
                print(f"  {key} = {value}")
            print()
        
        # Show audio settings
        audio_settings = {k: v for k, v in config.items() if k.startswith('GstAudio.')}
        if audio_settings:
            print("Audio Settings:")
            for key, value in audio_settings.items():
                print(f"  {key} = {value}")
            print()
        
        print("You can manually edit this file to change settings.")
        print("Common settings to modify:")
        print("  - GstRender.Dx12Enabled 1/0 (DirectX 12)")
        print("  - GstRender.ResolutionScale 0.5-2.0 (Resolution scaling)")
        print("  - GstRender.FullscreenMode 0/1 (Windowed/Fullscreen)")
        print("  - GstAudio.MasterVolume 0-100 (Master volume)")
        print("  - GstInput.MouseSensitivity 1-100 (Mouse sensitivity)")
        
    except Exception as e:
        print(f"ERROR: Error reading config file: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
