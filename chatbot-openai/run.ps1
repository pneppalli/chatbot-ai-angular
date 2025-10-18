Param()

Write-Host "Starting FastAPI server (uvicorn) from chatbot-python..."

# Ensure the script is run from the script's directory
Set-Location -Path $PSScriptRoot

if (-not (Get-Command uvicorn -ErrorAction SilentlyContinue)) {
    Write-Host "uvicorn not found in PATH. Activate your virtualenv or install requirements: pip install -r requirements.txt"
    exit 1
}

uvicorn app:app --host 0.0.0.0 --port 8000
