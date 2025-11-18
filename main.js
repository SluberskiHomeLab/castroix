/**
 * Castroix Electron Main Process
 * Handles window management, IPC communication, and system integration
 */

const { app, BrowserWindow, BrowserView, ipcMain, Menu } = require('electron');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');
const Store = require('electron-store');
const os = require('os');
const crypto = require('crypto');

// Configure Electron command-line switches to prevent GPU/WebGL errors
// These switches help avoid "Exiting GPU process due to errors" and WebGL fallback warnings
// Note: These switches trade some GPU sandboxing security for stability and cleaner logs
// This is acceptable for a media consumption application running trusted content
app.commandLine.appendSwitch('disable-gpu-sandbox');
app.commandLine.appendSwitch('ignore-gpu-blocklist'); // Updated from deprecated 'ignore-gpu-blacklist'
app.commandLine.appendSwitch('disable-software-rasterizer');

// Generate a unique encryption key per installation using machine hostname
const machineId = os.hostname();
const encryptionKey = crypto.createHash('sha256').update(machineId).digest('hex');

// Initialize secure storage for credentials
const store = new Store({
  encryptionKey: encryptionKey
});

let mainWindow;
let currentBrowserView;
let launchedProcesses = [];

// Configuration management
let config = {};

function loadConfig() {
  const configPath = path.join(__dirname, 'config.json');
  try {
    if (fs.existsSync(configPath)) {
      config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    } else {
      // Load default config
      const samplePath = path.join(__dirname, 'config.json.sample');
      if (fs.existsSync(samplePath)) {
        config = JSON.parse(fs.readFileSync(samplePath, 'utf-8'));
      } else {
        config = getDefaultConfig();
      }
      // Save config
      fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    }
  } catch (error) {
    console.error('Error loading config:', error);
    config = getDefaultConfig();
  }
  return config;
}

function getDefaultConfig() {
  return {
    services: {
      plex: {
        name: "Plex",
        url: "https://app.plex.tv",
        command: null,
        icon_color: "#e5a00d",
        icon_file: "plex.png"
      },
      jellyfin: {
        name: "Jellyfin",
        url: "https://jellyfin.org/downloads/",
        command: null,
        icon_color: "#00a4dc",
        icon_file: "jellyfin.png"
      },
      netflix: {
        name: "Netflix",
        url: "https://www.netflix.com",
        command: null,
        icon_color: "#e50914",
        icon_file: "netflix.png"
      },
      disneyplus: {
        name: "Disney+",
        url: "https://www.disneyplus.com",
        command: null,
        icon_color: "#113ccf",
        icon_file: "disney+.png"
      }
    }
  };
}

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1920,
    height: 1080,
    fullscreen: true,
    backgroundColor: '#1a1a1a',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    frame: false,
    show: false
  });

  // Load the home page
  mainWindow.loadFile('index.html');

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    if (currentBrowserView) {
      mainWindow.removeBrowserView(currentBrowserView);
      currentBrowserView = null;
    }
    mainWindow = null;
  });
}

// Create embedded browser view
function createBrowserView(url) {
  // Remove existing browser view if any
  if (currentBrowserView) {
    mainWindow.removeBrowserView(currentBrowserView);
  }

  // Create new browser view
  currentBrowserView = new BrowserView({
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  mainWindow.addBrowserView(currentBrowserView);

  // Set bounds to cover the full window
  const bounds = mainWindow.getBounds();
  currentBrowserView.setBounds({ x: 0, y: 0, width: bounds.width, height: bounds.height });
  currentBrowserView.setAutoResize({ width: true, height: true });

  // Load the URL
  currentBrowserView.webContents.loadURL(url);

  return currentBrowserView;
}

// IPC Handlers
ipcMain.handle('get-config', () => {
  return config;
});

ipcMain.handle('get-credentials', (event, service) => {
  return store.get(`credentials.${service}`, null);
});

ipcMain.handle('save-credentials', (event, service, credentials) => {
  store.set(`credentials.${service}`, credentials);
  return true;
});

ipcMain.handle('delete-credentials', (event, service) => {
  store.delete(`credentials.${service}`);
  return true;
});

ipcMain.handle('launch-service', async (event, service) => {
  const serviceConfig = config.services[service];
  if (!serviceConfig) {
    return { success: false, error: 'Service not found' };
  }

  try {
    // Try to get stored credentials
    const credentials = store.get(`credentials.${service}`, null);

    if (serviceConfig.command) {
      // Launch as external command
      const child = exec(serviceConfig.command);
      launchedProcesses.push({
        name: serviceConfig.name,
        process: child,
        pid: child.pid
      });
      return { success: true, mode: 'external' };
    } else if (serviceConfig.url) {
      // Launch in embedded browser
      createBrowserView(serviceConfig.url);

      // If we have credentials, attempt auto-login
      if (credentials && credentials.username && credentials.password) {
        // Send credentials to renderer for auto-login
        // This is a simplified approach - real implementation would need service-specific logic
        setTimeout(() => {
          if (currentBrowserView) {
            currentBrowserView.webContents.executeJavaScript(`
              // Auto-login attempt (service-specific logic needed)
              console.log('Auto-login credentials available');
            `);
          }
        }, 2000);
      }

      return { success: true, mode: 'embedded', credentials: credentials ? true : false };
    } else {
      return { success: false, error: 'No URL or command configured' };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('close-browser', () => {
  if (currentBrowserView) {
    mainWindow.removeBrowserView(currentBrowserView);
    currentBrowserView = null;
  }
  // Show the main interface again
  mainWindow.webContents.send('show-home');
  return true;
});

ipcMain.handle('close-last-app', () => {
  if (launchedProcesses.length === 0) {
    return { success: false, error: 'No apps running' };
  }

  const lastApp = launchedProcesses.pop();
  try {
    if (lastApp.process && !lastApp.process.killed) {
      lastApp.process.kill();
    }
    return { success: true, name: lastApp.name };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('exit-fullscreen', () => {
  if (mainWindow) {
    mainWindow.setFullScreen(false);
  }
  return true;
});

ipcMain.handle('quit-app', () => {
  app.quit();
});

// App lifecycle
app.whenReady().then(() => {
  // Load configuration
  loadConfig();

  // Create main window
  createWindow();

  // Remove default menu
  Menu.setApplicationMenu(null);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  // Clean up launched processes
  launchedProcesses.forEach(app => {
    if (app.process && !app.process.killed) {
      app.process.kill();
    }
  });
});
