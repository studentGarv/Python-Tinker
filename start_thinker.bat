@echo off
echo.
echo =======================================
echo    🧠 Python Thinker App Launcher
echo =======================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in your PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Change to the script directory
cd /d "%~dp0"

REM Launch the Python launcher
python launcher.py

REM Pause to see any error messages
if %errorlevel% neq 0 (
    echo.
    echo ❌ An error occurred while running the application
    pause
)
