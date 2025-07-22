#!/usr/bin/env python3
"""
Release Preparation Script for Python Thinker
Cleans up repository and prepares release assets
"""

import os
import shutil
import zipfile
import json
from datetime import datetime

def clean_repository():
    """Clean up build artifacts and temporary files from repository"""
    print("🧹 Cleaning repository...")
    
    # Directories to remove
    dirs_to_remove = [
        "build",
        "dist", 
        "__pycache__",
        "PythonThinker_Portable",
        ".conda"
    ]
    
    # Files to remove
    files_to_remove = [
        "PythonThinker.spec",
        # Remove user session files (but keep demo files)
        "thinking_session_00f7d99b_20250722_150745.txt",
        "thinking_session_1bc28e80_20250722_162755.txt", 
        "thinking_session_49b52af3_20250722_162751.md",
        "thinking_session_8e0d4bb3_20250722_150736.md",
        "thoughts.json"  # Remove any existing user data
    ]
    
    # Remove directories
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Removed directory: {dir_name}")
    
    # Remove files
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✅ Removed file: {file_name}")
    
    print("✅ Repository cleaned!")

def create_release_structure():
    """Create proper release structure"""
    print("📁 Creating release structure...")
    
    # Create release directory
    release_dir = "release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Create source code archive structure
    source_files = [
        "launcher.py",
        "thinker_app.py", 
        "thinker_gui.py",
        "build_standalone.bat",
        "build_standalone.ps1",
        "build_standalone.py",
        "start_thinker.bat",
        "start_thinker.ps1",
        "requirements.txt",
        "README.md",
        "SETUP.md",
        "STANDALONE_SETUP.md",
        "demo_thoughts.json",
        "workflow_demo.json",
        ".gitignore"
    ]
    
    # Copy source files to release directory
    source_dir = os.path.join(release_dir, "PythonThinker-Source")
    os.makedirs(source_dir)
    
    for file_name in source_files:
        if os.path.exists(file_name):
            shutil.copy2(file_name, source_dir)
            print(f"✅ Copied to source: {file_name}")
    
    return release_dir, source_dir

def build_executable_for_release():
    """Build the standalone executable for release"""
    print("🔨 Building executable for release...")
    
    # Run the build script
    import subprocess
    import sys
    
    try:
        # Use the Python build script for better control
        result = subprocess.run([sys.executable, "build_standalone.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executable built successfully!")
            return True
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def create_release_archives(release_dir):
    """Create ZIP archives for different release assets"""
    print("📦 Creating release archives...")
    
    version = datetime.now().strftime("%Y.%m.%d")
    
    # 1. Source Code Archive
    source_zip = f"PythonThinker-Source-v{version}.zip"
    source_path = os.path.join(release_dir, "PythonThinker-Source")
    
    if os.path.exists(source_path):
        with zipfile.ZipFile(os.path.join(release_dir, source_zip), 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, source_path)
                    zf.write(file_path, arc_name)
        print(f"✅ Created source archive: {source_zip}")
    
    # 2. Portable Executable Archive
    if os.path.exists("PythonThinker_Portable"):
        portable_zip = f"PythonThinker-Portable-Windows-v{version}.zip"
        with zipfile.ZipFile(os.path.join(release_dir, portable_zip), 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk("PythonThinker_Portable"):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, ".")
                    zf.write(file_path, arc_name)
        print(f"✅ Created portable archive: {portable_zip}")
    
    # 3. Standalone Executable Only
    if os.path.exists("dist/PythonThinker.exe"):
        exe_zip = f"PythonThinker-Executable-v{version}.zip"
        with zipfile.ZipFile(os.path.join(release_dir, exe_zip), 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write("dist/PythonThinker.exe", "PythonThinker.exe")
        print(f"✅ Created executable archive: {exe_zip}")
    
    return version

def create_release_notes(release_dir, version):
    """Create release notes"""
    print("📝 Creating release notes...")
    
    release_notes = f"""# Python Thinker v{version} Release Notes

## 🎉 What's New

Python Thinker is a comprehensive tool to help you organize thoughts, brainstorm ideas, and structure your thinking process.

## 📦 Release Assets

### For End Users (No Python Required)
- **`PythonThinker-Portable-Windows-v{version}.zip`** - Complete portable package
  - Extract and run `Start_PythonThinker.bat`
  - No installation required!
  - Works on Windows 7+

- **`PythonThinker-Executable-v{version}.zip`** - Just the executable
  - Single file: `PythonThinker.exe`
  - Minimal download size

### For Developers (Python Required)
- **`PythonThinker-Source-v{version}.zip`** - Complete source code
  - All Python files and build scripts
  - Run with: `python launcher.py`
  - Build your own executable

## ✨ Features

- 📚 **Multiple Thinking Sessions** - Organize thoughts by topic
- 💭 **Rich Thought Management** - Categories, priorities, and tags
- 🧠 **Brainstorming Mode** - Rapid idea capture
- ✅ **Progress Tracking** - Mark thoughts as completed
- 📄 **Export Capabilities** - TXT and Markdown formats
- 🖥️ **Dual Interface** - CLI and GUI versions
- 💾 **Data Persistence** - Automatic saving

## 🚀 Quick Start

### Portable Version (Recommended)
1. Download `PythonThinker-Portable-Windows-v{version}.zip`
2. Extract to any folder
3. Double-click `Start_PythonThinker.bat`
4. Choose CLI (1) or GUI (2) interface
5. Start organizing your thoughts!

### Source Version
1. Download `PythonThinker-Source-v{version}.zip`
2. Extract and open terminal in folder
3. Run: `python launcher.py`
4. Requires Python 3.7+

## 🛠️ System Requirements

### Portable Version
- Windows 7 or later
- No additional software required

### Source Version
- Python 3.7+
- tkinter (usually included)

## 📖 Documentation

- `README.md` - Complete user guide
- `STANDALONE_SETUP.md` - Build instructions
- `PORTABLE_README.md` - Portable version guide

## 🐛 Bug Reports & Feature Requests

Please report issues on the GitHub repository.

## 📄 License

Open source - modify and distribute freely.

---

*Happy thinking! 🧠*
"""
    
    with open(os.path.join(release_dir, f"RELEASE_NOTES_v{version}.md"), "w", encoding="utf-8") as f:
        f.write(release_notes)
    
    print(f"✅ Created release notes: RELEASE_NOTES_v{version}.md")

def main():
    """Main release preparation process"""
    print("🚀 Python Thinker Release Preparation")
    print("=" * 40)
    
    # Step 1: Clean repository
    clean_repository()
    print()
    
    # Step 2: Create release structure
    release_dir, source_dir = create_release_structure()
    print()
    
    # Step 3: Build executable
    if build_executable_for_release():
        print()
        
        # Step 4: Create archives
        version = create_release_archives(release_dir)
        print()
        
        # Step 5: Create release notes
        create_release_notes(release_dir, version)
        print()
        
        print("🎉 Release preparation complete!")
        print(f"\n📁 Check the '{release_dir}' folder for:")
        print("1. Source code archive")
        print("2. Portable executable archive") 
        print("3. Standalone executable archive")
        print("4. Release notes")
        print("\n🚀 Ready for GitHub release!")
        
        return True
    else:
        print("❌ Release preparation failed during build step")
        return False

if __name__ == "__main__":
    main()
