#!/usr/bin/env python3
"""
FieldTuner Launcher
Simple launcher script that checks dependencies and runs FieldTuner.
"""

import sys
import subprocess
import os
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import PyQt6
        return True
    except ImportError:
        return False


def install_dependencies():
    """Install required dependencies."""
    print("Installing required dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    """Main launcher function."""
    print("FieldTuner Launcher")
    print("==================")
    print()
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("Error: main.py not found. Please run this script from the FieldTuner directory.")
        return 1
    
    # Check dependencies
    if not check_dependencies():
        print("PyQt6 not found. Installing dependencies...")
        if not install_dependencies():
            print("Failed to install dependencies. Please install manually:")
            print("pip install -r requirements.txt")
            return 1
        print("Dependencies installed successfully!")
        print()
    
    # Run FieldTuner
    print("Starting FieldTuner...")
    try:
        import main
        return 0
    except Exception as e:
        print(f"Error starting FieldTuner: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
