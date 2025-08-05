import os
import time
import logging
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .auth import authenticate
from .drive_api import DriveAPI
from .utils import ensure_dir, get_file_hash

class SyncHandler(FileSystemEventHandler):
    def __init__(self, drive_api, local_folder, drive_folder_id, ignore_patterns=None):
        self.drive_api = drive_api
        self.local_folder = local_folder
        self.drive_folder_id = drive_folder_id
        self.ignore_patterns = ignore_patterns or []
        self.logger = logging.getLogger('drive_sync')
        self.file_index = self.build_file_index()
        self.last_sync_time = time.time()
    
    def build_file_index(self):
        """Create index of local files with metadata"""
        index = {}
        for root, _, files in os.walk(self.local_folder):
            for file in files:
                if any(file.endswith(pattern) for pattern in self.ignore_patterns):
                    continue
                    
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, self.local_folder)
                index[rel_path] = {
                    'path': path,
                    'size': os.path.getsize(path),
                    'modified': os.path.getmtime(path),
                    'hash': get_file_hash(path)
                }
        return index
    
    def on_modified(self, event):
        if not event.is_directory:
            self.sync_to_drive(event.src_path)
    
    def on_created(self, event):
        if not event.is_directory:
            self.sync_to_drive(event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.delete_from_drive(event.src_path)
    
    def sync_to_drive(self, local_path):
        """Sync a local file to Google Drive"""
        try:
            rel_path = os.path.relpath(local_path, self.local_folder)
            file_name = os.path.basename(local_path)
            
            # Skip files that match ignore patterns
            if any(file_name.endswith(pattern) for pattern in self.ignore_patterns):
                return
                
            # Check if file exists in Drive
            file_id = self.drive_api.get_file_id(self.drive_folder_id, file_name)
            
            if file_id:
                # Update existing file
                self.drive_api.update_file(file_id, local_path)
                self.logger.info(f"Updated file in Drive: {rel_path}")
            else:
                # Upload new file
                self.drive_api.upload_file(local_path, self.drive_folder_id)
                self.logger.info(f"Uploaded new file to Drive: {rel_path}")
                
            # Update file index
            if rel_path in self.file_index:
                self.file_index[rel_path]['modified'] = os.path.getmtime(local_path)
                self.file_index[rel_path]['hash'] = get_file_hash(local_path)
            else:
                self.file_index[rel_path] = {
                    'path': local_path,
                    'size': os.path.getsize(local_path),
                    'modified': os.path.getmtime(local_path),
                    'hash': get_file_hash(local_path)
                }
                
        except Exception as e:
            self.logger.error(f"Error syncing to Drive: {str(e)}")
    
    def delete_from_drive(self, local_path):
        """Delete a file from Google Drive"""
        try:
            rel_path = os.path.relpath(local_path, self.local_folder)
            file_name = os.path.basename(local_path)
            
            # Skip files that match ignore patterns
            if any(file_name.endswith(pattern) for pattern in self.ignore_patterns):
                return
                
            # Find corresponding Drive file and delete
            file_id = self.drive_api.get_file_id(self.drive_folder_id, file_name)
            if file_id:
                self.drive_api.delete_file(file_id)
                self.logger.info(f"Deleted file from Drive: {rel_path}")
                
            # Remove from file index
            if rel_path in self.file_index:
                del self.file_index[rel_path]
                
        except Exception as e:
            self.logger.error(f"Error deleting from Drive: {str(e)}")
    
    def poll_drive_changes(self):
        """Poll for changes in Google Drive and sync locally"""
        try:
            drive_files = self.drive_api.list_files(self.drive_folder_id)
            
            for drive_file in drive_files:
                file_name = drive_file['name']
                local_path = os.path.join(self.local_folder, file_name)
                
                # Skip files that match ignore patterns
                if any(file_name.endswith(pattern) for pattern in self.ignore_patterns):
                    continue
                    
                # Check if file exists locally
                if os.path.exists(local_path):
                    # Compare modification times
                    local_modified = os.path.getmtime(local_path)
                    drive_modified = time.mktime(time.strptime(
                        drive_file['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ'
                    ))
                    
                    # If Drive file is newer, download it
                    if drive_modified > local_modified and drive_modified > self.last_sync_time:
                        self.download_from_drive(drive_file, local_path)
                else:
                    # File doesn't exist locally, download it
                    self.download_from_drive(drive_file, local_path)
            
            # Check for deleted files in Drive
            local_files = set(os.listdir(self.local_folder))
            drive_files_set = set(f['name'] for f in drive_files)
            
            for file_name in local_files:
                if file_name not in drive_files_set and not any(
                    file_name.endswith(pattern) for pattern in self.ignore_patterns
                ):
                    local_path = os.path.join(self.local_folder, file_name)
                    if os.path.isfile(local_path):
                        os.remove(local_path)
                        self.logger.info(f"Deleted local file: {file_name}")
            
            self.last_sync_time = time.time()
            
        except Exception as e:
            self.logger.error(f"Error polling Drive changes: {str(e)}")
    
    def download_from_drive(self, drive_file, local_path):
        """Download a file from Google Drive"""
        try:
            file_id = drive_file['id']
            request = self.drive_api.service.files().get_media(fileId=file_id)
            
            ensure_dir(os.path.dirname(local_path))
            with open(local_path, 'wb') as local_file:
                downloader = request.execute()
                local_file.write(downloader)
                
            self.logger.info(f"Downloaded file from Drive: {drive_file['name']}")
            
            # Update file index
            rel_path = os.path.relpath(local_path, self.local_folder)
            self.file_index[rel_path] = {
                'path': local_path,
                'size': os.path.getsize(local_path),
                'modified': os.path.getmtime(local_path),
                'hash': get_file_hash(local_path)
            }
            
        except Exception as e:
            self.logger.error(f"Error downloading from Drive: {str(e)}")

class SyncEngine:
    def __init__(self, local_folder, drive_folder_name, ignore_patterns=None):
        self.local_folder = local_folder
        self.drive_folder_name = drive_folder_name
        self.ignore_patterns = ignore_patterns or []
        self.logger = logging.getLogger('drive_sync')
        self.running = False
        self.observer = None
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(os.path.dirname(__file__), '..', 'sync.log')),
                logging.StreamHandler()
            ]
        )
        
        # Authenticate with Google Drive
        self.creds = authenticate()
        self.drive_api = DriveAPI(self.creds)
        
        # Get or create Drive folder
        self.drive_folder_id = self.drive_api.get_folder_id(drive_folder_name)
        if not self.drive_folder_id:
            self.drive_folder_id = self.drive_api.create_folder(drive_folder_name)
            if not self.drive_folder_id:
                raise Exception(f"Could not create or find Drive folder: {drive_folder_name}")
            self.logger.info(f"Created new Drive folder: {drive_folder_name}")
    
    def start(self):
        """Start the sync engine"""
        self.logger.info(f"Starting sync between {self.local_folder} and Google Drive folder: {self.drive_folder_name}")
        
        # Set up file system watcher
        event_handler = SyncHandler(
            self.drive_api, 
            self.local_folder, 
            self.drive_folder_id,
            self.ignore_patterns
        )
        self.observer = Observer()
        self.observer.schedule(event_handler, self.local_folder, recursive=True)
        self.observer.start()
        self.running = True
        
        try:
            while self.running:
                # Poll for Drive changes periodically
                event_handler.poll_drive_changes()
                time.sleep(60)  # Poll every minute
        except KeyboardInterrupt:
            self.stop()
        finally:
            if self.observer:
                self.observer.stop()
                self.observer.join()
    
    def stop(self):
        """Stop the sync engine"""
        self.logger.info("Stopping sync engine")
        self.running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()