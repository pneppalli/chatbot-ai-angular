# OpenAI Function Calling - Visual Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                            │
│                     http://localhost:4200                       │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ HTTP Request
                 │ POST /chat
                 │ {"message": "What's the weather in Tokyo?"}
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│              Angular Frontend (Port 4200)                       │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  app.component.ts                                     │     │
│  │  - User input handling                                │     │
│  │  - Message display                                    │     │
│  │  - fetch('http://127.0.0.1:8000/chat')               │     │
│  └───────────────────────────────────────────────────────┘     │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ HTTP POST
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│             FastAPI Backend (Port 8000)                         │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  POST /chat Endpoint                                  │     │
│  │  1. Receive user message                              │     │
│  │  2. Build messages array                              │     │
│  │  3. Add tools definition (if use_tools=true)          │     │
│  └────────────┬──────────────────────────────────────────┘     │
│               │                                                 │
│               ▼                                                 │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  OpenAI API Call #1                                   │     │
│  │  client.chat.completions.create(                      │     │
│  │    model="gpt-3.5-turbo",                             │     │
│  │    messages=[...],                                    │     │
│  │    tools=TOOLS  ← Weather, Time, Calculate            │     │
│  │  )                                                     │     │
│  └────────────┬──────────────────────────────────────────┘     │
└───────────────┼─────────────────────────────────────────────────┘
                │
                │ HTTPS
                │
                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OpenAI API                                   │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  GPT Model Analyzes Request                           │     │
│  │  - Reads user message                                 │     │
│  │  - Sees available tools                               │     │
│  │  - Decides if tools are needed                        │     │
│  └────────────┬──────────────────────────────────────────┘     │
│               │                                                 │
│               ▼                                                 │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  Decision: Use Tool?                                  │     │
│  │  ┌─────────────┐         ┌─────────────┐             │     │
│  │  │   YES       │         │     NO      │             │     │
│  │  │ Generate    │         │ Generate    │             │     │
│  │  │ function    │         │ text        │             │     │
│  │  │ call        │         │ response    │             │     │
│  │  └──────┬──────┘         └──────┬──────┘             │     │
│  └─────────┼───────────────────────┼─────────────────────┘     │
└────────────┼───────────────────────┼───────────────────────────┘
             │                       │
             │                       └─────────────┐
             ▼                                     ▼
┌─────────────────────────────────────────────────────────────────┐
│             FastAPI Backend (Receives Response)                 │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  Tool Calls Detected?                                 │     │
│  │  ┌─────────────┐         ┌─────────────┐             │     │
│  │  │   YES       │         │     NO      │             │     │
│  │  └──────┬──────┘         └──────┬──────┘             │     │
│  └─────────┼───────────────────────┼─────────────────────┘     │
│            │                       │                           │
│            ▼                       │                           │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  Execute Functions                                    │     │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────┐  │     │
│  │  │ get_weather()  │  │ get_time()     │  │calculate│  │     │
│  │  │ ├─ location   │  │ ├─ timezone    │  │ ├─ expr │  │     │
│  │  │ └─ unit       │  │ └─ returns     │  │ └─ eval │  │     │
│  │  │   returns     │  │   timestamp    │  │   result│  │     │
│  │  │   weather     │  │                │  │         │  │     │
│  │  └────────────────┘  └────────────────┘  └────────┘  │     │
│  └────────────┬──────────────────────────────────────────┘     │
│               │                                                 │
│               ▼                                                 │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  OpenAI API Call #2                                   │     │
│  │  client.chat.completions.create(                      │     │
│  │    model="gpt-3.5-turbo",                             │     │
│  │    messages=[                                         │     │
│  │      {...original messages...},                       │     │
│  │      {...assistant tool_calls...},                    │     │
│  │      {...function results...}  ← New!                 │     │
│  │    ]                                                   │     │
│  │  )                                                     │     │
│  └────────────┬──────────────────────────────────────────┘     │
└───────────────┼──────────────────────────────────────────┬──────┘
                │                                          │
                │                                          │
                ▼                                          │
┌─────────────────────────────────────────────────────────────────┐
│                    OpenAI API                                   │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  GPT Formulates Final Response                        │     │
│  │  - Reads function results                             │     │
│  │  - Integrates data into natural language              │     │
│  │  - Returns conversational response                    │     │
│  └────────────┬──────────────────────────────────────────┘     │
└───────────────┼─────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────┐
│             FastAPI Backend                                     │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  Return Response                                      │     │
│  │  {                                                     │     │
│  │    "reply": "The weather in Tokyo is 68°F...",        │     │
│  │    "used_tools": true                                 │     │
│  │  }                                                     │     │
│  └────────────┬──────────────────────────────────────────┘     │
└───────────────┼─────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────┐
│              Angular Frontend                                   │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  Display Response                                     │     │
│  │  - Show bot message                                   │     │
│  │  - Update UI                                          │     │
│  └───────────────────────────────────────────────────────┘     │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
            User sees response!
```

## Function Call Flow (Detailed)

### Scenario: "What's the weather in San Francisco?"

```
Step 1: User Input
├─ User types message
└─ Frontend sends POST request

Step 2: Backend Processing
├─ Receive message
├─ Build conversation context
│  └─ [system]: "You are a helpful assistant..."
│  └─ [user]: "What's the weather in San Francisco?"
└─ Attach tools definition

Step 3: First OpenAI Call
├─ Send: messages + tools
└─ Receive: tool_calls response
    └─ function: "get_current_weather"
    └─ arguments: {"location": "San Francisco", "unit": "fahrenheit"}

Step 4: Function Execution
├─ Parse function name
├─ Parse arguments
├─ Execute: get_current_weather("San Francisco", "fahrenheit")
└─ Result: {"temperature": "72", "condition": "sunny", "humidity": "65%"}

Step 5: Second OpenAI Call
├─ Send: original messages + tool results
└─ Receive: natural language response
    └─ "The weather in San Francisco is currently 72°F and sunny..."

Step 6: Return to User
├─ Backend sends JSON response
└─ Frontend displays message
```

## Tools Definition Structure

```
TOOLS = [
  {
    "type": "function",
    "function": {
      "name": "get_current_weather",
      "description": "Get current weather...",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City name"
          },
          "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"]
          }
        },
        "required": ["location"]
      }
    }
  },
  // ... more tools
]
```

## Message Flow Examples

### Example 1: Tool Used

```json
// First API Call
{
  "messages": [
    {"role": "system", "content": "You are helpful..."},
    {"role": "user", "content": "Weather in Tokyo?"}
  ],
  "tools": [...],
  "model": "gpt-3.5-turbo"
}

// OpenAI Response
{
  "choices": [{
    "message": {
      "tool_calls": [{
        "id": "call_123",
        "function": {
          "name": "get_current_weather",
          "arguments": "{\"location\":\"Tokyo\"}"
        }
      }]
    }
  }]
}

// Function Execution
Result: {"temperature": "68", "condition": "clear"}

// Second API Call
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "Weather in Tokyo?"},
    {"role": "assistant", "tool_calls": [...]},
    {"role": "tool", "content": "{\"temperature\":\"68\",\"condition\":\"clear\"}"}
  ]
}

// Final Response
{
  "choices": [{
    "message": {
      "content": "The weather in Tokyo is currently 68°F and clear with 60% humidity."
    }
  }]
}
```

### Example 2: No Tool Needed

```json
// API Call
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "Tell me about space"}
  ],
  "tools": [...]
}

// OpenAI Response (no tool_calls)
{
  "choices": [{
    "message": {
      "content": "Space is the vast expanse..."
    }
  }]
}
```

## Docker Container Layout

```
┌──────────────────────────────────────────────────────────┐
│              Docker Host (Your Computer)                 │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │  chatbot-backend (Port 8000)                   │     │
│  │  ┌──────────────────────────────────────────┐  │     │
│  │  │  Python 3.11                             │  │     │
│  │  │  FastAPI + Uvicorn                       │  │     │
│  │  │  OpenAI SDK                              │  │     │
│  │  │  app.py (with function calling)          │  │     │
│  │  └──────────────────────────────────────────┘  │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │  chatbot-frontend (Port 4200)                  │     │
│  │  ┌──────────────────────────────────────────┐  │     │
│  │  │  Nginx                                   │  │     │
│  │  │  Angular 16 (compiled)                   │  │     │
│  │  │  Static files                            │  │     │
│  │  └──────────────────────────────────────────┘  │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │  chatbot-network (Bridge)                      │     │
│  │  - Connects frontend & backend                 │     │
│  └────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
         │                            │
         │ :4200                      │ :8000
         ▼                            ▼
    Browser Access              API Access
```

## File Structure

```
chatbot-ai/
│
├── chatbot-openai/                 Backend
│   ├── app.py                      ← Function calling logic here
│   │   ├── get_current_weather()
│   │   ├── get_current_time()
│   │   ├── calculate()
│   │   ├── TOOLS = [...]
│   │   ├── AVAILABLE_FUNCTIONS = {...}
│   │   └── execute_function_call()
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── TOOLS_GUIDE.md
│
├── chatbot-ui/                     Frontend
│   ├── src/app/
│   │   ├── app.component.ts        ← Chat interface
│   │   └── app.module.ts
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml              ← Orchestration
├── .env                            ← API keys (create this!)
├── .env.example
├── README.md
├── FUNCTION_CALLING_SUMMARY.md
└── test-tools.ps1
```

## Key Concepts

### 1. Tool Choice
- **"auto"** - AI decides when to use tools (current implementation)
- **"none"** - Never use tools
- **specific tool** - Force a particular tool

### 2. Multi-Turn Conversation
```
Turn 1: User asks question
Turn 2: AI requests tool
Turn 3: Backend executes tool
Turn 4: AI sees results
Turn 5: AI formulates answer
```

### 3. Parallel Function Calls
OpenAI can request multiple tools at once:
```json
"tool_calls": [
  {"function": {"name": "get_weather", "arguments": "..."}},
  {"function": {"name": "get_time", "arguments": "..."}}
]
```

### 4. Function Safety
- Input validation
- Sandboxed execution
- Error handling
- Timeout protection

## Performance Metrics

```
No Tools:
User → Backend → OpenAI → Response
       50ms      1.5s      50ms
       ═══════════════════════
       Total: ~1.6 seconds

With Tools:
User → Backend → OpenAI → Backend → OpenAI → Response
       50ms      1.5s      100ms     1.5s      50ms
       ═══════════════════════════════════════════
       Total: ~3.2 seconds
```

---

Made with ❤️ for understanding AI function calling!
