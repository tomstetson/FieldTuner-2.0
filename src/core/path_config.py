"""
Centralized path configuration for FieldTuner 2.0.

This module provides a centralized way to manage all file paths used by the application,
making it easy to update paths and follow best practices for cross-platform compatibility.
"""

import os
from pathlib import Path
from typing import List, Optional


class PathConfig:
    """Centralized path configuration for FieldTuner 2.0."""
    
    def __init__(self):
        """Initialize path configuration."""
        self._app_name = "FieldTuner"
        self._bf6_folder_name = "Battlefield 6"
        self._config_filename = "PROFSAVE_profile"
        
    @property
    def app_data_dir(self) -> Path:
        """Get the application data directory."""
        return Path.home() / "AppData" / "Roaming" / self._app_name
    
    @property
    def logs_dir(self) -> Path:
        """Get the logs directory."""
        return self.app_data_dir / "logs"
    
    @property
    def backups_dir(self) -> Path:
        """Get the backups directory."""
        return self.app_data_dir / "backups"
    
    @property
    def favorites_file(self) -> Path:
        """Get the favorites file path."""
        return self.app_data_dir / "favorites.json"
    
    @property
    def preferences_file(self) -> Path:
        """Get the preferences file path."""
        return self.app_data_dir / "preferences.json"
    
    @property
    def app_state_file(self) -> Path:
        """Get the app state file path."""
        return self.app_data_dir / "app_state.json"
    
    @property
    def test_config_file(self) -> Path:
        """Get the test config file path (for development/testing)."""
        # Use the BF6 profile file you provided for testing
        return Path(__file__).parent.parent.parent / "FT_2.0_BF6_Profile" / self._config_filename
    
    def get_bf6_config_paths(self) -> List[Path]:
        """
        Get all possible Battlefield 6 config file paths.
        
        Returns:
            List of Path objects representing possible config file locations.
        """
        paths = []
        
        # Standard Documents paths
        documents_paths = [
            Path("Documents") / self._bf6_folder_name / "settings" / "steam" / self._config_filename,
            Path("Documents") / self._bf6_folder_name / "settings" / self._config_filename,
            Path("Documents") / self._bf6_folder_name / "settings" / "EA App" / self._config_filename,
            Path("Documents") / self._bf6_folder_name / "settings" / "EA Desktop" / self._config_filename,
        ]
        
        # OneDrive Documents paths
        onedrive_paths = [
            Path("OneDrive") / "Documents" / self._bf6_folder_name / "settings" / "steam" / self._config_filename,
            Path("OneDrive") / "Documents" / self._bf6_folder_name / "settings" / self._config_filename,
            Path("OneDrive") / "Documents" / self._bf6_folder_name / "settings" / "EA App" / self._config_filename,
            Path("OneDrive") / "Documents" / self._bf6_folder_name / "settings" / "EA Desktop" / self._config_filename,
        ]
        
        # Full home directory paths
        home_paths = [
            Path.home() / "Documents" / self._bf6_folder_name / "settings" / "steam" / self._config_filename,
            Path.home() / "OneDrive" / "Documents" / self._bf6_folder_name / "settings" / "steam" / self._config_filename,
            Path.home() / "Documents" / self._bf6_folder_name / "settings" / self._config_filename,
            Path.home() / "OneDrive" / "Documents" / self._bf6_folder_name / "settings" / self._config_filename,
            Path.home() / "Documents" / self._bf6_folder_name / "settings" / "EA App" / self._config_filename,
            Path.home() / "Documents" / self._bf6_folder_name / "settings" / "EA Desktop" / self._config_filename,
            Path.home() / "Documents" / self._bf6_folder_name / "settings" / "Origin" / self._config_filename,
            Path.home() / "OneDrive" / "Documents" / self._bf6_folder_name / "settings" / "EA App" / self._config_filename,
            Path.home() / "OneDrive" / "Documents" / self._bf6_folder_name / "settings" / "EA Desktop" / self._config_filename,
            Path.home() / "OneDrive" / "Documents" / self._bf6_folder_name / "settings" / "Origin" / self._config_filename,
        ]
        
        # Combine all paths
        all_paths = documents_paths + onedrive_paths + home_paths
        
        # Add environment variable override if set
        env_config_path = os.environ.get('FIELDTUNER_CONFIG_PATH')
        if env_config_path:
            all_paths.insert(0, Path(env_config_path))
        
        return all_paths
    
    def get_project_root(self) -> Path:
        """Get the project root directory."""
        return Path(__file__).parent.parent.parent
    
    def get_assets_dir(self) -> Path:
        """Get the assets directory."""
        return self.get_project_root() / "assets"
    
    def get_docs_dir(self) -> Path:
        """Get the documentation directory."""
        return self.get_project_root() / "docs"
    
    def get_tests_dir(self) -> Path:
        """Get the tests directory."""
        return self.get_project_root() / "tests"
    
    def get_src_dir(self) -> Path:
        """Get the source directory."""
        return self.get_project_root() / "src"
    
    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        directories = [
            self.app_data_dir,
            self.logs_dir,
            self.backups_dir,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Global instance for easy access
path_config = PathConfig()
