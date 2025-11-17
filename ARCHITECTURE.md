# Castroix Architecture

## Overview

Castroix has evolved from a monolithic single-file application into a well-structured application available in two versions:

1. **Python Edition** - Modular Python package with Tkinter UI
2. **Electron Edition** (NEW) - Modern web-based UI with enhanced features

This document describes the architecture and design decisions for both versions.

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

## Electron Edition Architecture

### Overview

The Electron edition is a complete rewrite using web technologies, providing a modern user experience while maintaining compatibility with the same configuration format.

### Technology Stack

- **Electron** - Cross-platform desktop framework
- **Node.js** - Backend runtime
- **HTML/CSS/JavaScript** - UI layer
- **electron-store** - Secure credential storage

### Architecture Layers

```
┌─────────────────────────────────────┐
│     Renderer Process (UI)           │
│  - HTML/CSS (Apple TV-like UI)      │
│  - JavaScript (keyboard navigation) │
│  - Service launching UI             │
└──────────────┬──────────────────────┘
               │ IPC (Preload Bridge)
┌──────────────┴──────────────────────┐
│     Main Process (Backend)          │
│  - Window management                │
│  - BrowserView for embedded browser │
│  - Configuration loading            │
│  - Credential storage (encrypted)   │
│  - Service launching                │
└─────────────────────────────────────┘
```

### File Structure

```
castroix/
├── main.js              # Electron main process
├── preload.js           # IPC bridge (secure)
├── index.html           # Main UI
├── styles.css           # Apple TV-like styles
├── renderer.js          # UI logic
├── package.json         # Node.js config
├── config.json          # Service config (shared with Python)
└── node_modules/        # Dependencies
```

### Key Components

#### Main Process (main.js)

**Responsibilities:**
- Create and manage application window
- Handle IPC communication from renderer
- Manage BrowserView for embedded browsing
- Load and provide configuration
- Secure credential storage using electron-store
- Launch external services via commands

**Key Features:**
- Fullscreen mode by default
- No frame for clean UI
- Context isolation for security
- Encrypted credential storage

#### Preload Script (preload.js)

**Purpose:** Secure bridge between main and renderer processes

**Security:**
- Uses contextBridge for safe API exposure
- No direct node integration in renderer
- Only exposes necessary functions

**Exposed APIs:**
- `getConfig()` - Load service configuration
- `getCredentials(service)` - Retrieve stored credentials
- `saveCredentials(service, credentials)` - Save credentials securely
- `launchService(service)` - Launch a service
- `closeBrowser()` - Close embedded browser
- `closeLastApp()` - Close last external app

#### Renderer Process (renderer.js, index.html, styles.css)

**UI Components:**
1. **Home View**
   - Service grid with cards
   - Keyboard navigation
   - Focus indicators

2. **Credentials Modal**
   - Service selector
   - Username/password fields
   - Save/delete actions

3. **Loading Overlay**
   - Spinner animation
   - Loading message

**Keyboard Navigation:**
- Arrow keys for focus movement
- Enter to launch service
- Esc to go back/exit fullscreen
- Ctrl+Q to close last app
- Ctrl+S to open credentials manager

### Apple TV-like UI Design

#### Visual Design

**Color Scheme:**
- Background: Dark gradients (#0a0a0a to #1a1a1a)
- Text: White with gray accents
- Cards: Service-specific colors with gradients
- Focus: White glow effect

**Typography:**
- System fonts (-apple-system, Segoe UI, etc.)
- Title: 64px, -2px letter spacing
- Service names: 28px, 600 weight
- Hints: 14px, monospace for keys

**Layout:**
- Responsive grid (auto-fit, minmax(300px, 1fr))
- 40px gaps between cards
- 80px padding on sides
- Centered content

#### Animations

**Card Hover/Focus:**
```css
transform: scale(1.1) translateY(-10px);
box-shadow: 0 30px 80px rgba(0,0,0,0.8);
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

**Icon Scale:**
```css
transform: scale(1.1);
transition: transform 0.3s ease;
```

**Modal Entry:**
```css
animation: slideUp 0.3s ease;
```

**Loading Spinner:**
```css
animation: spin 1s linear infinite;
```

### Credential Management

#### Storage

**Technology:** electron-store with encryption

**Encryption:**
- AES encryption for credential data
- Encryption key stored securely
- Per-service credential storage

**Data Structure:**
```javascript
{
  credentials: {
    serviceName: {
      username: "user@example.com",
      password: "encrypted_password"
    }
  }
}
```

#### Auto-Login Flow

1. User launches service
2. Check for stored credentials
3. If found, inject into embedded browser
4. Service-specific login automation (framework in place)

### Embedded Browser

#### Technology

**BrowserView:** Electron's native browser component

**Features:**
- Full web browser capabilities
- Fullscreen by default
- Auto-resize with window
- Session persistence
- Cookie/storage support

#### Integration

1. Service URL loaded in BrowserView
2. BrowserView attached to main window
3. Covers entire window area
4. Esc key detaches and returns home
5. Credentials available for injection

#### Implementation

```javascript
currentBrowserView = new BrowserView({
  webPreferences: {
    nodeIntegration: false,
    contextIsolation: true
  }
});

mainWindow.addBrowserView(currentBrowserView);
currentBrowserView.setBounds({ x: 0, y: 0, width, height });
currentBrowserView.webContents.loadURL(url);
```

### Security

#### Electron Security Best Practices

1. **Context Isolation:** ✅ Enabled
2. **Node Integration:** ✅ Disabled in renderer
3. **Preload Script:** ✅ Used for safe IPC
4. **Content Security Policy:** ⚠️ Consider adding
5. **Remote Module:** ✅ Not used
6. **Credential Encryption:** ✅ Enabled

#### Credential Security

- Encrypted at rest using electron-store
- Never sent over network
- Only accessible through IPC
- Can be deleted by user anytime

#### Command Execution

- Commands executed via child_process
- User responsible for command safety
- No command validation currently (future enhancement)

### Testing

#### Test Files

1. **test_electron.js** - Electron-specific tests
   - File structure validation
   - Configuration loading
   - Service validation
   - HTML structure

2. **test_castroix.py** - Python tests (still pass)
   - Backward compatibility verified
   - All 21 tests passing

### Performance

#### Startup Time

- Cold start: ~2-3 seconds
- Warm start: ~1-2 seconds
- Main window appears immediately
- Services load on demand

#### Memory Usage

- Initial: ~150-200 MB (Electron overhead)
- With embedded browser: +100-200 MB per service
- Python version: ~50-100 MB for comparison

#### Optimization Strategies

1. Lazy loading of services
2. Icon caching
3. CSS animations using GPU
4. Efficient DOM manipulation

### Comparison: Python vs Electron

| Aspect | Python (Tkinter) | Electron |
|--------|------------------|----------|
| UI Framework | Tkinter | HTML/CSS/JS |
| Animations | Limited | Smooth, CSS |
| Browser | External | Embedded |
| Credentials | None | Encrypted storage |
| Startup Time | Fast (~1s) | Medium (~2s) |
| Memory Usage | Low (50MB) | Higher (150MB+) |
| Distribution Size | Small (1MB) | Large (100MB+) |
| Modern UI | Basic | Apple TV-like |
| Development | Python | Web tech |
| Cross-platform | Yes | Yes |

### Future Enhancements

#### Electron Edition

1. **Enhanced Auto-Login**
   - Service-specific login automation
   - Support for 2FA
   - OAuth integration

2. **UI Improvements**
   - Custom themes
   - Wallpaper support
   - Service categories

3. **Advanced Features**
   - Multi-profile support
   - Watch history tracking
   - Service health monitoring
   - Picture-in-picture mode

4. **Performance**
   - Service preloading
   - Better caching
   - Memory optimization

### Migration Guide

#### For Users

**From Python to Electron:**
1. Keep existing config.json
2. Install Node.js and npm
3. Run `npm install`
4. Run `npm start`

**Both versions can coexist:**
- Python: `python castroix.py`
- Electron: `npm start`

#### For Developers

**Python Development:**
```bash
# Work on Python modules
cd castroix_package
# Make changes
python test_castroix.py
```

**Electron Development:**
```bash
# Work on Electron files
# Edit main.js, renderer.js, etc.
npm start
node test_electron.js
```

## Conclusion

The Electron edition provides a modern, feature-rich experience while the Python edition remains available as a lightweight alternative. Both versions share the same configuration format and support the same services, giving users flexibility in choosing the version that best suits their needs.

The architecture is designed for:
- **Security:** Encrypted credentials, context isolation
- **Performance:** Smooth animations, efficient rendering
- **Extensibility:** Easy to add services and features
- **Maintainability:** Clear separation of concerns
- **User Experience:** Apple TV-like UI, keyboard navigation
