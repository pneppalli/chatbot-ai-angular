import os
from typing import Optional


def get_openai_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")
    return key


def get_pushover_user_key() -> Optional[str]:
    return os.getenv("PUSHOVER_USER_KEY")


def get_pushover_api_token() -> Optional[str]:
    return os.getenv("PUSHOVER_API_TOKEN")


def get_chat_backend() -> str:
    return os.getenv("CHAT_BACKEND", "openai").strip().lower()


def get_ollama_url() -> str:
    return os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")


CORS_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:8040",
    "http://127.0.0.1:8040",
]
