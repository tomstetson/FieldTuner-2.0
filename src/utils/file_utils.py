"""
FieldTuner V2.0 - File Utilities
Handles file operations, locking detection, and file system utilities.
"""

import os
import shutil
from pathlib import Path
from typing import Optional, List

from debug import log_info, log_error, log_warning


class FileUtils:
    """Utility class for file operations."""
    
    @staticmethod
    def is_file_locked(file_path: Path) -> bool:
        """Check if a file is locked by another process."""
        try:
            if not file_path.exists():
                return False
            
            # Try to open the file in exclusive mode to test if it's locked
            try:
                with open(file_path, 'r+b') as f:
                    # Try to acquire an exclusive lock
                    import fcntl
                    fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    return False  # File is not locked
            except (IOError, OSError, BlockingIOError):
                log_warning(f"File appears to be locked: {file_path}", "FILE_UTILS")
                return True
            except ImportError:
                # fcntl not available on Windows, use alternative method
                pass
            
            # Windows-specific file locking detection
            try:
                import msvcrt
                with open(file_path, 'r+b') as f:
                    msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                    return False  # File is not locked
            except (IOError, OSError):
                log_warning(f"File appears to be locked: {file_path}", "FILE_UTILS")
                return True
            except ImportError:
                pass
            
            # Fallback: try to rename the file temporarily
            try:
                temp_name = file_path.with_suffix('.tmp')
                file_path.rename(temp_name)
                temp_name.rename(file_path)
                return False  # File is not locked
            except (OSError, PermissionError):
                log_warning(f"File appears to be locked: {file_path}", "FILE_UTILS")
                return True
        
        except Exception as e:
            log_error(f"Error checking file lock status: {e}", "FILE_UTILS")
            return False
    
    @staticmethod
    def safe_copy(source: Path, destination: Path) -> bool:
        """Safely copy a file with error handling."""
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            log_info(f"File copied: {source} -> {destination}", "FILE_UTILS")
            return True
        except Exception as e:
            log_error(f"Failed to copy file {source} to {destination}: {str(e)}", "FILE_UTILS", e)
            return False
    
    @staticmethod
    def safe_move(source: Path, destination: Path) -> bool:
        """Safely move a file with error handling."""
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            log_info(f"File moved: {source} -> {destination}", "FILE_UTILS")
            return True
        except Exception as e:
            log_error(f"Failed to move file {source} to {destination}: {str(e)}", "FILE_UTILS", e)
            return False
    
    @staticmethod
    def atomic_write(file_path: Path, content: str) -> bool:
        """Atomically write content to a file."""
        try:
            temp_path = file_path.with_suffix('.tmp')
            
            # Write to temporary file first
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Atomic replace
            temp_path.replace(file_path)
            
            log_info(f"Content written atomically to: {file_path}", "FILE_UTILS")
            return True
            
        except Exception as e:
            log_error(f"Failed to write content to {file_path}: {str(e)}", "FILE_UTILS", e)
            return False
    
    @staticmethod
    def find_files_by_pattern(directory: Path, pattern: str) -> List[Path]:
        """Find files matching a pattern in a directory."""
        try:
            return list(directory.glob(pattern))
        except Exception as e:
            log_error(f"Failed to find files with pattern {pattern} in {directory}: {str(e)}", "FILE_UTILS", e)
            return []
    
    @staticmethod
    def ensure_directory_exists(directory: Path) -> bool:
        """Ensure a directory exists, creating it if necessary."""
        try:
            directory.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            log_error(f"Failed to create directory {directory}: {str(e)}", "FILE_UTILS", e)
            return False
