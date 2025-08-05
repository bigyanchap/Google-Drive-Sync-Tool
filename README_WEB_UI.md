# Google Drive Sync Tool - Web UI

A beautiful, modern web interface for the Google Drive Sync Tool with a sleek black background and glossy buttons.

## Features

- **Modern Web Interface**: Beautiful black background with glossy buttons and smooth animations
- **Real-time Status Monitoring**: Live status updates and activity logging
- **Configuration Management**: Easy-to-use form for updating sync settings
- **Manual Sync Control**: Start, stop, and trigger manual sync operations
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Activity Log**: Real-time display of sync activities and events

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Run the Web Application**:
   ```bash
   python3 app.py
   ```

3. **Access the Web UI**:
   Open your browser and navigate to: `http://localhost:8080`

## Web UI Features

### Google Drive Authentication Panel
- **Upload Credentials**: Drag and drop or select your `credentials.json` file
- **Credentials Status**: Real-time validation of uploaded credentials
- **Direct Link**: Quick access to Google Cloud Console for credentials download
- **File Validation**: Automatic validation of JSON structure and OAuth format

### Configuration Panel
- Set local folder path for syncing
- Configure Google Drive folder name
- Define ignore patterns for files to skip

### Sync Control Panel
- **Start Sync**: Begin automatic synchronization
- **Stop Sync**: Halt the sync process
- **Manual Sync**: Trigger immediate sync operation

### Status Information
- Real-time sync status indicator
- Current local and Drive folder paths
- Last sync timestamp

### Activity Log
- Live feed of sync activities
- Timestamped events
- Error and success notifications

## API Endpoints

The web UI communicates with the backend through RESTful API endpoints:

- `GET /api/status` - Get current sync status
- `POST /api/start` - Start the sync engine
- `POST /api/stop` - Stop the sync engine
- `POST /api/sync` - Trigger manual sync
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration

## Design Features

- **Dark Theme**: Elegant black background with subtle gradients
- **Glossy Buttons**: Beautiful gradient buttons with hover effects
- **Glass Morphism**: Translucent cards with backdrop blur effects
- **Smooth Animations**: CSS transitions and hover effects
- **Modern Typography**: Inter font family for clean readability
- **Responsive Layout**: Grid-based layout that adapts to screen size

## Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### Port Already in Use
If port 8080 is already in use, modify the port in `app.py`:
```python
app.run(host='0.0.0.0', port=8081, debug=True)
```

### Google Drive Authentication
Make sure you have:
1. Created a Google Cloud Project
2. Enabled the Google Drive API
3. Created OAuth 2.0 credentials
4. Downloaded and placed `credentials.json` in the project root

### File Permissions
Ensure the application has read/write permissions for the configured local folder.

## Development

The web UI is built with:
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with modern design patterns
- **Icons**: Font Awesome 6.0

## File Structure

```
Sync2GoogleDrive/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Beautiful dark theme styles
│   └── js/
│       └── app.js        # Interactive JavaScript
├── core/                 # Core sync functionality
├── ui/                   # System tray UI (legacy)
└── config.json          # Configuration file
```

## Google Drive Setup

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Drive API for your project

### 2. Create OAuth 2.0 Credentials
1. Navigate to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Desktop application" as the application type
4. Download the credentials file (it will be named something like `client_secret_xxx.json`)

### 3. Upload Credentials via Web UI
1. Open the web interface at `http://localhost:8080`
2. In the "Google Drive Authentication" section, click "Choose credentials.json file"
3. Select your downloaded credentials file
4. Click "Upload Credentials"
5. The status should change to "Valid" if the file is correct

### 4. Complete Authentication
1. After uploading credentials, start the sync engine
2. The first time you start sync, a browser window will open
3. Complete the OAuth authentication process
4. Grant the necessary permissions to access your Google Drive

## Next Steps

1. Upload your Google Drive credentials through the web interface
2. Configure your local and Drive folders
3. Start the sync engine through the web interface
4. Monitor sync activities in real-time

Enjoy your beautiful Google Drive sync experience! 🚀 