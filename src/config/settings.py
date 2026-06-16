"""
Application Configuration Management
====================================

Centralized configuration management using Pydantic for validation.
All environment variables and application settings are defined here.

Design Pattern: Singleton Configuration
Security: Secrets loaded from environment, never hardcoded
"""

from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path


class Settings(BaseSettings):
    """
    Application settings with validation and type safety.
    
    All settings are loaded from environment variables or .env file.
    Pydantic ensures type safety and validation.
    """
    
    # ===== Application Settings =====
    APP_NAME: str = "TravelAgent Pro"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"  # development, staging, production
    DEBUG: bool = False
    
    # ===== API Settings =====
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    
    # ===== CORS Settings =====
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8000",  # FastAPI
        "https://yourdomain.com",  # Production domain
    ]
    
    # ===== LiveKit Configuration =====
    LIVEKIT_URL: str
    LIVEKIT_API_KEY: str
    LIVEKIT_API_SECRET: str
    
    # ===== AI Service Keys =====
    GROQ_API_KEY: str
    DEEPGRAM_API_KEY: str
    GOOGLE_API_KEY: Optional[str] = None
    
    # ===== Model Selection =====
    LLM_CHOICE: str = "llama-3.1-8b-instant"
    
    # ===== MCP Server URLs =====
    AIRBNB_MCP_ENABLED: bool = True
    FLIGHT_MCP_URL: str = "https://flights.fctolabs.com/mcp"
    FLIGHT_MCP_ENABLED: bool = True
    
    # ===== Database Settings (for future expansion) =====
    DATABASE_URL: Optional[str] = None
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    
    # ===== Redis Cache (optional) =====
    REDIS_URL: Optional[str] = None
    CACHE_TTL: int = 3600  # 1 hour default
    
    # ===== Logging Configuration =====
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text
    LOG_FILE: Optional[str] = "app.log"  # Just filename, not path
    
    # ===== Rate Limiting =====
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # ===== Session Management =====
    SESSION_SECRET_KEY: str = "change-this-in-production-use-strong-key"
    SESSION_TIMEOUT_MINUTES: int = 30
    
    # ===== File Upload Settings =====
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_UPLOAD_TYPES: list[str] = ["image/jpeg", "image/png", "application/pdf"]
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached singleton).
    
    Returns:
        Settings: Application configuration
        
    Note:
        Uses @lru_cache to ensure settings are loaded only once
    """
    return Settings()


# Convenience accessor
settings = get_settings()


# ===== Path Configuration =====
class Paths:
    """Application path configuration"""
    
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    SRC_DIR = BASE_DIR / "src"
    STATIC_DIR = BASE_DIR / "static"
    TEMPLATES_DIR = BASE_DIR / "templates"
    LOGS_DIR = BASE_DIR / "logs"
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Create necessary directories if they don't exist"""
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.STATIC_DIR.mkdir(exist_ok=True)
        cls.TEMPLATES_DIR.mkdir(exist_ok=True)


# Create directories on import
Paths.ensure_directories()
