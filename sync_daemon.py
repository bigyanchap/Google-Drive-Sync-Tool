import json
import threading
import os
import sys
import logging
from core.sync_engine import SyncEngine
from ui.tray import create_tray_icon

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading config: {str(e)}")
        sys.exit(1)

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
    logger.info("Starting Google Drive Sync Tool")
    
    # Load configuration
    config = load_config()
    
    # Validate configuration
    if not os.path.exists(config['local_folder']):
        logger.error(f"Local folder does not exist: {config['local_folder']}")
        sys.exit(1)
    
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
    
    # Create and run system tray icon
    icon = create_tray_icon(sync_engine)
    icon.run()

if __name__ == "__main__":
    main()