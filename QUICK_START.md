# FieldTuner 2.0 - Quick Start Guide

## First Time Setup

```powershell
# 1. Create virtual environment
.\setup-venv.ps1

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Run the application
python src/main.py
```

## Daily Development

### Start Work Session
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### Run Application
```powershell
python src/main.py
```

### Run Tests
```powershell
pytest
```

### Build Executable
```powershell
# Build standalone .exe
.\build.py
```

### End Work Session
```powershell
# Deactivate virtual environment
deactivate
```

## Important Notes

- ✅ **Always activate venv before development**
- ✅ **venv/ is isolated from other projects**
- ✅ **AppData is separated per project**
- ✅ **Force-closing won't affect other projects**
- ✅ **venv/ is NOT committed to git**

## Troubleshooting

### Virtual environment won't activate
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Need to reinstall dependencies
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Project Structure

```
FieldTuner 2.0/
├── venv/              # ← Virtual environment (isolated, not in git)
├── src/               # ← Source code
├── tests/             # ← Tests
├── docs/              # ← Documentation
└── requirements.txt   # ← Dependencies
```

## Benefits

- 🎯 **Isolated**: No conflicts with other projects
- 🔒 **Safe**: Force-closing won't affect other projects  
- 🧹 **Clean**: Can delete venv/ anytime
- 📦 **Portable**: Works anywhere Python is installed
- 🚀 **Professional**: Industry best practice

