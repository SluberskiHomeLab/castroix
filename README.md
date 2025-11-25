#Castroix has now been moved to forgejo.  This repository is archived on Github.  Any future development will be done at the below link  

Forgejo Repo: https://git.sluberskihomelab.com/Public/castroix

# Castroix

Media Hub for Multi-Media Consumption

A cross-platform desktop application for launching and accessing popular media streaming services including Plex, Jellyfin, Netflix, and Disney+. Built with Electron featuring an Apple TV-like interface. Works on Windows, Linux, and MacOS.

## Features

- 🎨 **Apple TV-like UI** - Smooth animations, modern design, focus navigation
- 🔐 **Secure Credentials** - Encrypted storage with auto-login support
- 🌐 **Embedded Browser** - Full web browser wrapped in the application
- 🎬 **Multi-Service Support** - Quick access to multiple streaming services
- ⌨️ **Keyboard Navigation** - Full arrow key navigation and shortcuts
- ⚙️ **Configurable** - Customize service URLs, commands, and appearance
- 🎨 **Color-Coded Tiles** - Beautiful service cards with custom colors
- 🖼️ **Icon Support** - PNG icon display for each service

## Quick Start

### Automated Setup (Recommended)

The easiest way to get started is using the automated setup script:

**Linux/macOS:**
```bash
# Clone the repository
git clone https://github.com/SluberskiHomeLab/castroix.git
cd castroix

# Run the setup script
./setup.sh
```

**Windows (PowerShell - Recommended):**
```powershell
# Clone the repository
git clone https://github.com/SluberskiHomeLab/castroix.git
cd castroix

# Run the setup script
.\setup.ps1
```

**Windows (Command Prompt):**
```cmd
REM Clone the repository
git clone https://github.com/SluberskiHomeLab/castroix.git
cd castroix

REM Run the setup script
setup.bat
```

The setup script will:
- Detect your operating system
- Check if Node.js and npm are installed
- Install Node.js and npm if needed (or provide instructions)
- Install all dependencies
- Create config.json from the sample
- Ask if you want to launch the app

### Manual Setup

If you prefer to set up manually:

```bash
# Clone and install
git clone https://github.com/SluberskiHomeLab/castroix.git
cd castroix
npm install

# Run
npm start
```

## Supported Services

- **Plex** - Personal media server
- **Jellyfin** - Free software media system
- **Netflix** - Streaming service
- **Disney+** - Disney streaming service

## Requirements

- **Node.js** 16.x or higher
- **npm** (comes with Node.js)

## Installation

### Automated Installation (Recommended)

The easiest way to install Castroix is using the automated setup scripts. See the [Quick Start](#quick-start) section above for instructions.

### Manual Installation

If you prefer manual installation or the automated script doesn't work for your system:

#### Prerequisites

Install Node.js from [nodejs.org](https://nodejs.org/) or use your package manager:

**Ubuntu/Debian:**
```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Fedora:**
```bash
sudo dnf install nodejs
```

**MacOS (Homebrew):**
```bash
brew install node
```

**Windows:**
Download and install from [nodejs.org](https://nodejs.org/)

#### Install Dependencies

```bash
cd castroix
npm install
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
5. Next time you launch that service, credentials will be available for auto-fill

### Configuration

The application uses a `config.json` file to store service configurations. Copy the sample configuration:

```bash
cp config.json.sample config.json
```

Edit `config.json` to customize services:

```json
{
  "services": {
    "plex": {
      "name": "Plex",
      "url": "https://app.plex.tv",
      "command": null,
      "icon_color": "#e5a00d",
      "icon_file": "images/plex.png"
    },
    "jellyfin": {
      "name": "Jellyfin",
      "url": "http://localhost:8096",
      "command": null,
      "icon_color": "#00a4dc",
      "icon_file": "images/jellyfin.png"
    }
  }
}
```

**Configuration Options:**
- `name`: Display name for the service
- `url`: Web URL to open (will open in embedded browser)
- `command`: Shell command to execute (opens externally, takes precedence over URL)
- `icon_color`: Hex color code for the service card background
- `icon_file`: Path to icon image (PNG recommended, place in project root)

**Examples:**

For a local Jellyfin server:
```json
"jellyfin": {
  "name": "Jellyfin",
  "url": "http://192.168.1.100:8096",
  "command": null,
  "icon_color": "#00a4dc",
  "icon_file": "images/jellyfin.png"
}
```

For Windows Store apps (Netflix):
```json
"netflix": {
  "name": "Netflix",
  "url": null,
  "command": "start shell:AppsFolder\\4DF9E0F8.Netflix_mcm4njqhnhss8!Netflix.App",
  "icon_color": "#e50914",
  "icon_file": "images/netflix.png"
}
```

**Finding Windows Store App IDs:**

Open PowerShell and run:
```powershell
Get-StartApps | Where-Object {$_.Name -like "*AppName*"}
```

Use the AppID in your config with the `start shell:AppsFolder\` prefix (escape backslashes with `\\` in JSON).

### Adding New Services

To add a new streaming service:

1. Create a PNG icon file (128x128 recommended) and place it in the `images` folder
2. Edit `config.json` and add a new entry under `services`:

```json
"hulu": {
  "name": "Hulu",
  "url": "https://www.hulu.com",
  "command": null,
  "icon_color": "#1ce783",
  "icon_file": "images/hulu.png"
}
```

### Creating a Desktop Launcher

#### Linux

Create a `.desktop` file:

```bash
nano ~/.local/share/applications/castroix.desktop
```

Add the following content (adjust paths as needed):
```ini
[Desktop Entry]
Name=Castroix
Comment=Media Hub for Multi-Media Consumption
Exec=/path/to/castroix/castroix-electron.sh
Icon=video-display
Terminal=false
Type=Application
Categories=AudioVideo;Video;Player;
StartupNotify=true
```

Make it executable:
```bash
chmod +x ~/.local/share/applications/castroix.desktop
```

#### Windows

Create a shortcut to `castroix-electron.sh` or use the `npm start` command in a batch file:

1. Create `castroix.bat` with:
```batch
@echo off
cd /d "%~dp0"
npm start
```

2. Right-click and create a shortcut
3. Move the shortcut to your Desktop or Start Menu

#### MacOS

Create an app bundle or use Automator:

1. Open Automator
2. Create a new "Application"
3. Add "Run Shell Script" action
4. Enter: `cd /path/to/castroix && npm start`
5. Save the application to your Applications folder

## Architecture

### Electron Processes

**Main Process** (`main.js`)
- Window management
- Configuration loading
- IPC communication
- Credential storage (encrypted with electron-store)
- Service launching

**Preload Script** (`preload.js`)
- Secure bridge between main and renderer processes
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
├── castroix-electron.sh # Launch script
├── tests/               # Test files
│   └── test_electron.js # Test suite
└── images/              # Service icon images
    └── *.png            # PNG icon files
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

## Development

### Running Tests

```bash
npm test
```

This runs the test suite in `tests/test_electron.js` which validates:
- Required files exist
- Configuration is valid
- Service configurations are correct
- HTML structure is proper
- Keyboard shortcuts are implemented

### Customizing the UI

- **Colors**: Edit `styles.css` to change color schemes
- **Layout**: Modify grid settings in `styles.css`
- **Animations**: Adjust CSS transitions and keyframes
- **Fonts**: Change font-family in `styles.css`

## Troubleshooting

### Issue: Services not launching
- Check that URLs are valid in `config.json`
- Verify network connectivity
- Check console for error messages (`Ctrl+Shift+I` to open dev tools)

### Issue: Credentials not saving
- Ensure app has write permissions in its directory
- Check electron-store configuration
- Verify encryption key is set

### Issue: Icons not showing
- Confirm icon files exist in the `images` folder
- Check file paths in `config.json`
- Ensure icons are in PNG format

### Issue: Black screen on startup
- Try deleting `config.json` and copying from `config.json.sample`
- Check console for JavaScript errors
- Verify all files are present

### Issue: Cannot install dependencies
- Ensure Node.js and npm are properly installed
- Try deleting `node_modules` and `package-lock.json`, then run `npm install` again
- Check npm logs for specific errors

## Security Considerations

- Credentials are encrypted at rest using electron-store
- No credentials sent over network
- Context isolation enabled
- Node integration disabled in renderer process
- All IPC communication goes through secure preload bridge

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
