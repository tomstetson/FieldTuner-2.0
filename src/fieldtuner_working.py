#!/usr/bin/env python3
"""
FieldTuner - Working Launcher
Handles actual Battlefield 6 config files
"""

import sys
import os
import re
import shutil
from pathlib import Path
from datetime import datetime

def find_config_file():
    """Find Battlefield 6 config file."""
    config_paths = [
        Path.home() / "Documents" / "Battlefield 6" / "settings" / "steam" / "PROFSAVE_profile",
        Path.home() / "Documents" / "Battlefield 6" / "settings" / "PROFSAVE_profile",
        Path.home() / "OneDrive" / "Documents" / "Battlefield 6" / "settings" / "steam" / "PROFSAVE_profile",
        Path.home() / "OneDrive" / "Documents" / "Battlefield 6" / "settings" / "PROFSAVE_profile"
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

def create_backup(file_path):
    """Create a backup of the config file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.parent / f"PROFSAVE_profile_backup_{timestamp}.bak"
    shutil.copy2(file_path, backup_path)
    return backup_path

def save_config(file_path, data):
    """Save configuration to file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)

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
        print("  OneDrive Steam: %USERPROFILE%\\OneDrive\\Documents\\Battlefield 6\\settings\\steam\\PROFSAVE_profile")
        print("  OneDrive EA App: %USERPROFILE%\\OneDrive\\Documents\\Battlefield 6\\settings\\PROFSAVE_profile")
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
            for key, value in list(graphics_settings.items())[:10]:  # Show first 10
                print(f"  {key} = {value}")
            if len(graphics_settings) > 10:
                print(f"  ... and {len(graphics_settings) - 10} more graphics settings")
            print()
        
        # Show audio settings
        audio_settings = {k: v for k, v in config.items() if k.startswith('GstAudio.')}
        if audio_settings:
            print("Audio Settings:")
            for key, value in list(audio_settings.items())[:5]:  # Show first 5
                print(f"  {key} = {value}")
            if len(audio_settings) > 5:
                print(f"  ... and {len(audio_settings) - 5} more audio settings")
            print()
        
        # Interactive mode
        while True:
            print("Options:")
            print("1. Change DirectX 12 setting")
            print("2. Change Resolution Scale")
            print("3. Change Fullscreen Mode")
            print("4. Change Mouse Sensitivity")
            print("5. Show all graphics settings")
            print("6. Show all audio settings")
            print("7. Create backup")
            print("8. Exit")
            
            choice = input("\\nEnter choice (1-8): ").strip()
            
            if choice == "1":
                current = config.get('GstRender.Dx12Enabled', '0')
                new_value = "1" if current == "0" else "0"
                config['GstRender.Dx12Enabled'] = new_value
                print(f"DirectX 12: {current} -> {new_value}")
            
            elif choice == "2":
                try:
                    current = float(config.get('GstRender.ResolutionScale', '1.0'))
                    new_scale = float(input(f"Enter resolution scale (0.5-2.0, current: {current}): "))
                    if 0.5 <= new_scale <= 2.0:
                        config['GstRender.ResolutionScale'] = str(new_scale)
                        print(f"Resolution Scale: {current} -> {new_scale}")
                    else:
                        print("Invalid scale value!")
                except ValueError:
                    print("Invalid input!")
            
            elif choice == "3":
                current = config.get('GstRender.FullscreenMode', '0')
                new_value = "1" if current == "0" else "0"
                config['GstRender.FullscreenMode'] = new_value
                mode = "Fullscreen" if new_value == "1" else "Windowed"
                print(f"Fullscreen Mode: {current} -> {new_value} ({mode})")
            
            elif choice == "4":
                try:
                    current = float(config.get('GstInput.MouseSensitivity', '0.025500'))
                    new_sens = float(input(f"Enter mouse sensitivity (0.01-1.0, current: {current}): "))
                    if 0.01 <= new_sens <= 1.0:
                        config['GstInput.MouseSensitivity'] = str(new_sens)
                        print(f"Mouse Sensitivity: {current} -> {new_sens}")
                    else:
                        print("Invalid sensitivity value!")
                except ValueError:
                    print("Invalid input!")
            
            elif choice == "5":
                print("\\nAll Graphics Settings:")
                for key, value in graphics_settings.items():
                    print(f"  {key} = {value}")
            
            elif choice == "6":
                print("\\nAll Audio Settings:")
                for key, value in audio_settings.items():
                    print(f"  {key} = {value}")
            
            elif choice == "7":
                backup_path = create_backup(config_path)
                print(f"Created backup: {backup_path}")
            
            elif choice == "8":
                # Ask if user wants to save changes
                if config != parse_config(content):
                    save_choice = input("Save changes? (y/n): ").strip().lower()
                    if save_choice == 'y':
                        # Update config data
                        new_data = content
                        for key, value in config.items():
                            pattern = rf'({re.escape(key)})\\s+\\S+'
                            replacement = f'{key} {value}'
                            new_data = re.sub(pattern, replacement, new_data)
                        
                        # Save config
                        save_config(config_path, new_data)
                        print("Configuration saved!")
                    else:
                        print("Changes discarded.")
                break
            
            else:
                print("Invalid choice!")
        
    except Exception as e:
        print(f"ERROR: Error reading config file: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
