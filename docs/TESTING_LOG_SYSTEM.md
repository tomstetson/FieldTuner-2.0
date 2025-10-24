# FieldTuner Testing Log System

## 📋 Overview

The FieldTuner application includes a dedicated testing log system designed to help diagnose issues during development and testing phases.

## 📁 Log File Locations

### Primary Log Files
- **Location**: `%APPDATA%\Roaming\FieldTuner\logs\`
- **Main Log**: `fieldtuner_YYYYMMDD_HHMMSS.log` (timestamped)
- **Testing Log**: `fieldtuner_testing.log` (dedicated testing file)

### Log File Paths
```
C:\Users\[Username]\AppData\Roaming\FieldTuner\logs\
├── fieldtuner_20251024_024547.log    # Main application log
├── fieldtuner_testing.log            # Dedicated testing log
└── crash.log                         # Crash logs (if any)
```

## 🔧 Testing Log Features

### Dedicated Testing Log File
- **File**: `fieldtuner_testing.log`
- **Purpose**: Continuous logging for testing and debugging
- **Format**: `YYYY-MM-DD HH:MM:SS - [LEVEL] - [CATEGORY] Message`
- **Encoding**: UTF-8

### Log Levels
- **INFO**: General information and status updates
- **WARNING**: Non-critical issues and warnings
- **ERROR**: Errors and exceptions
- **DEBUG**: Detailed debugging information

### Categories
- **MAIN**: Main application logic
- **CONFIG**: Configuration management
- **UI**: User interface components
- **BACKUP**: Backup system operations
- **GENERAL**: General application events

## 📊 Usage for App Testing

### 1. **Startup Testing**
```
2025-10-24 02:45:47 - INFO - [MAIN] Starting FieldTuner application
2025-10-24 02:45:47 - INFO - [CONFIG] Initializing ConfigManager
2025-10-24 02:45:47 - INFO - [CONFIG] Config file found: C:\Users\...\PROFSAVE_profile
```

### 2. **Error Detection**
```
2025-10-24 02:46:04 - ERROR - [MAIN] Failed to start FieldTuner: 'NoneType' object has no attribute 'addWidget'
2025-10-24 02:46:04 - ERROR - [MAIN] Exception: AttributeError: 'NoneType' object has no attribute 'addWidget'
```

### 3. **Layout Issues**
```
2025-10-24 02:46:04 - ERROR - [MAIN] Main layout not available - cannot add action buttons
2025-10-24 02:46:04 - INFO - [MAIN] Action buttons added to main layout successfully
```

## 🚀 How to Use for Testing

### 1. **Run the Application**
```bash
python src/main.py
# or
dist/FieldTuner.exe
```

### 2. **Monitor the Testing Log**
```bash
# Windows PowerShell
Get-Content "C:\Users\Tom Stetson\AppData\Roaming\FieldTuner\logs\fieldtuner_testing.log" -Wait

# Or open in text editor for real-time monitoring
notepad "C:\Users\Tom Stetson\AppData\Roaming\FieldTuner\logs\fieldtuner_testing.log"
```

### 3. **Check for Errors**
Look for lines containing:
- `ERROR` - Critical issues
- `WARNING` - Potential problems
- `Failed to` - Operation failures
- `Exception` - Python exceptions

## 🔍 Common Issues and Solutions

### Issue: `'NoneType' object has no attribute 'addWidget'`
**Cause**: Layout not properly initialized when adding widgets
**Solution**: Ensure layout is created and stored before adding widgets

### Issue: `Main layout not available`
**Cause**: Layout reference not properly stored
**Solution**: Store layout reference during `setup_ui()` method

### Issue: App crashes after splash screen
**Cause**: UI initialization failure
**Solution**: Check testing log for specific error messages

## 📝 Log Analysis Tips

### 1. **Startup Sequence**
Look for the sequence:
1. `Starting FieldTuner application`
2. `Initializing FieldTuner MainWindow`
3. `ConfigManager` initialization
4. `UI setup` completion
5. `Action buttons added successfully`

### 2. **Error Patterns**
- **Layout Issues**: Look for `addWidget` errors
- **Config Issues**: Look for `CONFIG` category errors
- **UI Issues**: Look for `UI` category errors

### 3. **Success Indicators**
- `FieldTuner MainWindow initialized successfully`
- `Action buttons added to main layout successfully`
- `Startup message shown to user`

## 🛠️ Development Workflow

1. **Run Application**: Start the app and reproduce the issue
2. **Check Testing Log**: Review `fieldtuner_testing.log` for errors
3. **Identify Root Cause**: Look for the first ERROR in the sequence
4. **Fix and Test**: Make changes and re-run
5. **Verify Fix**: Check that errors are resolved in the log

## 📋 Log File Management

### Automatic Cleanup
- Log files are created with timestamps
- Old logs are preserved for historical analysis
- Testing log is continuously appended

### Manual Cleanup
```bash
# Clear testing log (start fresh)
Remove-Item "C:\Users\Tom Stetson\AppData\Roaming\FieldTuner\logs\fieldtuner_testing.log"
```

## 🎯 Best Practices

1. **Always check the testing log** when the app fails to start
2. **Look for the first ERROR** in the sequence to find root cause
3. **Use the testing log** for continuous monitoring during development
4. **Keep the testing log** for debugging session history
5. **Check both main and testing logs** for complete picture

---

**Note**: The testing log system is designed to provide comprehensive debugging information for FieldTuner development and testing phases.
