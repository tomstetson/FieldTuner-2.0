# Installation Guide

This guide covers how to install and set up FieldTuner on your system.

## 📋 System Requirements

### Minimum Requirements
- **Operating System**: Windows 10 (64-bit) or Windows 11
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 100 MB free space
- **Permissions**: Administrator privileges required
- **Game**: Battlefield 6 (Steam or Origin version)

### Recommended Requirements
- **Operating System**: Windows 11 (64-bit)
- **RAM**: 16 GB or more
- **Storage**: 1 GB free space
- **CPU**: Modern multi-core processor
- **Graphics**: DirectX 12 compatible graphics card

## 🚀 Installation Methods

### Method 1: Portable Executable (Recommended)

#### Download
1. Go to the [Releases](https://github.com/tomstetson/fieldtuner/releases) page
2. Download the latest `FieldTuner_v1.0_YYYYMMDD.zip` file
3. Extract the ZIP file to any folder on your system

#### Installation
1. Navigate to the extracted folder
2. Right-click `Run_FieldTuner.bat`
3. Select "Run as administrator"
4. FieldTuner will start automatically

#### Advantages
- No installation required
- No registry modifications
- Easy to uninstall (just delete the folder)
- Portable across different systems

### Method 2: From Source Code

#### Prerequisites
- Python 3.11 or higher
- Git
- pip package manager

#### Installation Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/tomstetson/fieldtuner.git
   cd fieldtuner
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python src/main.py
   ```

#### Development Setup
For development work, also install:
```bash
pip install -r requirements-dev.txt
```

## 🔧 Configuration

### First Run Setup
1. **Launch FieldTuner** as administrator
2. **Automatic Detection**: FieldTuner will automatically find your Battlefield 6 config file
3. **Backup Creation**: A backup of your current settings will be created automatically
4. **Ready to Use**: You can start configuring your settings immediately

### Config File Locations
FieldTuner automatically detects config files in these locations:
- `%USERPROFILE%\Documents\Battlefield 6\settings\steam\PROFSAVE_profile`
- `%USERPROFILE%\Documents\Battlefield 6\settings\PROFSAVE_profile`
- `%USERPROFILE%\OneDrive\Documents\Battlefield 6\settings\steam\PROFSAVE_profile`

### Data Storage Locations
- **Backups**: `%APPDATA%\FieldTuner\backups\`
- **Logs**: `%APPDATA%\FieldTuner\logs\`
- **Settings**: Stored with the application (portable mode)

## ⚠️ Important Notes

### Administrator Privileges
- FieldTuner requires administrator privileges to modify game configuration files
- Windows will prompt for permission when needed
- This is necessary for the tool to function properly

### Game Requirements
- Battlefield 6 must be installed on your system
- Run the game at least once to create configuration files
- Close the game before using FieldTuner

### Security Considerations
- FieldTuner only modifies Battlefield 6 configuration files
- No network connections are made
- All data is stored locally on your system
- Source code is available for review

## 🛠️ Troubleshooting

### Common Issues

#### "Config file not found"
- **Solution**: Make sure Battlefield 6 is installed and you've run it at least once
- **Check**: Verify the config file exists in your Documents folder
- **Alternative**: Use the manual config selection option

#### "Permission denied"
- **Solution**: Run FieldTuner as administrator
- **Check**: Ensure you have administrator privileges
- **Alternative**: Use the batch file launcher

#### "Application won't start"
- **Solution**: Check that all dependencies are installed
- **Check**: Verify Python version (3.11+)
- **Alternative**: Use the portable executable version

### Advanced Troubleshooting

#### Debug Mode
1. Open the Debug tab in FieldTuner
2. Check the real-time logs for error messages
3. Look for specific error patterns
4. Report issues with log details

#### Manual Config Selection
1. Go to Settings tab
2. Click "Select Config File Manually"
3. Navigate to your Battlefield 6 config file
4. Select the `PROFSAVE_profile` file

#### Reset to Defaults
1. Go to the Quick Settings tab
2. Click "Reset to Factory"
3. Confirm the reset operation
4. Your settings will be restored to Battlefield 6 defaults

## 🔄 Updates

### Automatic Updates
- FieldTuner checks for updates on startup
- Update notifications appear in the interface
- Download updates from the releases page

### Manual Updates
1. Download the latest release
2. Extract to a new folder
3. Copy your backup files if needed
4. Run the new version

### Backup Before Updates
- Always backup your settings before updating
- FieldTuner creates automatic backups
- Manual backups are recommended for major updates

## 🗑️ Uninstallation

### Portable Version
1. Close FieldTuner if running
2. Delete the FieldTuner folder
3. Optionally delete backup files in `%APPDATA%\FieldTuner\`

### Source Version
1. Close FieldTuner if running
2. Delete the source code folder
3. Uninstall Python dependencies if not needed elsewhere
4. Optionally delete backup files in `%APPDATA%\FieldTuner\`

## 📞 Support

### Getting Help
- **GitHub Issues**: For bug reports and technical issues
- **GitHub Discussions**: For questions and general help
- **Documentation**: Check this guide and other documentation

### Reporting Issues
When reporting installation issues, include:
- Operating system and version
- Python version (if using source)
- Error messages
- Steps to reproduce the issue
- Screenshots if applicable

---

**Last Updated**: October 24, 2025
**Version**: 1.0.0
