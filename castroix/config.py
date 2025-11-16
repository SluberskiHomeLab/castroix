"""
Configuration management for Castroix application.
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
        """Initialize configuration manager
        
        Args:
            config_path: Path to configuration file. If None, uses default location.
        """
        if config_path is None:
            # Use the parent directory of the package for config file
            package_dir = Path(__file__).parent.parent
            config_path = package_dir / "config.json"
        
        self.config_path = config_path
        self._config = None
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from file
        
        Returns:
            Configuration dictionary
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    self._config = json.load(f)
                    return self._config
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self._config = self.DEFAULT_CONFIG.copy()
            self.save(self._config)
            return self._config
    
    def save(self, config: Dict[str, Any]) -> None:
        """Save configuration to file
        
        Args:
            config: Configuration dictionary to save
        """
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get(self) -> Dict[str, Any]:
        """Get current configuration
        
        Returns:
            Configuration dictionary
        """
        if self._config is None:
            self._config = self.load()
        return self._config
    
    def get_services(self) -> Dict[str, Dict[str, Any]]:
        """Get services configuration
        
        Returns:
            Services dictionary
        """
        config = self.get()
        return config.get("services", {})
