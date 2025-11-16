"""
Utility functions for Castroix
"""


def lighten_color(hex_color: str, factor: float = 1.2) -> str:
    """
    Lighten a hex color
    
    Args:
        hex_color: Hex color code (e.g., '#ff0000')
        factor: Lightening factor (default: 1.2 for 20% lighter)
    
    Returns:
        Lightened hex color code
    """
    # Remove # if present
    hex_color = hex_color.lstrip('#')
    
    # Convert to RGB
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Lighten
    r = min(255, int(r * factor))
    g = min(255, int(g * factor))
    b = min(255, int(b * factor))
    
    # Convert back to hex
    return f"#{r:02x}{g:02x}{b:02x}"


def darken_color(hex_color: str, factor: float = 0.8) -> str:
    """
    Darken a hex color
    
    Args:
        hex_color: Hex color code (e.g., '#ff0000')
        factor: Darkening factor (default: 0.8 for 20% darker)
    
    Returns:
        Darkened hex color code
    """
    # Remove # if present
    hex_color = hex_color.lstrip('#')
    
    # Convert to RGB
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Darken
    r = max(0, int(r * factor))
    g = max(0, int(g * factor))
    b = max(0, int(b * factor))
    
    # Convert back to hex
    return f"#{r:02x}{g:02x}{b:02x}"


def is_valid_hex_color(hex_color: str) -> bool:
    """
    Check if a string is a valid hex color
    
    Args:
        hex_color: String to check
    
    Returns:
        True if valid hex color, False otherwise
    """
    if not hex_color.startswith('#'):
        return False
    
    if len(hex_color) != 7:
        return False
    
    try:
        int(hex_color[1:], 16)
        return True
    except ValueError:
        return False
