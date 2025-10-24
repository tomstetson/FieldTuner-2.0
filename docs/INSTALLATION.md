# FieldTuner Installation Guide

## 🚀 Quick Installation

### **Portable Version (Recommended)**

1. **Download** the latest release from [GitHub Releases](https://github.com/tomstetson/FieldTuner/releases)
2. **Download** `FieldTuner-V1.0.exe` (~42MB)
3. **Right-click** → "Run as administrator"
4. **Start** configuring your Battlefield 6 settings!

> **Note**: No installation required! The executable is completely portable.

## 📋 System Requirements

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

## 🔧 Installation Methods

### **Method 1: Portable Executable (Recommended)**

1. **Download** from [GitHub Releases](https://github.com/tomstetson/FieldTuner/releases)
2. **Save** `FieldTuner-V1.0.exe` to your desired location
3. **Right-click** the executable
4. **Select** "Run as administrator"
5. **Start** using FieldTuner!

**Advantages:**
- ✅ No installation required
- ✅ Portable - runs from any location
- ✅ No dependencies needed
- ✅ Easy to update

### **Method 2: From Source Code**

#### **Prerequisites**
- Python 3.11 or higher
- Git (optional, for cloning)

#### **Installation Steps**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tomstetson/FieldTuner.git
   cd FieldTuner
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python src/main.py
   ```

**Advantages:**
- ✅ Latest development version
- ✅ Can modify source code
- ✅ Development features available

## 🎮 First-Time Setup

### **Before Running FieldTuner**

1. **Install Battlefield 6** (if not already installed)
2. **Run Battlefield 6** at least once to create config files
3. **Ensure** you have administrator privileges

### **Config File Detection**

FieldTuner automatically detects config files in:
- `%USERPROFILE%\Documents\Battlefield 6\settings\steam\PROFSAVE_profile`
- `%USERPROFILE%\Documents\Battlefield 6\settings\PROFSAVE_profile`
- `%USERPROFILE%\OneDrive\Documents\Battlefield 6\settings\steam\PROFSAVE_profile`

### **First Launch**

1. **Run** FieldTuner as administrator
2. **Wait** for config file detection
3. **Select** your preferred preset
4. **Apply** changes to save settings

## 📁 File Locations

### **Application Files**
- **Executable**: Wherever you saved `FieldTuner-V1.0.exe`
- **Source Code**: `FieldTuner/src/main.py` (if running from source)

### **Data Storage**
- **Backups**: `%APPDATA%\FieldTuner\backups\`
- **Logs**: `%APPDATA%\FieldTuner\logs\`
- **Settings**: Portable data storage

### **Battlefield 6 Config Files**
- **Steam**: `%USERPROFILE%\Documents\Battlefield 6\settings\steam\PROFSAVE_profile`
- **EA App**: `%USERPROFILE%\Documents\Battlefield 6\settings\PROFSAVE_profile`
- **OneDrive**: `%USERPROFILE%\OneDrive\Documents\Battlefield 6\settings\steam\PROFSAVE_profile`

## 🆘 Troubleshooting

### **Common Installation Issues**

#### "Config file not found"
- ✅ Make sure Battlefield 6 is installed
- ✅ Run the game at least once to create config files
- ✅ Check that config files exist in your Documents folder

#### "Permission denied"
- ✅ Run FieldTuner as administrator
- ✅ Ensure you have administrator privileges
- ✅ Check Windows User Account Control (UAC) settings

#### "Application won't start"
- ✅ Check Windows version compatibility
- ✅ Use the portable executable version
- ✅ Check antivirus software isn't blocking the executable
- ✅ Try running from a different location

#### "Python not found" (Source installation)
- ✅ Install Python 3.11 or higher
- ✅ Add Python to your system PATH
- ✅ Use `python3` instead of `python` if needed

### **Debug Mode**

1. Open the **Debug** tab in FieldTuner
2. Check the real-time logs for error messages
3. Look for specific error patterns
4. Report issues with log details

## 🔄 Updates

### **Portable Version**
1. **Download** the latest release
2. **Replace** the old executable
3. **Run** the new version

### **Source Version**
1. **Pull** the latest changes:
   ```bash
   git pull origin main
   ```
2. **Update** dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run** the updated version

## 🗑️ Uninstallation

### **Portable Version**
- **Delete** the executable file
- **Delete** data folders (optional):
  - `%APPDATA%\FieldTuner\`

### **Source Version**
- **Delete** the project folder
- **Uninstall** Python dependencies (optional):
  ```bash
  pip uninstall PyQt6
  ```

## 📞 Support

If you encounter issues during installation:

1. **Check** the [Troubleshooting](#troubleshooting) section
2. **Review** the [Debug Mode](#debug-mode) logs
3. **Create** an issue on [GitHub](https://github.com/tomstetson/FieldTuner/issues)
4. **Include** your system information and error logs

---

**FieldTuner Installation Guide** - Getting you up and running quickly! 🚀

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/tomstetson/FieldTuner)
[![Download](https://img.shields.io/badge/Download-Latest-green.svg)](https://github.com/tomstetson/FieldTuner/releases)
