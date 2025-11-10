#!/usr/bin/env python3
"""
Castroix - A lightweight media streaming launcher for Linux desktop
"""
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import subprocess
import json
import os
from pathlib import Path


class MediaService:
    """Represents a media streaming service"""
    def __init__(self, name, url=None, command=None, icon_color="#4a90e2"):
        self.name = name
        self.url = url
        self.command = command
        self.icon_color = icon_color
    
    def launch(self):
        """Launch the media service"""
        try:
            if self.command:
                # Try to launch as a command (for installed apps)
                subprocess.Popen(self.command, shell=True)
            elif self.url:
                # Open URL in default browser
                webbrowser.open(self.url)
            else:
                messagebox.showwarning("Not Configured", 
                    f"{self.name} is not configured. Please check config.json")
        except Exception as e:
            messagebox.showerror("Launch Error", 
                f"Failed to launch {self.name}: {str(e)}")


class CastroixApp:
    """Main application window"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Castroix - Media Hub")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")
        
        # Load configuration
        self.config = self.load_config()
        self.services = self.create_services()
        
        # Setup UI
        self.setup_ui()
    
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
                    "icon_color": "#e5a00d"
                },
                "jellyfin": {
                    "name": "Jellyfin",
                    "url": "https://jellyfin.org/downloads/",
                    "command": None,
                    "icon_color": "#00a4dc"
                },
                "netflix": {
                    "name": "Netflix",
                    "url": "https://www.netflix.com",
                    "command": None,
                    "icon_color": "#e50914"
                },
                "disneyplus": {
                    "name": "Disney+",
                    "url": "https://www.disneyplus.com",
                    "command": None,
                    "icon_color": "#113ccf"
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
                icon_color=service_config.get("icon_color", "#4a90e2")
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
        
        # Footer
        footer_label = tk.Label(
            self.root,
            text="Click on a service to launch",
            font=("Arial", 10),
            bg="#1a1a1a",
            fg="#666666"
        )
        footer_label.pack(side="bottom", pady=10)
    
    def create_service_button(self, parent, service, row, col):
        """Create a button for a media service"""
        # Button frame with padding
        button_frame = tk.Frame(parent, bg="#1a1a1a")
        button_frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        
        # Service button
        button = tk.Button(
            button_frame,
            text=service.name,
            font=("Arial", 18, "bold"),
            bg=service.icon_color,
            fg="#ffffff",
            activebackground=self.lighten_color(service.icon_color),
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            command=service.launch
        )
        button.pack(expand=True, fill="both", ipadx=40, ipady=40)
        
        # Hover effects
        button.bind("<Enter>", lambda e: button.config(
            bg=self.lighten_color(service.icon_color)))
        button.bind("<Leave>", lambda e: button.config(
            bg=service.icon_color))
    
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
