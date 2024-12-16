import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class to manage environment variables."""
    
    # Google API settings
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Optional API keys for other services if needed
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

    @classmethod
    def validate_config(cls):
        """Validate that all required environment variables are set."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")