@echo off
echo.
echo =======================================
echo    🧠 Python Thinker App Launcher
echo =======================================
echo.
echo Choose your option:
echo 1. 🚀 Run Python Thinker (requires Python)
echo 2. 🔨 Build Standalone Executable (one-time setup)
echo 3. 📖 Help
echo 4. 🚪 Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto run_app
if "%choice%"=="2" goto build_standalone
if "%choice%"=="3" goto show_help
if "%choice%"=="4" goto exit
echo Invalid choice. Please try again.
pause
goto start

:run_app
echo.
echo 🚀 Starting Python Thinker...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in your PATH
    echo.
    echo 💡 Options:
    echo 1. Install Python 3.7+ and try again
    echo 2. Use option 2 to build a standalone version (no Python needed)
    echo.
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
goto end

:build_standalone
echo.
echo 🔨 Building standalone executable...
echo This will create a version that doesn't require Python!
echo.
pause

REM Check if Python is available for building
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required to BUILD the standalone version
    echo Please install Python 3.7+ first, then try again
    pause
    exit /b 1
)

REM Run the build script
call build_standalone.bat
pause
goto end

:show_help
echo.
echo 🧠 Python Thinker Help
echo =====================
echo.
echo OPTION 1 - Run Python Thinker:
echo • Requires Python 3.7+ to be installed
echo • Starts the application immediately
echo • Choose between CLI and GUI interfaces
echo.
echo OPTION 2 - Build Standalone Executable:
echo • Creates PythonThinker.exe (no Python needed to run!)
echo • One-time setup process (takes 2-5 minutes)
echo • Results in a portable version you can copy anywhere
echo • Perfect for sharing with users who don't have Python
echo.
echo After building standalone version:
echo • Go to PythonThinker_Portable folder
echo • Double-click Start_PythonThinker.bat
echo • Copy this folder to any Windows computer!
echo.
echo For detailed instructions, see:
echo • README.md - Complete documentation
echo • STANDALONE_SETUP.md - Standalone build guide
echo.
pause
goto start

:exit
echo.
echo 👋 Goodbye!
goto end

:start
cls
echo.
echo =======================================
echo    🧠 Python Thinker App Launcher
echo =======================================
echo.
echo Choose your option:
echo 1. 🚀 Run Python Thinker (requires Python)
echo 2. 🔨 Build Standalone Executable (one-time setup)
echo 3. 📖 Help
echo 4. 🚪 Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto run_app
if "%choice%"=="2" goto build_standalone
if "%choice%"=="3" goto show_help
if "%choice%"=="4" goto exit
echo Invalid choice. Please try again.
pause
goto start

:end
