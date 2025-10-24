# FieldTuner Project Structure

This document outlines the complete project structure and organization of FieldTuner.

## 📁 Directory Structure

```
FieldTuner/
├── .github/                          # GitHub workflows and templates
│   ├── workflows/
│   │   ├── build.yml                 # CI/CD build workflow
│   │   └── release.yml               # Release workflow
│   └── ISSUE_TEMPLATE/               # Issue templates
├── docs/                             # Documentation
│   ├── README.md                     # Documentation index
│   ├── installation.md               # Installation guide
│   ├── architecture.md               # System architecture
│   ├── user-guide.md                 # User manual
│   ├── api-reference.md              # API documentation
│   └── troubleshooting.md            # Troubleshooting guide
├── src/                              # Source code
│   ├── main.py                       # Main application entry point
│   ├── config_manager.py             # Configuration management
│   ├── ui_components.py               # UI components
│   └── utils.py                      # Utility functions
├── tests/                            # Test suite
│   ├── __init__.py                   # Test package init
│   ├── test_config_manager.py        # ConfigManager tests
│   ├── test_ui_components.py         # UI component tests
│   ├── test_integration.py           # Integration tests
│   └── fixtures/                     # Test data and fixtures
├── build/                            # Build scripts and tools
│   ├── build_portable.py             # Portable executable builder
│   ├── build_simple.py               # Simple build script
│   └── create_release.py              # Release package creator
├── releases/                         # Release packages
│   ├── FieldTuner_Portable_v1.0/     # Portable release
│   └── FieldTuner_v1.0_YYYYMMDD.zip  # Release ZIP packages
├── assets/                           # Static assets
│   ├── icon.ico                      # Application icon
│   ├── logo.png                      # Logo image
│   └── screenshots/                  # Screenshots for documentation
├── .github/                          # GitHub configuration
├── .pre-commit-config.yaml           # Pre-commit hooks
├── .gitignore                        # Git ignore rules
├── .gitattributes                    # Git attributes
├── pyproject.toml                    # Python project configuration
├── requirements.txt                  # Production dependencies
├── requirements-dev.txt              # Development dependencies
├── setup.py                          # Package setup
├── README.md                         # Main project README
├── CONTRIBUTING.md                   # Contributing guidelines
├── CODE_OF_CONDUCT.md                # Code of conduct
├── LICENSE                           # MIT License
├── CHANGELOG.md                      # Changelog
└── PROJECT_STRUCTURE.md              # This file
```

## 🏗️ Architecture Overview

### Core Components

#### 1. Main Application (`src/main.py`)
- **Purpose**: Main application entry point and window management
- **Responsibilities**:
  - Application initialization
  - Window creation and management
  - Tab coordination
  - Event handling

#### 2. Configuration Manager (`src/config_manager.py`)
- **Purpose**: Battlefield 6 configuration file management
- **Responsibilities**:
  - Config file detection and parsing
  - Settings modification and validation
  - Backup creation and management
  - Binary format handling

#### 3. UI Components (`src/ui_components.py`)
- **Purpose**: Reusable UI components and widgets
- **Responsibilities**:
  - Custom toggle switches
  - Professional styling
  - Component behavior
  - Event handling

#### 4. Utilities (`src/utils.py`)
- **Purpose**: Common utility functions
- **Responsibilities**:
  - File operations
  - Data validation
  - Helper functions
  - Error handling

### UI Architecture

#### Tab-Based Interface
- **QuickSettingsTab**: Preset management and quick configuration
- **GraphicsTab**: Graphics settings management
- **BackupTab**: Backup creation, restoration, and management
- **CodeViewTab**: Raw config file viewing and editing
- **DebugTab**: Logging and troubleshooting

#### Component Design
- **Professional Toggle Switches**: WeMod-inspired design
- **Responsive Layout**: Scales properly on different screen sizes
- **Consistent Styling**: Unified color scheme and typography
- **Accessibility**: High contrast and readable fonts

## 🧪 Testing Strategy

### Test Organization
```
tests/
├── test_config_manager.py            # ConfigManager unit tests
├── test_ui_components.py             # UI component tests
├── test_integration.py               # Integration tests
├── test_end_to_end.py                # End-to-end tests
└── fixtures/                         # Test data
    ├── sample_config.bin             # Sample config files
    ├── test_backups/                 # Test backup files
    └── mock_data.json                # Mock data
```

### Testing Levels
1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Component interaction testing
3. **UI Tests**: User interface testing with pytest-qt
4. **End-to-End Tests**: Complete workflow testing

## 🔧 Build System

### Build Scripts
- **`build_simple.py`**: Simple build script for development
- **`build_portable.py`**: Comprehensive build with all features
- **`create_release.py`**: Release package creation

### Build Process
1. **Dependency Installation**: Install PyInstaller and dependencies
2. **Source Compilation**: Compile Python source to bytecode
3. **Dependency Bundling**: Bundle all dependencies into executable
4. **Executable Creation**: Create self-contained .exe file
5. **Package Creation**: Create release package with documentation

### Release Process
1. **Version Tagging**: Create version tags
2. **Automated Build**: GitHub Actions build process
3. **Testing**: Automated test execution
4. **Package Creation**: Create release packages
5. **Distribution**: Upload to GitHub Releases

## 📚 Documentation Structure

### User Documentation
- **Installation Guide**: Step-by-step installation instructions
- **User Guide**: Complete user manual with screenshots
- **FAQ**: Frequently asked questions and answers
- **Troubleshooting**: Common issues and solutions

### Developer Documentation
- **Architecture**: System architecture and design decisions
- **API Reference**: Complete API documentation
- **Contributing**: Guidelines for contributing to the project
- **Testing**: Testing guidelines and procedures

### Technical Documentation
- **Configuration**: Configuration options and settings
- **Build System**: How to build and deploy the project
- **Security**: Security considerations and best practices

## 🚀 Deployment Strategy

### Release Types
1. **Portable Executable**: Self-contained .exe file
2. **Source Code**: Python source with requirements
3. **Development Build**: Development version with debug features

### Distribution Channels
- **GitHub Releases**: Primary distribution channel
- **GitHub Packages**: Package registry (future)
- **Direct Download**: From project website (future)

## 🔒 Security Considerations

### File Access
- **Read Access**: Configuration files only
- **Write Access**: Configuration files and backups only
- **No Network**: No external network connections
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

## 🔮 Future Considerations

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
