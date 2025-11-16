# Castroix Architecture

## Overview

Castroix has been refactored from a monolithic single-file application into a modular Python package with clear separation of concerns. This document describes the architecture and rationale behind the design decisions.

## Architecture Principles

### 1. Separation of Concerns
Each module has a single, well-defined responsibility:
- **Configuration** - Managing application settings
- **Services** - Business logic for media services
- **UI** - User interface presentation

### 2. Modularity
The codebase is organized into distinct modules that can be:
- Tested independently
- Modified without affecting other components
- Reused in other projects

### 3. Backward Compatibility
The original `castroix.py` file remains as a thin wrapper, ensuring existing users can continue using the application without changes.

## Package Structure

```
castroix/
├── castroix/              # Main package
│   ├── __init__.py        # Package initialization and exports
│   ├── __main__.py        # Entry point for `python -m castroix`
│   ├── config.py          # Configuration management
│   ├── services.py        # Service definitions and launching
│   └── ui.py              # User interface components
├── castroix.py            # Backward-compatible wrapper (28 lines)
├── test_castroix.py       # Original test suite (12 tests)
└── test_modular_architecture.py  # Modular tests (13 tests)
```

## Module Descriptions

### config.py (106 lines)

**Purpose**: Manage application configuration

**Key Classes**:
- `ConfigManager` - Handles loading, saving, and accessing configuration

**Responsibilities**:
- Load configuration from JSON file
- Provide default configuration
- Save configuration changes
- Expose services configuration to other modules

**Benefits**:
- Single source of truth for configuration
- Easy to test configuration logic
- Configuration can be used without UI

### services.py (152 lines)

**Purpose**: Define media services and handle launching

**Key Classes**:
- `MediaService` - Represents a single streaming service
- `ServiceManager` - Manages collection of services

**Responsibilities**:
- Store service properties (name, URL, command, colors, icons)
- Launch services via URL or command
- Handle platform-specific browser detection
- Provide service collection management

**Benefits**:
- Business logic isolated from UI
- Easy to add new service types
- Platform-specific code is contained
- Can be tested without GUI

### ui.py (240 lines)

**Purpose**: Provide user interface

**Key Classes**:
- `CastroixUI` - Main application window

**Responsibilities**:
- Create and manage Tkinter widgets
- Handle user interactions
- Display services as buttons
- Manage launched processes
- Provide keyboard shortcuts

**Benefits**:
- UI code separated from business logic
- Can swap UI framework without changing business logic
- UI components can be tested independently
- PIL/Pillow made optional for headless environments

## Design Decisions

### Why Separate Configuration?

**Before**: Configuration logic mixed with application logic
**After**: Dedicated `ConfigManager` class

**Rationale**:
- Configuration can be tested independently
- Other tools can use the same configuration
- Easier to add configuration validation
- Clear responsibility boundary

### Why Separate Services?

**Before**: Service launching embedded in UI code
**After**: Dedicated `MediaService` and `ServiceManager` classes

**Rationale**:
- Business logic independent of UI framework
- Can launch services from CLI or other interfaces
- Easier to add new service types
- Platform-specific code contained in one place

### Why Keep castroix.py?

**Rationale**:
- Maintains backward compatibility
- Users can still run `python castroix.py`
- No breaking changes for existing users
- Demonstrates how to use the package

### Why Optional PIL/Tkinter?

**Rationale**:
- Allows testing in headless environments
- Core logic can be used without GUI
- More flexible deployment options
- Better error handling

## Benefits of New Architecture

### Improved Code Quality
- **Reduced Complexity**: Main file reduced from 361 to 28 lines (92% reduction)
- **Single Responsibility**: Each module has one clear purpose
- **Better Organization**: Related code grouped together

### Enhanced Testability
- **Independent Testing**: Each module can be tested separately
- **More Tests**: Added 13 new tests (108% increase)
- **Better Coverage**: Can test components without GUI

### Easier Maintenance
- **Clear Boundaries**: Know where to make changes
- **Isolated Changes**: Modifications don't ripple through codebase
- **Better Documentation**: Each module is self-documenting

### Greater Extensibility
- **Plugin Architecture**: Easy to add new service types
- **Customization**: Users can import and customize components
- **Reusability**: Components can be used in other projects

### Professional Structure
- **Standard Package**: Follows Python packaging best practices
- **Proper Exports**: Clean public API via `__init__.py`
- **Module Entry Point**: Can run with `python -m castroix`
- **Version Management**: Centralized version number

## Usage Examples

### Direct Execution (Backward Compatible)
```bash
python castroix.py
```

### Module Execution
```bash
python -m castroix
```

### Programmatic Usage
```python
from castroix import ConfigManager, ServiceManager, CastroixUI
import tkinter as tk

# Load configuration
config_manager = ConfigManager()
services_config = config_manager.get_services()

# Create services
service_manager = ServiceManager(services_config)
services = service_manager.get_services()

# Create UI
root = tk.Tk()
app = CastroixUI(root, services)
app.run()
```

### Custom Configuration
```python
from castroix import ConfigManager
from pathlib import Path

# Use custom config location
config = ConfigManager(Path("/custom/path/config.json"))
services = config.get_services()
```

### Headless Service Management
```python
from castroix import ServiceManager

# Define services programmatically
services_config = {
    "plex": {
        "name": "Plex",
        "url": "https://app.plex.tv",
        "icon_color": "#e5a00d"
    }
}

# Create and launch services without UI
manager = ServiceManager(services_config)
services = manager.get_services()
services[0].launch()
```

## Testing Strategy

### Unit Tests
- Test individual classes and methods
- Mock dependencies to isolate components
- Verify expected behavior

### Integration Tests
- Test full flow from config to UI
- Verify components work together
- Ensure backward compatibility

### Test Organization
- `test_castroix.py` - Original tests (backward compatibility)
- `test_modular_architecture.py` - New modular tests

## Future Enhancements

The modular architecture enables future improvements:

1. **Plugin System**: Easy to add plugin support for custom services
2. **CLI Interface**: Add command-line interface alongside GUI
3. **Web Interface**: Create web-based UI using same services layer
4. **Service Discovery**: Auto-discover installed media applications
5. **Themes**: Add theme support without changing business logic
6. **Configuration GUI**: Build settings UI using same config module
7. **Remote Control**: Add network control without GUI changes

## Migration Guide

### For Users
No changes required! Continue using `python castroix.py` as before.

### For Developers
To work with the new architecture:
1. Import from `castroix` package instead of main file
2. Use `ConfigManager` for configuration
3. Use `ServiceManager` for service management
4. Use `CastroixUI` for UI components

### For Contributors
When adding features:
1. Determine which module is responsible
2. Add code to the appropriate module
3. Add tests to verify behavior
4. Update documentation if needed

## Conclusion

The new modular architecture provides a solid foundation for future development while maintaining full backward compatibility. The separation of concerns makes the codebase more maintainable, testable, and extensible, following Python best practices and professional software engineering principles.
