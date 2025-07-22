#!/usr/bin/env python3
"""
Build script to create standalone executable for Python Thinker App
Uses PyInstaller to package the application
"""

import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        subprocess.check_call([sys.executable, "-c", "import PyInstaller"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("PyInstaller is available")
        return True
    except (ImportError, subprocess.CalledProcessError):
        print("PyInstaller not found")
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install PyInstaller")
        return False

def build_executable():
    """Build the standalone executable"""
    print("Building standalone executable...")
    
    # PyInstaller command with options
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create a single executable file
        "--windowed",                   # Don't show console window (comment out if you want console)
        "--name=PythonThinker",         # Name of the executable
        "--icon=icon.ico",              # Icon file (optional)
        "--add-data=demo_thoughts.json;.",  # Include demo data
        "--add-data=workflow_demo.json;.",  # Include demo workflow
        "--distpath=dist",              # Output directory
        "--workpath=build",             # Working directory
        "--specpath=.",                 # Spec file location
        "launcher.py"                   # Main entry point
    ]
    
    # Remove --icon if icon.ico doesn't exist
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon=icon.ico")
    
    # Remove --windowed if you want to see console output during development
    # cmd.remove("--windowed")
    
    try:
        subprocess.check_call(cmd)
        print("Executable built successfully!")
        print("Check the 'dist' folder for PythonThinker.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False

def create_portable_package():
    """Create a portable package with the executable and necessary files"""
    print("Creating portable package...")
    
    package_dir = "PythonThinker_Portable"
    
    # Create package directory
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy executable
    exe_path = os.path.join("dist", "PythonThinker.exe")
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, package_dir)
        print(f"Copied executable to {package_dir}")
    else:
        print("Executable not found!")
        return False
    
    # Copy documentation and demo files
    files_to_copy = [
        "README.md",
        "demo_thoughts.json",
        "workflow_demo.json"
    ]
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, package_dir)
            print(f"Copied {file_name}")
    
    # Create a simple batch file to run the app
    batch_content = """@echo off
echo.
echo =======================================
echo    Python Thinker App (Portable)
echo =======================================
echo.
echo Starting Python Thinker...
PythonThinker.exe
pause
"""
    
    with open(os.path.join(package_dir, "Start_PythonThinker.bat"), "w") as f:
        f.write(batch_content)
    
    print(f"Portable package created in {package_dir}")
    return True

def main():
    """Main build process"""
    print("Python Thinker Standalone Builder")
    print("=" * 40)
    
    # Check and install PyInstaller if needed
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("Cannot proceed without PyInstaller")
            return False
    
    # Build the executable
    if not build_executable():
        return False
    
    # Create portable package
    if not create_portable_package():
        return False
    
    print("\nBuild complete!")
    print("\nYou now have:")
    print("1. Single executable: dist/PythonThinker.exe")
    print("2. Portable package: PythonThinker_Portable/")
    print("\nThe portable package can be copied to any Windows computer")
    print("and run without installing Python!")
    
    return True

if __name__ == "__main__":
    main()
