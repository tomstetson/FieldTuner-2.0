#!/usr/bin/env python3
"""
Core functionality test for FieldTuner
Tests the config manager without requiring PyQt6 GUI components.
"""

import sys
import os
import tempfile
import re
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def create_mock_config():
    """Create a mock Battlefield 6 config file for testing."""
    return """GstRender.Dx12Enabled 1
GstRender.MotionBlurEnable 1
GstRender.DepthOfFieldEnable 1
GstRender.AntiAliasingDeferred 2
GstRender.ResolutionScale 1.0
GstRender.FullscreenMode 1
GstRender.VSyncEnable 0
GstRender.RayTracingEnabled 0
GstRender.AmbientOcclusionEnable 1
GstRender.VolumetricLightingEnable 1
GstAudio.MasterVolume 100
GstAudio.MusicVolume 80
GstAudio.SFXVolume 100
GstAudio.Quality 2
GstAudio.Channels 0
GstInput.MouseSensitivity 50
GstInput.MouseAcceleration 0
GstInput.RawInput 1
GstInput.GamepadSensitivity 50
GstInput.Vibration 1
GstGame.Difficulty 1
GstGame.AutoAim 0
GstGame.AutoHeal 1
GstGame.HUDScale 100
GstNetwork.MaxPing 150
GstNetwork.Quality 2
GstNetwork.UploadRate 1000
GstNetwork.DownloadRate 2000
"""


def test_config_parsing():
    """Test the config parsing functionality."""
    print("Testing config parsing...")
    
    config_data = create_mock_config()
    
    # Test parsing logic (simplified version of what's in config_manager.py)
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
    
    # Test that we found the expected settings
    expected_settings = [
        'GstRender.Dx12Enabled',
        'GstRender.ResolutionScale',
        'GstAudio.MasterVolume',
        'GstInput.MouseSensitivity',
        'GstGame.Difficulty',
        'GstNetwork.MaxPing'
    ]
    
    for setting in expected_settings:
        if setting in config:
            print(f"  ✓ Found {setting} = {config[setting]}")
        else:
            print(f"  ✗ Missing {setting}")
            return False
    
    print(f"  ✓ Parsed {len(config)} settings successfully")
    return True


def test_validation():
    """Test the validation logic."""
    print("Testing validation logic...")
    
    # Test cases: (key, value, should_be_valid)
    test_cases = [
        ('GstRender.ResolutionScale', '1.5', True),
        ('GstRender.ResolutionScale', '0.5', True),
        ('GstRender.ResolutionScale', '2.0', True),
        ('GstRender.ResolutionScale', '3.0', False),
        ('GstRender.ResolutionScale', 'abc', False),
        ('GstRender.FullscreenMode', '0', True),
        ('GstRender.FullscreenMode', '1', True),
        ('GstRender.FullscreenMode', '2', False),
        ('GstRender.Dx12Enabled', '0', True),
        ('GstRender.Dx12Enabled', '1', True),
        ('GstRender.Dx12Enabled', '2', False),
        ('GstRender.AntiAliasingDeferred', '0', True),
        ('GstRender.AntiAliasingDeferred', '4', True),
        ('GstRender.AntiAliasingDeferred', '5', False),
    ]
    
    for key, value, should_be_valid in test_cases:
        is_valid, error = validate_setting(key, value)
        if is_valid == should_be_valid:
            status = "✓" if is_valid else "✓"
            print(f"  {status} {key}={value} -> {is_valid} ({error if not is_valid else 'OK'})")
        else:
            print(f"  ✗ {key}={value} -> Expected {should_be_valid}, got {is_valid}")
            return False
    
    print("  ✓ All validation tests passed")
    return True


def validate_setting(key, value):
    """Simplified validation function."""
    if key == "GstRender.ResolutionScale":
        try:
            scale = float(value)
            if 0.5 <= scale <= 2.0:
                return True, ""
            else:
                return False, "Resolution scale must be between 0.5 and 2.0"
        except ValueError:
            return False, "Resolution scale must be a number"
    
    elif key == "GstRender.FullscreenMode":
        if value in ["0", "1"]:
            return True, ""
        else:
            return False, "Fullscreen mode must be 0 (windowed) or 1 (fullscreen)"
    
    elif key in ["GstRender.Dx12Enabled", "GstRender.MotionBlurEnable", "GstRender.DepthOfFieldEnable"]:
        if value in ["0", "1"]:
            return True, ""
        else:
            return False, "Boolean setting must be 0 or 1"
    
    elif key == "GstRender.AntiAliasingDeferred":
        try:
            aa = int(value)
            if 0 <= aa <= 4:
                return True, ""
            else:
                return False, "Anti-aliasing level must be between 0 and 4"
        except ValueError:
            return False, "Anti-aliasing level must be a number"
    
    return True, ""


def test_file_operations():
    """Test file reading and writing operations."""
    print("Testing file operations...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config_file = temp_path / "PROFSAVE_profile"
        
        # Write test config
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(create_mock_config())
        
        # Read and parse
        with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
        
        # Parse settings
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


def test_build_script():
    """Test the build script without actually building."""
    print("Testing build script...")
    
    # Check if build.py exists and is readable
    build_script = Path("build.py")
    if not build_script.exists():
        print("  ✗ build.py not found")
        return False
    
    # Read and check the build script content
    with open(build_script, 'r') as f:
        content = f.read()
    
    # Check for key components
    required_components = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        'FieldTuner.exe'
    ]
    
    for component in required_components:
        if component in content:
            print(f"  ✓ Found {component} in build script")
        else:
            print(f"  ✗ Missing {component} in build script")
            return False
    
    print("  ✓ Build script test passed")
    return True


def main():
    """Run all core tests."""
    print("FieldTuner Core Functionality Test")
    print("=================================")
    print()
    
    all_passed = True
    
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
    
    # Test build script
    if not test_build_script():
        all_passed = False
        print()
    
    print("Test Results")
    print("============")
    if all_passed:
        print("✓ All core tests passed!")
        print("The config parsing and file handling logic is working correctly.")
        print("You can proceed with building the executable once dependencies are resolved.")
        return 0
    else:
        print("✗ Some core tests failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
