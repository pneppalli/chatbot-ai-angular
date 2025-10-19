# OpenAI Function Calling (Tools Prompting) Guide

## What is Function Calling?

**Function calling** (also known as **tools prompting**) is a powerful feature in ChatGPT that allows the AI model to intelligently decide when to call external functions to get information or perform actions. Instead of just generating text responses, the AI can:

1. **Analyze** the user's request
2. **Decide** if it needs to use a function/tool
3. **Generate** structured function calls with parameters
4. **Process** the function results
5. **Formulate** a natural language response

## Architecture

```
User Question
    ↓
ChatGPT analyzes question
    ↓
[Need external data?]
    ↓ YES
ChatGPT generates function call
    ↓
Your backend executes function
    ↓
Return results to ChatGPT
    ↓
ChatGPT formulates final answer
```

## Benefits

✅ **Dynamic Data Access**: Get real-time information (weather, time, etc.)  
✅ **Structured Interactions**: Type-safe function calls with validated parameters  
✅ **Smart Decisions**: Model decides when tools are needed  
✅ **Extended Capabilities**: Perform calculations, database queries, API calls  
✅ **Natural Responses**: AI integrates function results into conversational answers

## Implemented Tools

### 1. Get Current Weather 🌤️
**Function**: `get_current_weather(location, unit)`

**Description**: Retrieves current weather information for a specified location.

**Parameters**:
- `location` (string, required): City name (e.g., "San Francisco")
- `unit` (string, optional): Temperature unit - "celsius" or "fahrenheit" (default: fahrenheit)

**Example Usage**:
```
User: "What's the weather in New York?"
AI: Calls get_current_weather("New York", "fahrenheit")
Response: "The weather in New York is currently 65°F and cloudy with 70% humidity."
```

**Try it**:
- "What's the weather in Tokyo?"
- "How's the weather in London in celsius?"
- "Is it sunny in San Francisco?"

---

### 2. Get Current Time ⏰
**Function**: `get_current_time(timezone)`

**Description**: Returns the current date and time in a specified timezone.

**Parameters**:
- `timezone` (string, optional): Timezone identifier (e.g., "UTC", "EST", "PST")

**Example Usage**:
```
User: "What time is it?"
AI: Calls get_current_time("UTC")
Response: "The current time is 2025-10-19 14:30:45 UTC."
```

**Try it**:
- "What time is it right now?"
- "Give me the current timestamp"
- "What's the current date and time?"

---

### 3. Calculate 🔢
**Function**: `calculate(expression)`

**Description**: Safely evaluates mathematical expressions.

**Parameters**:
- `expression` (string, required): Mathematical expression using +, -, *, /, parentheses

**Example Usage**:
```
User: "What's 25 multiplied by 4?"
AI: Calls calculate("25 * 4")
Response: "25 multiplied by 4 equals 100."
```

**Try it**:
- "Calculate 123 + 456"
- "What's 15% of 200?"
- "Solve (50 + 30) * 2"

---

## API Endpoints

### POST /chat
Main chat endpoint with function calling support.

**Request Body**:
```json
{
  "message": "What's the weather in Paris?",
  "model": "gpt-3.5-turbo",
  "use_tools": true
}
```

**Response**:
```json
{
  "reply": "The weather in Paris is currently 62°F and partly cloudy with 75% humidity.",
  "used_tools": true
}
```

**Parameters**:
- `message` (string, required): User's message
- `model` (string, optional): OpenAI model to use (default: "gpt-3.5-turbo")
- `use_basic` (boolean, optional): Use basic completion API (default: false)
- `use_tools` (boolean, optional): Enable function calling (default: true)

---

### GET /tools
List all available tools and their definitions.

**Response**:
```json
{
  "tools": [...],
  "count": 3,
  "available_functions": [
    "get_current_weather",
    "get_current_time",
    "calculate"
  ]
}
```

---

## Testing Function Calling

### 1. Test with curl:

**Weather query**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather in Tokyo?"}'
```

**Time query**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What time is it now?"}'
```

**Calculation**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Calculate 25 * 8 + 100"}'
```

**Disable tools**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather in Tokyo?", "use_tools": false}'
```

### 2. Test with the UI:
Simply open http://localhost:4200 and type:
- "What's the weather in San Francisco?"
- "Calculate 50 * 20"
- "What time is it?"

### 3. Test via API Docs:
Visit http://localhost:8000/docs for interactive API documentation.

---

## How to Add Your Own Tools

### Step 1: Define the Function
Add your Python function in `app.py`:

```python
def search_database(query: str, limit: int = 10) -> str:
    """Search the database for relevant information."""
    # Your implementation here
    results = perform_database_search(query, limit)
    return json.dumps(results)
```

### Step 2: Add Tool Definition
Add the tool specification to the `TOOLS` list:

```python
{
    "type": "function",
    "function": {
        "name": "search_database",
        "description": "Search the database for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return"
                }
            },
            "required": ["query"]
        }
    }
}
```

### Step 3: Register the Function
Add it to the `AVAILABLE_FUNCTIONS` dictionary:

```python
AVAILABLE_FUNCTIONS = {
    "get_current_weather": get_current_weather,
    "get_current_time": get_current_time,
    "calculate": calculate,
    "search_database": search_database  # New function
}
```

### Step 4: Rebuild and Test
```bash
docker-compose up -d --build backend
```

---

## Advanced Use Cases

### 1. Multiple Function Calls
The AI can chain multiple function calls:
```
User: "What's the weather in Paris and what time is it there?"
AI: 
  1. Calls get_current_weather("Paris")
  2. Calls get_current_time("CET")
  3. Combines results into response
```

### 2. Real-World API Integration
Replace mock functions with real APIs:
- **Weather**: OpenWeatherMap, WeatherAPI
- **Database**: PostgreSQL, MongoDB
- **External APIs**: Google Maps, Stripe, Twilio
- **IoT**: Control smart home devices
- **Business Logic**: Order processing, inventory checks

### 3. Custom Business Logic
```python
def check_inventory(product_id: str) -> str:
    """Check product availability in inventory."""
    # Connect to your database
    # Query inventory
    # Return stock information
    pass

def place_order(product_id: str, quantity: int) -> str:
    """Place an order for a product."""
    # Validate product
    # Check inventory
    # Process order
    # Return confirmation
    pass
```

---

## Best Practices

### 1. Clear Descriptions
Write detailed function descriptions so the AI knows when to use them:
```python
"description": "Get the current weather in a given location. Use this when users ask about weather conditions, temperature, or climate in a specific city."
```

### 2. Parameter Validation
Always validate and sanitize function parameters:
```python
def safe_function(user_input: str) -> str:
    # Validate input
    if not user_input or len(user_input) > 1000:
        return json.dumps({"error": "Invalid input"})
    
    # Sanitize
    cleaned = sanitize_input(user_input)
    
    # Process
    return json.dumps({"result": cleaned})
```

### 3. Error Handling
Wrap function calls in try-except blocks:
```python
try:
    result = external_api.call(params)
    return json.dumps({"success": True, "data": result})
except Exception as e:
    return json.dumps({"success": False, "error": str(e)})
```

### 4. Return JSON
Always return JSON strings from functions:
```python
return json.dumps({
    "status": "success",
    "data": result_data
})
```

### 5. Logging
Log function calls for debugging:
```python
print(f"[tool] {function_name} called with {function_args}", flush=True)
```

---

## Security Considerations

⚠️ **Important Security Notes**:

1. **Never expose sensitive data** in function responses
2. **Validate all inputs** before processing
3. **Rate limit** function calls to prevent abuse
4. **Sanitize** user inputs in calculations and queries
5. **Use environment variables** for API keys and secrets
6. **Implement authentication** for production deployments
7. **Audit logs** for all function executions

---

## Troubleshooting

### Functions not being called?
- Check the function description is clear
- Verify the model supports function calling (GPT-3.5-turbo, GPT-4)
- Ensure `use_tools: true` in the request
- Check logs for errors: `docker logs chatbot-backend`

### Wrong parameters passed?
- Review parameter descriptions
- Make them more explicit
- Add examples in descriptions

### Function execution errors?
- Check function implementation
- Verify return format is JSON string
- Look at backend logs: `docker-compose logs -f backend`

---

## Resources

- [OpenAI Function Calling Documentation](https://platform.openai.com/docs/guides/function-calling)
- [Best Practices Guide](https://platform.openai.com/docs/guides/function-calling/best-practices)
- [API Reference](https://platform.openai.com/docs/api-reference/chat/create)

---

## Example Conversations

### Example 1: Weather Query
```
You: What's the weather like in San Francisco?
Bot: [Calls get_current_weather("San Francisco", "fahrenheit")]
Bot: The weather in San Francisco is currently 72°F and sunny with 65% humidity. It's a beautiful day!
```

### Example 2: Calculation
```
You: I need to calculate 15% tip on a $125 bill
Bot: [Calls calculate("125 * 0.15")]
Bot: A 15% tip on a $125 bill would be $18.75.
```

### Example 3: Multiple Tools
```
You: What's the weather in London and what time is it there?
Bot: [Calls get_current_weather("London", "fahrenheit")]
Bot: [Calls get_current_time("GMT")]
Bot: In London, it's currently 58°F and rainy. The local time is 14:30 GMT (2:30 PM).
```

---

## Next Steps

1. **Test the existing tools** with various queries
2. **Add your own custom tools** for your use case
3. **Integrate real APIs** (weather, database, etc.)
4. **Implement authentication** for production
5. **Add rate limiting** and monitoring
6. **Deploy to production** environment

Happy building! 🚀
