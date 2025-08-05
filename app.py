from flask import Flask, render_template, jsonify, request, flash, redirect, url_for, session
from flask_cors import CORS
import json
import os
import threading
import logging
from werkzeug.utils import secure_filename
from core.sync_engine import SyncEngine
from core.auth import authenticate, authenticate_with_code, get_auth_url, is_authenticated, clear_credentials
from ui.tray import create_tray_icon

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
CORS(app)

# Global variables
sync_engine = None
tray_icon = None
sync_thread = None

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading config: {str(e)}")
        return None

def start_sync_engine():
    """Start the sync engine in a separate thread"""
    global sync_engine, sync_thread
    
    config = load_config()
    if not config:
        return False
    
    if not os.path.exists(config['local_folder']):
        logging.error(f"Local folder does not exist: {config['local_folder']}")
        return False
    
    # Initialize sync engine
    sync_engine = SyncEngine(
        local_folder=config['local_folder'],
        drive_folder_name=config['drive_folder'],
        ignore_patterns=config.get('ignore_patterns', [])
    )
    
    # Start sync engine in a separate thread
    sync_thread = threading.Thread(target=sync_engine.start)
    sync_thread.daemon = True
    sync_thread.start()
    
    return True

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get sync status"""
    global sync_engine
    
    if sync_engine is None:
        return jsonify({
            'status': 'stopped',
            'message': 'Sync engine not started'
        })
    
    return jsonify({
        'status': 'running',
        'local_folder': sync_engine.local_folder,
        'drive_folder': sync_engine.drive_folder_name
    })

@app.route('/api/sync', methods=['POST'])
def manual_sync():
    """Trigger manual sync"""
    global sync_engine
    
    if sync_engine is None:
        return jsonify({'error': 'Sync engine not started'}), 400
    
    try:
        threading.Thread(target=sync_engine.poll_drive_changes).start()
        return jsonify({'message': 'Manual sync triggered'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config')
def get_config():
    """Get current configuration"""
    config = load_config()
    if config:
        return jsonify(config)
    return jsonify({'error': 'Failed to load config'}), 500

@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration"""
    try:
        new_config = request.json
        with open('config.json', 'w') as f:
            json.dump(new_config, f, indent=2)
        return jsonify({'message': 'Configuration updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/start', methods=['POST'])
def start_sync():
    """Start the sync engine"""
    global sync_engine
    
    if sync_engine is not None:
        return jsonify({'error': 'Sync engine already running'}), 400
    
    success = start_sync_engine()
    if success:
        return jsonify({'message': 'Sync engine started'})
    else:
        return jsonify({'error': 'Failed to start sync engine'}), 500

@app.route('/api/stop', methods=['POST'])
def stop_sync():
    """Stop the sync engine"""
    global sync_engine, tray_icon
    
    if sync_engine is None:
        return jsonify({'error': 'Sync engine not running'}), 400
    
    # Stop tray icon if running
    if tray_icon:
        tray_icon.stop()
    
    # Stop sync engine
    sync_engine.stop()
    sync_engine = None
    
    return jsonify({'message': 'Sync engine stopped'})



@app.route('/api/auth/status')
def check_auth_status():
    """Check if user is authenticated"""
    authenticated = is_authenticated()
    return jsonify({
        'authenticated': authenticated
    })

@app.route('/api/auth/login')
def start_auth():
    """Start OAuth authentication flow"""
    try:
        auth_url, state = get_auth_url()
        session['oauth_state'] = state
        return jsonify({
            'auth_url': auth_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/oauth2callback')
def oauth2callback():
    """Handle OAuth callback"""
    try:
        # Get authorization code from callback
        code = request.args.get('code')
        state = request.args.get('state')
        
        # Verify state matches
        if state != session.get('oauth_state'):
            return jsonify({'error': 'Invalid state parameter'}), 400
        
        # Complete authentication
        creds = authenticate_with_code(code)
        if creds:
            return render_template('auth_success.html')
        else:
            return render_template('auth_error.html')
            
    except Exception as e:
        return render_template('auth_error.html', error=str(e))

@app.route('/api/auth/logout')
def logout():
    """Clear authentication credentials"""
    try:
        clear_credentials()
        return jsonify({'message': 'Logged out successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    """Main application entry point"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(os.path.dirname(__file__), 'sync.log')),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger('drive_sync')
    logger.info("Starting Google Drive Sync Tool Web UI")
    
    # Check if OAuth credentials are configured
    from core.auth import OAUTH_CLIENT_CONFIG
    if (OAUTH_CLIENT_CONFIG['web']['client_id'] == 'YOUR_CLIENT_ID.apps.googleusercontent.com' or 
        OAUTH_CLIENT_CONFIG['web']['client_secret'] == 'YOUR_CLIENT_SECRET'):
        logger.warning("OAuth credentials not configured. Please follow the OAUTH_SETUP.md guide.")
        print("\n" + "="*60)
        print("OAuth credentials not configured!")
        print("Please follow the OAUTH_SETUP.md guide to set up your credentials.")
        print("="*60 + "\n")
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    main() 