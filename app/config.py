from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path

class Settings(BaseSettings):
    # Google OAuth Settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/oauth/callback"
    
    # Application Settings
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000
    
    # Storage Settings
    TOKENS_FILE: str = "tokens.json"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 