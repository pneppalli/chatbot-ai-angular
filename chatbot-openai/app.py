from typing import Optional
import os
import sys

from typing import Optional
import os
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

try:
    import openai
except Exception:  # pragma: no cover - handled at runtime
    openai = None


def get_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")
    return key


def make_openai_client():
  if openai is None:
    return None
  if hasattr(openai, "OpenAI"):
    try:
      return openai.OpenAI()
    except Exception:
      return openai
  return openai


def _extract_chat_content(resp):
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


@app.get("/", response_class=HTMLResponse)
def index():
    # Very small single-file web client for quick demos
    return """<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Simple Chatbot</title>
    <style>body{font-family:Arial,Helvetica,sans-serif;margin:2rem}#log{white-space:pre-wrap;border:1px solid #ddd;padding:1rem;height:60vh;overflow:auto}form{margin-top:1rem}</style>
  </head>
  <body>
    <h1>Simple OpenAI Chatbot</h1>
    <div id="log"></div>
    <form id="f" onsubmit="return send(event);">
      <input id="m" autocomplete="off" style="width:80%" placeholder="Type your message..." autofocus />
      <button type="submit">Send</button>
    </form>
    <script>
      const log = document.getElementById('log');
      const msgInput = document.getElementById('m');
      async function send(e){
        if(e && e.preventDefault) e.preventDefault();
        const text = msgInput.value.trim();
        if(!text) return false;
        log.innerText += '\nYou: ' + text + '\n';
        msgInput.value = '';
        try{
          const res = await fetch('/chat', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});
          const j = await res.json();
          if(res.ok){
            log.innerText += 'Assistant: ' + j.reply + '\n';
          } else {
            log.innerText += 'Error: ' + (j.detail || JSON.stringify(j)) + '\n';
          }
        }catch(err){
          log.innerText += 'Network error: ' + err + '\n';
        }
        log.scrollTop = log.scrollHeight;
        return false;
      }
    </script>
  </body>
</html>"""



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
