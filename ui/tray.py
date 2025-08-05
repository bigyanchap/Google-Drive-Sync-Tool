import pystray
from PIL import Image
import threading
import logging

def create_tray_icon(sync_engine):
    """Create a system tray icon for the sync application"""
    logger = logging.getLogger('drive_sync')
    
    # Create a simple icon (you can replace this with your own icon file)
    image = Image.new('RGB', (64, 64), color='blue')
    
    def on_sync_clicked(icon, item):
        """Handle sync now menu item click"""
        logger.info("Manual sync triggered")
        threading.Thread(target=sync_engine.poll_drive_changes).start()
    
    def on_exit_clicked(icon, item):
        """Handle exit menu item click"""
        logger.info("Exiting sync application")
        icon.stop()
    
    # Create the menu
    menu = pystray.Menu(
        pystray.MenuItem("Sync Now", on_sync_clicked),
        pystray.MenuItem("Exit", on_exit_clicked)
    )
    
    # Create the icon
    icon = pystray.Icon(
        "drive_sync",
        image,
        "Drive Sync",
        menu
    )
    
    return icon