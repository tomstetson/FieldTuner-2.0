"""
FieldTuner V2.0 - Main Entry Point
Clean, modular entry point for the application.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

# Import centralized path configuration
from core.path_config import path_config

from debug import log_info, log_error, log_warning
from core import ConfigManager, FavoritesManager, AppState
from core.user_preferences import UserPreferences
from ui import MainWindow


def main():
    """Main application entry point."""
    try:
        log_info("Starting FieldTuner 2.0", "MAIN")
        
        # Create QApplication
        app = QApplication(sys.argv)
        app.setApplicationName("FieldTuner 2.0")
        app.setApplicationVersion("2.0.0")
        app.setOrganizationName("FieldTuner 2.0")
        
        # Ensure application quits when last window closes
        app.setQuitOnLastWindowClosed(True)
        
        # High DPI scaling is handled automatically in PyQt6
        
        # Initialize core components
        log_info("Initializing core components", "MAIN")
        
        try:
            # Use the test config file from the centralized path configuration
            fresh_config_path = path_config.test_config_file
            config_manager = ConfigManager(fresh_config_path)
            log_info("ConfigManager initialized", "MAIN")
        except Exception as e:
            log_error(f"Failed to initialize ConfigManager: {str(e)}", "MAIN", e)
            QMessageBox.critical(
                None,
                "Configuration Error",
                f"Failed to initialize configuration manager:\n\n{str(e)}\n\n"
                "Please check your Battlefield 6 installation and try again."
            )
            return 1
        
        try:
            favorites_manager = FavoritesManager()
            log_info("FavoritesManager initialized", "MAIN")
        except Exception as e:
            log_error(f"Failed to initialize FavoritesManager: {str(e)}", "MAIN", e)
            # Continue without favorites - not critical
        
        try:
            app_state = AppState()
            log_info("AppState initialized", "MAIN")
        except Exception as e:
            log_error(f"Failed to initialize AppState: {str(e)}", "MAIN", e)
            # Continue with default state
        
        try:
            user_preferences = UserPreferences()
            log_info("UserPreferences initialized", "MAIN")
        except Exception as e:
            log_error(f"Failed to initialize UserPreferences: {str(e)}", "MAIN", e)
            # Continue without preferences
        
        # Create main window
        log_info("Creating main window", "MAIN")
        try:
            main_window = MainWindow(config_manager, favorites_manager, app_state, user_preferences)
            main_window.show()
            log_info("Main window created and shown", "MAIN")
        except Exception as e:
            log_error(f"Failed to create main window: {str(e)}", "MAIN", e)
            QMessageBox.critical(
                None,
                "UI Error",
                f"Failed to create main window:\n\n{str(e)}\n\n"
                "Please check the application logs for more details."
            )
            return 1
        
        # Show startup message if config was loaded
        if config_manager.config_path and hasattr(config_manager.config_path, 'exists') and config_manager.config_path.exists():
            # Check if Battlefield 6 is running and show warning
            if config_manager._is_battlefield_running():
                QMessageBox.warning(
                    main_window,
                    "⚠️ Battlefield 6 is Running",
                    "🎮 FieldTuner V2.0 Connected!\n\n"
                    f"✅ Config File: {config_manager.config_path.name}\n"
                    f"📊 Settings Loaded: {len(config_manager.config_data)}\n\n"
                    "⚠️ WARNING: Battlefield 6 is currently running!\n\n"
                    "🚫 You cannot edit configuration files while the game is running.\n"
                    "✅ Please close Battlefield 6 before making any changes.\n"
                    "🔄 This prevents configuration corruption and ensures changes are applied correctly."
                )
            else:
                QMessageBox.information(
                    main_window,
                    "🎮 FieldTuner V2.0 Connected!",
                    f"✅ Successfully connected to your Battlefield 6 configuration!\n\n"
                    f"📁 Config File: {config_manager.config_path.name}\n"
                    f"📂 Full Path: {config_manager.config_path}\n"
                    f"⚙️ Settings Loaded: {len(config_manager.config_data)}\n"
                    f"💾 Auto-backup Created: Your original config is safely backed up\n\n"
                    f"🚀 You can now safely modify your settings!\n\n"
                    f"Made with Love by SneakyTom"
                )
            log_info("Startup message shown to user", "MAIN")
        
        log_info("FieldTuner V2.0 startup completed successfully", "MAIN")
        
        # Run the application
        exit_code = app.exec()
        
        # Log shutdown
        log_info("FieldTuner V2.0 shutdown complete", "MAIN")
        
        # Ensure clean exit
        sys.exit(exit_code if exit_code is not None else 0)
        
    except Exception as e:
        log_error(f"Critical error during startup: {str(e)}", "MAIN", e)
        QMessageBox.critical(
            None,
            "Critical Error",
            f"FieldTuner V2.0 encountered a critical error:\n\n{str(e)}\n\n"
            "Please check the application logs for more details."
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
