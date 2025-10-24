@echo off
echo FieldTuner - Dependency-Free Test
echo =================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Running dependency-free tests...
python test_no_deps.py

echo.
echo Test completed. Press any key to continue...
pause
