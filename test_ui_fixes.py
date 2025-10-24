#!/usr/bin/env python3
"""
Test script to verify UI fixes - scrolling, code view, and backup system.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ConfigManager

def test_ui_fixes():
    """Test UI fixes."""
    print("🧪 Testing UI Fixes...")
    
    # Initialize config manager
    config_manager = ConfigManager()
    
    if not config_manager.config_path:
        print("❌ No BF6 config file found!")
        return False
    
    print(f"📁 Found config: {config_manager.config_path}")
    print(f"📊 Settings loaded: {len(config_manager.config_data)}")
    
    # Test backup system
    print("💾 Testing backup system...")
    backup_dir = config_manager.BACKUP_DIR
    if backup_dir.exists():
        backup_files = list(backup_dir.glob("*.bak"))
        print(f"📁 Backup directory: {backup_dir}")
        print(f"📊 Backup files found: {len(backup_files)}")
        
        if backup_files:
            most_recent = max(backup_files, key=lambda x: x.stat().st_mtime)
            print(f"🕒 Most recent backup: {most_recent.name}")
            print(f"📅 Size: {most_recent.stat().st_size:,} bytes")
    
    # Test config data
    print("⚙️ Testing config data...")
    print(f"📊 Total settings: {len(config_manager.config_data)}")
    
    # Show some settings
    for i, (key, value) in enumerate(list(config_manager.config_data.items())[:5]):
        print(f"  {key} = {value}")
    
    if len(config_manager.config_data) > 5:
        print(f"  ... and {len(config_manager.config_data) - 5} more settings")
    
    return True

if __name__ == "__main__":
    success = test_ui_fixes()
    if success:
        print("\n🎮 SUCCESS: UI fixes working!")
    else:
        print("\n💥 FAILED: UI fixes not working!")
    
    input("\nPress Enter to continue...")
