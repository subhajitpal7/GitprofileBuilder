"""
Configuration module implementing a singleton pattern using metaclass.
Ensures only one instance of Config exists throughout the application.
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv

class Singleton(type):
    """
    Metaclass for implementing the Singleton pattern.
    Ensures only one instance of a class is created.
    """
    _instances: Dict[type, object] = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=Singleton):
    """
    Configuration class to manage environment variables.
    Implements singleton pattern to ensure only one config instance exists.
    """
    
    def __init__(self):
        """Initialize the config and load environment variables."""
        # Load environment variables from .env file
        load_dotenv()
        
        # Google API settings
        self._GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
        
        # Optional API keys for other services
        self._huggingface_api_key: Optional[str] = os.getenv("HUGGINGFACE_API_KEY")
        
        # Validate configuration on initialization
        self.validate_config()
    
    @property
    def GOOGLE_API_KEY(self) -> str:
        """Get Google API key."""
        return self._GOOGLE_API_KEY
    
    @property
    def HUGGINGFACE_API_KEY(self) -> Optional[str]:
        """Get HuggingFace API key if available."""
        return self._huggingface_api_key
    
    def validate_config(self) -> None:
        """Validate that all required environment variables are set."""
        if not self._GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    def reload(self) -> None:
        """Reload configuration from environment variables."""
        load_dotenv()
        self._GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self._huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.validate_config()
    
    def __str__(self) -> str:
        """String representation of config state."""
        return (f"Config(google_api_key={'*' * 8 if self._GOOGLE_API_KEY else 'Not Set'}, "
                f"huggingface_api_key={'*' * 8 if self._huggingface_api_key else 'Not Set'})")
    
    def __repr__(self) -> str:
        """Developer representation of config state."""
        return self.__str__()