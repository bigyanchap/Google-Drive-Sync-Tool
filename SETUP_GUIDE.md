# Quick Setup Guide - Google Drive Sync Tool

## 🚀 Get Started in 5 Minutes

### Step 1: Start the Application
```bash
python3 app.py
```

### Step 2: Open the Web Interface
Open your browser and go to: **http://localhost:8080**

### Step 3: Set Up Google Drive Authentication

#### Option A: Upload Credentials via Web UI (Recommended)
1. In the "Google Drive Authentication" section, click "Choose credentials.json file"
2. Select your downloaded credentials file from Google Cloud Console
3. Click "Upload Credentials"
4. Status should show "Valid" if successful

#### Option B: Manual File Placement
1. Download your `credentials.json` from Google Cloud Console
2. Place it in the project root directory (same folder as `app.py`)
3. Restart the application

### Step 4: Configure Sync Settings
1. Set your local folder path (e.g., `/Users/yourname/Desktop/SyncFolder`)
2. Set your Google Drive folder name (e.g., "DesktopSync")
3. Add any ignore patterns (e.g., ".tmp,.DS_Store")
4. Click "Save Configuration"

### Step 5: Start Syncing
1. Click "Start Sync" to begin automatic synchronization
2. Complete OAuth authentication in the browser (first time only)
3. Monitor sync activities in the Activity Log

## 🔑 Getting Google Drive Credentials

### 1. Create Google Cloud Project
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project or select existing one
- Enable the Google Drive API

### 2. Create OAuth 2.0 Credentials
- Navigate to "APIs & Services" > "Credentials"
- Click "Create Credentials" > "OAuth 2.0 Client IDs"
- Choose "Desktop application"
- Download the credentials file

### 3. Upload via Web UI
- Use the beautiful upload interface in the web app
- Drag and drop or click to select your credentials file
- Automatic validation ensures correct format

## 📁 Folder Structure
```
Sync2GoogleDrive/
├── app.py                 # Main application
├── credentials.json       # Your Google Drive credentials (upload via UI)
├── config.json           # Sync configuration
├── templates/            # Web UI templates
├── static/              # CSS and JavaScript files
└── core/                # Core sync functionality
```

## 🎯 Features Overview

### Beautiful Web Interface
- **Dark Theme**: Elegant black background with glossy buttons
- **Real-time Status**: Live updates of sync status and activities
- **Drag & Drop**: Easy credentials file upload
- **Responsive Design**: Works on desktop and mobile

### Sync Capabilities
- **Bidirectional Sync**: Local ↔ Google Drive
- **Real-time Monitoring**: Automatic file change detection
- **Conflict Resolution**: Based on modification times
- **Ignore Patterns**: Skip temporary and system files

### Easy Management
- **Start/Stop Sync**: One-click control
- **Manual Sync**: Trigger immediate synchronization
- **Activity Log**: Real-time monitoring of all operations
- **Configuration**: Easy setup through web interface

## 🔧 Troubleshooting

### Port Already in Use
If port 8080 is busy, the app will automatically try alternative ports.

### Credentials Issues
- Ensure you're using OAuth 2.0 credentials (not API keys)
- Check that the Google Drive API is enabled
- Verify the credentials file is valid JSON

### Sync Issues
- Check folder permissions
- Ensure both local and Drive folders exist
- Review the activity log for error messages

## 🎉 You're Ready!

Your Google Drive sync tool is now running with a beautiful web interface. Enjoy seamless file synchronization between your local machine and Google Drive!

For more detailed information, see the main README files. 