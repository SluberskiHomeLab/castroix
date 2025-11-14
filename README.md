# Castroix

Media Hub for Multi-Media Consumption

A lightweight cross-platform desktop application for launching and accessing popular media streaming services including Plex, Jellyfin, Netflix, and Disney+. Works on Windows, Linux, and MacOS.

## Features

- 🎬 Quick access to multiple media streaming services
- 🖥️ Clean, modern GUI interface
- ⚙️ Configurable service URLs and commands
- 🚀 Lightweight - uses only Python standard library
- 🎨 Color-coded service tiles

## Supported Services

- **Plex** - Personal media server
- **Jellyfin** - Free software media system
- **Netflix** - Streaming service
- **Disney+** - Disney streaming service

## Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python)
- Pillow (PIL) library for image handling (optional but recommended for icon display)

### Platform-Specific Setup

#### Windows
Tkinter is typically included with Python installations from python.org. If needed, ensure you select "tcl/tk and IDLE" during Python installation.

#### MacOS
Tkinter is included with Python installations. If using Homebrew Python:
```bash
brew install python-tk
```

#### Linux
On most Linux distributions, Tkinter is included by default. If needed, install it:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S tk
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SluberskiHomeLab/castroix.git
cd castroix
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
   
   **Note:** If you skip this step, the application will still work but without icon images. Service buttons will display text labels instead.

3. Copy the Sample Config:

**Windows (PowerShell):**
```powershell
Copy-Item config.json.sample config.json
```

**Linux/MacOS:**
```bash
cp config.json.sample config.json
```
  
4. Make the script executable (Linux/MacOS only):
```bash
chmod +x castroix.py
```

## Usage

### Running the Application

**Windows:**
```cmd
python castroix.py
```

**Linux/MacOS:**
```bash
python3 castroix.py
```

Or if you made it executable (Linux/MacOS):
```bash
./castroix.py
```

### Configuration

The application uses a `config.json` file to store service configurations. This file is automatically created on first run with default settings.

You can customize the configuration by editing `config.json`:

```json
{
  "services": {
    "plex": {
      "name": "Plex",
      "url": "https://app.plex.tv",
      "command": null,
      "icon_color": "#e5a00d",
      "icon_file": "plex.png"
    },
    "jellyfin": {
      "name": "Jellyfin",
      "url": "http://localhost:8096",
      "command": null,
      "icon_color": "#00a4dc",
      "icon_file": "jellyfin.png"
    }
  }
}
```

**Configuration Options:**
- `name`: Display name for the service (shown below the button)
- `url`: Web URL to open (opened in default browser)
- `command`: Shell command to execute (for native apps) - takes precedence over URL
- `icon_color`: Hex color code for the button background
- `icon_file`: Path to PNG icon file (placed in project root, e.g., "plex.png")

**Examples:**

For a local Jellyfin server:
```json
"jellyfin": {
  "name": "Jellyfin",
  "url": "http://192.168.1.100:8096",
  "command": null,
  "icon_color": "#00a4dc",
  "icon_file": "jellyfin.png"
}
```

For a native Plex app (Linux):
```json
"plex": {
  "name": "Plex",
  "url": null,
  "command": "flatpak run tv.plex.PlexDesktop",
  "icon_color": "#e5a00d",
  "icon_file": "plex.png"
}
```

For Windows Store apps (Netflix):
```json
"netflix": {
  "name": "Netflix",
  "url": null,
  "command": "start shell:AppsFolder\\4DF9E0F8.Netflix_mcm4njqhnhss8!Netflix.App",
  "icon_color": "#e50914",
  "icon_file": "netflix.png"
}
```

For Windows Store apps (Disney+):
```json
"disneyplus": {
  "name": "Disney+",
  "url": null,
  "command": "start shell:AppsFolder\\Disney.37853FC22B2CE_6rarf9sa4v8jt!App",
  "icon_color": "#113ccf",
  "icon_file": "disney+.png"
}
```

For Windows Store apps (Plex):
```json
"plex": {
  "name": "Plex",
  "url": null,
  "command": "start shell:AppsFolder\\CAF9E577.PlexforWindows_aam28m9va5cke!Plex",
  "icon_color": "#e5a00d",
  "icon_file": "plex.png"
}
```

For traditional Windows executables:
```json
"vlc": {
  "name": "VLC",
  "url": null,
  "command": "\"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe\"",
  "icon_color": "#ff8800",
  "icon_file": "vlc.png"
}
```

**Finding Windows Store App IDs:**

To find the Application User Model ID (AUMID) for Windows Store apps:

1. Open PowerShell and run:
```powershell
Get-StartApps | Where-Object {$_.Name -like "*AppName*"}
```

2. Look for the `AppID` column in the results. For example:
```
Name                                          AppID
----                                          -----
Netflix                                       4DF9E0F8.Netflix_mcm4njqhnhss8!Netflix.App
Disney+                                       Disney.37853FC22B2CE_6rarf9sa4v8jt!App
```

3. Use the AppID in your config with the `start shell:AppsFolder\` prefix:
```json
"command": "start shell:AppsFolder\\AppID_Here"
```

**Note:** Remember to escape backslashes in JSON by using `\\` instead of `\`.

### Creating a Desktop Launcher

#### Windows
Create a shortcut:
1. Right-click on `castroix.py` and select "Create shortcut"
2. Move the shortcut to your Desktop or Start Menu folder
3. Optionally, right-click the shortcut, go to Properties, and set a custom icon

#### Linux
To add Castroix to your application menu, create a `.desktop` file:

1. Create the file:
```bash
nano ~/.local/share/applications/castroix.desktop
```

2. Add the following content (adjust paths as needed):
```ini
[Desktop Entry]
Name=Castroix
Comment=Media Hub for Multi-Media Consumption
Exec=/usr/bin/python3 /path/to/castroix/castroix.py
Icon=video-display
Terminal=false
Type=Application
Categories=AudioVideo;Video;Player;
```

3. Make it executable:
```bash
chmod +x ~/.local/share/applications/castroix.desktop
```

#### MacOS
Create an app bundle or use Automator:
1. Open Automator
2. Create a new "Application"
3. Add "Run Shell Script" action
4. Enter: `/usr/bin/python3 /path/to/castroix/castroix.py`
5. Save the application to your Applications folder

## Screenshots

The application features a clean, dark-themed interface with color-coded tiles for each streaming service.

## Development

### Project Structure

```
castroix/
├── castroix.py        # Main application file
├── config.json        # Configuration file
├── requirements.txt   # Python dependencies
├── plex.png          # Service icon files
├── jellyfin.png
├── netflix.png
├── disney+.png
└── README.md         # This file
```

### Adding New Services

To add a new streaming service:

1. Create a PNG icon file (128x128 recommended) and place it in the project root (e.g., `hulu.png`)
2. Edit `config.json` and add a new entry under `services`:

```json
"hulu": {
  "name": "Hulu",
  "url": "https://www.hulu.com",
  "command": null,
  "icon_color": "#1ce783",
  "icon_file": "hulu.png"
}
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
