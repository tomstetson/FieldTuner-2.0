# FieldTuner 2.0 - Development Environment Isolation

## Understanding the Isolation Layers

FieldTuner 2.0 uses a **three-layer isolation strategy** to ensure complete separation from other projects:

```
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 1: Project Root                      │
│  FieldTuner 2.0/  (isolated directory on disk)              │
│  - All source code                                            │
│  - All test data                                              │
│  - Project-specific assets                                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 2: Virtual Environment               │
│  venv/  (isolated Python environment)                        │
│  - Python interpreter                                          │
│  - Python dependencies only for FieldTuner                   │
│  - Completely separate from system Python                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 3: AppData Storage                   │
│  %APPDATA%\FieldTuner\  (isolated storage)                  │
│  - Logs, backups, preferences                                │
│  - No sharing with other applications                        │
└─────────────────────────────────────────────────────────────┘
```

## Why This Works

### 1. Project Directory Isolation
- **FieldTuner 2.0** in `F:\Vibe Projects\FieldTuner 2.0\`
- **Other Project A** in `F:\Vibe Projects\ProjectA\`
- **Other Project B** in `C:\Dev\ProjectB\`

**Result**: Complete file system separation

### 2. Virtual Environment Isolation
```
Project A:  C:\ProjectA\venv\    ← Python 3.11, Package v2.0
FieldTuner: F:\...\FieldTuner 2.0\venv\  ← Python 3.13, Package v2.5
Project B:  D:\ProjectB\venv\    ← Python 3.12, Package v1.8
```

**Result**: Different Python versions and package versions don't conflict

### 3. AppData Isolation
```
%APPDATA%/FieldTuner/      ← FieldTuner only
%APPDATA%/ProjectA/        ← Project A only  
%APPDATA%/Battlefield6/    ← Battlefield 6 only
```

**Result**: Settings, logs, and data are completely separated

## Common Scenarios

### Scenario 1: Working on Multiple Projects

**Setup**:
```
Terminal 1 (FieldTuner):
  cd "F:\Vibe Projects\FieldTuner 2.0"
  .\venv\Scripts\Activate.ps1
  python src/main.py

Terminal 2 (Project B):
  cd "C:\Dev\ProjectB"
  .\venv\Scripts\Activate.ps1
  python main.py
```

**What Happens**:
- Each terminal has its own Python interpreter
- Each project uses its own dependencies
- Both can run simultaneously without conflicts
- AppData stores are completely separate

**If You Force-Close FieldTuner**:
- Project B keeps running normally
- No shared resources affected
- FieldTuner's data remains intact in its AppData

### Scenario 2: Testing Different Versions

**Need to Test**:
- FieldTuner 2.0 with PyQt6 v6.5
- Another project with PyQt6 v6.4

**Solution**:
- FieldTuner's venv has PyQt6 v6.5
- Other project's venv has PyQt6 v6.4
- Both can coexist on the same machine
- No conflicts or interference

### Scenario 3: Deployment

**Building FieldTuner.exe**:
```powershell
.\build.py
```

**Result**:
- Creates standalone `FieldTuner.exe`
- Contains all dependencies bundled
- Runs on machines without Python installed
- Independent of development environment

## Troubleshooting

### Issue: "Package not found" when running

**Solution**:
```powershell
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Changes to other projects affecting FieldTuner

**Cause**: Not using virtual environment

**Solution**: Always activate venv before development

### Issue: Force-closing FieldTuner affects other projects

**Cause**: Shared AppData directory or global Python packages

**Solution**: 
- This shouldn't happen with proper isolation
- Verify AppData path in `src/core/path_config.py`
- Check that you're using venv, not global Python

## Verification Checklist

To verify your isolation is working:

- [ ] Virtual environment exists (`venv/` folder)
- [ ] Can activate venv without errors
- [ ] `python --version` shows venv Python
- [ ] AppData directory exists at `%APPDATA%\FieldTuner\`
- [ ] Other projects have their own venv folders
- [ ] Force-closing FieldTuner doesn't affect other projects
- [ ] No dependency conflicts between projects

## Next Steps

1. **Run setup script**: `.\setup-venv.ps1`
2. **Verify isolation**: `.\configure-isolation.ps1`
3. **Start development**: `.\QUICK_START.md`

## Resources

- `QUICK_START.md` - Daily workflow guide
- `docs/DEVELOPMENT.md` - Full development documentation
- `ISOLATION_SUMMARY.md` - Technical isolation summary

