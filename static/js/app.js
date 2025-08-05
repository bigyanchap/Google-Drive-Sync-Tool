// Global variables
let syncStatus = 'stopped';
let lastSyncTime = null;

// DOM elements
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const syncBtn = document.getElementById('syncBtn');
const configForm = document.getElementById('configForm');
const credentialsForm = document.getElementById('credentialsForm');
const credentialsFile = document.getElementById('credentialsFile');
const fileName = document.getElementById('fileName');
const uploadBtn = document.getElementById('uploadBtn');
const credentialsStatusValue = document.getElementById('credentialsStatusValue');
const localFolderInput = document.getElementById('localFolder');
const driveFolderInput = document.getElementById('driveFolder');
const ignorePatternsInput = document.getElementById('ignorePatterns');
const localFolderDisplay = document.getElementById('localFolderDisplay');
const driveFolderDisplay = document.getElementById('driveFolderDisplay');
const lastSyncDisplay = document.getElementById('lastSyncDisplay');
const activityLog = document.getElementById('activityLog');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadConfig();
    updateStatus();
    checkCredentialsStatus();
    setInterval(updateStatus, 5000); // Update status every 5 seconds
    setInterval(checkCredentialsStatus, 10000); // Check credentials every 10 seconds
});

// Load configuration from server
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();
        
        if (config.error) {
            showNotification('Error loading configuration', 'error');
            return;
        }
        
        // Populate form fields
        localFolderInput.value = config.local_folder || '';
        driveFolderInput.value = config.drive_folder || '';
        ignorePatternsInput.value = config.ignore_patterns ? config.ignore_patterns.join(', ') : '';
        
        // Update display
        localFolderDisplay.textContent = config.local_folder || 'Not configured';
        driveFolderDisplay.textContent = config.drive_folder || 'Not configured';
        
    } catch (error) {
        console.error('Error loading config:', error);
        showNotification('Failed to load configuration', 'error');
    }
}

// Update sync status
async function updateStatus() {
    try {
        const response = await fetch('/api/status');
        const status = await response.json();
        
        syncStatus = status.status;
        
        // Update status indicator
        if (status.status === 'running') {
            statusDot.classList.add('running');
            statusText.textContent = 'Running';
            startBtn.disabled = true;
            stopBtn.disabled = false;
            syncBtn.disabled = false;
        } else {
            statusDot.classList.remove('running');
            statusText.textContent = 'Stopped';
            startBtn.disabled = false;
            stopBtn.disabled = true;
            syncBtn.disabled = true;
        }
        
        // Update status info
        if (status.local_folder) {
            localFolderDisplay.textContent = status.local_folder;
        }
        if (status.drive_folder) {
            driveFolderDisplay.textContent = status.drive_folder;
        }
        
    } catch (error) {
        console.error('Error updating status:', error);
    }
}

// Start sync
startBtn.addEventListener('click', async function() {
    try {
        const response = await fetch('/api/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.error) {
            showNotification(result.error, 'error');
        } else {
            showNotification('Sync engine started successfully', 'success');
            updateStatus();
            addActivityLog('Sync engine started');
        }
        
    } catch (error) {
        console.error('Error starting sync:', error);
        showNotification('Failed to start sync engine', 'error');
    }
});

// Stop sync
stopBtn.addEventListener('click', async function() {
    try {
        const response = await fetch('/api/stop', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.error) {
            showNotification(result.error, 'error');
        } else {
            showNotification('Sync engine stopped', 'success');
            updateStatus();
            addActivityLog('Sync engine stopped');
        }
        
    } catch (error) {
        console.error('Error stopping sync:', error);
        showNotification('Failed to stop sync engine', 'error');
    }
});

// Manual sync
syncBtn.addEventListener('click', async function() {
    try {
        const response = await fetch('/api/sync', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (result.error) {
            showNotification(result.error, 'error');
        } else {
            showNotification('Manual sync triggered', 'success');
            lastSyncTime = new Date();
            updateLastSyncDisplay();
            addActivityLog('Manual sync triggered');
        }
        
    } catch (error) {
        console.error('Error triggering manual sync:', error);
        showNotification('Failed to trigger manual sync', 'error');
    }
});

// Save configuration
configForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const config = {
        local_folder: localFolderInput.value,
        drive_folder: driveFolderInput.value,
        ignore_patterns: ignorePatternsInput.value.split(',').map(pattern => pattern.trim()).filter(pattern => pattern)
    };
    
    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });
        
        const result = await response.json();
        
        if (result.error) {
            showNotification(result.error, 'error');
        } else {
            showNotification('Configuration saved successfully', 'success');
            localFolderDisplay.textContent = config.local_folder;
            driveFolderDisplay.textContent = config.drive_folder;
            addActivityLog('Configuration updated');
        }
        
    } catch (error) {
        console.error('Error saving config:', error);
        showNotification('Failed to save configuration', 'error');
    }
});

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    const notificationMessage = document.getElementById('notificationMessage');
    
    notificationMessage.textContent = message;
    notification.className = `notification show ${type}`;
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideNotification();
    }, 5000);
}

// Hide notification
function hideNotification() {
    const notification = document.getElementById('notification');
    notification.classList.remove('show');
}

// Add activity log entry
function addActivityLog(message) {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.innerHTML = `
        <div>${message}</div>
        <span class="timestamp">${timestamp}</span>
    `;
    
    // Add to the beginning of the log
    activityLog.insertBefore(logEntry, activityLog.firstChild);
    
    // Keep only the last 10 entries
    const entries = activityLog.querySelectorAll('.log-entry');
    if (entries.length > 10) {
        entries[entries.length - 1].remove();
    }
}

// Update last sync display
function updateLastSyncDisplay() {
    if (lastSyncTime) {
        lastSyncDisplay.textContent = lastSyncTime.toLocaleString();
    } else {
        lastSyncDisplay.textContent = 'Never';
    }
}

// Credentials file selection
credentialsFile.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        fileName.textContent = file.name;
        uploadBtn.disabled = false;
    } else {
        fileName.textContent = 'No file chosen';
        uploadBtn.disabled = true;
    }
});

// Upload credentials
credentialsForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    const file = credentialsFile.files[0];
    
    if (!file) {
        showNotification('Please select a credentials file', 'error');
        return;
    }
    
    formData.append('credentials', file);
    
    try {
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
        
        const response = await fetch('/api/credentials/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.error) {
            showNotification(result.error, 'error');
        } else {
            showNotification('Credentials uploaded successfully', 'success');
            addActivityLog('Google Drive credentials uploaded');
            checkCredentialsStatus();
        }
        
    } catch (error) {
        console.error('Error uploading credentials:', error);
        showNotification('Failed to upload credentials', 'error');
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<i class="fas fa-upload"></i> Upload Credentials';
    }
});

// Check credentials status
async function checkCredentialsStatus() {
    try {
        const response = await fetch('/api/credentials/status');
        const status = await response.json();
        
        if (status.exists && status.valid) {
            credentialsStatusValue.textContent = 'Valid';
            credentialsStatusValue.className = 'status-value valid';
        } else if (status.exists && !status.valid) {
            credentialsStatusValue.textContent = 'Invalid';
            credentialsStatusValue.className = 'status-value invalid';
        } else {
            credentialsStatusValue.textContent = 'Missing';
            credentialsStatusValue.className = 'status-value missing';
        }
        
    } catch (error) {
        console.error('Error checking credentials status:', error);
        credentialsStatusValue.textContent = 'Error';
        credentialsStatusValue.className = 'status-value invalid';
    }
}

// Add some initial activity log entries
addActivityLog('Application started');
addActivityLog('Ready to configure sync settings'); 