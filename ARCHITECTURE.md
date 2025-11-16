# Castroix Architecture

## Overview

Castroix has been refactored from a monolithic single-file application into a well-structured Python package with clear separation of concerns. This document describes the architecture and design decisions.

## Architecture Improvements

### Before (Monolithic)
- Single 372-line `castroix.py` file
- All code (UI, business logic, configuration) mixed together
- Difficult to test, extend, and maintain
- No proper package structure

### After (Modular)
- Organized package structure with separate modules
- Clear separation between business logic and UI
- Better testability and maintainability
- Proper Python package with installation support
- Backward compatible with original interface

## Package Structure

```
castroix/
├── castroix_package/          # Main package directory
│   ├── __init__.py           # Package initialization and exports
│   ├── __main__.py           # Entry point for module execution
│   ├── app.py                # Main application class (GUI coordination)
│   ├── config.py             # Configuration management
│   ├── services.py           # Media service handling
│   └── ui.py                 # UI components (buttons, widgets)
├── castroix.py               # Backward-compatible entry point
├── test_castroix.py          # Comprehensive test suite
├── config.json               # User configuration
├── setup.py                  # Package installation (legacy)
├── pyproject.toml            # Modern package configuration
└── README.md                 # User documentation
```

## Module Responsibilities

### `castroix_package/__init__.py`
- Package initialization
- Exports public API
- Lazy imports for GUI components (to avoid requiring tkinter at import time)

### `castroix_package/config.py`
**Purpose:** Configuration management
- `ConfigManager` class handles loading/saving configuration
- Provides default configuration
- Supports adding/removing services dynamically
- Configuration stored in JSON format

**Key Features:**
- Auto-creates default config if missing
- Validates configuration structure
- Provides clean API for accessing services

### `castroix_package/services.py`
**Purpose:** Media service logic
- `MediaService` class represents a streaming service
- Handles launching services via URL or command
- Platform-specific browser detection
- Fullscreen/kiosk mode support

**Key Features:**
- Cross-platform browser launching
- Command-based app launching
- Process tracking for launched services
- Fallback to default browser

### `castroix_package/ui.py`
**Purpose:** User interface components
- `ServiceButton` class encapsulates service button behavior
- Icon loading and display
- Hover effects
- Optional PIL/Pillow support

**Key Features:**
- Modular button components
- Icon image handling with graceful fallback
- Responsive grid layout support
- Separated from business logic

### `castroix_package/app.py`
**Purpose:** Main application coordination
- `CastroixApp` class manages the main window
- Coordinates UI, services, and configuration
- Handles keybindings and window management
- Tracks launched processes

**Key Features:**
- Fullscreen mode by default
- Process tracking for launched apps
- Keyboard shortcuts (Ctrl+Q to close last app)
- Clean separation from UI implementation

### `castroix_package/utils.py`
**Purpose:** Utility functions
- Color manipulation (lighten, darken)
- Color validation
- Reusable helper functions

## Design Patterns

### Separation of Concerns
Each module has a single, well-defined responsibility:
- Configuration management is isolated in `config.py`
- Service launching logic is in `services.py`
- UI components are in `ui.py`
- Application coordination is in `app.py`

### Dependency Injection
- `CastroixApp` accepts a `config_path` parameter
- `ServiceButton` accepts callbacks for actions
- Makes testing easier and components more flexible

### Optional Dependencies
- PIL/Pillow is optional - app works without it
- Lazy imports prevent requiring GUI libraries at import time

### Backward Compatibility
- Original `castroix.py` still works as entry point
- Imports from new package structure
- Maintains same command-line interface

## Configuration System

### ConfigManager
The `ConfigManager` class provides a clean interface for configuration:

```python
config_manager = ConfigManager()  # Auto-loads config.json
services = config_manager.get_services()
config_manager.add_service('hulu', {...})
config_manager.remove_service('netflix')
```

### Configuration Format
Configuration is stored in JSON with the following structure:
```json
{
  "services": {
    "service_id": {
      "name": "Display Name",
      "url": "https://...",
      "command": "command to run",
      "icon_color": "#hexcolor",
      "icon_file": "icon.png"
    }
  }
}
```

## Service Launching

### MediaService
The `MediaService` class encapsulates service launching:

```python
service = MediaService(
    name="Netflix",
    url="https://netflix.com",
    icon_color="#e50914"
)
process = service.launch(callback=on_launched)
```

### Platform Support
- Detects platform (Windows, macOS, Linux)
- Uses platform-specific browser commands
- Supports fullscreen/kiosk modes
- Falls back to default browser if needed

## Testing

### Test Structure
Tests are organized by functionality:
- `TestMediaService` - Service launching logic
- `TestConfiguration` - Config loading and structure
- `TestConfigManager` - Config management API
- `TestUtilities` - Utility functions
- `TestColorUtils` - Color validation
- `TestFullscreenFeatures` - Fullscreen and keybindings
- `TestCrossPlatform` - Platform compatibility

### Mocking Strategy
- Tkinter is mocked for headless testing
- Tests focus on business logic, not GUI rendering
- Configuration tests use actual JSON parsing

## Installation

### As a Package
```bash
pip install -e .
```

### Running
```bash
# Direct execution
python castroix.py

# As a module
python -m castroix_package

# After installation
castroix
```

## Extensibility

### Adding New Services
Services can be added via configuration or programmatically:

```python
config_manager = ConfigManager()
config_manager.add_service('hulu', {
    'name': 'Hulu',
    'url': 'https://hulu.com',
    'icon_color': '#1ce783',
    'icon_file': 'hulu.png'
})
```

### Custom UI Components
The modular structure allows replacing or extending UI components:

```python
from castroix_package.ui import ServiceButton

class CustomServiceButton(ServiceButton):
    # Override behavior
    pass
```

### Plugin Architecture
Future enhancement: Services could be loaded as plugins:
- Services directory with Python files
- Each file defines a service class
- Auto-discovery and loading

## Benefits of New Architecture

### Maintainability
- Each module has a clear, single responsibility
- Changes are localized to specific modules
- Easier to understand and modify

### Testability
- Business logic separated from UI
- Easier to mock dependencies
- Comprehensive test coverage

### Extensibility
- New features can be added without modifying core code
- Plugin architecture possible
- Custom UI components supported

### Reusability
- Modules can be imported and used independently
- Services can be launched programmatically
- Configuration can be managed via API

### Professional Quality
- Follows Python packaging best practices
- Proper dependency management
- Clear documentation and structure

## Future Enhancements

### Potential Improvements
1. **Plugin System** - Load services from external plugins
2. **Themes** - Customizable color schemes and layouts
3. **Service Templates** - Pre-configured service types
4. **Settings UI** - GUI for editing configuration
5. **Update Checker** - Auto-update functionality
6. **Service Groups** - Organize services into categories
7. **Search** - Quick service search and launch
8. **Recent Items** - Track recently launched services
9. **Favorites** - Pin frequently used services
10. **Multi-monitor** - Support for multiple displays

## Migration Guide

### For Users
No changes required - `castroix.py` works as before.

### For Developers
Old imports:
```python
from castroix import MediaService, CastroixApp
```

New imports:
```python
from castroix_package import MediaService, ConfigManager
from castroix_package.app import CastroixApp
```

## Performance Considerations

### Lazy Imports
GUI components are imported lazily to avoid tkinter dependency at import time.

### Resource Management
- Icons are loaded on-demand
- Processes are tracked for cleanup
- Configuration is cached in memory

### Startup Time
Modular structure has minimal impact on startup time due to lazy imports.

## Security Considerations

### Command Execution
- Commands are executed via subprocess with shell=True
- User is responsible for command validation
- Future: Add command validation/sanitization

### Configuration
- JSON configuration is user-editable
- Stored in application directory
- No sensitive data should be stored

## Conclusion

The refactored architecture provides a solid foundation for future development while maintaining backward compatibility. The modular structure improves code quality, testability, and maintainability without changing the user experience.
