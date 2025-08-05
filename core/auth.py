from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path
import pickle
import json
import logging

SCOPES = ['https://www.googleapis.com/auth/drive']

# Pre-configured OAuth client configuration
# This is a sample client ID - in production, you'd use your own
OAUTH_CLIENT_CONFIG = {
    "web": {
        "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
        "project_id": "your-project-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "YOUR_CLIENT_SECRET",
        "redirect_uris": ["http://localhost:8080/oauth2callback"]
    }
}

def authenticate():
    """Authenticate with Google Drive API using OAuth 2.0"""
    creds = None
    
    # Check if we have saved credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use the pre-configured OAuth client
            flow = Flow.from_client_config(
                OAUTH_CLIENT_CONFIG,
                scopes=SCOPES
            )
            flow.redirect_uri = 'http://localhost:8080/oauth2callback'
            
            # Generate authorization URL
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true'
            )
            
            print(f"Please visit this URL to authorize the application: {auth_url}")
            print("After authorization, you'll be redirected to localhost:8080/oauth2callback")
            
            # For web-based flow, we'll handle the callback in the Flask app
            # This function will be called from the web interface
            return None
            
        # Save credentials for next run
        if creds:
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
    
    return creds

def authenticate_with_code(authorization_code):
    """Complete OAuth flow with authorization code from web callback"""
    try:
        flow = Flow.from_client_config(
            OAUTH_CLIENT_CONFIG,
            scopes=SCOPES
        )
        flow.redirect_uri = 'http://localhost:8080/oauth2callback'
        
        # Exchange authorization code for credentials
        flow.fetch_token(code=authorization_code)
        creds = flow.credentials
        
        # Save credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
        return creds
    except Exception as e:
        logging.error(f"Error during OAuth authentication: {str(e)}")
        return None

def get_auth_url():
    """Get the authorization URL for OAuth flow"""
    flow = Flow.from_client_config(
        OAUTH_CLIENT_CONFIG,
        scopes=SCOPES
    )
    flow.redirect_uri = 'http://localhost:8080/oauth2callback'
    
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    return auth_url, state

def is_authenticated():
    """Check if user is already authenticated"""
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            return creds and creds.valid
    return False

def clear_credentials():
    """Clear saved credentials"""
    if os.path.exists('token.pickle'):
        os.remove('token.pickle')