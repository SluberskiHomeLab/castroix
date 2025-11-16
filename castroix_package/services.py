"""
Media service management for Castroix
Handles launching and managing media streaming services
"""
import webbrowser
import subprocess
import platform
import shutil
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
                    # Check if browser is available using cross-platform shutil.which
                    if shutil.which(browser_name):
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
