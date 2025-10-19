"""Configuration management for the chatbot application."""

import os
from typing import Optional


def get_openai_api_key() -> str:
    """Return the OPENAI_API_KEY from the environment or raise RuntimeError.
    
    This intentionally does not expose the key value anywhere else.
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")
    return key


def get_pushover_user_key() -> Optional[str]:
    """Return the PUSHOVER_USER_KEY from the environment."""
    return os.getenv("PUSHOVER_USER_KEY")


def get_pushover_api_token() -> Optional[str]:
    """Return the PUSHOVER_API_TOKEN from the environment."""
    return os.getenv("PUSHOVER_API_TOKEN")


def get_chat_backend() -> str:
    """Backend selection: 'openai' (default) or 'ollama'."""
    return os.getenv("CHAT_BACKEND", "openai").strip().lower()


def get_ollama_url() -> str:
    """Return the Ollama service URL."""
    return os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")


# CORS allowed origins for development
CORS_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:8040",
    "http://127.0.0.1:8040",
]
