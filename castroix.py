#!/usr/bin/env python3
"""
Castroix - A lightweight media streaming launcher for Windows, Linux, and MacOS

This is a backward-compatible entry point that uses the modular castroix_package.
For new code, prefer importing from castroix_package directly.
"""
import sys
from pathlib import Path

# Add the parent directory to Python path if needed
parent_dir = Path(__file__).parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# Import from the new modular package (non-GUI components only)
from castroix_package.services import MediaService
from castroix_package.config import ConfigManager

# Re-export for backward compatibility
__all__ = ['MediaService', 'ConfigManager']


def main():
    """Main entry point"""
    # Import tkinter and GUI components only when running as main
    import tkinter as tk
    from castroix_package.app import CastroixApp
    
    root = tk.Tk()
    app = CastroixApp(root)
    app.run()


if __name__ == "__main__":
    main()
