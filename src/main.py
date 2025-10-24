#!/usr/bin/env python3
"""
FieldTuner - Battlefield 6 Configuration Tool
A modern Windows GUI tool for managing Battlefield 6 config files.
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from gui.main_window import MainWindow
from core.config_manager import ConfigManager


def main():
    """Main entry point for FieldTuner."""
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("FieldTuner")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("FieldTuner")
    
    # Set application icon if available
    icon_path = Path(__file__).parent / "assets" / "icon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Initialize config manager
    config_manager = ConfigManager()
    
    # Create and show main window
    window = MainWindow(config_manager)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
