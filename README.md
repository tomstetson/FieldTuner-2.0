# FieldTuner V2.0 - Battlefield 6 Configuration Tool

<div align="center">

![FieldTuner Logo](assets/scaled_icon.png)

**A professional-grade configuration tool for Battlefield 6 with an intuitive interface and powerful features.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.5+-green.svg)](https://pypi.org/project/PyQt6/)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-blue.svg)](https://www.microsoft.com/windows)
[![Release](https://img.shields.io/badge/Release-V2.0-green.svg)](https://github.com/sneakytom/FieldTuner/releases)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](https://github.com/sneakytom/FieldTuner/actions)
[![Code Quality](https://img.shields.io/badge/Code%20Quality-A%2B-brightgreen.svg)](https://github.com/sneakytom/FieldTuner)

</div>

## 🎯 Overview

FieldTuner is a comprehensive configuration tool designed specifically for Battlefield 6. It provides an intuitive, WeMod-inspired interface for managing all aspects of your game settings, from graphics optimization to advanced technical configurations.

### ✨ Key Features

- 🎮 **Enhanced Config Detection** - Auto-detect + manual profile selection
- ⚡ **Optimized Quick Settings** - 3 performance presets with modern UI
- 🖥️ **Modular Graphics Management** - Separate tab for graphics settings
- 💾 **Bulletproof Backup System** - Enhanced backup with validation
- 🔧 **Advanced Settings** - Technical settings with search and favorites
- 🐛 **Real-time Debug Tools** - Comprehensive logging and troubleshooting
- 🚀 **Portable Design** - No installation required, runs anywhere
- ⚙️ **User Preferences** - Customizable application settings
- ⭐ **Favorites System** - Save and manage favorite settings
- 🎯 **Profile Selector** - Manual profile selection when auto-detect fails

## 🚀 Quick Start

### 📦 **Download & Run (Recommended)**

1. **Download** the latest release from [Releases](https://github.com/sneakytom/FieldTuner/releases)
2. **Download** `FieldTuner-2.0.exe` (~45MB)
3. **Right-click** → "Run as administrator"
4. **Start** configuring your Battlefield 6 settings!

> **Note**: No installation required! The executable is completely portable.

### 🔧 **From Source Code**

```bash
# Clone the repository
git clone https://github.com/sneakytom/FieldTuner.git
cd FieldTuner

# Install dependencies
pip install PyQt6

# Run the application
python src/main.py
```

## 🎮 Quick Settings Presets

| Preset | Description | Use Case |
|--------|-------------|----------|
| **Esports Pro** | Maximum performance for competitive play | Professional gaming, tournaments |
| **Competitive** | Balanced performance and quality | Ranked matches, competitive play |
| **Balanced** | Good performance with decent quality | Casual gaming, mixed use |
| **Quality** | High quality settings | Single-player, cinematic experience |
| **Performance** | Maximum performance settings | Low-end hardware, high FPS |

## 🛡️ Safety & Reliability

- ✅ **Automatic Backups** - Creates backups before any changes
- ✅ **Confirmation Dialogs** - Prevents accidental modifications
- ✅ **Error Recovery** - Robust error handling and recovery
- ✅ **Comprehensive Logging** - Detailed logs for troubleshooting
- ✅ **Admin Privileges** - Secure file modification with proper permissions

## 📁 Project Structure

```
FieldTuner/
├── 📁 src/                          # Main source code
│   ├── main.py                      # Core application (4,300+ lines)
│   ├── settings_database.py         # BF6 settings database
│   └── debug.py                     # Debug utilities
├── 📁 assets/                       # Application assets
│   ├── icon.ico                     # Application icon
│   ├── logo.png                     # Professional logo
│   └── scaled_icon.png              # GitHub logo
├── 📁 docs/                         # Documentation
├── 📁 tests/                        # Test suite
├── 📁 dist/                         # Built executables
├── 📁 releases/                     # Release packages
├── 📄 build.py                      # Build script
├── 📄 pyproject.toml                # Project configuration
└── 📄 README.md                     # This file
```

## 🔧 System Requirements

### **Minimum Requirements**
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB minimum
- **Storage**: 50MB free space
- **Battlefield 6**: Must be installed and run at least once

### **Recommended Requirements**
- **OS**: Windows 11 (64-bit)
- **RAM**: 8GB or more
- **Storage**: 100MB free space
- **Battlefield 6**: Latest version

## 📍 Config File Locations

FieldTuner automatically detects config files in:
- `%USERPROFILE%\Documents\Battlefield 6\settings\steam\PROFSAVE_profile`
- `%USERPROFILE%\Documents\Battlefield 6\settings\PROFSAVE_profile`
- `%USERPROFILE%\OneDrive\Documents\Battlefield 6\settings\steam\PROFSAVE_profile`

## 💾 Data Storage

- **Backups**: `%APPDATA%\FieldTuner\backups\`
- **Logs**: `%APPDATA%\FieldTuner\logs\`
- **Settings**: Portable data storage

## 🆘 Troubleshooting

### **Common Issues**

#### "Config file not found"
- ✅ Make sure Battlefield 6 is installed
- ✅ Run the game at least once to create config files
- ✅ Check that config files exist in your Documents folder

#### "Permission denied"
- ✅ Run FieldTuner as administrator
- ✅ Ensure you have administrator privileges

#### "Application won't start"
- ✅ Check Windows version compatibility
- ✅ Use the portable executable version
- ✅ Check antivirus software isn't blocking the executable

### **Debug Mode**
1. Open the **Debug** tab in FieldTuner
2. Check the real-time logs for error messages
3. Look for specific error patterns
4. Report issues with log details

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Setup**
```bash
# Clone the repository
git clone https://github.com/sneakytom/FieldTuner.git
cd FieldTuner

# Install dependencies
pip install PyQt6

# Run the application
python src/main.py

# Run tests
python -m pytest tests/ -v
```

## 📚 Documentation

- 📖 **[Installation Guide](docs/README.md)** - Detailed setup instructions
- 🧪 **[Testing Guide](docs/TESTING_LOG_SYSTEM.md)** - Testing and debugging
- 🏗️ **[Project Structure](PROJECT_STRUCTURE.md)** - Code organization
- 🤝 **[Contributing](CONTRIBUTING.md)** - How to contribute

## 🏆 Project Status

- ✅ **Core Features** - Complete and tested
- ✅ **UI/UX** - Professional, WeMod-inspired design
- ✅ **Backup System** - Robust backup and restore functionality
- ✅ **Portable Build** - Self-contained executable ready
- ✅ **Documentation** - Comprehensive guides
- ✅ **Testing** - Test coverage with automated testing
- 🔄 **V2.0** - Initial release available

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Nobody621** - For the original idea
- **PyQt6** - For the excellent GUI framework
- **Python Community** - For the amazing ecosystem
- **Cursor** - For the incredible AI-powered development experience

---

<div align="center">

**Made with Love by SneakyTom** ❤️

*Making Battlefield 6 configuration as smooth as butter*

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/tomstetson/FieldTuner)
[![Download](https://img.shields.io/badge/Download-Latest-green.svg)](https://github.com/tomstetson/FieldTuner/releases)

</div>