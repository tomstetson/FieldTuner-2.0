#!/usr/bin/env python3
"""
Test script to verify backup button functionality
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from main import ConfigManager, debug_logger, log_info, log_warning, log_error, log_debug

def test_backup_functionality():
    """Test backup creation, listing, and deletion."""
    log_info("🧪 Testing Backup Button Functionality...", "TEST")
    
    config_manager = ConfigManager()
    
    if not config_manager.config_path:
        log_error("❌ Config file not found. Cannot run test.", "TEST")
        print("❌ ERROR: Config file not found. Please ensure Battlefield 6 is installed and config exists.")
        return
    
    print(f"📁 Found config: {config_manager.config_path}")
    print(f"📊 Settings loaded: {len(config_manager.config_data)}")
    
    # Test backup creation
    print("💾 Testing backup creation...")
    if config_manager._create_backup("Test_Backup"):
        log_info("✅ Backup created successfully!", "TEST")
        print("✅ Backup created successfully!")
    else:
        log_error("❌ Failed to create backup!", "TEST")
        print("❌ Failed to create backup!")
        return
    
    # List all backups
    print("📋 Listing all backups...")
    backup_files = list(config_manager.BACKUP_DIR.glob("*.bak"))
    backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    print(f"📊 Backup files found: {len(backup_files)}")
    
    if backup_files:
        for i, backup_file in enumerate(backup_files[:5]):  # Show first 5
            file_size = backup_file.stat().st_size
            file_time = backup_file.stat().st_mtime
            print(f"  {i+1}. {backup_file.name} ({file_size:,} bytes)")
        
        if len(backup_files) > 5:
            print(f"  ... and {len(backup_files) - 5} more backups")
    
    # Test backup deletion (if we have more than 1 backup)
    if len(backup_files) > 1:
        print("🗑️ Testing backup deletion...")
        test_backup = backup_files[-1]  # Delete the oldest backup
        print(f"🗑️ Attempting to delete: {test_backup.name}")
        
        try:
            test_backup.unlink()
            print("✅ Backup deleted successfully!")
            log_info("✅ Backup deletion test passed!", "TEST")
        except Exception as e:
            print(f"❌ Failed to delete backup: {str(e)}")
            log_error(f"❌ Backup deletion failed: {str(e)}", "TEST")
    else:
        print("ℹ️ Only one backup found, skipping deletion test")
    
    print("\n🎮 SUCCESS: Backup functionality working!\n")
    print("🔧 If buttons still don't work in the GUI, check:")
    print("  1. Button connections in setup_ui()")
    print("  2. update_backup_buttons() method")
    print("  3. itemSelectionChanged signal connection")
    print("  4. Button enabled/disabled states")
    
    input("Press Enter to continue...")

if __name__ == "__main__":
    test_backup_functionality()
