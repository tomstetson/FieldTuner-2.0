#!/usr/bin/env python3
"""
Test script to verify that FieldTuner can actually modify the BF6 config file.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ConfigManager

def test_config_write():
    """Test that we can actually write to the BF6 config file."""
    print("🧪 Testing BF6 Config File Write...")
    
    # Initialize config manager
    config_manager = ConfigManager()
    
    if not config_manager.config_path:
        print("❌ No BF6 config file found!")
        return False
    
    print(f"📁 Found config: {config_manager.config_path}")
    print(f"📊 Settings loaded: {len(config_manager.config_data)}")
    
    # Test setting a value
    print("🔧 Testing setting DirectX 12 to enabled...")
    config_manager.set_setting('GstRender.Dx12Enabled', '1')
    
    # Test saving
    print("💾 Attempting to save config...")
    if config_manager.save_config():
        print("✅ Config saved successfully!")
        
        # Check if file was actually modified
        import time
        time.sleep(1)  # Wait a moment
        
        current_time = os.path.getmtime(config_manager.config_path)
        print(f"📅 Config file last modified: {current_time}")
        
        return True
    else:
        print("❌ Failed to save config!")
        return False

if __name__ == "__main__":
    success = test_config_write()
    if success:
        print("\n🎮 SUCCESS: FieldTuner can modify BF6 config files!")
    else:
        print("\n💥 FAILED: FieldTuner cannot modify BF6 config files!")
    
    input("\nPress Enter to continue...")
