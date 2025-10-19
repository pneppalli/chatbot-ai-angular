# Pushover.net Integration Guide

## What is Pushover?

Pushover is a simple notification service that sends real-time notifications to your devices (iOS, Android, Desktop). In this chatbot, we use it to alert you when the AI cannot provide sufficient information to answer a user's query.

## Why Use Pushover for Insufficient Information?

✅ **Monitoring** - Get alerted when your chatbot can't help users  
✅ **Quality Control** - Identify gaps in your knowledge base or tools  
✅ **User Experience** - Proactively address common unanswered questions  
✅ **Real-time Alerts** - Instant notifications to your phone/desktop  
✅ **Data Collection** - Track what information users are seeking  

## Setup Instructions

### Step 1: Create Pushover Account

1. Visit https://pushover.net/
2. Sign up for a free account (free tier includes 10,000 messages/month)
3. Download the Pushover app on your device:
   - iOS: https://apps.apple.com/app/pushover-notifications/id506088175
   - Android: https://play.google.com/store/apps/details?id=net.superblock.pushover

### Step 2: Get Your User Key

1. Log in to https://pushover.net/
2. Your User Key is displayed on the dashboard
3. Copy it (looks like: `uQiRzpo4DXghDmr9QzzfQu27cmVRsG`)

### Step 3: Create an Application

1. Go to https://pushover.net/apps/build
2. Fill in the application details:
   - **Name**: `Chatbot AI` (or any name you prefer)
   - **Type**: `Application`
   - **Description**: `Notifications for chatbot insufficient information alerts`
   - **URL**: (optional) `http://localhost:4200`
   - **Icon**: (optional) Upload a logo
3. Click "Create Application"
4. Copy your **API Token/Key** (looks like: `azGDORePK8gMaC0QOYAMyEEuzJnyUi`)

### Step 4: Configure Environment Variables

1. Open your `.env` file (or create one from `.env.example`):
   ```bash
   Copy-Item .env.example .env
   ```

2. Add your Pushover credentials:
   ```
   PUSHOVER_USER_KEY=uQiRzpo4DXghDmr9QzzfQu27cmVRsG
   PUSHOVER_API_TOKEN=azGDORePK8gMaC0QOYAMyEEuzJnyUi
   ```

3. Save the file

### Step 5: Rebuild and Restart

```powershell
# Rebuild the backend container
docker-compose up -d --build backend

# Or restart all containers
docker-compose down
docker-compose up -d --build
```

## Testing the Integration

### Method 1: Test Endpoint

Use the built-in test endpoint:

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/test-pushover" -Method Post
```

You should receive a test notification on your device!

**Expected Response:**
```json
{
  "configured": true,
  "success": true,
  "message": "Test notification sent!"
}
```

### Method 2: Trigger via Chat

Ask a question the bot can't answer:

```powershell
$body = @{
    message = "What's the weather in Atlantis?"
    use_tools = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
```

Since "Atlantis" is not in the mock weather data, you'll get a notification!

### Method 3: Via UI

1. Open http://localhost:4200
2. Ask: "What's the weather in Narnia?"
3. Check your phone/device for a Pushover notification

## How It Works

### Detection Logic

The system detects insufficient information by checking if the bot's response contains phrases like:

- "I don't have"
- "I don't know"
- "I cannot provide"
- "Not available"
- "No information"
- "Error"
- "Sorry, I"
- "Unfortunately"
- And more...

### Notification Content

When triggered, you'll receive:

**Title:** ⚠️ Chatbot: Insufficient Information

**Message:**
```
Query: What's the weather in Atlantis?

Response: I apologize, but the weather data is not available for Atlantis...
```

### Code Flow

```
User asks question
    ↓
Chatbot generates response
    ↓
detect_insufficient_information() checks response
    ↓
[Contains insufficient indicators?]
    ↓ YES
send_pushover_notification()
    ↓ POST to Pushover API
    ↓
Notification sent to your device!
```

## Customization

### 1. Adjust Detection Phrases

Edit the `detect_insufficient_information()` function in `app.py`:

```python
insufficient_indicators = [
    "i don't have",
    "i don't know",
    # Add your custom phrases here
    "data unavailable",
    "service down",
]
```

### 2. Change Notification Priority

Modify the `send_pushover_notification()` function:

```python
payload = {
    "token": api_token,
    "user": user_key,
    "message": message,
    "title": title,
    "priority": 1,  # -2=lowest, -1=low, 0=normal, 1=high, 2=emergency
    "sound": "pushover"  # Optional: custom sound
}
```

Available priorities:
- `-2` - No notification/alert
- `-1` - Quiet notification
- `0` - Normal priority (default)
- `1` - High priority
- `2` - Emergency (requires acknowledgment)

### 3. Add Custom Sounds

Available sounds:
- `pushover` (default)
- `bike`
- `bugle`
- `cashregister`
- `classical`
- `cosmic`
- `falling`
- `gamelan`
- `incoming`
- `intermission`
- `magic`
- `mechanical`
- `pianobar`
- `siren`
- `spacealarm`
- `tugboat`
- `alien`
- `climb`
- `persistent`
- `echo`
- `updown`
- `vibrate`
- `none`

Example:
```python
"sound": "siren"  # Use siren sound for alerts
```

### 4. Add URL to Notifications

Open the chat in browser from notification:

```python
payload = {
    # ... other fields
    "url": "http://localhost:4200",
    "url_title": "Open Chatbot"
}
```

### 5. Disable for Specific Queries

Add logic to skip notifications:

```python
def detect_insufficient_information(user_message: str, bot_response: str) -> bool:
    # Don't notify for greetings
    if user_message.lower() in ["hi", "hello", "hey"]:
        return False
    
    # Existing detection logic
    response_lower = bot_response.lower()
    return any(indicator in response_lower for indicator in insufficient_indicators)
```

## API Reference

### Endpoint: POST /test-pushover

Test your Pushover configuration.

**Response (Configured):**
```json
{
  "configured": true,
  "success": true,
  "message": "Test notification sent!"
}
```

**Response (Not Configured):**
```json
{
  "configured": false,
  "message": "Pushover not configured. Please set PUSHOVER_USER_KEY and PUSHOVER_API_TOKEN in .env file"
}
```

## Use Cases

### 1. Knowledge Base Gaps

Track questions users ask that your bot can't answer:
- Add missing weather cities
- Identify needed tools/functions
- Improve system prompts

### 2. Service Monitoring

Get alerted when:
- OpenAI API is down
- External APIs fail
- Tools malfunction

### 3. Quality Assurance

Monitor:
- Frequency of insufficient answers
- Common unanswered topics
- User satisfaction issues

### 4. Business Intelligence

Analyze notifications to:
- Identify feature requests
- Understand user needs
- Prioritize improvements

## Advanced Scenarios

### Scenario 1: Daily Summary

Instead of immediate notifications, collect and send a daily summary:

```python
# Store failed queries in a list/database
failed_queries = []

def detect_insufficient_information(user_message: str, bot_response: str) -> bool:
    if is_insufficient:
        failed_queries.append({
            "query": user_message,
            "response": bot_response,
            "timestamp": datetime.now()
        })
        return True
    return False

# Schedule daily summary (use APScheduler or similar)
def send_daily_summary():
    if failed_queries:
        summary = "\n\n".join([f"Q: {q['query']}\nA: {q['response'][:100]}" 
                               for q in failed_queries[-10:]])
        send_pushover_notification(summary, "Daily Insufficient Info Summary")
        failed_queries.clear()
```

### Scenario 2: Multiple Recipients

Send to different users based on query type:

```python
def send_targeted_notification(user_message: str, bot_response: str):
    if "weather" in user_message.lower():
        # Send to weather team
        send_pushover_notification(
            message=bot_response,
            title="Weather Query Failed",
            user_key=os.getenv("WEATHER_TEAM_USER_KEY")
        )
    elif "calculate" in user_message.lower():
        # Send to tech team
        send_pushover_notification(
            message=bot_response,
            title="Calculation Query Failed",
            user_key=os.getenv("TECH_TEAM_USER_KEY")
        )
```

### Scenario 3: Error Tracking Integration

Combine with error tracking services:

```python
def send_pushover_notification(message: str, title: str = "Chatbot Alert") -> bool:
    # Send Pushover notification
    success = # ... existing code ...
    
    # Also log to Sentry/Datadog/etc
    if not success:
        sentry_sdk.capture_message(f"Pushover failed: {message}")
    
    return success
```

## Troubleshooting

### Issue: "Pushover not configured"

**Solution:**
1. Check `.env` file exists
2. Verify `PUSHOVER_USER_KEY` and `PUSHOVER_API_TOKEN` are set
3. Restart containers: `docker-compose restart backend`

### Issue: Notifications not received

**Solutions:**
1. **Check Pushover app** is installed on your device
2. **Verify credentials** at http://localhost:8000/test-pushover
3. **Check limits** - Free tier: 10,000 messages/month
4. **Review logs**: `docker logs chatbot-backend | grep pushover`

### Issue: Too many notifications

**Solutions:**
1. **Increase threshold** - Only notify on specific error types
2. **Add cooldown** - Limit notifications per hour
3. **Use batching** - Collect and send summaries

Example cooldown:
```python
last_notification_time = {}

def should_notify(query_type: str, cooldown_minutes: int = 5) -> bool:
    now = datetime.now()
    if query_type in last_notification_time:
        elapsed = (now - last_notification_time[query_type]).total_seconds() / 60
        if elapsed < cooldown_minutes:
            return False
    
    last_notification_time[query_type] = now
    return True
```

### Issue: 429 Rate Limit Error

**Solution:**
Pushover rate limits:
- 10,000 messages/month (free tier)
- Consider upgrading or implementing batching

## Security Best Practices

✅ **Never commit .env file** with real credentials  
✅ **Use environment variables** for all secrets  
✅ **Rotate keys periodically** in Pushover dashboard  
✅ **Monitor usage** at https://pushover.net/  
✅ **Validate all inputs** before sending notifications  
✅ **Sanitize messages** to prevent injection attacks  

## Monitoring & Analytics

Track notification effectiveness:

```python
notification_stats = {
    "sent": 0,
    "failed": 0,
    "insufficient_info_count": 0
}

def send_pushover_notification(message: str, title: str = "Chatbot Alert") -> bool:
    success = # ... send notification ...
    
    if success:
        notification_stats["sent"] += 1
    else:
        notification_stats["failed"] += 1
    
    return success

# Add endpoint to view stats
@app.get("/notification-stats")
def get_notification_stats():
    return notification_stats
```

## Cost Considerations

**Free Tier:**
- 10,000 messages/month
- Unlimited devices
- 30-day message retention

**Paid ($5 one-time per platform):**
- Lifetime license per platform
- No monthly fees
- Same features as free tier

**Recommendations:**
- Start with free tier
- Monitor usage at https://pushover.net/
- Implement batching if approaching limits

## Resources

- **Pushover Website**: https://pushover.net/
- **API Documentation**: https://pushover.net/api
- **FAQ**: https://pushover.net/faq
- **Status Page**: https://status.pushover.net/

---

## Summary

You now have real-time notifications when your chatbot can't provide information! This helps you:

1. ✅ Monitor chatbot effectiveness
2. ✅ Identify knowledge gaps
3. ✅ Improve user experience
4. ✅ Track service issues
5. ✅ Collect improvement opportunities

Happy monitoring! 📱🔔
