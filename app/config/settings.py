# app/config/settings.py
"""
Application settings loader using python-dotenv.
This makes environment variables accessible across the app.
"""

import os
from dotenv import load_dotenv
# from pydantic import BaseSettings
from pydantic_settings import BaseSettings


# Load .env file
load_dotenv()


class Settings(BaseSettings):
    # Environment variables
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    APP_NAME: str = "LCA Backend"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


# Singleton pattern: one instance of settings used throughout the app
settings = Settings()


def get_settings() -> Settings:
    """
    Returns the settings object.
    Import and call this function anywhere in your code to get config values.
    Example:
        from app.config import get_settings
        api_key = get_settings().GROQ_API_KEY
    """
    return settings
