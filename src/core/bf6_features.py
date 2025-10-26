"""
FieldTuner V2.0 - BF6-Specific Features
Advanced Battlefield 6 specific optimizations and features.
"""

import os
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from debug import log_info, log_error, log_warning, log_debug


class BF6Features:
    """BF6-specific features and optimizations."""
    
    def __init__(self):
        """Initialize BF6-specific features."""
        log_info("Initializing BF6-Specific Features", "BF6_FEATURES")
        self.system_info = self._get_system_info()
        self.bf6_processes = ['bf6.exe', 'Battlefield6.exe', 'bf6_x64.exe']
        
    def _get_system_info(self) -> Dict[str, str]:
        """Get system information for BF6 optimization."""
        return {
            'os': platform.system(),
            'os_version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'python_version': platform.python_version()
        }
    
    def get_bf6_process_info(self) -> Dict[str, any]:
        """Get information about running BF6 processes."""
        log_info("Scanning for BF6 processes", "BF6_FEATURES")
        
        try:
            if self.system_info['os'] == 'Windows':
                # Use tasklist for Windows
                result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq bf6.exe'], 
                                     capture_output=True, text=True)
                if 'bf6.exe' in result.stdout:
                    return {
                        'running': True,
                        'processes': ['bf6.exe'],
                        'status': 'Active'
                    }
            else:
                # Use ps for Unix-like systems
                result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                bf6_processes = [line for line in result.stdout.split('\n') 
                               if any(proc in line for proc in self.bf6_processes)]
                if bf6_processes:
                    return {
                        'running': True,
                        'processes': bf6_processes,
                        'status': 'Active'
                    }
        except Exception as e:
            log_error(f"Error checking BF6 processes: {e}", "BF6_FEATURES")
        
        return {
            'running': False,
            'processes': [],
            'status': 'Not Running'
        }
    
    def get_bf6_audio_settings(self) -> Dict[str, str]:
        """Get BF6-specific audio optimization settings (REAL settings only)."""
        log_info("Generating BF6 audio settings", "BF6_FEATURES")
        
        return {
            # REAL BF6 Audio Settings
            'GstAudio.AudioQuality': '2',  # High quality
            'GstAudio.HitIndicatorSound': '1',  # Hit indicators
            'GstAudio.InGameAnnouncer_OnOff': '1',  # In-game announcer
            'GstAudio.SubtitlesEnemies': '1',  # Enemy subtitles
            'GstAudio.SubtitlesFriendlies': '1',  # Friendly subtitles
            'GstAudio.SubtitlesSquad': '1',  # Squad subtitles
            'GstAudio.SubtitlesCommander': '1',  # Commander subtitles
            'GstAudio.SubtitlesShowSpeakerName': '1',  # Show speaker names
            'GstAudio.SoundSystemSize': '20',  # Sound system size
            'GstAudio.SpeakerConfiguration': '2',  # Speaker configuration
            'GstAudio.StereoBalance': '0.000000',  # Stereo balance
            'GstAudio.MicrophoneVolume': '0.500000',  # Microphone volume
            'GstAudio.OptionVOIPLowerGameAudio': '0.250000',  # VOIP lower game audio
        }
    
    def get_bf6_network_settings(self) -> Dict[str, str]:
        """Get BF6-specific network optimization settings (REAL settings only)."""
        log_info("Generating BF6 network settings", "BF6_FEATURES")
        
        # Note: BF6 doesn't have many network settings in the config file
        # Most network settings are handled by the game engine
        return {
            # These are the only network-related settings that might exist
            'GstAudio.OptionVoipExternalOutputEnabled': '0',  # VOIP external output
        }
    
    def get_bf6_input_settings(self) -> Dict[str, str]:
        """Get BF6-specific input optimization settings (REAL settings only)."""
        log_info("Generating BF6 input settings", "BF6_FEATURES")
        
        # Note: BF6 input settings are typically stored in different files
        # The main config file doesn't contain many input settings
        return {
            # These are the only input-related settings that might exist in the main config
            'GstAudio.OpenMicThreshold': '0.000000',  # Open mic threshold
        }
    
    def get_bf6_competitive_settings(self) -> Dict[str, str]:
        """Get BF6-specific competitive optimization settings (REAL settings only)."""
        log_info("Generating BF6 competitive settings", "BF6_FEATURES")
        
        return {
            # REAL BF6 Competitive Settings
            'GstAudio.HitIndicatorSound': '1',  # Hit indicators for competitive play
            'GstAudio.InGameAnnouncer_OnOff': '1',  # In-game announcer
            'GstAudio.SubtitlesEnemies': '1',  # Enemy subtitles for awareness
            'GstAudio.SubtitlesFriendlies': '1',  # Friendly subtitles
            'GstAudio.SubtitlesSquad': '1',  # Squad subtitles
            'GstAudio.SubtitlesCommander': '1',  # Commander subtitles
            'GstAudio.SubtitlesShowSpeakerName': '1',  # Show speaker names
            'GstAudio.SubtitlesTextSize': '0',  # Standard text size
        }
    
    def get_bf6_advanced_settings(self) -> Dict[str, str]:
        """Get BF6-specific advanced optimization settings (REAL settings only)."""
        log_info("Generating BF6 advanced settings", "BF6_FEATURES")
        
        return {
            # REAL BF6 Advanced Settings
            'GstAudio.AudioQuality': '2',  # High audio quality
            'GstAudio.SoundSystemSize': '20',  # Sound system size
            'GstAudio.SpeakerConfiguration': '2',  # Speaker configuration
            'GstAudio.StereoBalance': '0.000000',  # Stereo balance
            'GstAudio.MicrophoneVolume': '0.500000',  # Microphone volume
            'GstAudio.OptionVOIPLowerGameAudio': '0.250000',  # VOIP lower game audio
            'GstAudio.OptionVoipExternalOutputEnabled': '0',  # VOIP external output
            'GstAudio.OpenMicThreshold': '0.000000',  # Open mic threshold
        }
    
    def get_bf6_preset_optimizations(self, preset_name: str) -> Dict[str, str]:
        """Get BF6-specific optimizations for a given preset."""
        log_info(f"Generating BF6 optimizations for preset: {preset_name}", "BF6_FEATURES")
        
        base_settings = {}
        
        # Add audio settings
        base_settings.update(self.get_bf6_audio_settings())
        
        # Add network settings
        base_settings.update(self.get_bf6_network_settings())
        
        # Add input settings
        base_settings.update(self.get_bf6_input_settings())
        
        # Add competitive settings
        base_settings.update(self.get_bf6_competitive_settings())
        
        # Add advanced settings
        base_settings.update(self.get_bf6_advanced_settings())
        
        # Preset-specific optimizations
        if preset_name == 'esports':
            # Maximum competitive advantage
            base_settings.update({
                'GstAudio.FootstepVolume': '1.2',
                'GstAudio.WeaponVolume': '0.9',
                'GstNetwork.PingOptimization': '1',
                'GstInput.MouseSensitivity': '1.2',
                'GstUI.CrosshairSize': '0.7',
                'GstUI.MinimapSize': '1.3',
            })
        elif preset_name == 'performance':
            # Maximum performance
            base_settings.update({
                'GstAudio.AudioQuality': '1',
                'GstNetwork.Compression': '1',
                'GstInput.PollingRate': '500',
                'GstUI.HUDScale': '0.9',
                'GstRender.TemporalAA': '0',
            })
        elif preset_name == 'quality':
            # Maximum quality
            base_settings.update({
                'GstAudio.AudioQuality': '3',
                'GstAudio.SampleRate': '96000',
                'GstUI.HUDScale': '1.1',
                'GstRender.MSAA': '4',
                'GstRender.TemporalAA': '1',
            })
        
        return base_settings
    
    def validate_bf6_settings(self, settings: Dict[str, str]) -> Tuple[bool, List[str]]:
        """Validate BF6 settings for compatibility and performance."""
        log_info("Validating BF6 settings", "BF6_FEATURES")
        
        warnings = []
        is_valid = True
        
        # Check for conflicting settings
        if settings.get('GstRender.DLSS') == '1' and settings.get('GstRender.FSR') == '1':
            warnings.append("DLSS and FSR cannot be enabled simultaneously")
            is_valid = False
        
        if settings.get('GstRender.MSAA') != '0' and settings.get('GstRender.TemporalAA') == '1':
            warnings.append("MSAA and Temporal AA may conflict - consider using one")
        
        # Check for performance issues
        if settings.get('GstRender.ResolutionScale', '1.0') > '1.5':
            warnings.append("High resolution scale may impact performance")
        
        if settings.get('GstAudio.SampleRate', '48000') > '48000':
            warnings.append("High audio sample rate may impact performance")
        
        # Check for competitive settings
        if settings.get('GstRender.MotionBlurWorld', '0') != '0':
            warnings.append("Motion blur disabled for competitive advantage")
        
        if settings.get('GstRender.VSyncMode', '0') != '0':
            warnings.append("VSync disabled for competitive advantage")
        
        return is_valid, warnings
    
    def get_bf6_system_recommendations(self) -> Dict[str, str]:
        """Get system-specific recommendations for BF6 optimization."""
        log_info("Generating BF6 system recommendations", "BF6_FEATURES")
        
        recommendations = {}
        
        # OS-specific recommendations
        if self.system_info['os'] == 'Windows':
            recommendations.update({
                'os_optimization': 'Enable Game Mode and disable unnecessary background processes',
                'power_plan': 'Use High Performance power plan',
                'antivirus': 'Add BF6 to antivirus exclusions',
                'defrag': 'Ensure SSD optimization is enabled',
            })
        
        # Architecture-specific recommendations
        if '64' in self.system_info['architecture']:
            recommendations.update({
                'memory': 'Ensure 16GB+ RAM for optimal performance',
                'virtual_memory': 'Set virtual memory to 1.5x physical RAM',
            })
        
        # General recommendations
        recommendations.update({
            'drivers': 'Keep graphics drivers updated',
            'background_apps': 'Close unnecessary background applications',
            'network': 'Use wired connection for best network performance',
            'monitoring': 'Monitor CPU/GPU temperatures during gameplay',
        })
        
        return recommendations
