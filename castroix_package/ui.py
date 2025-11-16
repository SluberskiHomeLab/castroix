"""
User interface components for Castroix
Handles the Tkinter GUI
"""
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from typing import List, Dict, Any
import subprocess

from castroix_package.services import MediaService
from castroix_package.utils import lighten_color

# Try to import PIL for icon support, but make it optional
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL (Pillow) not found. Icons will not be displayed.")
    print("To enable icons, install Pillow: pip install Pillow")


class ServiceButton:
    """Encapsulates a service button and its behavior"""
    
    def __init__(self, parent: tk.Frame, service: MediaService, 
                 on_launch: callable):
        """
        Initialize a service button
        
        Args:
            parent: Parent frame widget
            service: MediaService to represent
            on_launch: Callback function when service is launched
        """
        self.parent = parent
        self.service = service
        self.on_launch = on_launch
        
        # Create the button container
        self.container = tk.Frame(parent, bg="#1a1a1a")
        
        # Load icon if available
        self.icon_image = self._load_icon()
        
        # Create button
        self.button = self._create_button()
        self.button.pack(pady=(0, 10))
        
        # Create label
        self.label = tk.Label(
            self.container,
            text=service.name,
            font=("Arial", 14, "bold"),
            bg="#1a1a1a",
            fg="#ffffff"
        )
        self.label.pack()
        
        # Setup hover effects
        self._setup_hover_effects()
    
    def _load_icon(self):
        """Load the service icon if available"""
        if not self.service.icon_file or not PIL_AVAILABLE:
            return None
        
        # Look for icon in the project root (parent of package directory)
        icon_path = Path(__file__).parent.parent / self.service.icon_file
        if not icon_path.exists():
            return None
        
        try:
            img = Image.open(icon_path)
            # Resize to larger size for better visibility in fullscreen
            img = img.resize((120, 120), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading icon {self.service.icon_file}: {e}")
            return None
    
    def _create_button(self):
        """Create the button widget"""
        button_config = {
            'master': self.container,
            'image': self.icon_image if self.icon_image else None,
            'text': self.service.name if not self.icon_image else "",
            'font': ("Arial", 14, "bold") if not self.icon_image else None,
            'bg': self.service.icon_color,
            'fg': "#ffffff",
            'activebackground': lighten_color(self.service.icon_color),
            'activeforeground': "#ffffff",
            'relief': "flat",
            'cursor': "hand2",
            'command': self._on_click
        }
        
        # Only add width/height for text buttons
        if not self.icon_image:
            button_config['width'] = 20
            button_config['height'] = 6
        
        button = tk.Button(**button_config)
        
        # Keep a reference to prevent garbage collection
        button.image = self.icon_image
        
        return button
    
    def _setup_hover_effects(self):
        """Setup hover effects for the button"""
        lighter_color = lighten_color(self.service.icon_color)
        
        self.button.bind("<Enter>", 
            lambda e: self.button.config(bg=lighter_color))
        self.button.bind("<Leave>", 
            lambda e: self.button.config(bg=self.service.icon_color))
    
    def _on_click(self):
        """Handle button click"""
        self.on_launch(self.service)
    
    def grid(self, **kwargs):
        """Grid the button container"""
        self.container.grid(**kwargs)
