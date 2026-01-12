from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    # Application
    app_name: str = "MotoGP App"
    app_version: str = "0.1.0"
    debug: bool = True
    environment: str = "development"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: str
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "user"
    db_password: str = "password"
    db_name: str = "motogp_db"
    
    # backend 
    BACKEND_ROOT: Path = Path(__file__).resolve().parent.parent
    CHROMEDRIVER_PATH: Path = BACKEND_ROOT / "drivers" / "chromedriver"

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # MotoGP API
    motogp_api_key: str = ""
    motogp_api_url: str = "https://api.motogp.com/v1"

    # Supabase Storage
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_BUCKET: str = "motogp-pdfs"
    
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
