# Castroix Architecture

## Overview

Castroix is a modern desktop application built with Electron, providing a premium media streaming hub experience. The application features an Apple TV-like interface with embedded browser capabilities and secure credential management.

## Technology Stack

- **Electron** - Cross-platform desktop framework
- **Node.js** - Backend runtime
- **HTML/CSS/JavaScript** - UI layer
- **electron-store** - Secure credential storage

## Architecture Layers

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

## File Structure

```
castroix/
├── main.js              # Electron main process
├── preload.js           # IPC bridge (secure)
├── index.html           # Main UI
├── styles.css           # Apple TV-like styles
├── renderer.js          # UI logic
├── package.json         # Node.js config
├── config.json          # Service config
├── castroix-electron.sh # Launch script
├── tests/               # Test files
│   └── test_electron.js # Test suite
└── images/              # Service icon images
    └── *.png            # PNG icon files
```

## Key Components

### Main Process (main.js)

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

### Preload Script (preload.js)

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

### Renderer Process (renderer.js, index.html, styles.css)

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
- Esc to close embedded browser/exit fullscreen
- Ctrl+Q to close embedded browser or last app
- Ctrl+S to open credentials manager

## Apple TV-like UI Design

### Visual Design

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

### Animations

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

## Configuration System

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
      "icon_file": "images/icon.png"
    }
  }
}
```

### Configuration Loading

1. Application starts
2. Main process reads `config.json`
3. Configuration is provided to renderer via IPC
4. Renderer creates service cards dynamically

## Credential Management

### Storage

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

### Auto-Login Flow

1. User launches service
2. Check for stored credentials
3. If found, credentials are available for injection
4. Service-specific login automation (framework in place)

## Embedded Browser

### Technology

**BrowserView:** Electron's native browser component

**Features:**
- Full web browser capabilities
- Fullscreen by default
- Auto-resize with window
- Session persistence
- Cookie/storage support

### Integration

1. Service URL loaded in BrowserView
2. BrowserView attached to main window
3. Covers entire window area
4. Esc key detaches and returns home
5. Credentials available for injection

### Implementation

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

// Handle keyboard shortcuts via before-input-event
// This is necessary because global shortcuts don't work when BrowserView has focus
currentBrowserView.webContents.on('before-input-event', (event, input) => {
  if (input.type === 'keyDown' && input.key === 'Escape') {
    event.preventDefault();
    closeBrowserView();
  }
  if (input.type === 'keyDown' && input.key === 'q' && (input.control || input.meta)) {
    event.preventDefault();
    closeBrowserView();
  }
});
```

### Keyboard Shortcut Handling

When a BrowserView is active and has focus, global shortcuts registered with `globalShortcut.register()` may not work reliably because the BrowserView captures keyboard events before they reach the global shortcut handler. To solve this, we use the `before-input-event` listener on the BrowserView's webContents to intercept keyboard shortcuts before they're processed by the web page. This ensures that Escape and Ctrl+Q (or Cmd+Q on macOS) consistently close the embedded browser regardless of what web page is loaded.

## Service Launching

### URL-based Services

1. User selects service with URL
2. Embedded browser opens fullscreen
3. Service loads in BrowserView
4. User can return home with Esc

### Command-based Services

1. User selects service with command
2. Command executed via child_process
3. External application launches
4. Process tracked for cleanup

### Platform Support

- Windows: PowerShell commands, Windows Store apps
- macOS: Open commands, app bundles
- Linux: Shell commands, Flatpak, Snap

## Security

### Electron Security Best Practices

1. **Context Isolation:** ✅ Enabled
2. **Node Integration:** ✅ Disabled in renderer
3. **Preload Script:** ✅ Used for safe IPC
4. **Content Security Policy:** ⚠️ Consider adding
5. **Remote Module:** ✅ Not used
6. **Credential Encryption:** ✅ Enabled

### Credential Security

- Encrypted at rest using electron-store
- Never sent over network
- Only accessible through IPC
- Can be deleted by user anytime

### Command Execution

- Commands executed via child_process
- User responsible for command safety
- No command validation currently (future enhancement)

## Testing

### Test Suite (tests/test_electron.js)

**Test Categories:**
1. File structure validation
2. Configuration loading
3. Service validation
4. HTML structure checks
5. Keyboard shortcut implementation

**Running Tests:**
```bash
npm test
```

All tests must pass before deployment.

## Performance

### Startup Time

- Cold start: ~2-3 seconds
- Warm start: ~1-2 seconds
- Main window appears immediately
- Services load on demand

### Memory Usage

- Initial: ~150-200 MB (Electron overhead)
- With embedded browser: +100-200 MB per service
- Efficient for a full-featured media hub

### Optimization Strategies

1. Lazy loading of services
2. Icon caching
3. CSS animations using GPU
4. Efficient DOM manipulation

## Development Workflow

### Making Changes

1. Edit source files (main.js, renderer.js, etc.)
2. Save changes
3. Run `npm start` to test
4. Run `npm test` to validate
5. Commit changes

### Adding New Features

1. Plan feature architecture
2. Update relevant files (main, preload, renderer)
3. Add tests if applicable
4. Update documentation
5. Test thoroughly

### Debugging

**Developer Tools:**
- Press `Ctrl+Shift+I` in the app to open DevTools
- Console logs appear in DevTools console
- Inspect elements and network requests

**Main Process Debugging:**
- Add console.log statements to main.js
- Check terminal output where `npm start` was run

## Future Enhancements

### Potential Improvements

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

5. **Distribution**
   - Auto-updates
   - Signed installers
   - App store distribution

## Building and Distribution

### Creating Installers

Use electron-builder to create platform-specific installers:

```bash
npm install --save-dev electron-builder
npm run build
```

### Platform-Specific Considerations

**Windows:**
- Create .exe installer
- Consider code signing
- Include auto-updater

**MacOS:**
- Create .dmg or .app
- Code signing required for distribution
- Notarization for Gatekeeper

**Linux:**
- Create .deb, .rpm, or AppImage
- Desktop file integration
- Icon theme support

## Maintenance

### Regular Tasks

1. Keep Electron version updated
2. Update dependencies regularly
3. Monitor security advisories
4. Test on all platforms
5. Update documentation

### Version Control

- Follow semantic versioning
- Tag releases appropriately
- Maintain changelog
- Document breaking changes

## Contributing

### Code Style

- Use consistent indentation (2 spaces)
- Comment complex logic
- Follow existing patterns
- Keep functions focused

### Pull Request Process

1. Fork repository
2. Create feature branch
3. Make changes with tests
4. Update documentation
5. Submit pull request

## Conclusion

Castroix's Electron architecture provides a modern, secure, and extensible foundation for a premium media streaming hub experience. The architecture emphasizes:

- **Security:** Encrypted credentials, context isolation
- **Performance:** Smooth animations, efficient rendering
- **Extensibility:** Easy to add services and features
- **Maintainability:** Clear separation of concerns
- **User Experience:** Apple TV-like UI, keyboard navigation

This architecture supports the current feature set while providing a solid foundation for future enhancements.
