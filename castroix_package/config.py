"""
Configuration management for Castroix
Handles loading and saving of application configuration
"""
import json
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manages application configuration"""
    
    DEFAULT_CONFIG = {
        "services": {
            "plex": {
                "name": "Plex",
                "url": "https://app.plex.tv",
                "command": None,
                "icon_color": "#e5a00d",
                "icon_file": "plex.png"
            },
            "jellyfin": {
                "name": "Jellyfin",
                "url": "https://jellyfin.org/downloads/",
                "command": None,
                "icon_color": "#00a4dc",
                "icon_file": "jellyfin.png"
            },
            "netflix": {
                "name": "Netflix",
                "url": "https://www.netflix.com",
                "command": None,
                "icon_color": "#e50914",
                "icon_file": "netflix.png"
            },
            "disneyplus": {
                "name": "Disney+",
                "url": "https://www.disneyplus.com",
                "command": None,
                "icon_color": "#113ccf",
                "icon_file": "disney+.png"
            }
        }
    }
    
    def __init__(self, config_path: Path = None):
        """
        Initialize configuration manager
        
        Args:
            config_path: Path to configuration file. If None, uses default location.
        """
        if config_path is None:
            # Use the directory where castroix.py is located, not the package dir
            config_path = Path(__file__).parent.parent / "config.json"
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file
        
        Returns:
            Configuration dictionary
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.DEFAULT_CONFIG
        else:
            # Create default config file
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG
    
    def save_config(self, config: Dict[str, Any] = None) -> None:
        """
        Save configuration to file
        
        Args:
            config: Configuration to save. If None, saves current config.
        """
        if config is None:
            config = self.config
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_services(self) -> Dict[str, Dict[str, Any]]:
        """
        Get services configuration
        
        Returns:
            Dictionary of service configurations
        """
        return self.config.get("services", {})
    
    def add_service(self, key: str, service_config: Dict[str, Any]) -> None:
        """
        Add a new service to configuration
        
        Args:
            key: Service identifier
            service_config: Service configuration dictionary
        """
        if "services" not in self.config:
            self.config["services"] = {}
        self.config["services"][key] = service_config
        self.save_config()
    
    def remove_service(self, key: str) -> None:
        """
        Remove a service from configuration
        
        Args:
            key: Service identifier to remove
        """
        if key in self.config.get("services", {}):
            del self.config["services"][key]
            self.save_config()
