from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path
from typing import List

class Settings(BaseSettings):
    # Google OAuth settings
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str
    google_scopes: str

    # Application settings
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    
    # Storage Settings
    TOKENS_FILE: str = "tokens.json"
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"
    }

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 