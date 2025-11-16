"""
Castroix - A lightweight media streaming launcher
Cross-platform desktop application for launching media streaming services
"""

__version__ = "1.0.0"
__author__ = "SluberskiHomeLab"

# Import non-GUI components immediately
from castroix_package.services import MediaService
from castroix_package.config import ConfigManager
from castroix_package.utils import lighten_color, darken_color, is_valid_hex_color

# GUI components are imported lazily to avoid requiring tkinter at import time
def get_app():
    """Lazy import of CastroixApp to avoid requiring tkinter at import time"""
    from castroix_package.app import CastroixApp
    return CastroixApp

__all__ = ['MediaService', 'ConfigManager', 'get_app', 'lighten_color', 'darken_color', 'is_valid_hex_color']
