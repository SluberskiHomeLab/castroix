"""
Media service management for Castroix
Handles launching and managing media streaming services
"""
import webbrowser
import subprocess
import platform
import shutil
import os
import shlex
from typing import Optional, Callable, List, Tuple


class MediaService:
    """Represents a media streaming service"""
    
    def __init__(self, name: str, url: Optional[str] = None, 
                 command: Optional[str] = None, icon_color: str = "#4a90e2", 
                 icon_file: Optional[str] = None):
        """
        Initialize a media service
        
        Args:
            name: Display name of the service
            url: Web URL to open (optional)
            command: Shell command to execute (optional)
            icon_color: Hex color code for the service
            icon_file: Path to icon file (optional)
        """
        self.name = name
        self.url = url
        self.command = command
        self.icon_color = icon_color
        self.icon_file = icon_file
    
    def launch(self, launch_callback: Optional[Callable] = None) -> Optional[subprocess.Popen]:
        """
        Launch the media service
        
        Args:
            launch_callback: Optional callback function called with (name, process)
        
        Returns:
            Process object if launched, None otherwise
        """
        try:
            process = None
            if self.command:
                # Try to launch as a command (for installed apps)
                process = subprocess.Popen(self.command, shell=True)
            elif self.url:
                # Open URL in default browser with fullscreen flags
                # Get platform-specific browser configurations
                system = platform.system()
                browsers = self._get_browsers_for_platform(system)
                
                launched = False
                for browser_name, browser_cmd in browsers:
                    # Check if browser is available
                    if self._is_browser_available(browser_name, browser_cmd, system):
                        # Format the command with the URL
                        cmd = browser_cmd.format(url=self.url)
                        process = subprocess.Popen(cmd, shell=True)
                        launched = True
                        break
                
                if not launched:
                    # Fallback to default browser (won't be fullscreen)
                    webbrowser.open(self.url)
            else:
                # No URL or command configured
                return None
            
            # Call callback with process info
            if launch_callback and process:
                launch_callback(self.name, process)
            
            return process
        except Exception as e:
            raise RuntimeError(f"Failed to launch {self.name}: {str(e)}")
    
    def _is_browser_available(self, browser_name: str, browser_cmd: str, system: str) -> bool:
        """
        Check if a browser is available on the system
        
        Args:
            browser_name: Name of the browser to check
            browser_cmd: Command template for the browser
            system: Operating system name
        
        Returns:
            True if browser is available, False otherwise
        """
        if system == "Darwin":  # macOS
            # For macOS, extract the executable path from the command and check if it exists
            # Use shlex.split to properly handle escaped spaces in paths
            try:
                parts = shlex.split(browser_cmd.replace('{url}', 'placeholder'))
                if parts:
                    exe_path = parts[0]
                    # If it's a full path (starts with /), check if it exists
                    if exe_path.startswith('/'):
                        return os.path.exists(exe_path)
                    # Otherwise, check using shutil.which for commands like 'open'
                    return shutil.which(exe_path) is not None
            except ValueError:
                # If shlex fails to parse, fall back to shutil.which
                return shutil.which(browser_name) is not None
        else:
            # For Windows and Linux, use shutil.which
            return shutil.which(browser_name) is not None
    
    def _get_browsers_for_platform(self, system: str) -> List[Tuple[str, str]]:
        """
        Get platform-specific browser configurations
        
        Args:
            system: Operating system name
        
        Returns:
            List of tuples containing (browser_name, command_template)
        """
        if system == "Windows":
            # Windows browser configurations
            return [
                ('firefox', 'firefox -kiosk {url}'),
                ('chrome', 'chrome --start-fullscreen --app={url}'),
                ('msedge', 'msedge --start-fullscreen --app={url}'),
                ('brave', 'brave --start-fullscreen --app={url}')
            ]
        elif system == "Darwin":  # MacOS
            # MacOS browser configurations
            return [
                ('firefox', '/Applications/Firefox.app/Contents/MacOS/firefox -kiosk {url}'),
                ('Google Chrome', '/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --start-fullscreen --app={url}'),
                ('Brave Browser', '/Applications/Brave\\ Browser.app/Contents/MacOS/Brave\\ Browser --start-fullscreen --app={url}'),
                ('Safari', 'open -a Safari {url}')  # Safari doesn't support kiosk mode via command line
            ]
        else:  # Linux and other Unix-like systems
            # Linux browser configurations
            return [
                ('firefox', 'firefox --kiosk {url}'),
                ('chromium', 'chromium --start-fullscreen --app={url}'),
                ('google-chrome', 'google-chrome --start-fullscreen --app={url}'),
                ('brave', 'brave --start-fullscreen --app={url}')
            ]
