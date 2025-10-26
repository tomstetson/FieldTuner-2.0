"""
FieldTuner V2.0 - UI Tabs
Contains all tab components for the main interface.
"""

from .quick_settings import QuickSettingsTab
from .graphics import GraphicsTab
from .input import InputTab
from .advanced import AdvancedTab
from .backup import BackupTab
from .code_view import CodeViewTab
from .debug import DebugTab

__all__ = [
    'QuickSettingsTab',
    'GraphicsTab',
    'InputTab',
    'AdvancedTab',
    'BackupTab',
    'CodeViewTab',
    'DebugTab'
]
