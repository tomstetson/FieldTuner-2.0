# FieldTuner Project Structure

## 🎯 Clean, Concise Project Organization

This document outlines the clean, organized structure of the FieldTuner project - a professional, self-contained Battlefield 6 configuration tool.

## 📁 Project Structure

```
FieldTuner/
├── 📁 src/                          # Main source code
│   ├── main.py                      # Core application (MainWindow, all tabs)
│   ├── settings_database.py         # BF6 settings database
│   └── debug.py                     # Debug utilities
│
├── 📁 assets/                       # Application assets
│   ├── icon.ico                     # Main application icon
│   ├── logo.png                     # Professional logo
│   ├── banner.png                   # GitHub banner
│   ├── icon_*.png                   # Various icon sizes
│   ├── create_icon.py               # Icon generation script
│   ├── create_professional_logo.py  # Logo generation script
│   └── screenshots/                 # Screenshots for documentation
│
├── 📁 docs/                         # Documentation
│   └── README.md                    # Documentation index
│
├── 📁 tests/                        # Test suite
│   ├── test_config_manager.py       # Config manager tests
│   ├── test_ui_components.py       # UI component tests
│   └── fixtures/                    # Test fixtures
│
├── 📁 installer/                    # Installation system
│   ├── create_installer.py          # Main installer creator
│   ├── create_installer_package.py  # Package creator
│   ├── install_fieldtuner.py       # Python installer
│   └── install.bat                 # Batch installer
│
├── 📁 releases/                     # Release packages
│   ├── FieldTuner_Installer_v1.0/  # Installer package
│   ├── FieldTuner_Portable_v1.0/    # Portable package
│   ├── FieldTuner_v1.0_20251024/   # Standard package
│   └── *.zip                       # Release archives
│
├── 📄 README.md                     # Main project README
├── 📄 LICENSE                       # MIT License
├── 📄 pyproject.toml                # Modern Python project config
├── 📄 setup.py                      # Package setup
├── 📄 requirements.txt              # Dependencies
├── 📄 requirements-dev.txt         # Development dependencies
├── 📄 FieldTuner.spec              # PyInstaller spec
├── 📄 build_simple.py              # Simple build script
├── 📄 build_portable.bat            # Portable build script
├── 📄 build.bat                     # Main build script
├── 📄 create_release.py             # Release creation script
├── 📄 CODE_OF_CONDUCT.md            # Code of conduct
├── 📄 CONTRIBUTING.md               # Contribution guidelines
└── 📄 PROJECT_STRUCTURE.md          # This file
```

## 🎯 Key Improvements

### ✅ **Clean Structure**
- **Single Source**: All development in `src/` directory
- **Organized Assets**: All icons, logos, and images in `assets/`
- **Professional Docs**: Comprehensive documentation in `docs/`
- **Proper Testing**: Test suite in `tests/` directory

### ✅ **Removed Legacy Files**
- ❌ Old `main.py` files scattered around
- ❌ Duplicate `build.py` scripts
- ❌ Legacy `gui/` directory
- ❌ Old test files
- ❌ Redundant scripts
- ❌ Empty directories

### ✅ **Best Practices**
- **Modern Python**: Uses `pyproject.toml` for configuration
- **Proper Packaging**: Clean `setup.py` and requirements
- **Version Control**: Git-ready with proper `.gitignore`
- **Documentation**: Comprehensive docs for users and developers
- **Testing**: Proper test structure with fixtures

## 🚀 Development Workflow

### **Main Development**
- **Source Code**: `src/main.py` - Core application
- **Settings**: `src/settings_database.py` - BF6 settings
- **Assets**: `assets/` - Icons, logos, images

### **Building**
- **Simple Build**: `python build_simple.py`
- **Portable Build**: `build_portable.bat`
- **Full Build**: `build.bat`

### **Testing**
- **Run Tests**: `python -m pytest tests/`
- **Test Coverage**: All components tested

### **Releases**
- **Create Release**: `python create_release.py`
- **Release Packages**: `releases/` directory

## 📊 Project Statistics

- **Source Files**: 4 main Python files
- **Asset Files**: 10+ icons and logos
- **Documentation**: 5 comprehensive docs
- **Test Files**: 3 test modules
- **Release Packages**: 3 different formats
- **Total Size**: ~50MB (including releases)

## 🎉 Result

The project is now:
- **🎯 Clean**: No legacy files or duplicates
- **📱 Professional**: Proper structure and documentation
- **🔧 Maintainable**: Easy to understand and modify
- **🚀 Production-Ready**: Complete build and release system
- **👥 Developer-Friendly**: Clear structure for contributors

**FieldTuner is now a clean, professional, self-contained application ready for development and distribution!** 🎉