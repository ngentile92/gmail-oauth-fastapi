from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from typing import List
import json
import os
from datetime import datetime
from .config import settings
from .schemas import EmailResponse
from .services.gmail_service import GmailService
from .services.auth_service import AuthService

app = FastAPI(title="Gmail Bot Module", description="OAuth + Mail Reader Service")
auth_service = AuthService()
gmail_service = GmailService()

@app.get("/")
async def root():
    return {"message": "Gmail Bot Module API"}

@app.get("/login/{user_id}")
async def login(user_id: str):
    """Generate OAuth login URL for a specific user"""
    auth_url = auth_service.get_authorization_url(user_id)
    return {"auth_url": auth_url}

@app.get("/oauth/callback")
async def oauth_callback(state: str, code: str):
    """Handle OAuth callback and store tokens"""
    try:
        user_id = state  # state contains the user_id
        tokens = await auth_service.handle_oauth_callback(code, state)
        return {"message": "Authentication successful! You can close this window."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/unread_emails/{user_id}", response_model=List[EmailResponse])
async def get_unread_emails(user_id: str):
    """Get last 5 unread emails for a user"""
    try:
        credentials = auth_service.get_credentials(user_id)
        if not credentials:
            raise HTTPException(status_code=401, detail="User not authenticated")
        
        emails = await gmail_service.get_unread_emails(credentials)
        return emails[:5]  # Return only the last 5 emails
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 