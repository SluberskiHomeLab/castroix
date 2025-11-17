/**
 * Castroix Renderer Process
 * Handles UI interactions and service launching
 */

// Grid layout constants
// This should match the CSS grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))
// The value accounts for minimum card width (300px) + gap (40px) + padding considerations
const CARD_WIDTH_WITH_GAP = 400;

let config = null;
let services = [];
let focusedIndex = 0;
let serviceKeys = [];

// Initialize the application
async function init() {
  try {
    // Load configuration
    config = await window.castroix.getConfig();
    services = config.services || {};
    serviceKeys = Object.keys(services);

    // Populate services grid
    populateServices();

    // Populate credentials modal
    populateCredentialsSelect();

    // Setup keyboard navigation
    setupKeyboardNavigation();

    // Set initial focus
    if (serviceKeys.length > 0) {
      setFocus(0);
    }

    // Listen for show home event
    window.castroix.onShowHome(() => {
      document.getElementById('home-view').style.display = 'flex';
    });
  } catch (error) {
    console.error('Error initializing app:', error);
    showError('Failed to initialize application');
  }
}

// Populate services grid
function populateServices() {
  const grid = document.getElementById('services-grid');
  grid.innerHTML = '';

  serviceKeys.forEach((key, index) => {
    const service = services[key];
    const card = createServiceCard(key, service, index);
    grid.appendChild(card);
  });
}

// Create a service card element
function createServiceCard(key, service, index) {
  const card = document.createElement('div');
  card.className = 'service-card';
  card.dataset.index = index;
  card.dataset.key = key;
  card.style.background = service.icon_color || '#4a90e2';

  const content = document.createElement('div');
  content.className = 'service-content';

  // Try to load icon
  const iconPath = service.icon_file;
  if (iconPath) {
    const icon = document.createElement('img');
    icon.className = 'service-icon';
    icon.src = iconPath;
    icon.onerror = () => {
      // If icon fails to load, hide it
      icon.style.display = 'none';
    };
    content.appendChild(icon);
  }

  const name = document.createElement('div');
  name.className = 'service-name';
  name.textContent = service.name;
  content.appendChild(name);

  card.appendChild(content);

  // Click handler
  card.addEventListener('click', () => {
    setFocus(index);
    launchService(key);
  });

  // Hover handler
  card.addEventListener('mouseenter', () => {
    setFocus(index);
  });

  return card;
}

// Set focus on a service card
function setFocus(index) {
  // Remove focus from all cards
  document.querySelectorAll('.service-card').forEach(card => {
    card.classList.remove('focused');
  });

  // Add focus to selected card
  const cards = Array.from(document.querySelectorAll('.service-card'));
  if (index >= 0 && index < cards.length) {
    focusedIndex = index;
    cards[index].classList.add('focused');
    cards[index].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

// Launch a service
async function launchService(key) {
  showLoading(true);

  try {
    const result = await window.castroix.launchService(key);

    if (result.success) {
      if (result.mode === 'embedded') {
        // Hide home view when showing embedded browser
        document.getElementById('home-view').style.display = 'none';
        
        if (result.credentials) {
          showNotification(`${services[key].name} launched with auto-login`);
        } else {
          showNotification(`${services[key].name} launched`);
        }
      } else {
        showNotification(`${services[key].name} launched externally`);
      }
    } else {
      showError(result.error || 'Failed to launch service');
    }
  } catch (error) {
    console.error('Error launching service:', error);
    showError('Failed to launch service');
  } finally {
    showLoading(false);
  }
}

// Keyboard navigation
function setupKeyboardNavigation() {
  document.addEventListener('keydown', async (e) => {
    // Handle modal keyboard events
    if (!document.getElementById('credentials-modal').classList.contains('hidden')) {
      if (e.key === 'Escape') {
        closeCredentialsModal();
      }
      return;
    }

    const cards = document.querySelectorAll('.service-card');
    const cols = Math.floor(window.innerWidth / CARD_WIDTH_WITH_GAP);

    switch (e.key) {
      case 'ArrowUp':
        e.preventDefault();
        if (focusedIndex >= cols) {
          setFocus(focusedIndex - cols);
        }
        break;

      case 'ArrowDown':
        e.preventDefault();
        if (focusedIndex + cols < cards.length) {
          setFocus(focusedIndex + cols);
        }
        break;

      case 'ArrowLeft':
        e.preventDefault();
        if (focusedIndex > 0) {
          setFocus(focusedIndex - 1);
        }
        break;

      case 'ArrowRight':
        e.preventDefault();
        if (focusedIndex < cards.length - 1) {
          setFocus(focusedIndex + 1);
        }
        break;

      case 'Enter':
        e.preventDefault();
        if (serviceKeys[focusedIndex]) {
          launchService(serviceKeys[focusedIndex]);
        }
        break;

      case 'Escape':
        e.preventDefault();
        // Check if in embedded browser
        if (document.getElementById('home-view').style.display === 'none') {
          await window.castroix.closeBrowser();
          document.getElementById('home-view').style.display = 'flex';
        } else {
          await window.castroix.exitFullscreen();
        }
        break;
    }

    // Ctrl+Q - Close embedded browser or last app
    if (e.ctrlKey && e.key === 'q') {
      e.preventDefault();
      // Check if in embedded browser
      if (document.getElementById('home-view').style.display === 'none') {
        // Close embedded browser
        await window.castroix.closeBrowser();
        document.getElementById('home-view').style.display = 'flex';
        showNotification('Browser closed');
      } else {
        // Close last external app
        const result = await window.castroix.closeLastApp();
        if (result.success) {
          showNotification(`Closed ${result.name}`);
        } else {
          showNotification('No apps running');
        }
      }
    }

    // Ctrl+S - Show credentials modal
    if (e.ctrlKey && e.key === 's') {
      e.preventDefault();
      showCredentialsModal();
    }
  });
}

// Credentials Modal Functions
function showCredentialsModal() {
  document.getElementById('credentials-modal').classList.remove('hidden');
  
  // Load credentials for selected service
  const serviceSelect = document.getElementById('service-select');
  if (serviceSelect.value) {
    loadCredentials(serviceSelect.value);
  }
}

function closeCredentialsModal() {
  document.getElementById('credentials-modal').classList.add('hidden');
  document.getElementById('username').value = '';
  document.getElementById('password').value = '';
}

function populateCredentialsSelect() {
  const select = document.getElementById('service-select');
  select.innerHTML = '';

  serviceKeys.forEach(key => {
    const option = document.createElement('option');
    option.value = key;
    option.textContent = services[key].name;
    select.appendChild(option);
  });

  // Add change listener
  select.addEventListener('change', (e) => {
    loadCredentials(e.target.value);
  });
}

async function loadCredentials(service) {
  try {
    const credentials = await window.castroix.getCredentials(service);
    if (credentials) {
      document.getElementById('username').value = credentials.username || '';
      document.getElementById('password').value = credentials.password || '';
    } else {
      document.getElementById('username').value = '';
      document.getElementById('password').value = '';
    }
  } catch (error) {
    console.error('Error loading credentials:', error);
  }
}

async function saveCredentials() {
  const service = document.getElementById('service-select').value;
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  if (!username || !password) {
    showError('Please enter both username and password');
    return;
  }

  try {
    await window.castroix.saveCredentials(service, { username, password });
    showNotification('Credentials saved successfully');
    closeCredentialsModal();
  } catch (error) {
    console.error('Error saving credentials:', error);
    showError('Failed to save credentials');
  }
}

async function deleteCredentials() {
  const service = document.getElementById('service-select').value;

  try {
    await window.castroix.deleteCredentials(service);
    showNotification('Credentials deleted');
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
  } catch (error) {
    console.error('Error deleting credentials:', error);
    showError('Failed to delete credentials');
  }
}

// UI Helper Functions
function showLoading(show) {
  const loading = document.getElementById('loading');
  if (show) {
    loading.classList.remove('hidden');
  } else {
    loading.classList.add('hidden');
  }
}

function showNotification(message) {
  // Simple notification - could be enhanced with a toast library
  console.log('Notification:', message);
  // For now, we'll use a simple alert-style approach
  // In production, consider using a toast notification library
}

function showError(message) {
  console.error('Error:', message);
  showErrorToast(message);
}

// Initialize on load
window.addEventListener('DOMContentLoaded', () => {
  // Inject error toast element if not present
  if (!document.getElementById('error-toast')) {
    const toast = document.createElement('div');
    toast.id = 'error-toast';
    toast.style.position = 'fixed';
    toast.style.bottom = '40px';
    toast.style.left = '50%';
    toast.style.transform = 'translateX(-50%)';
    toast.style.background = 'rgba(200, 0, 0, 0.95)';
    toast.style.color = '#fff';
    toast.style.padding = '16px 32px';
    toast.style.borderRadius = '8px';
    toast.style.fontSize = '1.2em';
    toast.style.zIndex = '9999';
    toast.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
    toast.style.display = 'none';
    toast.style.pointerEvents = 'none';
    toast.style.transition = 'opacity 0.3s';
    document.body.appendChild(toast);
  }
  init();
});

function showErrorToast(message) {
  const toast = document.getElementById('error-toast');
  if (!toast) return;
  toast.textContent = `Error: ${message}`;
  toast.style.display = 'block';
  toast.style.opacity = '1';
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => {
      toast.style.display = 'none';
    }, 300);
  }, 3500);
}
