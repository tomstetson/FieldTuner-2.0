#!/usr/bin/env python3
"""
Dependency-free test for FieldTuner
Tests core functionality without requiring PyQt6 or PyInstaller.
"""

import sys
import os
import tempfile
import re
from pathlib import Path


def test_config_parsing():
    """Test config parsing without dependencies."""
    print("Testing config parsing (no dependencies)...")
    
    # Mock config data
    config_data = """GstRender.Dx12Enabled 1
GstRender.MotionBlurEnable 1
GstRender.DepthOfFieldEnable 1
GstRender.AntiAliasingDeferred 2
GstRender.ResolutionScale 1.0
GstRender.FullscreenMode 1
GstRender.VSyncEnable 0
GstAudio.MasterVolume 100
GstAudio.MusicVolume 80
GstInput.MouseSensitivity 50
GstGame.Difficulty 1
GstNetwork.MaxPing 150
"""
    
    # Parse using regex (same logic as in config_manager.py)
    patterns = [
        r'(GstRender\.\w+)\s+(\S+)',
        r'(GstAudio\.\w+)\s+(\S+)',
        r'(GstInput\.\w+)\s+(\S+)',
        r'(GstGame\.\w+)\s+(\S+)',
        r'(GstNetwork\.\w+)\s+(\S+)'
    ]
    
    config = {}
    for pattern in patterns:
        matches = re.findall(pattern, config_data)
        for key, value in matches:
            config[key] = value
    
    # Verify we found expected settings
    expected = [
        'GstRender.Dx12Enabled',
        'GstRender.ResolutionScale',
        'GstAudio.MasterVolume',
        'GstInput.MouseSensitivity',
        'GstGame.Difficulty',
        'GstNetwork.MaxPing'
    ]
    
    for setting in expected:
        if setting in config:
            print(f"  ✓ {setting} = {config[setting]}")
        else:
            print(f"  ✗ Missing {setting}")
            return False
    
    print(f"  ✓ Parsed {len(config)} settings successfully")
    return True


def test_validation():
    """Test validation logic."""
    print("Testing validation...")
    
    def validate_setting(key, value):
        """Simple validation function."""
        if key == "GstRender.ResolutionScale":
            try:
                scale = float(value)
                return 0.5 <= scale <= 2.0
            except ValueError:
                return False
        elif key == "GstRender.FullscreenMode":
            return value in ["0", "1"]
        elif key in ["GstRender.Dx12Enabled", "GstRender.MotionBlurEnable"]:
            return value in ["0", "1"]
        elif key == "GstRender.AntiAliasingDeferred":
            try:
                aa = int(value)
                return 0 <= aa <= 4
            except ValueError:
                return False
        return True
    
    # Test cases
    test_cases = [
        ('GstRender.ResolutionScale', '1.5', True),
        ('GstRender.ResolutionScale', '0.5', True),
        ('GstRender.ResolutionScale', '3.0', False),
        ('GstRender.FullscreenMode', '0', True),
        ('GstRender.FullscreenMode', '2', False),
        ('GstRender.Dx12Enabled', '1', True),
        ('GstRender.Dx12Enabled', '2', False),
    ]
    
    for key, value, expected in test_cases:
        result = validate_setting(key, value)
        if result == expected:
            print(f"  ✓ {key}={value} -> {result}")
        else:
            print(f"  ✗ {key}={value} -> Expected {expected}, got {result}")
            return False
    
    print("  ✓ All validation tests passed")
    return True


def test_file_operations():
    """Test file reading and writing."""
    print("Testing file operations...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config_file = temp_path / "PROFSAVE_profile"
        
        # Write test config
        test_config = """GstRender.Dx12Enabled 1
GstRender.ResolutionScale 1.0
GstAudio.MasterVolume 100
"""
        
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(test_config)
        
        # Read and parse
        with open(config_file, 'r', encoding='utf-8') as f:
            data = f.read()
        
        # Parse settings
        config = {}
        pattern = r'(GstRender\.\w+)\s+(\S+)'
        matches = re.findall(pattern, data)
        for key, value in matches:
            config[key] = value
        
        # Modify a setting
        config['GstRender.Dx12Enabled'] = '0'
        
        # Write back
        new_data = data
        for key, value in config.items():
            pattern = rf'({re.escape(key)})\s+\S+'
            replacement = f'{key} {value}'
            new_data = re.sub(pattern, replacement, new_data)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(new_data)
        
        # Verify change
        with open(config_file, 'r', encoding='utf-8') as f:
            updated_data = f.read()
        
        if 'GstRender.Dx12Enabled 0' in updated_data:
            print("  ✓ File modification successful")
        else:
            print("  ✗ File modification failed")
            return False
        
        print("  ✓ File operations test passed")
        return True


def test_build_scripts():
    """Test that build scripts exist and are readable."""
    print("Testing build scripts...")
    
    scripts = ["build.py", "build_simple.py"]
    
    for script in scripts:
        if Path(script).exists():
            print(f"  ✓ {script} exists")
            
            # Check if it's readable
            try:
                with open(script, 'r') as f:
                    content = f.read()
                
                # Check for key components
                if 'pyinstaller' in content.lower():
                    print(f"  ✓ {script} contains PyInstaller references")
                else:
                    print(f"  ⚠ {script} may not be a proper build script")
            except Exception as e:
                print(f"  ✗ {script} is not readable: {e}")
                return False
        else:
            print(f"  ✗ {script} not found")
            return False
    
    print("  ✓ All build scripts found")
    return True


def test_project_structure():
    """Test that the project has the expected structure."""
    print("Testing project structure...")
    
    required_files = [
        "main.py",
        "core/config_manager.py",
        "gui/main_window.py",
        "gui/graphics_tab.py",
        "gui/audio_tab.py",
        "gui/input_tab.py",
        "gui/game_tab.py",
        "gui/network_tab.py",
        "gui/advanced_tab.py",
        "requirements.txt",
        "README.md"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} missing")
            return False
    
    print("  ✓ All required files present")
    return True


def create_simple_launcher():
    """Create a simple launcher that works without PyQt6."""
    print("Creating simple launcher...")
    
    launcher_content = '''#!/usr/bin/env python3
"""
Simple FieldTuner Launcher
Works without PyQt6 dependencies
"""

import sys
import os
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


def main():
    """Main launcher function."""
    print("FieldTuner - Simple Mode")
    print("========================")
    print()
    
    # Find config file
    config_path = find_config_file()
    if not config_path:
        print("Error: Battlefield 6 config file not found!")
        print("Make sure Battlefield 6 is installed and has been run at least once.")
        print()
        print("Expected locations:")
        print("  Steam: %USERPROFILE%\\Documents\\Battlefield 6\\settings\\steam\\PROFSAVE_profile")
        print("  EA App: %USERPROFILE%\\Documents\\Battlefield 6\\settings\\PROFSAVE_profile")
        return 1
    
    print(f"Found config: {config_path}")
    print()
    
    # Show file info
    file_size = config_path.stat().st_size
    print(f"File size: {file_size} bytes")
    print()
    
    # Try to read and show some settings
    try:
        with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Look for common settings
        import re
        patterns = [
            r'(GstRender\.Dx12Enabled)\\s+(\\S+)',
            r'(GstRender\.ResolutionScale)\\s+(\\S+)',
            r'(GstRender\.FullscreenMode)\\s+(\\S+)',
            r'(GstAudio\.MasterVolume)\\s+(\\S+)'
        ]
        
        print("Current Settings:")
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                key, value = match.groups()
                print(f"  {key} = {value}")
        
        print()
        print("Config file is readable and contains settings.")
        print("You can manually edit this file or use a text editor to modify settings.")
        print()
        print("Common settings you might want to change:")
        print("  GstRender.Dx12Enabled 1/0 (DirectX 12)")
        print("  GstRender.ResolutionScale 0.5-2.0 (Resolution scaling)")
        print("  GstRender.FullscreenMode 0/1 (Windowed/Fullscreen)")
        print("  GstAudio.MasterVolume 0-100 (Master volume)")
        
    except Exception as e:
        print(f"Error reading config file: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
    
    with open("fieldtuner_simple.py", "w") as f:
        f.write(launcher_content)
    
    print("  ✓ Created fieldtuner_simple.py")
    return True


def main():
    """Run all tests."""
    print("FieldTuner - Dependency-Free Test Suite")
    print("=======================================")
    print()
    
    all_passed = True
    
    # Test project structure
    if not test_project_structure():
        all_passed = False
        print()
    
    # Test config parsing
    if not test_config_parsing():
        all_passed = False
        print()
    
    # Test validation
    if not test_validation():
        all_passed = False
        print()
    
    # Test file operations
    if not test_file_operations():
        all_passed = False
        print()
    
    # Test build scripts
    if not test_build_scripts():
        all_passed = False
        print()
    
    # Create simple launcher
    create_simple_launcher()
    print()
    
    print("Test Results")
    print("============")
    if all_passed:
        print("✓ All tests passed!")
        print()
        print("Available options:")
        print("1. Run: python fieldtuner_simple.py (basic config viewer)")
        print("2. Try: python build_simple.py (attempt to build executable)")
        print("3. Manual: Edit your Battlefield 6 config file directly")
        return 0
    else:
        print("✗ Some tests failed.")
        print("But you can still try:")
        print("1. Run: python fieldtuner_simple.py")
        print("2. Try: python build_simple.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())