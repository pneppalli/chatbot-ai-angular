import requests
from typing import Optional
from config import get_pushover_user_key, get_pushover_api_token


def send_pushover_notification(message: str, title: str = "Chatbot Alert") -> bool:
    user_key = get_pushover_user_key()
    api_token = get_pushover_api_token()
    
    if not user_key or not api_token:
        print("[pushover] Pushover not configured (missing PUSHOVER_USER_KEY or PUSHOVER_API_TOKEN)", flush=True)
        return False
    
    try:
        pushover_url = "https://api.pushover.net/1/messages.json"
        payload = {
            "token": api_token,
            "user": user_key,
            "message": message,
            "title": title,
            "priority": 0
        }
        
        response = requests.post(pushover_url, data=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"[pushover] Notification sent successfully: {title}", flush=True)
            return True
        else:
            print(f"[pushover] Failed to send notification: {response.status_code} - {response.text}", flush=True)
            return False
            
    except Exception as e:
        print(f"[pushover] Error sending notification: {str(e)}", flush=True)
        return False


def detect_insufficient_information(user_message: str, bot_response: str) -> bool:
    insufficient_indicators = [
        "i don't have",
        "i don't know",
        "i cannot provide",
        "i'm not able to",
        "i don't have access",
        "i can't access",
        "i'm unable to",
        "no information",
        "not available",
        "don't have data",
        "cannot find",
        "not found",
        "weather data not available",
        "error",
        "sorry, i",
        "unfortunately",
        "i apologize",
    ]
    
    response_lower = bot_response.lower()
    return any(indicator in response_lower for indicator in insufficient_indicators)


def notify_insufficient_information(user_message: str, bot_response: str) -> None:
    if detect_insufficient_information(user_message, bot_response):
        notification_msg = f"Query: {user_message[:100]}\n\nResponse: {bot_response[:200]}"
        send_pushover_notification(
            message=notification_msg,
            title="⚠️ Chatbot: Insufficient Information"
        )
