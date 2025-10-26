# FieldTuner 2.0 - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Download
Download `FieldTuner-2.0.exe` from the [latest release](https://github.com/tomstetson/FieldTuner-2.0/releases).

### Step 2: Run
Right-click the file → **"Run as administrator"**

### Step 3: Apply a Preset
Choose a preset from the Quick Settings tab and click **"Apply Preset"**

> ✅ **That's it!** Your Battlefield 6 settings are now optimized.

---

## 🎮 Quick Reference

### For Different Gaming Goals

**Want maximum FPS?**
→ Use **"Performance"** preset

**Competitive player?**
→ Use **"Competitive"** or **"Esports Pro"** preset

**Want beautiful graphics?**
→ Use **"Quality"** preset

**Balanced experience?**
→ Use **"Balanced"** preset

### Common Actions

| What you want to do | Where to go |
|---------------------|-------------|
| Apply a preset | Quick Settings tab |
| Fine-tune graphics | Graphics tab |
| Adjust mouse sensitivity | Input tab |
| Restore old settings | Backup tab |
| See system info | BF6 Features tab |
| View raw config | Code View tab |
| Troubleshoot issues | Debug tab |

---

## ⚙️ Important Notes

### Before Using FieldTuner
- ✅ **Battlefield 6 must be installed**
- ✅ **Run Battlefield 6 once** to create config files
- ✅ **Close Battlefield 6** before making changes

### Safety Features
- 🔒 **Automatic backups** are created before any changes
- 🔒 **Confirmation dialogs** prevent accidents
- 🔒 **Easy restore** from the Backup tab

### After Applying Settings
- 🔄 **Restart Battlefield 6** to see changes
- ✅ **Test in-game** to make sure settings work
- 💾 **Keep backups** until you're satisfied

---

## 🆘 Having Issues?

### Config File Not Found
- Run Battlefield 6 at least once
- Check your Documents folder

### Permission Denied
- Run FieldTuner as administrator
- Right-click → "Run as administrator"

### Settings Not Working
- Close Battlefield 6 before making changes
- Apply settings in FieldTuner
- Restart Battlefield 6

### Need More Help?
- 📖 Read the [Full User Guide](USER_GUIDE.md)
- 🐛 Check the [Debug Tab](USER_GUIDE.md#debug-tab)
- 📞 [Report an Issue](https://github.com/tomstetson/FieldTuner-2.0/issues)

---

## 🎯 Advanced Users

### From Source Code

```bash
# Clone the repository
git clone https://github.com/tomstetson/FieldTuner-2.0.git
cd FieldTuner-2.0

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main_v2.py
```

### Build Your Own Executable

```bash
# Activate virtual environment
venv\Scripts\activate

# Install PyInstaller
pip install pyinstaller

# Build executable
python build.py
```

---

**Made with Love by SneakyTom** ❤️

For more detailed information, see the [Full User Guide](USER_GUIDE.md).
