"""
Castroix - A lightweight media streaming launcher for Windows, Linux, and MacOS
"""

from .config import ConfigManager
from .services import MediaService, ServiceManager

# Try to import UI components, but make them optional for headless environments
try:
    from .ui import CastroixUI, PIL_AVAILABLE
    UI_AVAILABLE = True
except ImportError:
    CastroixUI = None
    PIL_AVAILABLE = False
    UI_AVAILABLE = False

__version__ = "2.0.0"
__all__ = [
    'ConfigManager',
    'MediaService', 
    'ServiceManager',
    'CastroixUI',
    'PIL_AVAILABLE',
    'UI_AVAILABLE'
]
