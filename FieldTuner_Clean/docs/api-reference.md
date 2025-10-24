# FieldTuner API Reference

## ConfigManager

### Methods
- `detect_config()`: Detect Battlefield 6 config file
- `load_config()`: Load configuration from file
- `save_config()`: Save configuration to file
- `create_backup(name)`: Create a backup with optional name
- `restore_backup(path)`: Restore from backup file
- `list_backups()`: List all available backups

### Properties
- `config_path`: Path to the config file
- `settings`: Dictionary of current settings
- `BACKUP_DIR`: Path to backup directory

## UI Components

### MainWindow
- Main application window
- Tab management
- Event handling

### QuickSettingsTab
- Preset management
- Quick configuration
- Toggle switches

### GraphicsTab
- Graphics settings
- Resolution management
- Quality settings

### BackupTab
- Backup creation
- Backup restoration
- Backup management

## Events and Signals
- `settings_changed`: Emitted when settings are modified
- `backup_created`: Emitted when backup is created
- `config_loaded`: Emitted when config is loaded
