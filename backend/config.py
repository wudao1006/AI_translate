"""
Configuration management for AI Translation Assistant.
Loads settings from environment variables with sensible defaults.
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationInfo
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Provider Configuration
    llm_provider: Literal["openai", "claude", "deepseek", "qwen"] = "openai"
    llm_api_key: str = ""
    llm_model: str = "gpt-3.5-turbo"
    llm_timeout: int = 30
    llm_base_url: str = ""  # Optional custom base URL for compatible providers

    # API Configuration
    max_text_length: int = 4000
    cors_origins: list[str] = ["*"]

    # Logging
    log_level: str = "INFO"

    @field_validator("llm_api_key")
    @classmethod
    def validate_api_key(cls, v: str, info: ValidationInfo) -> str:
        """Validate that API key is not empty."""
        if not v or v.strip() == "":
            raise ValueError(
                "LLM_API_KEY is required! Please set it in your .env file.\n"
                "Example: LLM_API_KEY=sk-your-api-key-here"
            )
        return v.strip()

    @field_validator("llm_base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """Clean up base URL (remove quotes if present)."""
        return v.strip().strip('"').strip("'")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
