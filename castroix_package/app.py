"""
Main application class for Castroix
"""
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from typing import List, Dict, Any
import subprocess

from castroix_package.config import ConfigManager
from castroix_package.services import MediaService
from castroix_package.ui import ServiceButton


class CastroixApp:
    """Main application window"""
    
    def __init__(self, root: tk.Tk, config_path: Path = None):
        """
        Initialize the Castroix application
        
        Args:
            root: Tkinter root window
            config_path: Optional path to configuration file
        """
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
        self.config_manager = ConfigManager(config_path)
        self.services = self._create_services()
        
        # Setup UI
        self._setup_ui()
        
        # Setup keybindings
        self._setup_keybindings()
    
    def _create_services(self) -> List[MediaService]:
        """
        Create MediaService objects from configuration
        
        Returns:
            List of MediaService instances
        """
        services = []
        for key, service_config in self.config_manager.get_services().items():
            service = MediaService(
                name=service_config.get("name", key),
                url=service_config.get("url"),
                command=service_config.get("command"),
                icon_color=service_config.get("icon_color", "#4a90e2"),
                icon_file=service_config.get("icon_file", None)
            )
            services.append(service)
        return services
    
    def _setup_ui(self):
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
            button = ServiceButton(services_frame, service, self._launch_service)
            button.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        
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
    
    def _launch_service(self, service: MediaService):
        """
        Launch a service and track its process
        
        Args:
            service: MediaService to launch
        """
        try:
            process = service.launch(self._on_service_launched)
            if process is None and not service.command and not service.url:
                messagebox.showwarning("Not Configured", 
                    f"{service.name} is not configured. Please check config.json")
        except RuntimeError as e:
            messagebox.showerror("Launch Error", str(e))
    
    def _on_service_launched(self, name: str, process: subprocess.Popen):
        """
        Callback when a service is launched
        
        Args:
            name: Name of the service
            process: Process object
        """
        self.launched_processes.append({
            'name': name,
            'process': process
        })
    
    def _close_last_app(self):
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
    
    def _setup_keybindings(self):
        """Setup keyboard shortcuts"""
        # Ctrl+Q to close last opened app
        self.root.bind('<Control-q>', lambda e: self._close_last_app())
        self.root.bind('<Control-Q>', lambda e: self._close_last_app())
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()
