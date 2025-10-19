# 🚀 Complete Docker Deployment Guide for Hugging Face Spaces

This guide will walk you through deploying both the AI Chatbot backend and frontend to Hugging Face Spaces using Docker containers.

## 📋 Prerequisites

- A Hugging Face account ([sign up here](https://huggingface.co/join))
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Basic understanding of Git and Docker (helpful but not required)

## 🏗️ Project Structure

Your project contains two deployable components:

```
chatbot-ai/
├── huggingface-backend/     # FastAPI backend (Docker)
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
└── huggingface-frontend/    # Angular frontend (Docker)
    ├── Dockerfile
    ├── nginx.conf
    ├── package.json
    ├── angular.json
    ├── tsconfig.json
    ├── src/
    └── README.md
```

## 🎯 Deployment Strategy

We'll deploy in this order:
1. **Backend first** - API server that handles AI requests
2. **Frontend second** - User interface that connects to the backend

---

## 🔧 Part 1: Deploy the Backend API

### Step 1.1: Create Backend Space

1. **Go to Hugging Face Spaces**
   - Visit [https://huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "**Create new Space**"

2. **Configure the Space**
   - **Owner**: Select your username or organization
   - **Space name**: `ai-chatbot-api` (or your preferred name)
   - **License**: MIT
   - **SDK**: Select "**Docker**"
   - **Visibility**: Public (recommended) or Private
   - Click "**Create space**"

### Step 1.2: Upload Backend Files

1. **Upload via Web Interface** (easiest):
   - In your new Space, click "**Files and versions**"
   - Click "**Add file**" → "**Upload files**"
   - Upload all files from `huggingface-backend/` folder:
     - `Dockerfile`
     - `app.py`
     - `requirements.txt`
     - `README.md`
   - Click "**Commit new files**"

2. **Alternative: Git clone method**:
   ```bash
   git clone https://huggingface.co/spaces/YOUR-USERNAME/ai-chatbot-api
   cd ai-chatbot-api
   # Copy files from huggingface-backend/ to this directory
   git add .
   git commit -m "Add backend files"
   git push
   ```

### Step 1.3: Configure Environment Variables

1. **Go to Space Settings**
   - Click on your Space name to go to the main page
   - Click "**Settings**" (gear icon in top right)

2. **Add OpenAI API Key**
   - Scroll down to "**Repository secrets**"
   - Click "**New secret**"
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key (e.g., `sk-...`)
   - Click "**Add secret**"

### Step 1.4: Deploy and Test Backend

1. **Wait for Build**
   - Go back to your Space main page
   - Watch the build logs (takes 2-3 minutes)
   - When complete, you'll see "**Running**" status

2. **Test the API**
   - Your backend URL will be: `https://YOUR-USERNAME-ai-chatbot-api.hf.space`
   - Test endpoints:
     ```bash
     # Health check
     curl https://YOUR-USERNAME-ai-chatbot-api.hf.space/health
     
     # Status check
     curl https://YOUR-USERNAME-ai-chatbot-api.hf.space/status
     
     # Chat test
     curl -X POST "https://YOUR-USERNAME-ai-chatbot-api.hf.space/chat" \
          -H "Content-Type: application/json" \
          -d '{"message": "Hello!"}'
     ```

3. **Expected Responses**
   - `/health`: `{"status": "healthy", "service": "ai-chatbot-api"}`
   - `/status`: `{"has_api_key": true, "status": "ready"}`
   - `/chat`: `{"reply": "Hello! How can I help you today?"}`

---

## 🖼️ Part 2: Deploy the Frontend

### Step 2.1: Create Frontend Space

1. **Create Another Space**
   - Go to [https://huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "**Create new Space**"

2. **Configure Frontend Space**
   - **Owner**: Your username
   - **Space name**: `talksy-frontend` (or your preferred name)
   - **License**: MIT
   - **SDK**: Select "**Docker**"
   - **Visibility**: Public
   - Click "**Create space**"

### Step 2.2: Upload Frontend Files

1. **Upload All Frontend Files**
   - Click "**Files and versions**"
   - Click "**Add file**" → "**Upload files**"
   - Upload all files from `huggingface-frontend/` folder:
     - `Dockerfile`
     - `nginx.conf`
     - `package.json`
     - `angular.json`
     - `tsconfig.json`
     - `README.md`
     - `src/` folder (upload the entire folder)
   - Click "**Commit new files**"

### Step 2.3: Deploy Frontend

1. **Wait for Build**
   - The build process takes 3-5 minutes (Angular compilation + Docker)
   - Watch the build logs for any errors
   - When complete, you'll see the frontend interface

2. **Access Your Frontend**
   - URL: `https://YOUR-USERNAME-talksy-frontend.hf.space`
   - You should see the Talksy chat interface

### Step 2.4: Configure Frontend

1. **Open the Frontend**
   - Visit your frontend URL
   - You'll see the chat interface with a sidebar

2. **Configure Backend Connection**
   - In the sidebar, find "**Backend URL**" field
   - Enter your backend URL: `https://YOUR-USERNAME-ai-chatbot-api.hf.space`
   - Choose your preferred AI model (GPT-3.5 Turbo recommended)
   - Adjust temperature if desired (0.7 is good default)

3. **Test the Connection**
   - Type a message like "Hello, can you help me?"
   - Press Enter or click Send
   - You should get a response from the AI

---

## ✅ Verification Checklist

### Backend Verification
- [ ] Space builds successfully without errors
- [ ] `/health` endpoint returns healthy status
- [ ] `/status` endpoint shows `has_api_key: true`
- [ ] `/chat` endpoint responds to test messages
- [ ] No CORS errors in browser console

### Frontend Verification
- [ ] Angular app builds and loads properly
- [ ] Chat interface is visible and responsive
- [ ] Backend URL can be configured in sidebar
- [ ] Messages can be sent and received
- [ ] Typing indicator works
- [ ] Error handling works (try invalid backend URL)

---

## 🐛 Troubleshooting

### Backend Issues

**Build Fails**
- Check Dockerfile syntax
- Verify all files are uploaded
- Check build logs for specific errors

**API Key Not Working**
- Verify the secret name is exactly `OPENAI_API_KEY`
- Check that your OpenAI API key is valid
- Ensure you have credits in your OpenAI account

**CORS Errors**
- Backend includes CORS headers for `*.hf.space`
- Try refreshing the frontend page
- Check browser console for specific errors

### Frontend Issues

**Build Fails**
- Check that all `src/` files are uploaded
- Verify `package.json` and `angular.json` are present
- Review build logs for npm/Angular errors

**Cannot Connect to Backend**
- Verify backend URL is correct (no trailing slash)
- Ensure backend is running (check backend Space status)
- Test backend endpoints manually with curl

**UI Not Loading**
- Check that `index.html` and `styles.css` are in `src/`
- Verify nginx configuration
- Check browser console for JavaScript errors

---

## 🎨 Customization Options

### Backend Customization
- **Add new models**: Edit the model options in `app.py`
- **Modify responses**: Update the system message
- **Add authentication**: Implement API keys or tokens
- **Rate limiting**: Add request throttling

### Frontend Customization
- **Change theme**: Modify CSS variables in `styles.css`
- **Add features**: Extend `app.component.ts`
- **Update branding**: Change logo, title, and colors
- **Add animations**: Enhance the chat experience

---

## 🔒 Security Best Practices

1. **API Key Management**
   - Never commit API keys to Git
   - Use Hugging Face Spaces secrets
   - Rotate keys regularly

2. **CORS Configuration**
   - Backend allows specific origins
   - Avoid using `*` in production
   - Validate all inputs

3. **Rate Limiting**
   - Consider adding rate limits to prevent abuse
   - Monitor usage and costs
   - Implement user session management

---

## 📊 Monitoring and Maintenance

### Check Space Status
- Monitor build logs for errors
- Watch for API quota limits
- Review user feedback and issues

### Cost Management
- Monitor OpenAI API usage
- Set billing alerts
- Consider caching responses for common queries

### Updates
- Keep dependencies updated
- Monitor for security patches
- Test changes in development before deploying

---

## 🎉 Success!

If you've followed this guide, you now have:

1. ✅ **Backend API** running at `https://YOUR-USERNAME-ai-chatbot-api.hf.space`
2. ✅ **Frontend UI** running at `https://YOUR-USERNAME-talksy-frontend.hf.space`
3. ✅ **Full chat experience** with AI responses
4. ✅ **Configurable settings** for different models and parameters

### Next Steps
- Share your chat app with friends and colleagues
- Customize the design and functionality
- Add new features like conversation history
- Integrate with other AI models or services

### Need Help?
- Check the individual README files in each project folder
- Review Hugging Face Spaces documentation
- Open issues in your GitHub repository for community support

---

**Happy chatting! 🤖💬**