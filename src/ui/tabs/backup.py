"""
FieldTuner V2.0 - Backup Tab
Backup management with restore functionality.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, 
    QLabel, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from pathlib import Path

from debug import log_info, log_error, log_warning


class BackupTab(QWidget):
    """Backup management tab with restore functionality."""
    
    backup_restored = pyqtSignal()
    
    def __init__(self, config_manager, favorites_manager):
        super().__init__()
        self.config_manager = config_manager
        self.favorites_manager = favorites_manager
        self.setup_ui()
        self.refresh_backups()
    
    def setup_ui(self):
        """Setup the backup tab UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Backup Management")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 16px;
            padding: 8px 0px;
        """)
        layout.addWidget(header)
        
        # Create backup section
        self.create_backup_section(layout)
        
        # Create restore section
        self.create_restore_section(layout)
        
        layout.addStretch()
    
    def create_backup_section(self, parent_layout):
        """Create backup section."""
        group = QGroupBox("Create Backup")
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Backup description
        desc_label = QLabel("Create a backup of your current configuration:")
        desc_label.setStyleSheet("color: #ccc; font-size: 14px;")
        layout.addWidget(desc_label)
        
        # Create backup button
        self.create_backup_btn = QPushButton("Create New Backup")
        self.create_backup_btn.setStyleSheet(self.get_button_style())
        self.create_backup_btn.clicked.connect(self.create_backup)
        layout.addWidget(self.create_backup_btn)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def create_restore_section(self, parent_layout):
        """Create restore section."""
        group = QGroupBox("Restore Backup")
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Available backups list
        self.backups_list = QListWidget()
        self.backups_list.setStyleSheet("""
            QListWidget {
                background-color: #333;
                color: white;
                border: 1px solid #666;
                border-radius: 4px;
                padding: 8px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #555;
            }
            QListWidget::item:selected {
                background-color: #4a90e2;
            }
        """)
        layout.addWidget(self.backups_list)
        
        # Restore button
        self.restore_btn = QPushButton("Restore Selected Backup")
        self.restore_btn.setStyleSheet(self.get_button_style())
        self.restore_btn.clicked.connect(self.restore_backup)
        layout.addWidget(self.restore_btn)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
    
    def get_group_style(self):
        """Get group box styling."""
        return """
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #e0e0e0;
                border: 2px solid #444;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """
    
    def get_button_style(self):
        """Get button styling."""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2,
                    stop:1 #357abd);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5ba0f2,
                    stop:1 #4a90e2);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #357abd,
                    stop:1 #2c5aa0);
            }
        """
    
    def create_backup(self):
        """Create a new backup."""
        try:
            log_info("Creating new backup", "BACKUP")
            
            # Create backup using config manager
            backup_path = self.config_manager.create_backup()
            
            if backup_path:
                log_info(f"Backup created successfully: {backup_path}", "BACKUP")
                self.refresh_backups()
                
                # Show success message
                QMessageBox.information(
                    self, 
                    "Backup Created", 
                    f"Backup created successfully!\n\nLocation: {backup_path.name}"
                )
            else:
                log_error("Failed to create backup", "BACKUP")
                QMessageBox.warning(self, "Backup Failed", "Failed to create backup. Please try again.")
                
        except Exception as e:
            log_error(f"Failed to create backup: {str(e)}", "BACKUP", e)
            QMessageBox.critical(self, "Backup Error", f"Failed to create backup:\n{str(e)}")
    
    def restore_backup(self):
        """Restore selected backup."""
        try:
            current_item = self.backups_list.currentItem()
            if not current_item:
                QMessageBox.warning(self, "No Selection", "Please select a backup to restore.")
                return
            
            backup_name = current_item.text()
            
            # Confirm restore
            reply = QMessageBox.question(
                self, 
                "Confirm Restore", 
                f"Are you sure you want to restore backup '{backup_name}'?\n\nThis will overwrite your current configuration.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                log_info(f"Restoring backup: {backup_name}", "BACKUP")
                
                # Find backup file
                backup_path = None
                try:
                    backup_files = list(self.config_manager.BACKUP_DIR.glob("*.bak"))
                    for backup_file in backup_files:
                        if backup_name in backup_file.name:
                            backup_path = backup_file
                            break
                    
                    if backup_path and backup_path.exists():
                        # Restore backup
                        success = self.config_manager.restore_backup(backup_path)
                        
                        if success:
                            log_info("Backup restored successfully", "BACKUP")
                            self.backup_restored.emit()
                            
                            QMessageBox.information(
                                self, 
                                "Backup Restored", 
                                f"Backup '{backup_name}' restored successfully!\n\nPlease restart the application to apply changes."
                            )
                        else:
                            log_error("Failed to restore backup", "BACKUP")
                            QMessageBox.warning(self, "Restore Failed", "Failed to restore backup. Please try again.")
                    else:
                        log_error(f"Backup file not found: {backup_name}", "BACKUP")
                        QMessageBox.warning(self, "Backup Not Found", f"Backup file '{backup_name}' not found.")
                        
                except Exception as e:
                    log_error(f"Error during restore: {str(e)}", "BACKUP", e)
                    QMessageBox.critical(self, "Restore Error", f"Error during restore:\n{str(e)}")
                
        except Exception as e:
            log_error(f"Failed to restore backup: {str(e)}", "BACKUP", e)
            QMessageBox.critical(self, "Restore Error", f"Failed to restore backup:\n{str(e)}")
    
    def refresh_backups(self):
        """Refresh the backups list."""
        try:
            log_info("Refreshing backups list", "BACKUP")
            
            self.backups_list.clear()
            
            # Get backup files
            try:
                backup_files = list(self.config_manager.BACKUP_DIR.glob("*.bak"))
                backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                for backup_file in backup_files:
                    item = QListWidgetItem(backup_file.name)
                    item.setToolTip(f"Created: {backup_file.stat().st_mtime}")
                    self.backups_list.addItem(item)
                
                log_info(f"Found {len(backup_files)} backup files", "BACKUP")
                
            except Exception as e:
                log_error(f"Failed to list backup files: {str(e)}", "BACKUP", e)
                # Add placeholder item
                item = QListWidgetItem("No backups found")
                item.setFlags(Qt.ItemFlag.NoItemFlags)
                self.backups_list.addItem(item)
                
        except Exception as e:
            log_error(f"Failed to refresh backups: {str(e)}", "BACKUP", e)
    
    def save_settings(self):
        """Save backup settings (no-op for backup tab)."""
        pass
