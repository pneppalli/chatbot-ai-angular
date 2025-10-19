"""Main FastAPI application for the chatbot.

This is the refactored main application file. The code has been split into modules:
- config.py: Configuration and environment variables
- models.py: Pydantic request/response models
- openai_client.py: OpenAI client and helper functions
- notifications.py: Pushover notification logic
- tools.py: Function calling tools and definitions
"""

import json
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import from our modules
from config import CORS_ORIGINS, get_pushover_user_key, get_pushover_api_token
from models import ChatRequest, ChatResponse
from openai_client import initialize_openai_client, extract_chat_content, openai
from notifications import send_pushover_notification, notify_insufficient_information
from tools import TOOLS, AVAILABLE_FUNCTIONS, execute_function_call


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Chatbot AI with OpenAI Function Calling",
    description="AI chatbot with function calling capabilities and Pushover notifications",
    version="2.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "Chatbot AI API",
        "version": "2.0.0",
        "features": [
            "OpenAI GPT integration",
            "Function calling (weather, time, calculator)",
            "Pushover notifications",
            "Modular architecture"
        ],
        "endpoints": {
            "chat": "/chat (POST)",
            "status": "/status (GET)",
            "tools": "/tools (GET)",
            "test_pushover": "/test-pushover (POST)",
            "docs": "/docs"
        }
    }


@app.get("/status")
def status():
    """Return system status and configuration."""
    has_openai_key = False
    try:
        from config import get_openai_api_key
        get_openai_api_key()
        has_openai_key = True
    except:
        pass
    
    has_pushover = bool(get_pushover_user_key() and get_pushover_api_token())
    
    return {
        "status": "running",
        "openai_configured": has_openai_key,
        "pushover_configured": has_pushover,
        "tools_available": len(AVAILABLE_FUNCTIONS),
        "openai_package": openai is not None
    }


@app.get("/tools")
def list_tools():
    """Return the list of available tools/functions."""
    return {
        "tools": TOOLS,
        "count": len(TOOLS),
        "available_functions": list(AVAILABLE_FUNCTIONS.keys())
    }


@app.post("/test-pushover")
def test_pushover():
    """Test Pushover notification integration."""
    user_key = get_pushover_user_key()
    api_token = get_pushover_api_token()
    
    if not user_key or not api_token:
        return {
            "configured": False,
            "message": "Pushover not configured. Please set PUSHOVER_USER_KEY and PUSHOVER_API_TOKEN in .env file"
        }
    
    success = send_pushover_notification(
        message="This is a test notification from your chatbot. Pushover integration is working correctly!",
        title="✅ Chatbot Test Notification"
    )
    
    return {
        "configured": True,
        "success": success,
        "message": "Test notification sent!" if success else "Failed to send notification"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Main chat endpoint with function calling support.
    
    Args:
        req: ChatRequest with message and options
        
    Returns:
        ChatResponse with bot reply and metadata
    """
    try:
        print("[chat] handler invoked", flush=True)
        print(f"[chat] message: {req.message[:100]}...", flush=True)

        # Check if OpenAI is available
        if openai is None:
            print("[chat] openai package is missing", flush=True)
            raise HTTPException(
                status_code=500,
                detail="'openai' package is not installed on the server"
            )

        # Initialize OpenAI client
        try:
            client = initialize_openai_client()
        except RuntimeError as e:
            print(f"[chat] initialization error: {str(e)}", flush=True)
            raise HTTPException(status_code=500, detail=str(e))

        # Handle basic completion mode (legacy)
        if req.use_basic:
            return _handle_basic_completion(client, req)

        # Handle chat completion with function calling
        return _handle_chat_completion(client, req)
        
    except HTTPException:
        # Re-raise FastAPI HTTPExceptions unchanged
        raise
    except Exception as exc:
        # Catch everything else and return a 500 with the error string
        print(f"[chat] unexpected exception: {repr(exc)}", flush=True)
        raise HTTPException(status_code=500, detail=str(exc))


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _handle_basic_completion(client, req: ChatRequest) -> ChatResponse:
    """Handle basic completion API (legacy mode)."""
    prompt = f"User: {req.message}\nAssistant:"
    print(f"[chat] using basic Completion API", flush=True)
    
    try:
        if hasattr(client, "completions"):
            resp = client.completions.create(
                model=req.model or "text-davinci-003",
                prompt=prompt,
                max_tokens=250,
                temperature=0.7
            )
        else:
            resp = openai.Completion.create(
                model=req.model or "text-davinci-003",
                prompt=prompt,
                max_tokens=250,
                temperature=0.7
            )
        
        content = extract_chat_content(resp).strip()
        print(f"[chat] completion result length: {len(content)}", flush=True)
        
        # Check for insufficient information
        notify_insufficient_information(req.message, content)
        
        return ChatResponse(reply=content, used_tools=False)
        
    except Exception as exc:
        print(f"[chat] completion exception: {repr(exc)}", flush=True)
        raise HTTPException(status_code=502, detail=str(exc))


def _handle_chat_completion(client, req: ChatRequest) -> ChatResponse:
    """Handle chat completion API with function calling support."""
    # Build conversation messages
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with access to various tools. Use them when needed to provide accurate information."
        },
        {"role": "user", "content": req.message}
    ]
    
    print("[chat] using ChatCompletion API", flush=True)

    try:
        # Prepare API call parameters
        chat_params = {
            "model": req.model,
            "messages": messages
        }
        
        # Add tools if requested
        if req.use_tools:
            chat_params["tools"] = TOOLS
            chat_params["tool_choice"] = "auto"
            print("[chat] tools enabled", flush=True)
        
        # Make the initial API call
        if hasattr(client, "chat"):
            resp = client.chat.completions.create(**chat_params)
        else:
            resp = openai.ChatCompletion.create(**chat_params)
        
        response_message = resp.choices[0].message
        tool_calls = getattr(response_message, "tool_calls", None)
        
        # Check if the model wants to call functions
        if tool_calls:
            print(f"[chat] model requested {len(tool_calls)} tool call(s)", flush=True)
            
            # Add assistant's response to messages
            messages.append(response_message)
            
            # Execute each tool call
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"[chat] executing: {function_name}({function_args})", flush=True)
                
                # Execute the function
                function_response = execute_function_call(function_name, function_args)
                
                # Add function response to messages
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response
                })
            
            # Make second API call with function results
            print("[chat] making second API call with function results", flush=True)
            if hasattr(client, "chat"):
                second_resp = client.chat.completions.create(
                    model=req.model,
                    messages=messages
                )
            else:
                second_resp = openai.ChatCompletion.create(
                    model=req.model,
                    messages=messages
                )
            
            content = extract_chat_content(second_resp).strip()
            print(f"[chat] final response length: {len(content)}", flush=True)
            
            # Check for insufficient information
            notify_insufficient_information(req.message, content)
            
            return ChatResponse(reply=content, used_tools=True)
        else:
            # No tool calls, return direct response
            content = extract_chat_content(resp).strip()
            print(f"[chat] direct response length: {len(content)}", flush=True)
            
            # Check for insufficient information
            notify_insufficient_information(req.message, content)
            
            return ChatResponse(reply=content, used_tools=False)
            
    except Exception as exc:
        print(f"[chat] chatcompletion exception: {repr(exc)}", flush=True)
        raise HTTPException(status_code=502, detail=str(exc))


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    print("=" * 60, flush=True)
    print("🤖 Chatbot AI Starting...", flush=True)
    print("=" * 60, flush=True)
    print(f"OpenAI package available: {openai is not None}", flush=True)
    print(f"Tools registered: {len(AVAILABLE_FUNCTIONS)}", flush=True)
    print(f"CORS origins: {len(CORS_ORIGINS)}", flush=True)
    print("=" * 60, flush=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
