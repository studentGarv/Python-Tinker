# Python Thinker App PowerShell Launcher
# Run this script to start the Python Thinker App

Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "   🧠 Python Thinker App Launcher" -ForegroundColor Cyan  
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python is not installed or not in your PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.7+ and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Change to script directory
Set-Location $PSScriptRoot

# Launch the application
try {
    Write-Host "🚀 Starting Python Thinker App..." -ForegroundColor Yellow
    python launcher.py
} catch {
    Write-Host ""
    Write-Host "❌ An error occurred while running the application" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
