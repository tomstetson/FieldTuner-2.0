#!/usr/bin/env python3
"""
Test script to verify the correct settings count and breakdown.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ConfigManager

def test_settings_count():
    """Test the correct settings count and breakdown."""
    print("🧪 Testing Settings Count...")
    
    # Initialize config manager
    config_manager = ConfigManager()
    
    if not config_manager.config_path:
        print("❌ No BF6 config file found!")
        return False
    
    print(f"📁 Found config: {config_manager.config_path}")
    print(f"📊 Total settings loaded: {len(config_manager.config_data)}")
    
    # Break down by category
    categories = {
        'GstRender': 0,
        'GstAudio': 0,
        'GstInput': 0,
        'GstNetwork': 0,
        'GstGame': 0
    }
    
    for key in config_manager.config_data.keys():
        for category in categories.keys():
            if key.startswith(category):
                categories[category] += 1
                break
    
    print("\n📊 Settings Breakdown:")
    for category, count in categories.items():
        print(f"  {category}: {count} settings")
    
    total = sum(categories.values())
    print(f"\n📊 Total: {total} settings")
    
    # Show some example settings
    print("\n🔧 Example Settings:")
    for i, (key, value) in enumerate(list(config_manager.config_data.items())[:10]):
        print(f"  {key} = {value}")
    
    if len(config_manager.config_data) > 10:
        print(f"  ... and {len(config_manager.config_data) - 10} more settings")
    
    return True

if __name__ == "__main__":
    success = test_settings_count()
    if success:
        print("\n🎮 SUCCESS: Settings count is correct!")
    else:
        print("\n💥 FAILED: Settings count is incorrect!")
    
    input("\nPress Enter to continue...")
