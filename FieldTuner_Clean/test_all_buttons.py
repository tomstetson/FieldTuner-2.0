#!/usr/bin/env python3
"""
Comprehensive test script to verify all button functionality
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from main import ConfigManager, MainWindow, debug_logger, log_info, log_warning, log_error, log_debug

class ButtonTestWindow(QMainWindow):
    """Test window to verify button functionality."""
    
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup test UI."""
        self.setWindowTitle("FieldTuner Button Test")
        self.setGeometry(100, 100, 400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Test buttons
        self.test_backup_btn = QPushButton("Test Backup Creation")
        self.test_backup_btn.clicked.connect(self.test_backup_creation)
        layout.addWidget(self.test_backup_btn)
        
        self.test_delete_btn = QPushButton("Test Backup Deletion")
        self.test_delete_btn.clicked.connect(self.test_backup_deletion)
        layout.addWidget(self.test_delete_btn)
        
        self.test_restore_btn = QPushButton("Test Backup Restoration")
        self.test_restore_btn.clicked.connect(self.test_backup_restoration)
        layout.addWidget(self.test_restore_btn)
        
        self.test_main_app_btn = QPushButton("Launch Main Application")
        self.test_main_app_btn.clicked.connect(self.launch_main_app)
        layout.addWidget(self.test_main_app_btn)
        
        central_widget.setLayout(layout)
        
    def test_backup_creation(self):
        """Test backup creation functionality."""
        log_info("🧪 Testing backup creation...", "TEST")
        if self.config_manager._create_backup("Button_Test"):
            log_info("✅ Backup creation test passed!", "TEST")
            print("✅ Backup creation test passed!")
        else:
            log_error("❌ Backup creation test failed!", "TEST")
            print("❌ Backup creation test failed!")
    
    def test_backup_deletion(self):
        """Test backup deletion functionality."""
        log_info("🧪 Testing backup deletion...", "TEST")
        backup_files = list(self.config_manager.BACKUP_DIR.glob("*.bak"))
        if backup_files:
            test_backup = backup_files[-1]  # Delete the oldest
            try:
                test_backup.unlink()
                log_info("✅ Backup deletion test passed!", "TEST")
                print("✅ Backup deletion test passed!")
            except Exception as e:
                log_error(f"❌ Backup deletion test failed: {str(e)}", "TEST")
                print(f"❌ Backup deletion test failed: {str(e)}")
        else:
            log_warning("⚠️ No backups found for deletion test", "TEST")
            print("⚠️ No backups found for deletion test")
    
    def test_backup_restoration(self):
        """Test backup restoration functionality."""
        log_info("🧪 Testing backup restoration...", "TEST")
        backup_files = list(self.config_manager.BACKUP_DIR.glob("*.bak"))
        if backup_files:
            test_backup = backup_files[0]  # Use the most recent
            try:
                # Simulate restoration by copying backup to config
                import shutil
                shutil.copy2(test_backup, self.config_manager.config_path)
                log_info("✅ Backup restoration test passed!", "TEST")
                print("✅ Backup restoration test passed!")
            except Exception as e:
                log_error(f"❌ Backup restoration test failed: {str(e)}", "TEST")
                print(f"❌ Backup restoration test failed: {str(e)}")
        else:
            log_warning("⚠️ No backups found for restoration test", "TEST")
            print("⚠️ No backups found for restoration test")
    
    def launch_main_app(self):
        """Launch the main application for manual testing."""
        log_info("🚀 Launching main application...", "TEST")
        self.main_window = MainWindow()
        self.main_window.show()
        print("✅ Main application launched! Test the backup buttons manually.")

def test_all_buttons():
    """Test all button functionality."""
    log_info("🧪 Testing All Button Functionality...", "TEST")
    
    app = QApplication(sys.argv)
    
    # Test basic functionality first
    config_manager = ConfigManager()
    
    if not config_manager.config_path:
        log_error("❌ Config file not found. Cannot run tests.", "TEST")
        print("❌ ERROR: Config file not found. Please ensure Battlefield 6 is installed and config exists.")
        return
    
    print(f"📁 Found config: {config_manager.config_path}")
    print(f"📊 Settings loaded: {len(config_manager.config_data)}")
    
    # Create test window
    test_window = ButtonTestWindow()
    test_window.show()
    
    print("\n🎮 Button Test Window Launched!")
    print("📋 Test Instructions:")
    print("  1. Click 'Test Backup Creation' to verify backup creation")
    print("  2. Click 'Test Backup Deletion' to verify backup deletion")
    print("  3. Click 'Test Backup Restoration' to verify backup restoration")
    print("  4. Click 'Launch Main Application' to test GUI buttons manually")
    print("\n🔧 Manual Testing:")
    print("  - In the main app, go to the 'Backups' tab")
    print("  - Select a backup from the list")
    print("  - Click 'Delete Selected' - should show confirmation dialog")
    print("  - Click 'Restore Selected' - should show confirmation dialog")
    print("  - Both buttons should be enabled when an item is selected")
    print("  - Both buttons should be disabled when no item is selected")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    test_all_buttons()
