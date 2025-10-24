# FieldTuner Architecture

This document provides an overview of the FieldTuner system architecture, design decisions, and technical implementation.

## 🏗️ System Overview

FieldTuner is a desktop application built with Python and PyQt6, designed to manage Battlefield 6 configuration files. The application follows a modular architecture with clear separation of concerns.

## 📐 Architecture Principles

### Design Goals
- **Modularity**: Clear separation between UI, business logic, and data access
- **Maintainability**: Easy to understand, modify, and extend
- **Testability**: Comprehensive test coverage for all components
- **Portability**: Cross-platform compatibility where possible
- **Performance**: Efficient handling of large configuration files

### Key Design Decisions
- **PyQt6**: Chosen for modern, native-looking UI and excellent Python integration
- **Binary Config Handling**: Custom parser for Battlefield 6's binary format
- **Portable Design**: Self-contained executable with no external dependencies
- **Backup System**: Automatic backup creation before any modifications

## 🧩 Component Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    FieldTuner Application                   │
├─────────────────────────────────────────────────────────────┤
│  MainWindow (UI Controller)                                │
│  ├── QuickSettingsTab                                       │
│  ├── GraphicsTab                                            │
│  ├── BackupTab                                              │
│  ├── CodeViewTab                                            │
│  └── DebugTab                                               │
├─────────────────────────────────────────────────────────────┤
│  ConfigManager (Business Logic)                             │
│  ├── Config Detection                                       │
│  ├── Binary Parsing                                         │
│  ├── Settings Management                                    │
│  └── Backup Operations                                      │
├─────────────────────────────────────────────────────────────┤
│  Data Layer                                                 │
│  ├── Battlefield 6 Config Files                             │
│  ├── Backup Storage                                         │
│  └── Log Files                                              │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

#### MainWindow
- **Purpose**: Main application window and UI coordination
- **Responsibilities**:
  - Tab management
  - UI initialization
  - Event handling
  - Application lifecycle

#### ConfigManager
- **Purpose**: Core business logic for configuration management
- **Responsibilities**:
  - Config file detection and parsing
  - Settings modification
  - Backup creation and management
  - Data validation

#### UI Tabs
- **QuickSettingsTab**: Preset management and quick configuration
- **GraphicsTab**: Graphics settings management
- **BackupTab**: Backup creation, restoration, and management
- **CodeViewTab**: Raw config file viewing
- **DebugTab**: Logging and troubleshooting

## 🔄 Data Flow

### Configuration Loading
```
1. Application Start
2. ConfigManager.detect_config()
3. ConfigManager._parse_config_data()
4. Settings loaded into UI components
5. User can modify settings
```

### Settings Modification
```
1. User modifies setting in UI
2. Setting stored in ConfigManager.settings
3. User clicks "Apply Changes"
4. ConfigManager.save_config()
5. Backup created automatically
6. Config file updated
```

### Backup Operations
```
1. User requests backup
2. ConfigManager._create_backup()
3. Current config copied to backup directory
4. Backup added to list
5. User can restore from backup
```

## 🗄️ Data Storage

### Configuration Files
- **Format**: Binary PROFSAVE_profile format
- **Location**: Battlefield 6 settings directory
- **Size**: Typically 100-200 KB
- **Structure**: Binary format with specific field layouts

### Backup System
- **Location**: `%APPDATA%\FieldTuner\backups\`
- **Format**: `.bak` files (copies of original config)
- **Naming**: `FieldTuner_Backup_YYYY-MM-DD_HH-MM-SS.bak`
- **Retention**: Manual management by user

### Logging
- **Location**: `%APPDATA%\FieldTuner\logs\`
- **Format**: Text files with timestamps
- **Levels**: DEBUG, INFO, WARNING, ERROR
- **Rotation**: Automatic log rotation

## 🔧 Technical Implementation

### Binary Config Parsing
```python
class ConfigManager:
    def _parse_config_data(self):
        # Read binary config file
        # Parse known settings with their types
        # Extract values based on field definitions
        # Store in settings dictionary
```

### UI Component Architecture
```python
class QuickSettingsTab(QWidget):
    def __init__(self, config_manager):
        # Initialize UI components
        # Connect signals and slots
        # Load current settings
    
    def create_professional_toggle(self, setting, description):
        # Create custom toggle switch
        # Apply styling and behavior
        # Return configured component
```

### Backup Management
```python
class BackupTab(QWidget):
    def create_backup(self):
        # Get backup name from user
        # Call ConfigManager._create_backup()
        # Refresh backup list
        # Show success message
```

## 🧪 Testing Architecture

### Test Structure
```
tests/
├── test_config_manager.py      # ConfigManager tests
├── test_ui_components.py       # UI component tests
├── test_integration.py         # Integration tests
└── fixtures/                   # Test data and fixtures
```

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **UI Tests**: User interface testing with pytest-qt
- **End-to-End Tests**: Complete workflow testing

## 🚀 Build and Deployment

### Build Process
1. **Source Code**: Python source files
2. **Dependencies**: PyInstaller, PyQt6
3. **Build Script**: Automated build process
4. **Output**: Self-contained executable

### Deployment Strategy
- **Portable Executable**: Single .exe file
- **No Installation**: Extract and run
- **Data Persistence**: AppData directory
- **Update Mechanism**: Manual download and replace

## 🔒 Security Considerations

### File Access
- **Read Access**: Configuration files
- **Write Access**: Configuration files and backups
- **No Network**: No external connections
- **Local Storage**: All data stored locally

### Permission Requirements
- **Administrator**: Required for config file modification
- **File System**: Read/write access to game directories
- **Registry**: No registry modifications

## 📈 Performance Considerations

### Memory Usage
- **Base Application**: ~50 MB
- **Config Loading**: ~10 MB for large configs
- **UI Components**: ~20 MB for all tabs
- **Total**: ~80 MB typical usage

### File I/O
- **Config Reading**: ~100ms for typical config
- **Config Writing**: ~200ms with backup creation
- **Backup Operations**: ~50ms per backup

### UI Responsiveness
- **Async Operations**: Non-blocking file operations
- **Progress Indicators**: User feedback for long operations
- **Error Handling**: Graceful failure recovery

## 🔮 Future Architecture Considerations

### Potential Improvements
- **Plugin System**: Extensible architecture for new features
- **Cloud Sync**: Optional cloud backup integration
- **Multi-Game Support**: Support for other Battlefield games
- **API Integration**: Official EA API integration

### Scalability
- **Modular Design**: Easy to add new features
- **Plugin Architecture**: Extensible without core changes
- **Configuration System**: Flexible settings management
- **Testing Framework**: Comprehensive test coverage

---

**Last Updated**: October 24, 2025
**Version**: 1.0.0
