# OAuth Setup Guide

This guide will help you set up OAuth 2.0 credentials for the Google Drive Sync Tool.

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" at the top of the page
3. Click "New Project"
4. Enter a project name (e.g., "Drive Sync Tool")
5. Click "Create"

## Step 2: Enable the Google Drive API

1. In your new project, go to the [APIs & Services > Library](https://console.cloud.google.com/apis/library)
2. Search for "Google Drive API"
3. Click on "Google Drive API"
4. Click "Enable"

## Step 3: Create OAuth 2.0 Credentials

1. Go to [APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: "Drive Sync Tool"
   - User support email: Your email
   - Developer contact information: Your email
   - Save and continue through the other sections
4. Back in "Create OAuth client ID":
   - Application type: Web application
   - Name: "Drive Sync Tool Web Client"
   - Authorized redirect URIs: `http://localhost:8080/oauth2callback`
   - Click "Create"

## Step 4: Update the Application

1. Copy your Client ID and Client Secret from the credentials page
2. Open `core/auth.py` in the application
3. Replace the placeholder values in `OAUTH_CLIENT_CONFIG`:

```python
OAUTH_CLIENT_CONFIG = {
    "web": {
        "client_id": "YOUR_ACTUAL_CLIENT_ID.apps.googleusercontent.com",
        "project_id": "your-actual-project-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "YOUR_ACTUAL_CLIENT_SECRET",
        "redirect_uris": ["http://localhost:8080/oauth2callback"]
    }
}
```

## Step 5: Test the Application

1. Run the application: `python app.py`
2. Open http://localhost:8080 in your browser
3. Click "Sign in with Google"
4. Complete the OAuth flow in the popup window
5. You should see "Authentication Successful!"

## Security Notes

- Keep your client secret secure and never share it publicly
- The application stores authentication tokens locally in `token.pickle`
- You can revoke access at any time from your Google Account settings

## Troubleshooting

- **"Invalid client" error**: Make sure you've updated the client ID and secret correctly
- **"Redirect URI mismatch"**: Ensure the redirect URI in your OAuth credentials matches exactly: `http://localhost:8080/oauth2callback`
- **"Access blocked"**: Make sure you've enabled the Google Drive API in your project 