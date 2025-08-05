from flask import Flask, render_template, jsonify, request, flash
from flask_cors import CORS
import json
import os
import threading
import logging
from werkzeug.utils import secure_filename
from core.sync_engine import SyncEngine
from ui.tray import create_tray_icon

app = Flask(__name__)
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

@app.route('/api/credentials/upload', methods=['POST'])
def upload_credentials():
    """Upload Google Drive credentials file"""
    try:
        if 'credentials' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['credentials']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename.endswith('.json'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(os.path.dirname(__file__), 'credentials.json')
            
            # Save the file
            file.save(filepath)
            
            # Validate the JSON structure
            try:
                with open(filepath, 'r') as f:
                    creds_data = json.load(f)
                
                # Check if it has the expected Google OAuth structure
                if 'installed' in creds_data or 'web' in creds_data:
                    return jsonify({'message': 'Credentials uploaded successfully'})
                else:
                    # Remove invalid file
                    os.remove(filepath)
                    return jsonify({'error': 'Invalid credentials file format'}), 400
                    
            except json.JSONDecodeError:
                # Remove invalid file
                os.remove(filepath)
                return jsonify({'error': 'Invalid JSON file'}), 400
        else:
            return jsonify({'error': 'Please upload a valid JSON file'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Error uploading credentials: {str(e)}'}), 500

@app.route('/api/credentials/status')
def check_credentials():
    """Check if credentials file exists"""
    creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
    exists = os.path.exists(creds_path)
    
    if exists:
        try:
            with open(creds_path, 'r') as f:
                creds_data = json.load(f)
            return jsonify({
                'exists': True,
                'valid': 'installed' in creds_data or 'web' in creds_data
            })
        except:
            return jsonify({
                'exists': True,
                'valid': False
            })
    else:
        return jsonify({
            'exists': False,
            'valid': False
        })

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
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    main() 