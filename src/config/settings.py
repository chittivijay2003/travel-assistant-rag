"""Application settings and configuration management."""

from functools import lru_cache
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # Application
    app_name: str = Field(
        default="Travel Assistant RAG", description="Application name"
    )
    environment: str = Field(default="development", description="Environment")
    debug: bool = Field(default=False, description="Debug mode")

    # Google Gemini
    google_api_key: str = Field(..., description="Google Gemini API key")
    gemini_model: str = Field(
        default="gemini-2.0-flash", description="Gemini model name"
    )
    embedding_model: str = Field(
        default="models/embedding-001", description="Embedding model"
    )

    @property
    def gemini_api_key(self) -> str:
        """Alias for google_api_key for backward compatibility."""
        return self.google_api_key

    # Qdrant
    qdrant_host: str = Field(default="localhost", description="Qdrant host")
    qdrant_port: int = Field(default=6333, description="Qdrant port")
    qdrant_collection: str = Field(
        default="travel_documents", description="Qdrant collection name"
    )
    qdrant_api_key: Optional[str] = Field(default=None, description="Qdrant API key")
    qdrant_use_memory: bool = Field(default=True, description="Use in-memory Qdrant")

    # API
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_reload: bool = Field(default=True, description="API auto-reload")

    # UI
    ui_port: int = Field(default=7860, description="UI port")
    ui_share: bool = Field(default=False, description="Share UI publicly")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(default="logs/app.log", description="Log file path")
    log_format: str = Field(default="json", description="Log format (json/text)")
    log_rotation: str = Field(default="daily", description="Log rotation (daily/size)")

    # Search
    search_top_k: int = Field(
        default=5, ge=1, le=20, description="Number of results to retrieve"
    )
    hybrid_alpha: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Hybrid search weight (0=keyword, 1=semantic)",
    )

    # RAG
    rag_max_context_length: int = Field(
        default=2000, description="Max context length for RAG"
    )
    rag_temperature: float = Field(
        default=0.7, ge=0.0, le=2.0, description="LLM temperature"
    )
    rag_max_tokens: int = Field(default=1024, description="Max tokens for LLM response")

    # LLM Settings (aliases for backward compatibility)
    @property
    def llm_temperature(self) -> float:
        """Alias for rag_temperature."""
        return self.rag_temperature

    @property
    def llm_max_tokens(self) -> int:
        """Alias for rag_max_tokens."""
        return self.rag_max_tokens

    @property
    def llm_top_p(self) -> float:
        """Top P for LLM."""
        return 0.95

    @property
    def llm_top_k(self) -> int:
        """Top K for LLM."""
        return 40

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in allowed:
            raise ValueError(f"Log level must be one of {allowed}")
        return v

    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"

    @property
    def qdrant_url(self) -> str:
        """Get Qdrant URL."""
        return f"http://{self.qdrant_host}:{self.qdrant_port}"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
