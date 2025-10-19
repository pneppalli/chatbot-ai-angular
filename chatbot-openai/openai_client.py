from typing import Any, Optional
import requests
from config import get_openai_api_key, get_chat_backend, get_ollama_url

try:
    import openai
except Exception:
    openai = None


def make_openai_client() -> Any:
    if openai is None:
        return None

    if hasattr(openai, "OpenAI"):
        try:
            return openai.OpenAI()
        except Exception:
            return openai

    return openai


def extract_chat_content(resp: Any) -> str:
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

    try:
        j = resp.json()
        if isinstance(j, dict):
            if "results" in j and isinstance(j["results"], list) and len(j["results"]) > 0:
                first = j["results"][0]
                for key in ("content", "text", "output", "result"):
                    if isinstance(first, dict) and key in first:
                        return first[key]

            for key in ("output", "result", "text", "content"):
                if key in j:
                    return j[key]

        return str(j)
    except ValueError:
        return resp.text


def initialize_openai_client():
    if openai is None:
        raise RuntimeError("'openai' package is not installed on the server")
    
    openai.api_key = get_openai_api_key()
    return make_openai_client()
