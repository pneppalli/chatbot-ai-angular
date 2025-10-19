# Pushover Integration - Quick Reference

## 🎯 What Was Added

### Real-time Notifications
Your chatbot now sends **Pushover notifications** to your phone/desktop when it can't provide sufficient information to answer user queries.

## ✅ Features Implemented

### 1. Insufficient Information Detection
Automatically detects when responses contain phrases like:
- "I don't have"
- "I don't know"
- "Not available"
- "Cannot find"
- "Error"
- And 15+ more indicators

### 2. Pushover Integration Functions

**`send_pushover_notification()`**
- Sends notifications via Pushover API
- Includes query and response in notification
- Configurable priority and title
- Error handling and logging

**`detect_insufficient_information()`**
- Analyzes bot responses
- Pattern matching for common failure phrases
- Returns boolean for notification trigger

### 3. New API Endpoint

**POST /test-pushover**
- Test your Pushover configuration
- Sends a test notification
- Returns configuration status

### 4. Automatic Notification Triggers

Notifications are sent automatically when:
- Weather data is unavailable for a location
- Tools return errors
- AI responds with "I don't know" type answers
- Any response matches insufficient information patterns

## 📋 Setup Steps

### Quick Setup (5 minutes)

1. **Get Pushover Account**
   - Visit: https://pushover.net/
   - Sign up (free - 10,000 msgs/month)
   - Install app on your device

2. **Get API Keys**
   - User Key: From dashboard
   - API Token: Create app at https://pushover.net/apps/build

3. **Add to .env file**
   ```
   PUSHOVER_USER_KEY=your_user_key_here
   PUSHOVER_API_TOKEN=your_api_token_here
   ```

4. **Restart Backend**
   ```powershell
   docker-compose restart backend
   ```

5. **Test It**
   ```powershell
   .\test-pushover.ps1
   ```

## 🧪 Testing

### Method 1: Test Script
```powershell
.\test-pushover.ps1
```
Runs comprehensive tests including:
- Configuration check
- Test notification
- Insufficient info trigger test
- Normal query test

### Method 2: Manual API Test
```powershell
# Test configuration
Invoke-RestMethod -Uri "http://localhost:8000/test-pushover" -Method Post

# Trigger notification with unanswerable question
$body = @{
    message = "What's the weather in Atlantis?"
} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
```

### Method 3: UI Testing
1. Open http://localhost:4200
2. Ask: "What's the weather in Narnia?"
3. Check your phone for notification!

## 📱 Notification Example

When triggered, you receive:

**Title:** ⚠️ Chatbot: Insufficient Information

**Message:**
```
Query: What's the weather in Atlantis?

Response: I apologize, but the weather data is not available for Atlantis. I can provide weather information for...
```

## 🔧 Configuration Options

### Optional: Already Configured
If you skip Pushover setup:
- Chatbot still works normally
- No notifications sent
- Logs show: "Pushover not configured"

### Optional: Enable Later
You can add Pushover anytime:
1. Add keys to .env
2. Restart: `docker-compose restart backend`
3. No code changes needed

## 📂 Files Modified

1. **app.py** - Added:
   - `send_pushover_notification()` function
   - `detect_insufficient_information()` function
   - Notification triggers in `/chat` endpoint
   - `/test-pushover` endpoint

2. **.env.example** - Added:
   - `PUSHOVER_USER_KEY` template
   - `PUSHOVER_API_TOKEN` template

3. **Documentation**:
   - PUSHOVER_INTEGRATION_GUIDE.md (comprehensive guide)
   - test-pushover.ps1 (test script)
   - README.md (updated with Pushover info)

## 🎯 Use Cases

### 1. Knowledge Gap Identification
Get notified when users ask about:
- Missing weather cities
- Unavailable data
- Unsupported features

**Action:** Add more cities to weather data or create new tools

### 2. Service Monitoring
Alerts when:
- OpenAI API errors occur
- External APIs fail
- Tools malfunction

**Action:** Check service status and fix issues

### 3. User Need Analysis
Track what information users frequently request but can't get

**Action:** Prioritize feature development

### 4. Quality Assurance
Monitor chatbot effectiveness in real-time

**Action:** Improve responses and add capabilities

## 🎨 Customization Examples

### Change Notification Priority
```python
# In send_pushover_notification()
"priority": 1,  # High priority instead of 0 (normal)
```

### Add Custom Sound
```python
"sound": "siren",  # Use siren for alerts
```

### Filter by Query Type
```python
def detect_insufficient_information(user_message: str, bot_response: str) -> bool:
    # Don't notify for greetings
    if user_message.lower() in ["hi", "hello", "hey"]:
        return False
    
    # Existing detection logic...
```

### Add Cooldown Period
```python
last_notification = {}

def should_notify(key: str, cooldown_min: int = 5) -> bool:
    now = datetime.now()
    if key in last_notification:
        elapsed = (now - last_notification[key]).total_seconds() / 60
        if elapsed < cooldown_min:
            return False
    last_notification[key] = now
    return True
```

## 🔍 Debugging

### Check Logs
```powershell
# View Pushover-related logs
docker logs chatbot-backend | Select-String "pushover"

# Example output:
# [pushover] Pushover not configured
# [pushover] Notification sent successfully: Chatbot Alert
```

### Common Issues

**"Pushover not configured"**
- ✅ Normal if you haven't set up Pushover yet
- ✅ Chatbot works fine without it

**"Failed to send notification"**
- ❌ Check your API keys
- ❌ Verify internet connection
- ❌ Check Pushover service status

**Too many notifications**
- Add cooldown period
- Filter specific query types
- Use batching (daily summaries)

## 📊 Monitoring

### View Backend Logs
```powershell
docker-compose logs -f backend
```

Look for:
```
[pushover] Notification sent successfully
[pushover] Pushover not configured
[pushover] Error sending notification: ...
```

### Check Pushover Dashboard
Visit https://pushover.net/ to see:
- Message count
- Delivery status
- Quota remaining

## 🚀 Next Steps

1. **Set up Pushover** (optional but recommended)
2. **Test notifications** with test script
3. **Monitor for patterns** in insufficient responses
4. **Add more tools** to cover common queries
5. **Customize detection** for your use case

## 📚 Resources

- **Full Guide**: PUSHOVER_INTEGRATION_GUIDE.md
- **Pushover Docs**: https://pushover.net/api
- **Test Script**: test-pushover.ps1
- **Backend Code**: chatbot-openai/app.py

## 💡 Pro Tips

✅ **Start without Pushover** - Test chatbot first  
✅ **Add Pushover later** - No code changes needed  
✅ **Monitor notifications** - Identify improvement areas  
✅ **Customize detection** - Tune for your domain  
✅ **Use free tier** - 10,000 msgs/month is generous  

---

**Summary:** Your chatbot now has intelligent notification system that alerts you when users need information you don't have. This helps you continuously improve your chatbot! 📱✨
