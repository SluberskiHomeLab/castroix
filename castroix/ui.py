"""
User interface components for Castroix application.
"""
import tkinter as tk
from tkinter import messagebox
import subprocess
from pathlib import Path
from typing import List, Optional

from .services import MediaService

# Try to import PIL for icon support, but make it optional
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL (Pillow) not found. Icons will not be displayed.")
    print("To enable icons, install Pillow: pip install Pillow")


class CastroixUI:
    """Main application window"""
    
    def __init__(self, root: tk.Tk, services: List[MediaService]):
        """Initialize the UI
        
        Args:
            root: Tkinter root window
            services: List of MediaService objects to display
        """
        self.root = root
        self.services = services
        self.launched_processes = []
        
        # Configure window
        self.root.title("Castroix - Media Hub")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")
        
        # Setup UI components
        self._setup_ui()
        self._setup_keybindings()
    
    def _setup_ui(self) -> None:
        """Setup the user interface components"""
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
            self._create_service_button(services_frame, service, row, col)
        
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
    
    def _create_service_button(self, parent: tk.Frame, service: MediaService, 
                               row: int, col: int) -> None:
        """Create a button for a media service
        
        Args:
            parent: Parent frame widget
            service: MediaService to create button for
            row: Grid row position
            col: Grid column position
        """
        # Container frame for button and label
        container_frame = tk.Frame(parent, bg="#1a1a1a")
        container_frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        
        # Load the icon image
        icon_image = None
        if service.icon_file and PIL_AVAILABLE:
            # Look for icon in parent directory (where original castroix.py is)
            package_dir = Path(__file__).parent.parent
            icon_path = package_dir / service.icon_file
            if icon_path.exists():
                try:
                    img = Image.open(icon_path)
                    img = img.resize((80, 80), Image.Resampling.LANCZOS)
                    icon_image = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Error loading icon {service.icon_file}: {e}")
        
        # Service button with icon or text
        button = tk.Button(
            container_frame,
            image=icon_image if icon_image else None,
            text=service.name if not icon_image else "",
            font=("Arial", 14, "bold") if not icon_image else None,
            bg=service.icon_color,
            fg="#ffffff",
            activebackground=self._lighten_color(service.icon_color),
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            command=lambda s=service: self._launch_service(s),
            width=120,
            height=120
        )
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
        button.bind("<Enter>", lambda e, b=button, c=service.icon_color: 
                   b.config(bg=self._lighten_color(c)))
        button.bind("<Leave>", lambda e, b=button, c=service.icon_color: 
                   b.config(bg=c))
    
    def _launch_service(self, service: MediaService) -> None:
        """Launch a service and track its process
        
        Args:
            service: MediaService to launch
        """
        try:
            process = service.launch(self._on_service_launched)
            if process is None and not service.command and not service.url:
                messagebox.showwarning("Not Configured", 
                    f"{service.name} is not configured. Please check config.json")
        except Exception as e:
            messagebox.showerror("Launch Error", str(e))
    
    def _on_service_launched(self, name: str, process: subprocess.Popen) -> None:
        """Callback when a service is launched
        
        Args:
            name: Name of the service
            process: Process object
        """
        self.launched_processes.append({
            'name': name,
            'process': process
        })
    
    def _close_last_app(self) -> None:
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
    
    def _setup_keybindings(self) -> None:
        """Setup keyboard shortcuts"""
        # Ctrl+Q to close last opened app
        self.root.bind('<Control-q>', lambda e: self._close_last_app())
        self.root.bind('<Control-Q>', lambda e: self._close_last_app())
    
    def _lighten_color(self, hex_color: str) -> str:
        """Lighten a hex color for hover effect
        
        Args:
            hex_color: Hex color string (e.g., "#123456")
            
        Returns:
            Lightened hex color string
        """
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
    
    def run(self) -> None:
        """Start the UI main loop"""
        self.root.mainloop()
