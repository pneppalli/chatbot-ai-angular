"""Function calling tools and definitions for OpenAI."""

import json
from typing import Dict, List
from datetime import datetime


# ============================================================================
# TOOL FUNCTIONS
# ============================================================================

def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather in a given location.
    
    This is a mock function - in production, you'd call a real weather API.
    
    Args:
        location: City name (e.g., "San Francisco")
        unit: Temperature unit - "celsius" or "fahrenheit" (default: fahrenheit)
        
    Returns:
        JSON string with weather data or error message
    """
    # Mock weather data
    weather_data = {
        "san francisco": {"temperature": "72", "condition": "sunny", "humidity": "65%"},
        "new york": {"temperature": "65", "condition": "cloudy", "humidity": "70%"},
        "london": {"temperature": "58", "condition": "rainy", "humidity": "85%"},
        "tokyo": {"temperature": "68", "condition": "clear", "humidity": "60%"},
        "paris": {"temperature": "62", "condition": "partly cloudy", "humidity": "75%"},
    }
    
    location_lower = location.lower()
    if location_lower in weather_data:
        data = weather_data[location_lower]
        temp = data["temperature"]
        if unit.lower() == "celsius":
            # Simple conversion (mock)
            temp = str(int((int(temp) - 32) * 5/9))
        
        return json.dumps({
            "location": location,
            "temperature": temp,
            "unit": unit,
            "condition": data["condition"],
            "humidity": data["humidity"]
        })
    else:
        return json.dumps({"error": f"Weather data not available for {location}"})


def get_current_time(timezone: str = "UTC") -> str:
    """Get the current time in a specific timezone.
    
    This is a simplified mock - in production, use proper timezone libraries.
    
    Args:
        timezone: Timezone identifier (e.g., "UTC", "EST", "PST")
        
    Returns:
        JSON string with current time information
    """
    current_time = datetime.now()
    return json.dumps({
        "timezone": timezone,
        "time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": int(current_time.timestamp())
    })


def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression.
    
    Only allows basic arithmetic operations.
    
    Args:
        expression: Mathematical expression (e.g., "2 + 2" or "(10 * 5) / 2")
        
    Returns:
        JSON string with calculation result or error message
    """
    try:
        # Basic safety check - only allow numbers and basic operators
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return json.dumps({"error": "Invalid characters in expression"})
        
        # Evaluate safely
        result = eval(expression, {"__builtins__": {}}, {})
        return json.dumps({"expression": expression, "result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ============================================================================
# TOOL DEFINITIONS (OpenAI Format)
# ============================================================================

TOOLS: List[Dict] = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g. San Francisco"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time in a specific timezone",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "The timezone, e.g. UTC, EST, PST"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression. Supports +, -, *, /, parentheses.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate, e.g. '2 + 2' or '(10 * 5) / 2'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


# Map function names to actual Python functions
AVAILABLE_FUNCTIONS = {
    "get_current_weather": get_current_weather,
    "get_current_time": get_current_time,
    "calculate": calculate
}


def execute_function_call(function_name: str, function_args: Dict) -> str:
    """Execute a function call and return the result.
    
    Args:
        function_name: Name of the function to call
        function_args: Dictionary of arguments to pass to the function
        
    Returns:
        JSON string with function result or error message
    """
    if function_name not in AVAILABLE_FUNCTIONS:
        return json.dumps({"error": f"Function {function_name} not found"})
    
    try:
        function_to_call = AVAILABLE_FUNCTIONS[function_name]
        result = function_to_call(**function_args)
        return result
    except Exception as e:
        return json.dumps({"error": str(e)})
