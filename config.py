# config.py
"""Configuration settings for the PDF service."""

import os
from typing import Dict, Any

class Config:
    """Application configuration."""
    
    # API Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8734  # Random port as requested
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GPT_MODEL: str = "gpt-4"  # Will use GPT-5 when available
    
    # PDF Generation Settings
    DEFAULT_PAGE_SIZE: str = "A4"
    DEFAULT_MARGINS: Dict[str, int] = {
        "top": 72,
        "bottom": 72,
        "left": 72,
        "right": 72
    }
    
    # File Settings
    MAX_FILE_SIZE_MB: int = 50
    TEMP_DIR: str = os.getenv("TEMP_DIR", "/tmp")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration."""
        if not cls.OPENAI_API_KEY:
            print("Warning: OPENAI_API_KEY not set")
            return False
        return True


