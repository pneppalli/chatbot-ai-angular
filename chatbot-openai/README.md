# Chatbot (Python)

This folder contains the Python backend for the chatbot extracted from the repository's `chatbot/` directory.

Quick start (Windows PowerShell):

```powershell
cd chatbot-python
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Start FastAPI server
uvicorn app:app --host 0.0.0.0 --port 8000
```

Set `OPENAI_API_KEY` in the environment before running (or use a .env loader).

Start the FastAPI server (Windows PowerShell):

```powershell
cd chatbot-python
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Start FastAPI server
uvicorn app:app --host 0.0.0.0 --port 8000
```
