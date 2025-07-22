# Python Thinker Standalone Builder
# PowerShell script to create a standalone executable

Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "   🧠 Python Thinker Standalone Builder" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if PyInstaller is installed
Write-Host "🔍 Checking for PyInstaller..." -ForegroundColor Yellow
try {
    $pyinstallerVersion = python -m PyInstaller --version 2>$null
    Write-Host "✅ PyInstaller found: $pyinstallerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ PyInstaller not found" -ForegroundColor Red
    Write-Host "📦 Installing PyInstaller..." -ForegroundColor Yellow
    
    try {
        python -m pip install pyinstaller
        Write-Host "✅ PyInstaller installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install PyInstaller" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Create the executable
Write-Host ""
Write-Host "🔨 Building standalone executable..." -ForegroundColor Yellow

# Clean previous builds
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "PythonThinker.spec") { Remove-Item -Force "PythonThinker.spec" }

# PyInstaller command
$pyinstallerArgs = @(
    "--onefile"
    "--name=PythonThinker"
    "--distpath=dist"
    "--workpath=build"
    "--specpath=."
    "launcher.py"
)

# Add data files if they exist
if (Test-Path "demo_thoughts.json") {
    $pyinstallerArgs += "--add-data=demo_thoughts.json;."
}
if (Test-Path "workflow_demo.json") {
    $pyinstallerArgs += "--add-data=workflow_demo.json;."
}

# Add icon if it exists
if (Test-Path "icon.ico") {
    $pyinstallerArgs += "--icon=icon.ico"
}

try {
    python -m PyInstaller @pyinstallerArgs
    Write-Host "✅ Executable built successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create portable package
Write-Host ""
Write-Host "📦 Creating portable package..." -ForegroundColor Yellow

$packageDir = "PythonThinker_Portable"

# Remove existing package directory
if (Test-Path $packageDir) {
    Remove-Item -Recurse -Force $packageDir
}
New-Item -ItemType Directory -Path $packageDir | Out-Null

# Copy executable
$exePath = "dist\PythonThinker.exe"
if (Test-Path $exePath) {
    Copy-Item $exePath $packageDir
    Write-Host "✅ Copied executable to $packageDir" -ForegroundColor Green
} else {
    Write-Host "❌ Executable not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Copy documentation and demo files
$filesToCopy = @("README.md", "demo_thoughts.json", "workflow_demo.json")
foreach ($file in $filesToCopy) {
    if (Test-Path $file) {
        Copy-Item $file $packageDir
        Write-Host "✅ Copied $file" -ForegroundColor Green
    }
}

# Create a batch file to run the app
$batchContent = @"
@echo off
echo.
echo =======================================
echo    🧠 Python Thinker App (Portable)
echo =======================================
echo.
echo Starting Python Thinker...
echo.
PythonThinker.exe
echo.
echo Application closed.
pause
"@

$batchContent | Out-File -FilePath "$packageDir\Start_PythonThinker.bat" -Encoding ASCII

# Create a README for the portable version
$portableReadme = @"
# Python Thinker - Portable Version

This is a standalone version of Python Thinker that doesn't require Python to be installed.

## How to Run

### Option 1: Double-click the executable
- Double-click `PythonThinker.exe` to start the application

### Option 2: Use the batch file
- Double-click `Start_PythonThinker.bat` for a better experience with pause at the end

## Features

- Complete Python Thinker functionality
- No Python installation required
- Portable - copy this folder to any Windows computer
- All your data is saved in the same folder

## Files

- `PythonThinker.exe` - The main application
- `Start_PythonThinker.bat` - Launcher script
- `README.md` - Original documentation
- `demo_thoughts.json` - Sample data (if included)
- `workflow_demo.json` - Demo workflow (if included)

## Data Storage

Your thoughts and sessions are automatically saved to `thoughts.json` in this folder.
You can backup this file to preserve your data.

## System Requirements

- Windows 7 or later
- No other software required!

---
Built with PyInstaller for maximum compatibility.
"@

$portableReadme | Out-File -FilePath "$packageDir\PORTABLE_README.md" -Encoding UTF8

Write-Host ""
Write-Host "🎉 Build complete!" -ForegroundColor Green
Write-Host ""
Write-Host "You now have:" -ForegroundColor Cyan
Write-Host "1. Single executable: dist\PythonThinker.exe" -ForegroundColor White
Write-Host "2. Portable package: $packageDir\" -ForegroundColor White
Write-Host ""
Write-Host "The portable package can be copied to any Windows computer" -ForegroundColor Yellow
Write-Host "and run without installing Python!" -ForegroundColor Yellow
Write-Host ""

# Test the executable
Write-Host "🧪 Testing the executable..." -ForegroundColor Yellow
if (Test-Path $exePath) {
    $testResult = & $exePath --help 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Executable test passed!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Executable may have issues, but it was created successfully" -ForegroundColor Yellow
    }
}

Read-Host "`nPress Enter to exit"
