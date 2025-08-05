from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import logging

class DriveAPI:
    def __init__(self, creds):
        self.service = build('drive', 'v3', credentials=creds)
        self.logger = logging.getLogger('drive_sync')
    
    def get_folder_id(self, folder_name):
        """Get the ID of a folder by name"""
        try:
            response = self.service.files().list(
                q=f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_name}'",
                spaces='drive'
            ).execute()
            return response['files'][0]['id'] if response['files'] else None
        except Exception as e:
            self.logger.error(f"Error getting folder ID: {str(e)}")
            return None
    
    def create_folder(self, folder_name, parent_id=None):
        """Create a new folder in Google Drive"""
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_id:
                file_metadata['parents'] = [parent_id]
                
            folder = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            return folder.get('id')
        except Exception as e:
            self.logger.error(f"Error creating folder: {str(e)}")
            return None
    
    def upload_file(self, local_path, parent_id):
        """Upload a file to Google Drive"""
        try:
            file_name = os.path.basename(local_path)
            media = MediaFileUpload(local_path, resumable=True)
            
            file_metadata = {'name': file_name, 'parents': [parent_id]}
            return self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
        except Exception as e:
            self.logger.error(f"Error uploading file: {str(e)}")
            return None
    
    def update_file(self, file_id, local_path):
        """Update an existing file in Google Drive"""
        try:
            media = MediaFileUpload(local_path, resumable=True)
            return self.service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()
        except Exception as e:
            self.logger.error(f"Error updating file: {str(e)}")
            return None
    
    def delete_file(self, file_id):
        """Delete a file from Google Drive"""
        try:
            self.service.files().delete(fileId=file_id).execute()
            return True
        except Exception as e:
            self.logger.error(f"Error deleting file: {str(e)}")
            return False
    
    def list_files(self, folder_id):
        """List all files in a folder"""
        try:
            response = self.service.files().list(
                q=f"'{folder_id}' in parents",
                fields="files(id, name, modifiedTime, size)"
            ).execute()
            return response.get('files', [])
        except Exception as e:
            self.logger.error(f"Error listing files: {str(e)}")
            return []
    
    def get_file_id(self, folder_id, file_name):
        """Get the ID of a file by name in a specific folder"""
        try:
            response = self.service.files().list(
                q=f"name='{file_name}' and '{folder_id}' in parents",
                fields="files(id)"
            ).execute()
            files = response.get('files', [])
            return files[0]['id'] if files else None
        except Exception as e:
            self.logger.error(f"Error getting file ID: {str(e)}")
            return None