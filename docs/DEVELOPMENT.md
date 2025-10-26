# FieldTuner 2.0 - Development Environment Guide

This guide explains how to set up an isolated development environment for FieldTuner 2.0 that won't interfere with other projects.

## Why Isolation is Important

- **Prevents Dependency Conflicts**: Different projects may use different versions of the same library
- **Avoids Cross-Project Issues**: Force-closing FieldTuner won't affect other projects
- **Clean Testing Environment**: Each project has its own test data and configurations
- **Easy Cleanup**: Can remove the entire environment without affecting other projects
- **Professional Best Practice**: Standard practice in Python development

## Setup Process

### 1. Create Virtual Environment

Run the setup script:

```powershell
.\setup-venv.ps1
```

This will:
- Create a `venv` folder with isolated Python installation
- Install all required dependencies
- Set up the development environment

### 2. Activate Virtual Environment

Before working on FieldTuner 2.0, activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

You'll see `(venv)` in your command prompt, indicating the environment is active.

### 3. Run the Application

```powershell
python src/main.py
```

### 4. Deactivate When Done

```powershell
deactivate
```

## Directory Structure

```
FieldTuner 2.0/
├── venv/                    # Virtual environment (isolated)
├── src/                      # Source code
├── tests/                    # Test files
├── docs/                     # Documentation
├── FT_2.0_BF6_Profile/       # Test BF6 profile
└── requirements.txt          # Python dependencies
```

## Isolation Strategy

### 1. Python Virtual Environment

The `venv` folder contains:
- Isolated Python interpreter
- Only FieldTuner 2.0 dependencies
- Completely separate from system Python and other projects

### 2. Isolated AppData Directory

FieldTuner 2.0 uses its own AppData subdirectory:
```
%APPDATA%/FieldTuner/
├── logs/         # FieldTuner logs only
├── backups/      # BF6 config backups
├── favorites.json
├── preferences.json
└── app_state.json
```

### 3. Project-Specific Test Data

- Test BF6 profile in `FT_2.0_BF6_Profile/`
- Test fixtures in `tests/fixtures/`
- Separated from other projects' test data

## Daily Workflow

### Starting Development Session

1. Open PowerShell in FieldTuner 2.0 directory
2. Activate virtual environment: `.\venv\Scripts\Activate.ps1`
3. Work on your code
4. Run tests: `pytest`
5. Test application: `python src/main.py`

### Ending Development Session

1. Save all work
2. Deactivate: `deactivate`
3. Close terminal

## Building the Executable

The virtual environment is for development only. To build the portable executable:

```powershell
.\build.py
```

This creates a standalone `FieldTuner.exe` in the `dist/` folder that:
- Contains all dependencies
- Can run on any Windows machine
- Is completely independent of the development environment

## Troubleshooting

### Virtual Environment Not Activating

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Dependencies Out of Date

Update dependencies:
```powershell
.\venv\Scripts\Activate.ps1
pip install --upgrade -r requirements.txt
```

### Rebuilding Virtual Environment

If something goes wrong:
```powershell
Remove-Item -Recurse -Force venv
.\setup-venv.ps1
```

## Best Practices

### ✅ DO:
- Always activate venv before development
- Deactivate when switching to other projects
- Commit `requirements.txt` to version control
- Never commit `venv/` folder (already in .gitignore)
- Use `requirements.txt` for all dependencies

### ❌ DON'T:
- Install global packages that are in requirements.txt
- Share venv folders between projects
- Edit files in venv/ directly
- Commit venv/ to git (it's in .gitignore)

## Testing Isolation

To verify isolation is working:

1. **Check Python Location:**
   ```powershell
   which python  # Should point to venv\Scripts\python.exe
   ```

2. **Check Installed Packages:**
   ```powershell
   pip list  # Should only show FieldTuner dependencies
   ```

3. **Check AppData:**
   ```powershell
   ls $env:APPDATA\FieldTuner  # Should only contain FieldTuner files
   ```

## Multiple Projects

When working on multiple projects simultaneously:

- **Each project gets its own venv**: `ProjectA/venv`, `ProjectB/venv`
- **Each project uses its own AppData subdirectory**: FieldTuner, ProjectB, etc.
- **Activate the correct venv for each project**
- **No conflicts or interference between projects**

## CI/CD Integration

The isolated environment makes CI/CD easy:
- CI runner creates fresh venv from requirements.txt
- No dependency conflicts
- Clean builds every time
- GitHub Actions works perfectly

