#!/usr/bin/env python3
"""
Test script to verify enhanced backup system and settings management.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ConfigManager

def test_enhanced_features():
    """Test enhanced backup system and settings."""
    print("🧪 Testing Enhanced FieldTuner Features...")
    
    # Initialize config manager
    config_manager = ConfigManager()
    
    if not config_manager.config_path:
        print("❌ No BF6 config file found!")
        return False
    
    print(f"📁 Found config: {config_manager.config_path}")
    print(f"📊 Settings loaded: {len(config_manager.config_data)}")
    
    # Test backup creation
    print("💾 Testing backup creation...")
    if config_manager._create_backup("Enhanced_Test"):
        print("✅ Backup created successfully!")
        
        # Check backup directory
        backup_dir = config_manager.BACKUP_DIR
        if backup_dir.exists():
            backup_files = list(backup_dir.glob("*.bak"))
            print(f"📁 Backup directory: {backup_dir}")
            print(f"📊 Backup files found: {len(backup_files)}")
            
            if backup_files:
                most_recent = max(backup_files, key=lambda x: x.stat().st_mtime)
                print(f"🕒 Most recent backup: {most_recent.name}")
                print(f"📅 Size: {most_recent.stat().st_size:,} bytes")
        
        return True
    else:
        print("❌ Failed to create backup!")
        return False

if __name__ == "__main__":
    success = test_enhanced_features()
    if success:
        print("\n🎮 SUCCESS: Enhanced features working!")
    else:
        print("\n💥 FAILED: Enhanced features not working!")
    
    input("\nPress Enter to continue...")
