from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    mistral_api_key: str
    upload_dir: str = "uploads"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
