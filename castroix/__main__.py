#!/usr/bin/env python3
"""
Main entry point for Castroix application.
Can be run as: python -m castroix
"""
import tkinter as tk
from .config import ConfigManager
from .services import ServiceManager
from .ui import CastroixUI


def main():
    """Main entry point"""
    # Load configuration
    config_manager = ConfigManager()
    services_config = config_manager.get_services()
    
    # Create service manager
    service_manager = ServiceManager(services_config)
    services = service_manager.get_services()
    
    # Create and run UI
    root = tk.Tk()
    app = CastroixUI(root, services)
    app.run()


if __name__ == "__main__":
    main()
