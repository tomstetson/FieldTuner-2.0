#!/usr/bin/env python3
"""
Simplified build script for FieldTuner
Handles dependency issues and provides fallback options.
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print(f"Error: Python 3.8+ required. Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version}")
    return True


def install_pyqt6():
    """Install PyQt6 with fallback options."""
    print("Installing PyQt6...")
    
    # Try different PyQt6 versions
    pyqt_versions = [
        "PyQt6>=6.4.0",
        "PyQt6>=6.0.0",
        "PyQt6",
        "PyQt6-Qt6>=6.4.0"
    ]
    
    for version in pyqt_versions:
        try:
            print(f"  Trying {version}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", version], 
                                capture_output=True)
            print(f"  ✓ Successfully installed {version}")
            return True
        except subprocess.CalledProcessError:
            print(f"  ✗ Failed to install {version}")
            continue
    
    print("  ✗ Could not install any PyQt6 version")
    return False


def install_pyinstaller():
    """Install PyInstaller with fallback options."""
    print("Installing PyInstaller...")
    
    # Try different PyInstaller versions
    pyinstaller_versions = [
        "pyinstaller>=6.0.0",
        "pyinstaller>=5.0.0",
        "pyinstaller",
        "pyinstaller==5.13.2"
    ]
    
    for version in pyinstaller_versions:
        try:
            print(f"  Trying {version}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", version], 
                                capture_output=True)
            print(f"  ✓ Successfully installed {version}")
            return True
        except subprocess.CalledProcessError:
            print(f"  ✗ Failed to install {version}")
            continue
    
    print("  ✗ Could not install any PyInstaller version")
    return False


def test_imports():
    """Test if we can import required modules."""
    print("Testing imports...")
    
    try:
        import PyQt6
        print("  ✓ PyQt6 imported")
    except ImportError:
        print("  ✗ PyQt6 import failed")
        return False
    
    try:
        import pyinstaller
        print("  ✓ PyInstaller imported")
    except ImportError:
        print("  ✗ PyInstaller import failed")
        return False
    
    return True


def build_executable():
    """Build the executable."""
    print("Building executable...")
    
    # Clean previous builds
    for dir_name in ["dist", "build"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Cleaned {dir_name}/")
    
    # Basic PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=FieldTuner",
        "main.py"
    ]
    
    # Add windowed mode if available
    try:
        subprocess.run(["pyinstaller", "--help"], capture_output=True, text=True)
        if "--windowed" in subprocess.run(["pyinstaller", "--help"], 
                                        capture_output=True, text=True).stdout:
            cmd.insert(-1, "--windowed")
            print("  Using --windowed mode")
    except:
        print("  Skipping --windowed mode")
    
    try:
        print(f"  Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("  ✓ Build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Build failed: {e}")
        if e.stderr:
            print(f"  Error: {e.stderr}")
        return False


def create_standalone_script():
    """Create a standalone Python script that doesn't require PyQt6."""
    print("Creating standalone script...")
    
    standalone_content = '''#!/usr/bin/env python3
"""
Standalone FieldTuner - No GUI dependencies
Basic config file editor for Battlefield 6
"""

import sys
import os
import re
import shutil
from pathlib import Path
from datetime import datetime


def find_config_file():
    """Find the Battlefield 6 config file."""
    config_paths = [
        Path.home() / "Documents" / "Battlefield 6" / "settings" / "steam" / "PROFSAVE_profile",
        Path.home() / "Documents" / "Battlefield 6" / "settings" / "PROFSAVE_profile"
    ]
    
    for path in config_paths:
        if path.exists():
            return path
    
    return None


def load_config(file_path):
    """Load configuration from file."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def parse_config(data):
    """Parse config data into key-value pairs."""
    config = {}
    patterns = [
        r'(GstRender\.\\w+)\\s+(\\S+)',
        r'(GstAudio\.\\w+)\\s+(\\S+)',
        r'(GstInput\.\\w+)\\s+(\\S+)',
        r'(GstGame\.\\w+)\\s+(\\S+)',
        r'(GstNetwork\.\\w+)\\s+(\\S+)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, data)
        for key, value in matches:
            config[key] = value
    
    return config


def save_config(file_path, data):
    """Save configuration to file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)


def create_backup(file_path):
    """Create a backup of the config file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.parent / f"PROFSAVE_profile_backup_{timestamp}.bak"
    shutil.copy2(file_path, backup_path)
    return backup_path


def main():
    """Main function."""
    print("FieldTuner - Standalone Mode")
    print("============================")
    print()
    
    # Find config file
    config_path = find_config_file()
    if not config_path:
        print("Error: Battlefield 6 config file not found!")
        print("Make sure Battlefield 6 is installed and has been run at least once.")
        return 1
    
    print(f"Found config: {config_path}")
    
    # Load config
    config_data = load_config(config_path)
    config = parse_config(config_data)
    
    print(f"Loaded {len(config)} settings")
    print()
    
    # Show current settings
    print("Current Graphics Settings:")
    graphics_settings = {k: v for k, v in config.items() if k.startswith('GstRender.')}
    for key, value in graphics_settings.items():
        print(f"  {key} = {value}")
    
    print()
    
    # Interactive mode
    while True:
        print("Options:")
        print("1. Change DirectX 12 setting")
        print("2. Change Resolution Scale")
        print("3. Change Fullscreen Mode")
        print("4. Show all settings")
        print("5. Save and exit")
        print("6. Exit without saving")
        
        choice = input("\\nEnter choice (1-6): ").strip()
        
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
            print("\\nAll Settings:")
            for key, value in sorted(config.items()):
                print(f"  {key} = {value}")
        
        elif choice == "5":
            # Create backup
            backup_path = create_backup(config_path)
            print(f"Created backup: {backup_path}")
            
            # Update config data
            new_data = config_data
            for key, value in config.items():
                pattern = rf'({re.escape(key)})\\s+\\S+'
                replacement = f'{key} {value}'
                new_data = re.sub(pattern, replacement, new_data)
            
            # Save config
            save_config(config_path, new_data)
            print("Configuration saved!")
            break
        
        elif choice == "6":
            print("Exiting without saving...")
            break
        
        else:
            print("Invalid choice!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
    
    with open("fieldtuner_standalone.py", "w") as f:
        f.write(standalone_content)
    
    print("  ✓ Created fieldtuner_standalone.py")
    return True


def main():
    """Main build function."""
    print("FieldTuner Simplified Build")
    print("===========================")
    print()
    
    # Check Python version
    if not check_python_version():
        return 1
    
    print()
    
    # Try to install dependencies
    pyqt6_ok = install_pyqt6()
    print()
    
    pyinstaller_ok = install_pyinstaller()
    print()
    
    # Test imports
    if pyqt6_ok and pyinstaller_ok:
        if test_imports():
            print("✓ All dependencies available")
            print()
            
            # Try to build executable
            if build_executable():
                print("\\n✓ Build successful!")
                print("Executable created: dist/FieldTuner.exe")
                return 0
            else:
                print("\\n✗ Build failed, creating standalone script...")
                create_standalone_script()
                print("\\n✓ Created fieldtuner_standalone.py")
                print("You can run this script directly: python fieldtuner_standalone.py")
                return 0
        else:
            print("✗ Import test failed")
            create_standalone_script()
            return 0
    else:
        print("✗ Could not install dependencies")
        print("Creating standalone script as fallback...")
        create_standalone_script()
        print("\\n✓ Created fieldtuner_standalone.py")
        print("You can run this script directly: python fieldtuner_standalone.py")
        return 0


if __name__ == "__main__":
    sys.exit(main())
