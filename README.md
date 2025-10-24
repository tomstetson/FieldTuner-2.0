# FieldTuner - Battlefield 6 Configuration Tool

<div align="center">

![FieldTuner Logo](assets/icon.ico)

**A comprehensive, world-class tool for managing Battlefield 6 settings with an intuitive interface and powerful features.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.5+-green.svg)](https://pypi.org/project/PyQt6/)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-blue.svg)](https://www.microsoft.com/windows)

</div>

## 🎯 Overview

FieldTuner is a professional-grade configuration tool designed specifically for Battlefield 6. It provides an intuitive, WeMod-inspired interface for managing all aspects of your game settings, from graphics optimization to advanced technical configurations.

### ✨ Key Features

- 🎮 **Automatic Config Detection** - Finds your BF6 config files automatically
- ⚡ **Quick Settings Presets** - 5 optimized presets for different playstyles
- 🖥️ **Graphics Management** - Comprehensive graphics settings control
- 💾 **Smart Backup System** - Automatic backups with easy restoration
- 🔧 **Advanced Settings** - Technical settings with user-friendly descriptions
- 🐛 **Debug Tools** - Real-time logging and troubleshooting
- 🚀 **Portable Design** - No installation required, runs anywhere

## 🚀 Quick Start

### 📦 Portable Version (Recommended)

1. **Download** the latest release from [Releases](https://github.com/tomstetson/fieldtuner/releases)
2. **Extract** the ZIP file to any folder
3. **Run** `Run_FieldTuner.bat` as administrator
4. **Start** configuring your Battlefield 6 settings!

### 🔧 From Source Code

```bash
# Clone the repository
git clone https://github.com/tomstetson/fieldtuner.git
cd fieldtuner

# Install dependencies
pip install -r requirements.txt

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

### Clean Organization
```
FieldTuner/
├── 📁 src/                          # Main source code
│   ├── main.py                      # Core application
│   ├── settings_database.py         # BF6 settings database
│   └── backup_tab_clean.py          # Clean backup implementation
├── 📁 assets/                       # Application assets
├── 📁 docs/                         # Documentation
├── 📁 tests/                        # Test suite
├── 📁 installer/                    # Installation system
└── 📁 releases/                     # Release packages
```

### Config File Locations
FieldTuner automatically detects config files in:
- `%USERPROFILE%\Documents\Battlefield 6\settings\steam\PROFSAVE_profile`
- `%USERPROFILE%\Documents\Battlefield 6\settings\PROFSAVE_profile`
- `%USERPROFILE%\OneDrive\Documents\Battlefield 6\settings\steam\PROFSAVE_profile`

### Data Storage
- **Backups**: `%APPDATA%\FieldTuner\backups\`
- **Logs**: `%APPDATA%\FieldTuner\logs\`
- **Settings**: Portable data storage

## 🆘 Troubleshooting

### Common Issues

#### "Config file not found"
- ✅ Make sure Battlefield 6 is installed
- ✅ Run the game at least once to create config files
- ✅ Check that config files exist in your Documents folder

#### "Permission denied"
- ✅ Run FieldTuner as administrator
- ✅ Ensure you have administrator privileges
- ✅ Use the batch file launcher

#### "Application won't start"
- ✅ Check that all dependencies are installed
- ✅ Verify Python version (3.11+)
- ✅ Use the portable executable version

### Debug Mode
1. Open the **Debug** tab in FieldTuner
2. Check the real-time logs for error messages
3. Look for specific error patterns
4. Report issues with log details

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/tomstetson/fieldtuner.git
cd fieldtuner

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
python -m pytest tests/ -v
```

## 📚 Documentation

- 📖 **[Installation Guide](docs/installation.md)** - Detailed installation instructions
- 🏗️ **[Architecture](docs/architecture.md)** - System architecture overview
- 🧪 **[Testing](docs/testing.md)** - Testing guidelines and procedures
- 🔧 **[API Reference](docs/api-reference.md)** - Complete API documentation

## 🏆 Project Status

- ✅ **Core Features** - Complete and tested
- ✅ **UI/UX** - Professional, WeMod-inspired design
- ✅ **Backup System** - Robust backup and restore functionality
- ✅ **Portable Build** - Self-contained executable ready
- ✅ **Documentation** - Comprehensive guides and API docs
- ✅ **Testing** - Full test coverage with automated CI/CD

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Nobody621** - For the idea
- **PyQt6** - For the excellent GUI framework
- **Python Community** - For the amazing ecosystem
- **Cursor** - For the incredible AI-powered development experience

---

<div align="center">

**Created by Tom with Love from Cursor** ❤️

*Making Battlefield 6 configuration as smooth as butter*

</div>