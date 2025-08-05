# Google Drive Sync Tool

A Python-based tool to automatically sync a local folder with a folder in Google Drive.

## Features

- Real-time monitoring of local folder changes
- Bidirectional synchronization (local ↔ Google Drive)
- Conflict resolution based on modification times
- System tray icon for easy control
- Configurable ignore patterns for temporary files
- Detailed logging

## Setup Instructions

1. **Prerequisites**
   - Python 3.7 or higher
   - A Google Cloud Project with Google Drive API enabled

2. **Google Cloud Setup**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Drive API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download the credentials file and save it as `credentials.json` in the project root

3. **Installation**
   - Clone or download this project
   - Install dependencies: `pip install -r requirements.txt`
   - Configure `config.json` with your folder paths

4. **Running the Application**
   - Run the script: `python sync_daemon.py`
   - Complete OAuth authentication in the browser
   - The application will start syncing and appear in the system tray

## Configuration

Edit `config.json` to customize:
- `local_folder`: Path to the local folder to sync
- `drive_folder`: Name of the Google Drive folder to sync with
- `ignore_patterns`: List of file patterns to ignore (e.g., temporary files)

## Usage

- The application runs in the background and syncs automatically
- Right-click the system tray icon to:
  - Manually trigger a sync
  - Exit the application
- View sync activity in the `sync.log` file

## Troubleshooting

- Check `sync.log` for error messages
- Ensure your Google Cloud credentials are valid
- Verify folder paths in `config.json`
- Make sure you have sufficient permissions for both local and Drive folders