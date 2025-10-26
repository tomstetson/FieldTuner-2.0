"""
FieldTuner V2.0 - Process Utilities
Handles process detection and system monitoring.
"""

from typing import List, Dict, Any

from debug import log_info, log_error, log_warning


class ProcessUtils:
    """Utility class for process operations."""
    
    @staticmethod
    def is_battlefield_running() -> bool:
        """Check if Battlefield 6 is currently running."""
        try:
            import psutil
            
            # Common Battlefield 6 process names
            bf6_process_names = [
                'bf6.exe',
                'battlefield6.exe',
                'battlefield 6.exe',
                'bf6.exe',
                'bf6_x64.exe',
                'bf6_x86.exe',
                'battlefield6_x64.exe',
                'battlefield6_x86.exe',
            ]
            
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    proc_name = proc.info['name'].lower() if proc.info['name'] else ''
                    proc_exe = proc.info['exe'].lower() if proc.info['exe'] else ''
                    
                    # Check process name
                    for bf6_name in bf6_process_names:
                        if bf6_name.lower() in proc_name or bf6_name.lower() in proc_exe:
                            log_info(f"Battlefield 6 process detected: {proc.info['name']} (PID: {proc.info['pid']})", "PROCESS")
                            return True
                    
                    # Check for Battlefield-related processes
                    if any(keyword in proc_name for keyword in ['battlefield', 'bf6', 'bf2042']):
                        log_info(f"Battlefield-related process detected: {proc.info['name']} (PID: {proc.info['pid']})", "PROCESS")
                        return True
                
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            return False
        
        except ImportError:
            log_warning("psutil not available - cannot detect running processes", "PROCESS")
            return False
        except Exception as e:
            log_error(f"Error checking for running processes: {e}", "PROCESS")
            return False
    
    @staticmethod
    def get_process_info(process_name: str) -> List[Dict[str, Any]]:
        """Get information about processes with a specific name."""
        try:
            import psutil
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'status', 'create_time']):
                try:
                    if process_name.lower() in proc.info['name'].lower():
                        processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'exe': proc.info['exe'],
                            'status': proc.info['status'],
                            'create_time': proc.info['create_time']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            return processes
            
        except ImportError:
            log_warning("psutil not available - cannot get process info", "PROCESS")
            return []
        except Exception as e:
            log_error(f"Error getting process info: {e}", "PROCESS")
            return []
    
    @staticmethod
    def kill_process_by_name(process_name: str) -> bool:
        """Kill all processes with a specific name."""
        try:
            import psutil
            
            killed_count = 0
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if process_name.lower() in proc.info['name'].lower():
                        proc.kill()
                        killed_count += 1
                        log_info(f"Killed process: {proc.info['name']} (PID: {proc.info['pid']})", "PROCESS")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            if killed_count > 0:
                log_info(f"Killed {killed_count} processes matching '{process_name}'", "PROCESS")
                return True
            else:
                log_warning(f"No processes found matching '{process_name}'", "PROCESS")
                return False
                
        except ImportError:
            log_warning("psutil not available - cannot kill processes", "PROCESS")
            return False
        except Exception as e:
            log_error(f"Error killing processes: {e}", "PROCESS")
            return False
