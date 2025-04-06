from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import json
from pathlib import Path
from ..config import settings
import os

class AuthService:
    def __init__(self):
        self.tokens_file = Path(settings.TOKENS_FILE)
        self.scopes = ['https://www.googleapis.com/auth/gmail.readonly']
        
        # Create client config dict
        self.client_config = {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }

    def get_authorization_url(self, user_id: str) -> str:
        """Generate OAuth URL for user authorization"""
        flow = Flow.from_client_config(
            self.client_config,
            scopes=self.scopes,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        
        # Use user_id as state parameter for security
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=user_id
        )
        
        return auth_url

    async def handle_oauth_callback(self, code: str, state: str):
        """Handle OAuth callback and store tokens"""
        flow = Flow.from_client_config(
            self.client_config,
            scopes=self.scopes,
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
            state=state
        )
        
        # Exchange code for tokens
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Store tokens
        self._save_tokens(state, {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        })
        
        return credentials

    def get_credentials(self, user_id: str) -> Credentials:
        """Get stored credentials for user"""
        tokens = self._load_tokens()
        if user_id not in tokens:
            return None
            
        token_data = tokens[user_id]
        return Credentials(
            token=token_data['token'],
            refresh_token=token_data['refresh_token'],
            token_uri=token_data['token_uri'],
            client_id=token_data['client_id'],
            client_secret=token_data['client_secret'],
            scopes=token_data['scopes']
        )

    def _save_tokens(self, user_id: str, token_data: dict):
        """Save tokens to file"""
        tokens = self._load_tokens()
        tokens[user_id] = token_data
        
        with open(self.tokens_file, 'w') as f:
            json.dump(tokens, f)

    def _load_tokens(self) -> dict:
        """Load tokens from file"""
        if not self.tokens_file.exists():
            return {}
            
        with open(self.tokens_file) as f:
            return json.load(f) 