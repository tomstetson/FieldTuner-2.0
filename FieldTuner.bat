@echo off
setlocal enabledelayedexpansion

title FieldTuner - World-Class Battlefield 6 Configuration Tool

:: Create logs directory if it doesn't exist
if not exist "%APPDATA%\FieldTuner\logs" mkdir "%APPDATA%\FieldTuner\logs"

:: Set up logging
set LOG_FILE=%APPDATA%\FieldTuner\logs\fieldtuner_launcher_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
set LOG_FILE=%LOG_FILE: =0%

:: Log startup
echo [%date% %time%] FieldTuner Launcher Starting >> "%LOG_FILE%"
echo [%date% %time%] Working Directory: %CD% >> "%LOG_FILE%"

echo.
echo  🎮 FieldTuner - World-Class Battlefield 6 Configuration Tool
echo  ============================================================
echo  💝 Created by Tom with Love from Cursor
echo.
echo  Starting FieldTuner...
echo.

cd /d "%~dp0"

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [%date% %time%] ERROR: Python not found in PATH >> "%LOG_FILE%"
    echo.
    echo ERROR: Python could not be found.
    echo Please ensure Python 3.8+ is installed and added to your system PATH.
    echo You can download Python from https://www.python.org/downloads/
    echo.
    echo Check the log file for more details: %LOG_FILE%
    echo.
    pause
    goto :end
)

:: Log Python version
python --version >> "%LOG_FILE%" 2>&1

:: Check if main.py exists
if not exist "main.py" (
    echo [%date% %time%] ERROR: main.py not found in %CD% >> "%LOG_FILE%"
    echo.
    echo ERROR: main.py not found in the current directory.
    echo Please ensure you're running this from the FieldTuner directory.
    echo Current directory: %CD%
    echo.
    echo Check the log file for more details: %LOG_FILE%
    echo.
    pause
    goto :end
)

:: Log main.py found
echo [%date% %time%] main.py found, starting application >> "%LOG_FILE%"

:: Run the main application
python main.py

:: Check exit code
if %errorlevel% neq 0 (
    echo [%date% %time%] ERROR: Application exited with code %errorlevel% >> "%LOG_FILE%"
    echo.
    echo ERROR: FieldTuner encountered an error and exited with code %errorlevel%
    echo.
    echo Check the log file for more details: %LOG_FILE%
    echo.
    echo You can also check the debug tab in the application for real-time logs.
    echo.
) else (
    echo [%date% %time%] Application exited successfully >> "%LOG_FILE%"
    echo.
    echo FieldTuner has closed successfully.
)

:end
echo.
pause
endlocal