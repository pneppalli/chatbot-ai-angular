# Local Docker Desktop Deployment Guide

This guide will help you deploy the chatbot application locally using Docker Desktop.

## Prerequisites

1. **Docker Desktop** installed and running on your Windows machine
2. **OpenAI API Key** from https://platform.openai.com/api-keys

## Setup Instructions

### Step 1: Create Environment File

1. Copy the `.env.example` file to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Open the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=sk-proj-...your-actual-key...
   ```

### Step 2: Update Frontend Configuration (Important!)

The frontend needs to communicate with the backend container. You have two options:

#### Option A: Access from Host Machine (Recommended for Local Testing)
Keep the current configuration in `chatbot-ui/src/app/app.component.ts`:
```typescript
const res = await fetch('http://127.0.0.1:8000/chat', {
```
This allows you to access the frontend from your browser at `http://localhost:4200`

#### Option B: Container-to-Container Communication
If you want the frontend container to communicate directly with the backend:
```typescript
const res = await fetch('http://backend:8000/chat', {
```
**Note:** This requires updating the nginx configuration to proxy the requests.

**For simplicity, we'll use Option A (current setup).**

### Step 3: Build and Run the Containers

1. Open PowerShell and navigate to the project root:
   ```powershell
   cd c:\Users\pragn\projects\chatbot\chatbot-ai
   ```

2. Build and start all services:
   ```powershell
   docker-compose up --build
   ```

   This will:
   - Build the backend Docker image (Python/FastAPI)
   - Build the frontend Docker image (Angular/Nginx)
   - Start both containers
   - Create a Docker network for inter-container communication

3. Wait for the build to complete. You should see:
   ```
   backend_1   | INFO:     Uvicorn running on http://0.0.0.0:8000
   frontend_1  | ... nginx started
   ```

### Step 4: Access the Application

1. **Frontend**: Open your browser and navigate to:
   ```
   http://localhost:4200
   ```

2. **Backend API** (optional, for testing):
   ```
   http://localhost:8000/docs
   ```
   This will show the FastAPI interactive documentation.

### Step 5: Test the Chatbot

1. Type a message in the chat interface
2. Click "Send" or press Enter
3. Wait for the AI response

## Managing the Containers

### View Running Containers
```powershell
docker ps
```

### View Logs
```powershell
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Stop the Containers
```powershell
# Stop and remove containers (Ctrl+C if running in foreground, then:)
docker-compose down
```

### Restart After Code Changes
```powershell
# Rebuild and restart
docker-compose up --build

# Or rebuild specific service
docker-compose up --build backend
docker-compose up --build frontend
```

### Clean Up (Remove Images)
```powershell
docker-compose down --rmi all
```

## Troubleshooting

### Issue: "Cannot connect to backend"
- Check if backend container is running: `docker ps`
- View backend logs: `docker-compose logs backend`
- Ensure your `.env` file has a valid OpenAI API key

### Issue: "Port already in use"
- Stop any services using ports 4200 or 8000
- Or modify the port mappings in `docker-compose.yml`

### Issue: Frontend shows blank page
- Check browser console for errors (F12)
- View frontend logs: `docker-compose logs frontend`
- Try accessing `http://localhost:4200` directly

### Issue: OpenAI API errors
- Verify your API key in `.env` file
- Check your OpenAI account has credits
- View backend logs for specific error messages

## Project Structure

```
chatbot-ai/
├── docker-compose.yml          # Orchestrates both services
├── .env                        # Your OpenAI API key (create this!)
├── .env.example               # Template for .env file
├── chatbot-openai/            # Backend service
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── chatbot-ui/                # Frontend service
    ├── Dockerfile
    ├── nginx.conf
    ├── package.json
    └── src/
```

## Port Mappings

- **Frontend**: `localhost:4200` → Container port 80
- **Backend**: `localhost:8000` → Container port 8000

## Next Steps

- Customize the UI in `chatbot-ui/src/app/app.component.ts`
- Modify the backend logic in `chatbot-openai/app.py`
- Update OpenAI model parameters (temperature, max_tokens, etc.)
- Add more features to the chat interface

## Support

For issues specific to:
- **Docker**: Check Docker Desktop logs and ensure it's running
- **OpenAI API**: Visit https://platform.openai.com/docs
- **Angular**: Check the browser console (F12)
- **FastAPI**: View backend logs with `docker-compose logs backend`
