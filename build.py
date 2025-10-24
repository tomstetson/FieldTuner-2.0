#!/usr/bin/env python3
"""
FieldTuner Build Script
Builds a portable executable using PyInstaller with comprehensive error handling.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

def clean_build_directories():
    """Clean previous build artifacts."""
    print("🧹 Cleaning previous builds...")
    
    directories_to_clean = ["dist", "build"]
    for directory in directories_to_clean:
        if Path(directory).exists():
            try:
                shutil.rmtree(directory)
                print(f"✅ Cleaned {directory}/")
            except PermissionError:
                print(f"⚠️  Warning: Could not clean {directory}/ (files may be in use)")
                print("   Continuing with build...")

def check_dependencies():
    """Check if required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    try:
        import PyQt6
        print("✅ PyQt6 available")
    except ImportError:
        print("❌ PyQt6 not found. Install with: pip install PyQt6")
        return False
    
    try:
        import PyInstaller
        print("✅ PyInstaller available")
    except ImportError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False
    
    return True

def build_executable():
    """Build the FieldTuner executable."""
    print("🔨 Building FieldTuner executable...")
    
    # Build command
    cmd = [
        "python", "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=FieldTuner",
        "--icon=assets/icon.ico",
        "--add-data=assets;assets",
        "--clean",
        "src/main.py"
    ]
    
    print(f"📝 Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def post_build_actions():
    """Perform post-build actions."""
    print("📦 Post-build actions...")
    
    exe_path = Path("dist/FieldTuner.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Executable created: {exe_path} ({size_mb:.1f} MB)")
        
        # Copy to releases if it doesn't exist
        releases_dir = Path("releases")
        releases_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        release_name = f"FieldTuner-{timestamp}.exe"
        release_path = releases_dir / release_name
        
        shutil.copy2(exe_path, release_path)
        print(f"📁 Copied to releases: {release_path}")
        
        return True
    else:
        print("❌ Executable not found after build")
        return False

def main():
    """Main build process."""
    print("🚀 FieldTuner Build Script")
    print("=" * 50)
    
    start_time = datetime.now()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        return False
    
    # Clean previous builds
    clean_build_directories()
    
    # Build executable
    if not build_executable():
        print("❌ Build failed")
        return False
    
    # Post-build actions
    if not post_build_actions():
        print("❌ Post-build actions failed")
        return False
    
    # Success
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("=" * 50)
    print(f"🎉 Build completed successfully in {duration:.1f} seconds!")
    print("📁 Executable: dist/FieldTuner.exe")
    print("📁 Release: releases/FieldTuner-*.exe")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
