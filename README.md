# Chatbot AI - OpenAI ChatGPT with Function Calling

A modern chatbot application with Angular frontend and FastAPI backend, featuring OpenAI's GPT models with advanced **function calling** capabilities.

## ✨ Features

- 🤖 **OpenAI GPT Integration** - ChatGPT 3.5/4 with streaming responses
- 🔧 **Function Calling** - AI can call external functions for real-time data
- 🎨 **Modern UI** - Clean Angular interface with real-time chat
- � **Pushover Notifications** - Get alerted when bot can't answer questions
- �🐳 **Docker Support** - Full containerization for easy deployment
- ☁️ **Hugging Face Spaces** - Cloud deployment ready
- 🔒 **CORS Configured** - Secure cross-origin requests
- 📊 **Interactive API Docs** - FastAPI Swagger UI

## 🔧 Built-in Tools/Functions

The chatbot can intelligently use the following tools:

1. **Weather Information** 🌤️ - Get current weather for any city
2. **Current Time** ⏰ - Retrieve date/time in any timezone
3. **Calculator** 🔢 - Perform mathematical calculations

**Example queries:**
- "What's the weather in San Francisco?"
- "What time is it right now?"
- "Calculate 25 * 8 + 100"

See [TOOLS_GUIDE.md](chatbot-openai/TOOLS_GUIDE.md) for detailed documentation.

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

### Local Deployment

1. **Clone and navigate to the project:**
   ```bash
   cd chatbot-ai
   ```

2. **Create environment file:**
   ```bash
   Copy-Item .env.example .env
   ```
   Edit `.env` and add your API keys:
   ```
   OPENAI_API_KEY=sk-proj-your-key-here
   
   # Optional: Pushover notifications
   PUSHOVER_USER_KEY=your_pushover_user_key
   PUSHOVER_API_TOKEN=your_pushover_api_token
   ```

3. **Start with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:8000/docs

**Or use the quick-start script:**
```powershell
.\start-local.ps1
```

## 📁 Project Structure

```
chatbot-ai/
├── chatbot-openai/          # FastAPI Backend
│   ├── app.py               # Main application with function calling
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Backend container
│   └── TOOLS_GUIDE.md       # Function calling documentation
├── chatbot-ui/              # Angular Frontend
│   ├── src/                 # Source code
│   ├── Dockerfile           # Frontend container
│   └── nginx.conf           # Nginx configuration
├── docker-compose.yml       # Orchestration
├── .env.example             # Environment template
└── LOCAL_DEPLOYMENT_GUIDE.md
```

## 🧪 Testing Function Calling

Run the test script:
```powershell
.\test-tools.ps1
```

This will test:
- Weather queries
- Time queries
- Calculations
- Regular chat
- Multiple tool usage

## 📱 Testing Pushover Notifications

Run the Pushover test script:
```powershell
.\test-pushover.ps1
```

This will:
- Check configuration
- Send test notification
- Trigger insufficient information alert
- Verify normal queries don't send alerts

## 📖 Documentation

- [Local Deployment Guide](LOCAL_DEPLOYMENT_GUIDE.md) - Detailed local setup
- [Docker Deployment Guide](DOCKER_DEPLOYMENT_GUIDE.md) - Docker configuration
- [Tools/Functions Guide](chatbot-openai/TOOLS_GUIDE.md) - Function calling docs
- [Pushover Integration Guide](PUSHOVER_INTEGRATION_GUIDE.md) - Notification setup

## 🔌 API Endpoints

### POST /chat
Send messages to the chatbot with optional tool usage.

**Request:**
```json
{
  "message": "What's the weather in Tokyo?",
  "model": "gpt-3.5-turbo",
  "use_tools": true
}
```

**Response:**
```json
{
  "reply": "The weather in Tokyo is currently 68°F and clear...",
  "used_tools": true
}
```

### GET /tools
List all available tools/functions.

### GET /status
Check API key configuration and server status.

### POST /test-pushover
Test Pushover notification configuration and send a test alert.

## 🎯 Use Cases

- Customer support chatbots
- Virtual assistants with real-time data
- Educational chatbots with calculations
- Information retrieval systems
- Automated FAQ systems

## 🛠️ Adding Custom Tools

See [TOOLS_GUIDE.md](chatbot-openai/TOOLS_GUIDE.md) for step-by-step instructions on:
- Creating custom functions
- Defining tool schemas
- Integrating real APIs
- Security best practices

## 🌐 Cloud Deployment

Deploy to Hugging Face Spaces (see [DOCKER_DEPLOYMENT_GUIDE.md](DOCKER_DEPLOYMENT_GUIDE.md)):
- Backend: FastAPI backend with Docker SDK
- Frontend: Static Angular app with Docker SDK

## 🔒 Security Notes

- Never commit `.env` file with real API keys
- Validate all function inputs
- Use environment variables for secrets
- Implement rate limiting in production
- Enable authentication for public deployments

## 🐛 Troubleshooting

**Backend not starting?**
```bash
docker logs chatbot-backend
```

**Frontend not loading?**
```bash
docker logs chatbot-frontend
```

**API key issues?**
- Check `.env` file exists
- Verify OpenAI API key is valid
- Restart containers: `docker-compose restart`

**Tools not working?**
- Ensure `use_tools: true` in requests
- Check backend logs for errors
- Verify model supports function calling (GPT-3.5-turbo or GPT-4)

## 📊 Tech Stack

**Frontend:**
- Angular 16
- TypeScript 5.1
- RxJS
- Nginx (production)

**Backend:**
- Python 3.11
- FastAPI
- OpenAI Python SDK
- Uvicorn

**Infrastructure:**
- Docker
- Docker Compose
- Nginx

## 📝 License

MIT License - feel free to use this project for your own applications!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions:
- Check the documentation guides
- Review the TOOLS_GUIDE.md
- Check Docker logs
- Visit [OpenAI Documentation](https://platform.openai.com/docs)

---

Made with ❤️ using OpenAI GPT and Function Calling

