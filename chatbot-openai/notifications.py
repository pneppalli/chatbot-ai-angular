"""Pushover notification integration."""

import requests
from typing import Optional
from config import get_pushover_user_key, get_pushover_api_token


def send_pushover_notification(message: str, title: str = "Chatbot Alert") -> bool:
    """Send a notification via Pushover.net when information is unavailable.
    
    Requires PUSHOVER_USER_KEY and PUSHOVER_API_TOKEN in environment variables.
    Get your keys from: https://pushover.net/
    
    Args:
        message: The notification message to send
        title: The notification title (default: "Chatbot Alert")
        
    Returns:
        bool: True if notification sent successfully, False otherwise
    """
    user_key = get_pushover_user_key()
    api_token = get_pushover_api_token()
    
    # If Pushover is not configured, log and return
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
            "priority": 0  # Normal priority
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
    """Detect if the bot couldn't provide sufficient information.
    
    Returns True if the response indicates lack of information.
    
    Args:
        user_message: The user's original question
        bot_response: The bot's response to analyze
        
    Returns:
        bool: True if response indicates insufficient information
    """
    # Common phrases indicating insufficient information
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
    """Send a notification if the response indicates insufficient information.
    
    Args:
        user_message: The user's original question
        bot_response: The bot's response
    """
    if detect_insufficient_information(user_message, bot_response):
        notification_msg = f"Query: {user_message[:100]}\n\nResponse: {bot_response[:200]}"
        send_pushover_notification(
            message=notification_msg,
            title="⚠️ Chatbot: Insufficient Information"
        )
