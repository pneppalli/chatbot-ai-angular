Param()

Write-Host "Starting Gradio UI from chatbot-python..."
Set-Location -Path $PSScriptRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found in PATH. Activate your virtualenv or ensure Python is installed."
    exit 1
}

python gradio_app.py
