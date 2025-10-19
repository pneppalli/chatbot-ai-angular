# Docker Deployment Guide - Refactored Architecture

## Overview
This guide covers deploying the refactored chatbot application (with modular architecture) using Docker and Docker Compose locally.

## What Changed in Refactoring

### Before (Monolithic)
- Single `app.py` file (554 lines)
- No `gradio_app.py` needed

### After (Modular)
- `config.py` - Configuration (47 lines)
- `models.py` - Data models (18 lines)  
- `openai_client.py` - OpenAI integration (124 lines)
- `notifications.py` - Pushover alerts (102 lines)
- `tools.py` - Function calling (204 lines)
- `app.py` - FastAPI routes (365 lines)

## Updated Files

### ✅ Backend Dockerfile
**Updated:** Removed `gradio_app.py`, added `curl` for health checks

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (including curl for health checks)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy refactored modules
COPY config.py .
COPY models.py .
COPY openai_client.py .
COPY notifications.py .
COPY tools.py .
COPY app.py .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### ✅ docker-compose.yml
**Updated:** Added Pushover environment variables and health checks

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./chatbot-openai
      dockerfile: Dockerfile
    container_name: chatbot-backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PUSHOVER_USER_KEY=${PUSHOVER_USER_KEY:-}
      - PUSHOVER_API_TOKEN=${PUSHOVER_API_TOKEN:-}
    env_file:
      - .env
    networks:
      - chatbot-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  frontend:
    build:
      context: ./chatbot-ui
      dockerfile: Dockerfile
    container_name: chatbot-frontend
    ports:
      - "4200:80"
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - chatbot-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:80"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 20s

networks:
  chatbot-network:
    driver: bridge
```

### ✅ New .dockerignore Files

**chatbot-openai/.dockerignore**
```
__pycache__/
venv/
.env
*.md
*.ps1
*.log
.git/
.vscode/
```

**chatbot-ui/.dockerignore**
```
node_modules/
dist/
.angular/
.env
*.md
*.log
.git/
static_test/
```

## Deployment Commands

### First Time Setup
```powershell
# 1. Make sure .env file exists with your keys
if (!(Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "⚠️ Edit .env and add your API keys!"
    notepad .env
}

# 2. Build images
docker-compose build

# 3. Start services
docker-compose up -d

# 4. Check status
docker-compose ps
```

### Rebuild After Code Changes
```powershell
# Quick rebuild (code changes only)
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build backend
docker-compose up -d --build frontend

# Full rebuild (dependencies changed)
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### View Logs
```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 50 lines
docker-compose logs --tail=50 backend
```

### Health Checks
```powershell
# Check health status
docker-compose ps

# Detailed health
docker inspect chatbot-backend --format='{{.State.Health.Status}}'
docker inspect chatbot-frontend --format='{{.State.Health.Status}}'

# Test endpoints
curl http://localhost:8000/
curl http://localhost:8000/status
Start-Process "http://localhost:4200"
```

### Stop and Cleanup
```powershell
# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Remove everything including images
docker-compose down --rmi all

# Full cleanup with volumes
docker-compose down -v --rmi all
```

## Verification Checklist

Before deploying, verify all files exist:

```powershell
# Run this to check all required files
$files = @(
    "chatbot-openai/config.py",
    "chatbot-openai/models.py",
    "chatbot-openai/openai_client.py",
    "chatbot-openai/notifications.py",
    "chatbot-openai/tools.py",
    "chatbot-openai/app.py",
    "chatbot-openai/requirements.txt",
    "chatbot-openai/Dockerfile",
    "chatbot-openai/.dockerignore",
    "chatbot-ui/Dockerfile",
    "chatbot-ui/.dockerignore",
    "docker-compose.yml",
    ".env"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file MISSING!" -ForegroundColor Red
    }
}
```

## Troubleshooting

### Backend Won't Start
```powershell
# Check logs
docker-compose logs backend

# Common issues:
# 1. Missing .env file
# 2. Invalid OPENAI_API_KEY
# 3. Port 8000 in use
# 4. Module import errors

# Fix port conflict
netstat -ano | findstr :8000
# Kill process or change port in docker-compose.yml
```

### Frontend Build Fails
```powershell
# Check logs
docker-compose logs frontend

# Common issues:
# 1. Not enough memory (increase Docker memory limit)
# 2. npm install failures
# 3. Angular build errors

# Increase Docker memory:
# Docker Desktop -> Settings -> Resources -> Memory
```

### Health Check Failing
```powershell
# Enter container
docker exec -it chatbot-backend bash

# Test endpoint
curl http://localhost:8000/

# Check process
ps aux | grep uvicorn

# Check logs
cat /proc/1/fd/1
```

### Module Not Found Errors
```powershell
# Verify all modules copied
docker exec chatbot-backend ls -la

# Should see:
# config.py
# models.py
# openai_client.py
# notifications.py
# tools.py
# app.py

# If missing, rebuild
docker-compose build --no-cache backend
```

## Testing the Deployment

### 1. Backend API
```powershell
# Root endpoint
curl http://localhost:8000/

# Status endpoint
curl http://localhost:8000/status

# Tools endpoint
curl http://localhost:8000/tools

# Chat endpoint (POST)
$body = @{
    message = "What's the weather in Tokyo?"
    use_tools = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
```

### 2. Frontend UI
```powershell
# Open in browser
Start-Process "http://localhost:4200"

# Test features:
# - Send a message
# - Try tool calling (weather, time, calculator)
# - Check console for errors (F12)
```

### 3. Pushover Notifications (if configured)
```powershell
# Test endpoint
$body = @{
    message = "Test notification"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/test-pushover" -Method Post -Body $body -ContentType "application/json"
```

## Monitoring

### Resource Usage
```powershell
# View container stats
docker stats chatbot-backend chatbot-frontend

# Detailed info
docker inspect chatbot-backend
```

### Network Inspection
```powershell
# List networks
docker network ls

# Inspect chatbot network
docker network inspect chatbot-ai_chatbot-network

# Test connectivity
docker exec chatbot-frontend ping chatbot-backend
```

## Quick Reference Card

```powershell
# Start everything
docker-compose up -d

# Stop everything
docker-compose down

# Rebuild after changes
docker-compose up -d --build

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Restart a service
docker-compose restart backend

# Shell access
docker exec -it chatbot-backend bash

# Remove everything
docker-compose down -v --rmi all
```

## Environment Variables

Required in `.env`:
```bash
OPENAI_API_KEY=sk-proj-...your_key_here...
```

Optional in `.env`:
```bash
PUSHOVER_USER_KEY=your_user_key
PUSHOVER_API_TOKEN=your_api_token
```

## Port Mapping

| Service | Container Port | Host Port | URL |
|---------|---------------|-----------|-----|
| Backend | 8000 | 8000 | http://localhost:8000 |
| Frontend | 80 | 4200 | http://localhost:4200 |

## Health Check Details

### Backend
- **Check**: `curl -f http://localhost:8000/`
- **Interval**: 30s
- **Timeout**: 10s
- **Retries**: 3
- **Grace Period**: 40s

### Frontend
- **Check**: `wget --quiet --tries=1 --spider http://localhost:80`
- **Interval**: 30s
- **Timeout**: 10s
- **Retries**: 3
- **Grace Period**: 20s

## Benefits of Refactored Docker Setup

✅ **Modular Architecture** - Each module can be tested independently  
✅ **Health Checks** - Services won't accept traffic until ready  
✅ **Dependency Management** - Frontend waits for backend to be healthy  
✅ **Clean Builds** - .dockerignore speeds up builds  
✅ **Environment Flexibility** - Pushover optional via environment variables  
✅ **Better Logging** - Separate logs per module  
✅ **Easier Debugging** - Smaller, focused files  

---

**Last Updated**: October 19, 2025  
**Version**: 2.0 - Refactored Modular Architecture
