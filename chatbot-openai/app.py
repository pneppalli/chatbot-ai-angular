from typing import Optional, Any
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

try:
    import openai
except Exception:  # pragma: no cover - handled at runtime
    openai = None


def get_api_key() -> str:
  """Return the OPENAI_API_KEY from the environment or raise RuntimeError.

  This intentionally does not expose the key value anywhere else.
  """
  key = os.getenv("OPENAI_API_KEY")
  if not key:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set")
  return key


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


def _extract_chat_content(resp: Any) -> str:
    """Extracts the assistant content from various possible OpenAI response shapes.

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


app = FastAPI(title="Simple OpenAI Chatbot API")

# Allow local frontend origins for development
app.add_middleware(
    CORSMiddleware,
    # Allow local frontend origins for development (include both 4200 and 8040)
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "http://localhost:8040",
        "http://127.0.0.1:8040",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/status")
def status():
  """Return a minimal status indicating whether the OpenAI API key is configured.

  This intentionally does NOT return the key value.
  """
  has_key = bool(os.getenv("OPENAI_API_KEY"))
  return {"has_api_key": has_key}


class ChatRequest(BaseModel):
  message: str
  model: Optional[str] = "gpt-3.5-turbo"
  use_basic: Optional[bool] = False


@app.post("/chat")
def chat(req: ChatRequest):
  try:
    print("[chat] handler invoked", flush=True)
    print("[chat] request:", req.json(), flush=True)

    if openai is None:
      print("[chat] openai package is missing", flush=True)
      raise HTTPException(status_code=500, detail="'openai' package is not installed on the server")

    try:
      openai.api_key = get_api_key()
    except RuntimeError as e:
      print("[chat] missing API key:", str(e), flush=True)
      raise HTTPException(status_code=500, detail=str(e))

    # If the client requested the basic completion API, use it
    client = make_openai_client()
    if req.use_basic:
      prompt = f"User: {req.message}\nAssistant:"
      print("[chat] using basic Completion API, prompt=", prompt, flush=True)
      try:
        if hasattr(client, "completions"):
          resp = client.completions.create(model=req.model or "text-davinci-003", prompt=prompt, max_tokens=250, temperature=0.7)
        else:
          resp = openai.Completion.create(model=req.model or "text-davinci-003", prompt=prompt, max_tokens=250, temperature=0.7)
        content = _extract_chat_content(resp).strip()
        print("[chat] completion result length=", len(content), flush=True)
        return {"reply": content}
      except Exception as exc:
        print("[chat] completion exception:", repr(exc), flush=True)
        raise HTTPException(status_code=502, detail=str(exc))

    # Otherwise use the ChatCompletion API
    messages = [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": req.message},
    ]
    print("[chat] using ChatCompletion API, messages=", messages, flush=True)

    try:
      if hasattr(client, "chat"):
        resp = client.chat.completions.create(model=req.model, messages=messages)
      else:
        resp = openai.ChatCompletion.create(model=req.model, messages=messages)
      content = _extract_chat_content(resp).strip()
      print("[chat] chatcompletion result length=", len(content), flush=True)
      return {"reply": content}
    except Exception as exc:
      print("[chat] chatcompletion exception:", repr(exc), flush=True)
      raise HTTPException(status_code=502, detail=str(exc))
  except HTTPException:
    # re-raise FastAPI HTTPExceptions unchanged
    raise
  except Exception as exc:
    # Catch everything else and return a 500 with the error string
    print("[chat] unexpected exception:", repr(exc), flush=True)
    raise HTTPException(status_code=500, detail=str(exc))
