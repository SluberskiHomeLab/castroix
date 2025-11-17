# Castroix Electron Edition

## Overview

Castroix has been upgraded with a modern **Electron-based interface** featuring Apple TV-like UI, automatic credentials, and embedded browser functionality.

## New Features

### 🎨 Apple TV-like UI
- **Smooth Animations** - Fluid transitions and hover effects
- **Modern Design** - Gradient backgrounds, glass morphism effects
- **Focus Navigation** - Full keyboard/remote control support with arrow keys
- **Card-based Layout** - Beautiful service tiles with icons and colors
- **Responsive Grid** - Adapts to screen size automatically

### 🔐 Automatic Credentials
- **Secure Storage** - Credentials encrypted using electron-store
- **Auto-Login** - Automatically fills credentials for streaming services
- **Per-Service Management** - Individual credential storage for each service
- **Easy Management** - Press `Ctrl+S` to open credential manager

### 🌐 Embedded Browser
- **In-App Browsing** - Full web browser built into the application
- **No External Windows** - Services open within Castroix
- **Seamless Experience** - Navigate between home and services smoothly
- **Browser Controls** - Back, forward, refresh functionality

## Installation

### Prerequisites

- **Node.js** 16.x or higher
- **npm** (comes with Node.js)
- Python 3.6+ (for backward compatibility with Python modules)

### Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies (optional, for Python scripts)
pip install -r requirements.txt
```

## Usage

### Starting Castroix

```bash
npm start
```

This will launch the Electron app in fullscreen mode.

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `↑↓←→` | Navigate between services |
| `Enter` | Launch selected service |
| `Esc` | Close embedded browser / Exit fullscreen |
| `Ctrl+Q` | Close embedded browser or last launched app |
| `Ctrl+S` | Open credentials manager |

### Managing Credentials

1. Press `Ctrl+S` to open the credentials manager
2. Select a service from the dropdown
3. Enter your username/email and password
4. Click "Save" to store credentials securely
5. Next time you launch that service, credentials will auto-fill

### Configuration

The application uses the same `config.json` file as before:

```json
{
  "services": {
    "plex": {
      "name": "Plex",
      "url": "https://app.plex.tv",
      "command": null,
      "icon_color": "#e5a00d",
      "icon_file": "plex.png"
    }
  }
}
```

**Configuration Options:**
- `name`: Display name for the service
- `url`: Web URL to open (will open in embedded browser)
- `command`: Shell command to execute (opens externally)
- `icon_color`: Hex color code for the service card background
- `icon_file`: Path to icon image (PNG recommended)

## Features in Detail

### Apple TV-like UI

The interface is inspired by Apple TV's design language:

- **Focus States**: Services scale up and glow when focused
- **Smooth Animations**: All interactions use smooth CSS transitions
- **Modern Typography**: Clean, readable fonts with proper hierarchy
- **Dark Theme**: Eye-friendly dark theme optimized for TV/projector viewing
- **Visual Feedback**: Hover and click states provide clear feedback

### Embedded Browser

When you launch a service with a URL:
1. The embedded browser opens fullscreen
2. Your saved credentials are available for auto-login
3. Press `Esc` to return to the home screen
4. Browser state is preserved while navigating

### Secure Credential Storage

Credentials are stored using `electron-store` with encryption:
- Credentials never stored in plain text
- Each service has separate credential storage
- Credentials persist across app restarts
- Can be deleted at any time from the manager

## Architecture

### Electron Processes

**Main Process** (`main.js`)
- Window management
- Configuration loading
- IPC communication
- Credential storage
- Service launching

**Preload Script** (`preload.js`)
- Secure bridge between main and renderer
- Exposes safe APIs to renderer

**Renderer Process** (`renderer.js`)
- UI interactions
- Keyboard navigation
- Service card management
- Modal handling

### Files

```
castroix/
├── main.js              # Electron main process
├── preload.js           # Preload script for IPC
├── index.html           # Main UI HTML
├── styles.css           # Apple TV-like styles
├── renderer.js          # UI logic and interactions
├── package.json         # Node.js dependencies
├── config.json          # Service configuration
└── *.png                # Service icons
```

## Building for Production

### Package the Application

To create distributable packages:

```bash
# Install electron-builder
npm install --save-dev electron-builder

# Build for current platform
npm run build

# Build for specific platforms
npm run build:win     # Windows
npm run build:mac     # macOS
npm run build:linux   # Linux
```

Add these scripts to `package.json`:

```json
"scripts": {
  "build": "electron-builder",
  "build:win": "electron-builder --win",
  "build:mac": "electron-builder --mac",
  "build:linux": "electron-builder --linux"
}
```

## Troubleshooting

### Issue: Services not launching
- Check that URLs are valid in `config.json`
- Verify network connectivity
- Check console for error messages

### Issue: Credentials not saving
- Ensure app has write permissions
- Check electron-store configuration
- Verify encryption key is set

### Issue: Icons not showing
- Confirm icon files exist in project root
- Check file paths in `config.json`
- Ensure icons are in PNG format

### Issue: Black screen on startup
- Try deleting `config.json` to reset
- Check console for JavaScript errors
- Verify all files are present

## Comparison: Python vs Electron

| Feature | Python (Tkinter) | Electron |
|---------|------------------|----------|
| UI Framework | Tkinter | HTML/CSS/JS |
| Animations | Limited | Smooth, CSS-based |
| Browser Integration | External | Embedded |
| Credential Storage | None | Encrypted storage |
| Modern UI | Basic | Apple TV-like |
| Cross-platform | Yes | Yes |
| Package Size | Small (~1MB) | Large (~100MB) |

## Migration from Python Version

The Electron version is a complete rewrite but maintains compatibility:

1. **Config files** - Same `config.json` format
2. **Icons** - Same icon files work
3. **Services** - All existing services work
4. **Commands** - External commands still supported

To use the old Python version:
```bash
python castroix.py
```

To use the new Electron version:
```bash
npm start
```

## Development

### Adding New Services

Edit `config.json` and add a new service:

```json
"hulu": {
  "name": "Hulu",
  "url": "https://www.hulu.com",
  "command": null,
  "icon_color": "#1ce783",
  "icon_file": "hulu.png"
}
```

### Customizing the UI

- **Colors**: Edit `styles.css` to change color schemes
- **Layout**: Modify grid settings in `styles.css`
- **Animations**: Adjust CSS transitions and keyframes
- **Fonts**: Change font-family in `styles.css`

## Security Considerations

- Credentials are encrypted at rest
- No credentials sent over network
- Content Security Policy enabled
- Context isolation active
- Node integration disabled in renderer

## Future Enhancements

Potential improvements:
- [ ] Voice control integration
- [ ] Multi-profile support
- [ ] Recently watched tracking
- [ ] Service health monitoring
- [ ] Custom themes
- [ ] Plugin system

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- GitHub Issues: https://github.com/SluberskiHomeLab/castroix/issues
- Discussions: https://github.com/SluberskiHomeLab/castroix/discussions
