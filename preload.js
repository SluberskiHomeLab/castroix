/**
 * Castroix Preload Script
 * Provides secure bridge between renderer and main process
 */

const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods to renderer process
contextBridge.exposeInMainWorld('castroix', {
  // Configuration
  getConfig: () => ipcRenderer.invoke('get-config'),

  // Credentials management
  getCredentials: (service) => ipcRenderer.invoke('get-credentials', service),
  saveCredentials: (service, credentials) => ipcRenderer.invoke('save-credentials', service, credentials),
  deleteCredentials: (service) => ipcRenderer.invoke('delete-credentials', service),

  // Service launching
  launchService: (service) => ipcRenderer.invoke('launch-service', service),
  closeBrowser: () => ipcRenderer.invoke('close-browser'),
  closeLastApp: () => ipcRenderer.invoke('close-last-app'),

  // Window management
  exitFullscreen: () => ipcRenderer.invoke('exit-fullscreen'),
  quitApp: () => ipcRenderer.invoke('quit-app'),

  // Event listeners
  onShowHome: (callback) => {
    ipcRenderer.on('show-home', () => callback());
  }
});
