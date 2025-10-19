# Quick start script for local Docker deployment

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Chatbot Local Deployment Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker Desktop..." -ForegroundColor Yellow
try {
    docker ps > $null 2>&1
    Write-Host "✓ Docker Desktop is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker Desktop is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠ IMPORTANT: Please edit the .env file and add your OpenAI API key!" -ForegroundColor Red
    Write-Host "Then run this script again." -ForegroundColor Yellow
    Write-Host ""
    notepad .env
    exit 0
}

# Check if OpenAI API key is set
$envContent = Get-Content ".env" -Raw
if ($envContent -match "your_openai_api_key_here") {
    Write-Host ""
    Write-Host "⚠ IMPORTANT: Please edit the .env file and add your OpenAI API key!" -ForegroundColor Red
    Write-Host "Opening .env file for editing..." -ForegroundColor Yellow
    Write-Host ""
    notepad .env
    exit 0
}

Write-Host ""
Write-Host "Starting Docker containers..." -ForegroundColor Yellow
Write-Host ""

# Build and run containers
docker-compose up --build
