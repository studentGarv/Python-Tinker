@echo off
setlocal enabledelayedexpansion

echo.
echo =======================================
echo    🧠 Python Thinker Standalone Builder
echo =======================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in your PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if PyInstaller is installed
echo.
echo 🔍 Checking for PyInstaller...
python -m PyInstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PyInstaller not found
    echo 📦 Installing PyInstaller...
    python -m pip install pyinstaller
    if !errorlevel! neq 0 (
        echo ❌ Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo ✅ PyInstaller installed successfully
) else (
    echo ✅ PyInstaller found
)

REM Clean previous builds
echo.
echo 🧹 Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "PythonThinker.spec" del "PythonThinker.spec"

REM Build the executable
echo.
echo 🔨 Building standalone executable...

REM Base PyInstaller command
set "cmd=python -m PyInstaller --onefile --name=PythonThinker --distpath=dist --workpath=build --specpath=. launcher.py"

REM Add data files if they exist
if exist "demo_thoughts.json" (
    set "cmd=!cmd! --add-data=demo_thoughts.json;."
)
if exist "workflow_demo.json" (
    set "cmd=!cmd! --add-data=workflow_demo.json;."
)

REM Add icon if it exists
if exist "icon.ico" (
    set "cmd=!cmd! --icon=icon.ico"
)

REM Execute the build command
!cmd!

if %errorlevel% neq 0 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo ✅ Executable built successfully!

REM Create portable package
echo.
echo 📦 Creating portable package...

set "packageDir=PythonThinker_Portable"

REM Remove existing package directory
if exist "%packageDir%" rmdir /s /q "%packageDir%"
mkdir "%packageDir%"

REM Copy executable
if exist "dist\PythonThinker.exe" (
    copy "dist\PythonThinker.exe" "%packageDir%"
    echo ✅ Copied executable to %packageDir%
) else (
    echo ❌ Executable not found!
    pause
    exit /b 1
)

REM Copy documentation and demo files
if exist "README.md" (
    copy "README.md" "%packageDir%"
    echo ✅ Copied README.md
)
if exist "demo_thoughts.json" (
    copy "demo_thoughts.json" "%packageDir%"
    echo ✅ Copied demo_thoughts.json
)
if exist "workflow_demo.json" (
    copy "workflow_demo.json" "%packageDir%"
    echo ✅ Copied workflow_demo.json
)

REM Create a batch file to run the app
echo @echo off > "%packageDir%\Start_PythonThinker.bat"
echo echo. >> "%packageDir%\Start_PythonThinker.bat"
echo echo ======================================= >> "%packageDir%\Start_PythonThinker.bat"
echo echo    🧠 Python Thinker App (Portable) >> "%packageDir%\Start_PythonThinker.bat"
echo echo ======================================= >> "%packageDir%\Start_PythonThinker.bat"
echo echo. >> "%packageDir%\Start_PythonThinker.bat"
echo echo Starting Python Thinker... >> "%packageDir%\Start_PythonThinker.bat"
echo echo. >> "%packageDir%\Start_PythonThinker.bat"
echo PythonThinker.exe >> "%packageDir%\Start_PythonThinker.bat"
echo echo. >> "%packageDir%\Start_PythonThinker.bat"
echo echo Application closed. >> "%packageDir%\Start_PythonThinker.bat"
echo pause >> "%packageDir%\Start_PythonThinker.bat"

echo ✅ Created Start_PythonThinker.bat

REM Create portable README
(
echo # Python Thinker - Portable Version
echo.
echo This is a standalone version of Python Thinker that doesn't require Python to be installed.
echo.
echo ## How to Run
echo.
echo ### Option 1: Double-click the executable
echo - Double-click `PythonThinker.exe` to start the application
echo.
echo ### Option 2: Use the batch file
echo - Double-click `Start_PythonThinker.bat` for a better experience
echo.
echo ## Features
echo.
echo - Complete Python Thinker functionality
echo - No Python installation required
echo - Portable - copy this folder to any Windows computer
echo - All your data is saved in the same folder
echo.
echo ## Data Storage
echo.
echo Your thoughts and sessions are automatically saved to `thoughts.json` in this folder.
echo You can backup this file to preserve your data.
echo.
echo ## System Requirements
echo.
echo - Windows 7 or later
echo - No other software required!
) > "%packageDir%\PORTABLE_README.md"

echo ✅ Created PORTABLE_README.md

echo.
echo 🎉 Build complete!
echo.
echo You now have:
echo 1. Single executable: dist\PythonThinker.exe
echo 2. Portable package: %packageDir%\
echo.
echo The portable package can be copied to any Windows computer
echo and run without installing Python!
echo.

pause
