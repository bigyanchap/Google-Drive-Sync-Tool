# Google Drive Sync Tool

A modern Python-based tool to automatically sync a local folder with Google Drive using a beautiful web interface and simplified OAuth authentication.

## ✨ Features

- **🔐 Simple OAuth Authentication** - Sign in with Google directly, no credential files needed
- **🌐 Modern Web Interface** - Beautiful, responsive web UI for easy control
- **🔄 Real-time Sync** - Automatic bidirectional synchronization (local ↔ Google Drive)
- **📁 Smart Conflict Resolution** - Based on modification times
- **⚙️ Easy Configuration** - Web-based configuration management
- **📊 Live Status Monitoring** - Real-time sync status and activity logs
- **🚫 Configurable Ignore Patterns** - Skip temporary files and system files
- **💾 Persistent Authentication** - Stay signed in across sessions

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- A Google account
- A Google Cloud Project (free)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up OAuth Credentials
Follow the [OAuth Setup Guide](OAUTH_SETUP.md) to create your Google Cloud credentials.

### 3. Run the Application
```bash
python3 app.py
```

### 4. Open the Web Interface
Navigate to `http://localhost:8080` in your browser.

## 📖 How to Use

### Step 1: Authentication
1. **Sign in with Google**: Click the "Sign in with Google" button
2. **Complete OAuth**: A popup window will open for Google authentication
3. **Grant Permissions**: Allow the app to access your Google Drive
4. **Success**: You'll see "Authentication Successful!" when done

### Step 2: Configuration
1. **Local Folder**: Enter the path to your local folder (e.g., `/Users/username/Documents/Sync`)
2. **Drive Folder**: Enter the name of the Google Drive folder to sync with
3. **Ignore Patterns**: Optionally add file patterns to ignore (e.g., `.tmp,~$,.DS_Store`)
4. **Save Configuration**: Click "Save Configuration"

### Step 3: Start Syncing
1. **Start Sync**: Click "Start Sync" to begin automatic synchronization
2. **Monitor Status**: Watch the real-time status indicator and activity log
3. **Manual Sync**: Use "Manual Sync" for immediate synchronization

## 🎯 Usage Examples

### Basic File Sync
```
Local Folder: /Users/john/Documents/Work
Drive Folder: Work Documents
```
- All files in your local "Work" folder will sync with a "Work Documents" folder in Google Drive
- Changes in either location will automatically sync to the other

### Project Backup
```
Local Folder: /Users/john/Projects/MyApp
Drive Folder: Project Backup
Ignore Patterns: node_modules,.git,*.log
```
- Sync your project files while ignoring temporary and build files
- Perfect for backing up important work

### Photo Library Sync
```
Local Folder: /Users/john/Pictures/Camera
Drive Folder: Photo Library
Ignore Patterns: .DS_Store,Thumbs.db
```
- Keep your photos backed up to Google Drive
- Access them from anywhere

## ⚙️ Configuration Options

### Local Folder Path
- **Windows**: `C:\Users\username\Documents\Sync`
- **macOS**: `/Users/username/Documents/Sync`
- **Linux**: `/home/username/documents/sync`

### Drive Folder Name
- The folder will be created in your Google Drive root
- If the folder doesn't exist, it will be created automatically
- Use descriptive names like "Work Documents" or "Photo Backup"

### Ignore Patterns
Common patterns to ignore:
- **Temporary files**: `.tmp`, `~$`, `*.swp`
- **System files**: `.DS_Store`, `Thumbs.db`, `.git`
- **Build files**: `node_modules`, `dist`, `build`
- **Log files**: `*.log`, `*.out`

## 🔧 Advanced Features

### Real-time Monitoring
- **Status Indicator**: Green dot shows when sync is running
- **Activity Log**: See recent sync activities and file changes
- **Last Sync Time**: Track when the last sync occurred

### Manual Controls
- **Start/Stop**: Control sync engine manually
- **Manual Sync**: Trigger immediate synchronization
- **Configuration Updates**: Modify settings without restarting

### Error Handling
- **Automatic Retry**: Failed operations are retried automatically
- **Error Logging**: Detailed error messages in the activity log
- **Graceful Recovery**: App continues working even if some files fail

## 🛠️ Troubleshooting

### Authentication Issues
- **"Invalid client" error**: Check your OAuth credentials in `core/auth.py`
- **"Redirect URI mismatch"**: Ensure redirect URI is `http://localhost:8080/oauth2callback`
- **"Access blocked"**: Enable Google Drive API in your Google Cloud project

### Sync Issues
- **Files not syncing**: Check folder permissions and paths
- **Conflicts**: Check the activity log for conflict resolution details
- **Performance**: Large files may take time to upload/download

### Common Problems
- **App won't start**: Check Python version and dependencies (use `python3` on macOS/Linux)
- **Web interface not loading**: Ensure port 8080 is available
- **Authentication lost**: Click "Sign in with Google" again

## 📁 File Structure
```
Google-Drive-Sync-Tool/
├── app.py                 # Main Flask application
├── core/                  # Core sync functionality
│   ├── auth.py           # OAuth authentication
│   ├── drive_api.py      # Google Drive API wrapper
│   ├── sync_engine.py    # Sync logic
│   └── utils.py          # Utility functions
├── templates/            # HTML templates
├── static/              # CSS and JavaScript
├── config.json          # Configuration file
├── token.pickle         # OAuth tokens (auto-generated)
└── sync.log             # Application logs
```

## 🔒 Security & Privacy

- **OAuth 2.0**: Uses Google's secure authentication standard
- **Local Storage**: Tokens stored locally in `token.pickle`
- **Minimal Permissions**: Only accesses specified Drive folders
- **No Data Collection**: App doesn't collect or transmit personal data
- **Revocable Access**: Users can revoke access anytime from Google Account

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License & Usage Terms

### Individual Use
This software is **free for individual, personal use**. You may download, install, and use this tool for your personal file synchronization needs without any cost.

### Commercial Use
**Commercial licensing is required for business and organizational use.** This includes but is not limited to:
- Companies and corporations
- Government agencies
- Educational institutions
- Non-profit organizations
- Any entity using this software for business purposes

### Licensing Inquiries
For commercial licensing, enterprise support, or bulk deployments, please contact:
- **Email**: admin@onlysatvic.com
- **Subject**: Commercial License Inquiry - Google Drive Sync Tool

### Terms
- Individual users may use this software freely for personal purposes
- Commercial entities must obtain proper licensing before deployment
- Unauthorized commercial use is prohibited
- This software is provided "as is" without warranty

## 🆘 Support

- **Documentation**: Check this README and `OAUTH_SETUP.md`
- **Issues**: Report bugs on GitHub
- **Questions**: Open a GitHub discussion

---

**Happy Syncing! 🚀**