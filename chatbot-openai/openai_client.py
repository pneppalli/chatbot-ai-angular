"""OpenAI client creation and helper functions."""

from typing import Any, Optional
import requests
from config import get_openai_api_key, get_chat_backend, get_ollama_url

try:
    import openai
except Exception:  # pragma: no cover - handled at runtime
    openai = None


def make_openai_client() -> Any:
    """Create and return an OpenAI client object compatible with multiple SDK versions.
    
    If the `openai` package provides a top-level `OpenAI` client class (newer SDK),
    return an instance of that. Otherwise return the `openai` module object
    which exposes legacy functions like `ChatCompletion.create`.
    If `openai` is not importable, returns None.
    """
    if openai is None:
        return None

    # Newer OpenAI SDK exposes an `OpenAI` client class
    if hasattr(openai, "OpenAI"):
        try:
            return openai.OpenAI()
        except Exception:
            # Fall back to the module object if instantiation fails
            return openai

    return openai


def extract_chat_content(resp: Any) -> str:
    """Extract the assistant content from various possible OpenAI response shapes.
    
    The function attempts several common access patterns to be compatible with
    different OpenAI SDK response formats. If none match, returns the
    stringified response.
    """
    try:
        return resp.choices[0].message.content
    except Exception:
        pass

    try:
        return resp.choices[0].message["content"]
    except Exception:
        pass

    try:
        return resp.choices[0].text
    except Exception:
        pass

    return str(resp)


def call_ollama(prompt: str, model: Optional[str] = None, max_tokens: int = 250, temperature: float = 0.7) -> str:
    """Call an Ollama HTTP generate endpoint and return the generated text.
    
    Assumptions: Ollama is available at OLLAMA_URL (default http://localhost:11434)
    and exposes a POST /api/generate endpoint that accepts JSON with keys
    like `model`, `prompt`, `max_tokens`, `temperature`.
    
    The implementation attempts to parse common response shapes and falls
    back to the raw text body.
    """
    base = get_ollama_url()
    endpoint = f"{base}/api/generate"
    payload = {
        "model": model or "",
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    try:
        resp = requests.post(endpoint, json=payload, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"Ollama request failed: {e}")

    # Try to decode JSON and extract common fields
    try:
        j = resp.json()
        # Common shape: { "results": [ { "content": "..." } ] }
        if isinstance(j, dict):
            if "results" in j and isinstance(j["results"], list) and len(j["results"]) > 0:
                first = j["results"][0]
                for key in ("content", "text", "output", "result"):
                    if isinstance(first, dict) and key in first:
                        return first[key]

            for key in ("output", "result", "text", "content"):
                if key in j:
                    return j[key]

        # If the JSON is a string or other primitive, stringify it
        return str(j)
    except ValueError:
        # Not JSON, return raw text
        return resp.text


def initialize_openai_client():
    """Initialize the OpenAI client with API key."""
    if openai is None:
        raise RuntimeError("'openai' package is not installed on the server")
    
    openai.api_key = get_openai_api_key()
    return make_openai_client()
