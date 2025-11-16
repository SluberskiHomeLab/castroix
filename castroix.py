#!/usr/bin/env python3
"""
Castroix - A lightweight media streaming launcher for Windows, Linux, and MacOS
"""
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import subprocess
import json
import os
import signal
import platform
import shutil
from pathlib import Path

# Try to import PIL for icon support, but make it optional
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL (Pillow) not found. Icons will not be displayed.")
    print("To enable icons, install Pillow: pip install Pillow")


class MediaService:
    """Represents a media streaming service"""
    def __init__(self, name, url=None, command=None, icon_color="#4a90e2", icon_file=None):
        self.name = name
        self.url = url
        self.command = command
        self.icon_color = icon_color
        self.icon_file = icon_file
    
    def launch(self, launch_callback=None):
        """Launch the media service"""
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
                messagebox.showwarning("Not Configured", 
                    f"{self.name} is not configured. Please check config.json")
                return None
            
            # Call callback with process info
            if launch_callback and process:
                launch_callback(self.name, process)
            
            return process
        except Exception as e:
            messagebox.showerror("Launch Error", 
                f"Failed to launch {self.name}: {str(e)}")
            return None
    
    def _get_browsers_for_platform(self, system):
        """Get platform-specific browser configurations"""
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


class CastroixApp:
    """Main application window"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Castroix - Media Hub")
        # Start in fullscreen mode
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#1a1a1a")
        # Bind Escape key to exit fullscreen
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        
        # Track launched processes
        self.launched_processes = []
        
        # Load configuration
        self.config = self.load_config()
        self.services = self.create_services()
        
        # Setup UI
        self.setup_ui()
        
        # Setup keybindings
        self.setup_keybindings()
    
    def load_config(self):
        """Load configuration from config.json"""
        config_path = Path(__file__).parent / "config.json"
        
        # Default configuration
        default_config = {
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
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return default_config
        else:
            # Create default config file
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def create_services(self):
        """Create MediaService objects from configuration"""
        services = []
        for key, service_config in self.config.get("services", {}).items():
            service = MediaService(
                name=service_config.get("name", key),
                url=service_config.get("url"),
                command=service_config.get("command"),
                icon_color=service_config.get("icon_color", "#4a90e2"),
                icon_file=service_config.get("icon_file", None)
            )
            services.append(service)
        return services
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title label
        title_label = tk.Label(
            self.root,
            text="Castroix",
            font=("Arial", 32, "bold"),
            bg="#1a1a1a",
            fg="#ffffff"
        )
        title_label.pack(pady=30)
        
        subtitle_label = tk.Label(
            self.root,
            text="Media Hub for Multi-Media Consumption",
            font=("Arial", 12),
            bg="#1a1a1a",
            fg="#888888"
        )
        subtitle_label.pack(pady=5)
        
        # Services grid frame
        services_frame = tk.Frame(self.root, bg="#1a1a1a")
        services_frame.pack(expand=True, fill="both", padx=50, pady=30)
        
        # Configure grid to be responsive
        for i in range(2):
            services_frame.grid_rowconfigure(i, weight=1)
            services_frame.grid_columnconfigure(i, weight=1)
        
        # Create service buttons
        for idx, service in enumerate(self.services):
            row = idx // 2
            col = idx % 2
            self.create_service_button(services_frame, service, row, col)
        
        # Footer with keybind info
        footer_text = "Click on a service to launch | Press Ctrl+Q to close the last opened app/webpage"
        footer_label = tk.Label(
            self.root,
            text=footer_text,
            font=("Arial", 10),
            bg="#1a1a1a",
            fg="#666666"
        )
        footer_label.pack(side="bottom", pady=10)
    
    def create_service_button(self, parent, service, row, col):
        """Create a button for a media service"""
        # Container frame for button and label
        container_frame = tk.Frame(parent, bg="#1a1a1a")
        container_frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        
        # Load the icon image
        icon_image = None
        if service.icon_file and PIL_AVAILABLE:
            icon_path = Path(__file__).parent / service.icon_file
            if icon_path.exists():
                try:
                    img = Image.open(icon_path)
                    # Resize to larger size for better visibility in fullscreen
                    img = img.resize((120, 120), Image.Resampling.LANCZOS)
                    icon_image = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Error loading icon {service.icon_file}: {e}")
        
        # Service button with icon or text
        # Note: width/height are only set for text buttons (where they represent characters)
        # For image buttons, the size is determined by the image itself
        button_config = {
            'master': container_frame,
            'image': icon_image if icon_image else None,
            'text': service.name if not icon_image else "",
            'font': ("Arial", 14, "bold") if not icon_image else None,
            'bg': service.icon_color,
            'fg': "#ffffff",
            'activebackground': self.lighten_color(service.icon_color),
            'activeforeground': "#ffffff",
            'relief': "flat",
            'cursor': "hand2",
            'command': lambda: self.launch_service(service)
        }
        
        # Only add width/height for text buttons
        if not icon_image:
            button_config['width'] = 20
            button_config['height'] = 6
        
        button = tk.Button(**button_config)
        button.pack(pady=(0, 10))
        
        # Keep a reference to prevent garbage collection
        button.image = icon_image
        
        # Service name label below the button
        label = tk.Label(
            container_frame,
            text=service.name,
            font=("Arial", 14, "bold"),
            bg="#1a1a1a",
            fg="#ffffff"
        )
        label.pack()
        
        # Hover effects
        button.bind("<Enter>", lambda e: button.config(
            bg=self.lighten_color(service.icon_color)))
        button.bind("<Leave>", lambda e: button.config(
            bg=service.icon_color))
    
    def launch_service(self, service):
        """Launch a service and track its process"""
        process = service.launch(self.on_service_launched)
    
    def on_service_launched(self, name, process):
        """Callback when a service is launched"""
        self.launched_processes.append({
            'name': name,
            'process': process
        })
    
    def close_last_app(self):
        """Close the most recently launched app"""
        if not self.launched_processes:
            messagebox.showinfo("No Apps", "No apps are currently running from Castroix")
            return
        
        # Get the last launched process
        last_app = self.launched_processes.pop()
        
        try:
            # Try to terminate the process gracefully
            process = last_app['process']
            if process.poll() is None:  # Process is still running
                process.terminate()
                # Give it a moment to close gracefully
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    # Force kill if it doesn't close
                    process.kill()
                messagebox.showinfo("App Closed", 
                    f"Closed {last_app['name']}")
            else:
                messagebox.showinfo("Already Closed", 
                    f"{last_app['name']} has already closed")
        except Exception as e:
            messagebox.showerror("Error", 
                f"Failed to close {last_app['name']}: {str(e)}")
    
    def setup_keybindings(self):
        """Setup keyboard shortcuts"""
        # Ctrl+Q to close last opened app
        self.root.bind('<Control-q>', lambda e: self.close_last_app())
        self.root.bind('<Control-Q>', lambda e: self.close_last_app())
    
    def lighten_color(self, hex_color):
        """Lighten a hex color for hover effect"""
        # Remove # if present
        hex_color = hex_color.lstrip('#')
        # Convert to RGB
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        # Lighten by 20%
        r = min(255, int(r * 1.2))
        g = min(255, int(g * 1.2))
        b = min(255, int(b * 1.2))
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"


def main():
    """Main entry point"""
    root = tk.Tk()
    app = CastroixApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
