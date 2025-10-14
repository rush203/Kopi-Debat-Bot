"""Configuration management for the debate bot API."""

from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    # API Settings
    app_name: str = "Kopi Debate Bot"
    app_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # OpenRouter/OpenAI Settings
    openai_api_key: str =""
    openai_base_url: str = "https://openrouter.ai/api/v1"
    openai_model: str = "openai/o1"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 500
    
    # Conversation Settings
    max_history_messages: int = 5
    conversation_timeout_seconds: int = 3600  # 1 hour
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


settings = Settings()

