"""
Clean, organized BackupTab implementation
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from datetime import datetime
import subprocess
import os
from pathlib import Path

class BackupTab(QWidget):
    """Clean, organized backup management tab."""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.setup_ui()
        self.refresh_backups()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("💾 Backup Management")
        header.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #ffffff; 
            margin-bottom: 10px;
            padding: 15px;
            background-color: #2a2a2a;
            border-radius: 8px;
            border: 1px solid #444;
        """)
        layout.addWidget(header)
        
        # Most Recent Backup - Prominent Display
        recent_group = QGroupBox("🕒 Most Recent Backup")
        recent_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #4a90e2;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                font-size: 16px;
            }
        """)
        
        recent_layout = QVBoxLayout()
        
        # Recent backup info
        self.recent_backup_label = QLabel("No recent backup found")
        self.recent_backup_label.setStyleSheet("""
            color: #cccccc;
            font-size: 14px;
            padding: 12px;
            background-color: #333;
            border-radius: 6px;
            border: 1px solid #555;
        """)
        recent_layout.addWidget(self.recent_backup_label)
        
        # Quick restore button
        self.quick_restore_btn = QPushButton("💾 Restore Most Recent Backup")
        self.quick_restore_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1b5e20;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        self.quick_restore_btn.clicked.connect(self.restore_most_recent)
        self.quick_restore_btn.setEnabled(False)
        recent_layout.addWidget(self.quick_restore_btn)
        
        recent_group.setLayout(recent_layout)
        layout.addWidget(recent_group)
        
        # Create Backup Section
        create_group = QGroupBox("💾 Create New Backup")
        create_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                font-size: 16px;
            }
        """)
        
        create_layout = QHBoxLayout()
        
        # Backup name input
        self.backup_name_input = QLineEdit()
        self.backup_name_input.setPlaceholderText("Enter backup name (optional)")
        self.backup_name_input.setStyleSheet("""
            QLineEdit {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 10px;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
            }
        """)
        create_layout.addWidget(QLabel("Name:"))
        create_layout.addWidget(self.backup_name_input)
        
        # Create backup button
        self.create_backup_btn = QPushButton("💾 Create Backup")
        self.create_backup_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        self.create_backup_btn.clicked.connect(self.create_backup)
        create_layout.addWidget(self.create_backup_btn)
        
        create_group.setLayout(create_layout)
        layout.addWidget(create_group)
        
        # Available Backups Section - Single, Clean Section
        list_group = QGroupBox("📋 Available Backups")
        list_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #2a2a2a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                font-size: 16px;
            }
        """)
        
        list_layout = QVBoxLayout()
        
        # Backup list with better formatting
        self.backup_list = QListWidget()
        self.backup_list.setStyleSheet("""
            QListWidget {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #444;
                border-radius: 4px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #4a90e2;
                border: 1px solid #4a90e2;
            }
            QListWidget::item:hover {
                background-color: #444;
            }
        """)
        self.backup_list.setMaximumHeight(300)
        list_layout.addWidget(self.backup_list)
        
        # Action buttons - All in one clean row
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_backups)
        button_layout.addWidget(self.refresh_btn)
        
        # Open folder button
        self.open_folder_btn = QPushButton("📂 Open Folder")
        self.open_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        self.open_folder_btn.clicked.connect(self.open_backup_folder)
        button_layout.addWidget(self.open_folder_btn)
        
        button_layout.addStretch()
        
        # Restore selected button
        self.restore_btn = QPushButton("🔄 Restore Selected")
        self.restore_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1b5e20;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        self.restore_btn.clicked.connect(self.restore_selected_backup)
        self.restore_btn.setEnabled(False)
        button_layout.addWidget(self.restore_btn)
        
        # Open backup file button
        self.open_backup_btn = QPushButton("📂 Open File")
        self.open_backup_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        self.open_backup_btn.clicked.connect(self.open_selected_backup)
        self.open_backup_btn.setEnabled(False)
        button_layout.addWidget(self.open_backup_btn)
        
        # Delete selected button
        self.delete_btn = QPushButton("🗑️ Delete Selected")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_selected_backup)
        self.delete_btn.setEnabled(False)
        button_layout.addWidget(self.delete_btn)
        
        list_layout.addLayout(button_layout)
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)
        
        # Connect selection change signal
        self.backup_list.itemSelectionChanged.connect(self.update_backup_buttons)
    
    def refresh_backups(self):
        """Refresh the backup list and update recent backup display."""
        self.backup_list.clear()
        
        if not self.config_manager.BACKUP_DIR.exists():
            self.recent_backup_label.setText("No backup directory found")
            self.quick_restore_btn.setEnabled(False)
            return
        
        backup_files = list(self.config_manager.BACKUP_DIR.glob("*.bak"))
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Update recent backup display
        if backup_files:
            most_recent = backup_files[0]
            file_size = most_recent.stat().st_size
            file_time = datetime.fromtimestamp(most_recent.stat().st_mtime)
            time_str = file_time.strftime("%Y-%m-%d %H:%M:%S")
            
            self.recent_backup_label.setText(f"📁 {most_recent.name}\n📅 {time_str}\n📊 {file_size:,} bytes")
            self.quick_restore_btn.setEnabled(True)
        else:
            self.recent_backup_label.setText("No recent backup found")
            self.quick_restore_btn.setEnabled(False)
        
        # Populate backup list
        for backup_file in backup_files:
            try:
                timestamp = datetime.fromtimestamp(backup_file.stat().st_mtime)
                size = backup_file.stat().st_size
                
                # Format file size
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size / 1024:.1f} KB"
                else:
                    size_str = f"{size / (1024 * 1024):1f} MB"
                
                # Create a more readable display
                item_text = f"📁 {backup_file.name}\n🕒 {timestamp.strftime('%Y-%m-%d at %H:%M:%S')} • 📊 {size_str}"
                
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, backup_file)
                self.backup_list.addItem(item)
            except Exception as e:
                print(f"Error processing backup file {backup_file}: {e}")
    
    def create_backup(self):
        """Create a new backup."""
        backup_name = self.backup_name_input.text().strip()
        if self.config_manager._create_backup(backup_name if backup_name else None):
            QMessageBox.information(self, "Backup Created", "✅ Backup created successfully!")
            self.backup_name_input.clear()
            self.refresh_backups()
        else:
            QMessageBox.warning(self, "Backup Failed", "❌ Failed to create backup!")
    
    def restore_most_recent(self):
        """Restore the most recent backup."""
        backup_files = list(self.config_manager.BACKUP_DIR.glob("*.bak"))
        if not backup_files:
            QMessageBox.warning(self, "No Backups", "❌ No backups found!")
            return
        
        most_recent = max(backup_files, key=lambda x: x.stat().st_mtime)
        
        reply = QMessageBox.question(
            self, 
            "Restore Most Recent Backup",
            f"🔄 Are you sure you want to restore the most recent backup?\n\n"
            f"📁 File: {most_recent.name}\n"
            f"📅 Date: {datetime.fromtimestamp(most_recent.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"⚠️ This will overwrite your current settings!\n"
            f"💾 A backup of your current settings will be created first.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Create backup of current settings first
                self.config_manager._create_backup("Before_Restore")
                
                # Restore the backup
                import shutil
                shutil.copy2(most_recent, self.config_manager.config_path)
                
                QMessageBox.information(self, "Backup Restored", "✅ Most recent backup restored successfully!")
                self.refresh_backups()
            except Exception as e:
                QMessageBox.critical(self, "Restore Failed", f"❌ Failed to restore backup: {str(e)}")
    
    def restore_selected_backup(self):
        """Restore the selected backup."""
        current_item = self.backup_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "❌ Please select a backup to restore!")
            return
        
        backup_file = current_item.data(Qt.ItemDataRole.UserRole)
        if not backup_file or not backup_file.exists():
            QMessageBox.warning(self, "Error", "❌ Selected backup file not found!")
            return
        
        reply = QMessageBox.question(
            self, 
            "Restore Backup",
            f"🔄 Are you sure you want to restore this backup?\n\n"
            f"📁 File: {backup_file.name}\n"
            f"📅 Date: {current_item.text()}\n\n"
            f"⚠️ This will overwrite your current settings!\n"
            f"💾 A backup of your current settings will be created first.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Create backup of current settings first
                self.config_manager._create_backup("Before_Restore")
                
                # Restore the backup
                import shutil
                shutil.copy2(backup_file, self.config_manager.config_path)
                
                QMessageBox.information(self, "Backup Restored", "✅ Backup restored successfully!")
                self.refresh_backups()
            except Exception as e:
                QMessageBox.critical(self, "Restore Failed", f"❌ Failed to restore backup: {str(e)}")
    
    def delete_selected_backup(self):
        """Delete the selected backup."""
        current_item = self.backup_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "❌ Please select a backup to delete!")
            return
        
        backup_file = current_item.data(Qt.ItemDataRole.UserRole)
        if not backup_file or not backup_file.exists():
            QMessageBox.warning(self, "Error", "❌ Selected backup file not found!")
            return
        
        reply = QMessageBox.question(
            self, 
            "Delete Backup",
            f"🗑️ Are you sure you want to delete this backup?\n\n"
            f"📁 File: {backup_file.name}\n"
            f"📅 Date: {current_item.text()}\n\n"
            f"⚠️ This action cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                backup_file.unlink()
                QMessageBox.information(self, "Backup Deleted", "✅ Backup deleted successfully!")
                self.refresh_backups()
            except Exception as e:
                QMessageBox.critical(self, "Delete Failed", f"❌ Failed to delete backup: {str(e)}")
    
    def open_backup_folder(self):
        """Open the backup folder in file explorer."""
        try:
            backup_path = str(self.config_manager.BACKUP_DIR)
            os.makedirs(backup_path, exist_ok=True)
            subprocess.run(f'explorer "{backup_path}"', shell=True, check=False)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"❌ Failed to open backup folder: {str(e)}")
    
    def open_selected_backup(self):
        """Open the selected backup file in file explorer."""
        current_item = self.backup_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "❌ Please select a backup to open!")
            return
        
        backup_file = current_item.data(Qt.ItemDataRole.UserRole)
        if not backup_file or not backup_file.exists():
            QMessageBox.warning(self, "Error", "❌ Selected backup file not found!")
            return
        
        try:
            subprocess.run(f'explorer /select,"{backup_file}"', shell=True, check=False)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"❌ Failed to open backup file: {str(e)}")
    
    def update_backup_buttons(self):
        """Update backup action buttons based on selection."""
        has_selection = self.backup_list.currentItem() is not None
        self.restore_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        self.open_backup_btn.setEnabled(has_selection)
