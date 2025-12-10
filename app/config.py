"""
Configuration management for the application.

This module handles loading environment variables from the .env file
using Pydantic's settings management.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        mistral_api_key (str): API key for Mistral AI service
        upload_dir (str): Directory for file uploads (default: "uploads")
    """
    mistral_api_key: str
    upload_dir: str = "uploads"

    class Config:
        """Pydantic configuration."""
        env_file = ".env"  # Load variables from .env file


@lru_cache()
def get_settings():
    """
    Get application settings singleton.
    
    Uses lru_cache to ensure settings are loaded only once
    and reused across the application.
    
    Returns:
        Settings: Application configuration instance
    """
    return Settings()
