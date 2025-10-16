"""Configuration management for the debate-bot API."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-wide settings loaded from .env or the OS environment."""

    # tell Pydantic Settings where to find .env
    model_config = SettingsConfigDict(
        env_file=".env",          # ← same directory as main.py
        env_file_encoding="utf-8",
        case_sensitive=False,     # OPENAI_API_KEY or openai_api_key both fine
    )

    # ── API settings ────────────────────────────────
    app_name: str = "Kopi Debate Bot"
    app_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int =8000

    # ── OpenAI / OpenRouter settings ────────────────
    openai_api_key: str                 # ← required (no default)
    openai_base_url: str = "https://openrouter.ai/api/v1"
    openai_model: str = "meta-llama/llama-3.1-8b-instruct"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 500

    # ── Conversation settings ───────────────────────
    max_history_messages: int = 5
    conversation_timeout_seconds: int = 3600


settings = Settings()
