# Castroix

Media Hub for Multi-Media Consumption

A lightweight Linux desktop application for launching and accessing popular media streaming services including Plex, Jellyfin, Netflix, and Disney+.

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

2. Copy the Sample Config:
```bash
cp comfig.json.sample config.json
```
  
3. Make the script executable (optional):
```bash
chmod +x castroix.py
```

## Usage

### Running the Application

```bash
python3 castroix.py
```

Or if you made it executable:
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
      "icon_color": "#e5a00d"
    },
    "jellyfin": {
      "name": "Jellyfin",
      "url": "http://localhost:8096",
      "command": null,
      "icon_color": "#00a4dc"
    }
  }
}
```

**Configuration Options:**
- `name`: Display name for the service
- `url`: Web URL to open (opened in default browser)
- `command`: Shell command to execute (for native apps) - takes precedence over URL
- `icon_color`: Hex color code for the service tile

**Examples:**

For a local Jellyfin server:
```json
"jellyfin": {
  "name": "Jellyfin",
  "url": "http://192.168.1.100:8096",
  "command": null,
  "icon_color": "#00a4dc"
}
```

For a native Plex app:
```json
"plex": {
  "name": "Plex",
  "url": null,
  "command": "flatpak run tv.plex.PlexDesktop",
  "icon_color": "#e5a00d"
}
```

### Creating a Desktop Launcher

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

## Screenshots

The application features a clean, dark-themed interface with color-coded tiles for each streaming service.

## Development

### Project Structure

```
castroix/
├── castroix.py        # Main application file
├── config.json        # Configuration file
├── requirements.txt   # Python dependencies (none required)
└── README.md         # This file
```

### Adding New Services

To add a new streaming service, edit `config.json` and add a new entry under `services`:

```json
"hulu": {
  "name": "Hulu",
  "url": "https://www.hulu.com",
  "command": null,
  "icon_color": "#1ce783"
}
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
