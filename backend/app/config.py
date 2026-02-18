"""Configuration module for the CodeScale Research Radar backend.

Handles environment variables and LiteLLM configuration.
"""

import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        """Initialize settings from environment."""
        # Database
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///./radar.db")

        # Server
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"

        # LiteLLM / xAI Configuration
        self.xai_api_key: Optional[str] = os.getenv("XAI_API_KEY")
        self.default_model: str = os.getenv("DEFAULT_MODEL", "xai/grok-beta")

        # LiteLLM General Settings
        self.litellm_timeout: int = int(os.getenv("LITELLM_TIMEOUT", "60"))
        self.litellm_max_retries: int = int(os.getenv("LITELLM_MAX_RETRIES", "3"))

    @property
    def is_ai_configured(self) -> bool:
        """Check if AI services are properly configured.

        Returns:
            True if API key is set.
        """
        return bool(self.xai_api_key)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        The application settings.
    """
    return Settings()


def configure_litellm() -> None:
    """Configure LiteLLM with application settings.

    This should be called at application startup.
    """
    import litellm

    settings = get_settings()

    # Set API key
    if settings.xai_api_key:
        litellm.xai_key = settings.xai_api_key

    # Configure general LiteLLM settings
    litellm.request_timeout = settings.litellm_timeout
    litellm.num_retries = settings.litellm_max_retries

    # Enable verbose logging in debug mode
    if settings.debug:
        litellm.set_verbose = True
