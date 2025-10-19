# Modular Architecture Diagram

## New Module Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                         app.py (365 lines)                      │
│                    Main FastAPI Application                     │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  API Endpoints:                                        │    │
│  │  • GET /          - API info                           │    │
│  │  • GET /status    - System status                      │    │
│  │  • GET /tools     - List tools                         │    │
│  │  • POST /chat     - Main chat endpoint                 │    │
│  │  • POST /test-pushover - Test notifications            │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Imports from modules ↓                                         │
└─────────────────────────────────────────────────────────────────┘
         │         │          │           │            │
         ▼         ▼          ▼           ▼            ▼
    ┌────────┐ ┌──────┐ ┌──────────┐ ┌────────────┐ ┌──────┐
    │config.py│ │models│ │openai_   │ │notifications│ │tools │
    │         │ │.py   │ │client.py │ │.py         │ │.py   │
    │ 47 lines│ │18 ln │ │ 124 lines│ │ 102 lines  │ │204 ln│
    └────────┘ └──────┘ └──────────┘ └────────────┘ └──────┘
```

## Detailed Module View

### config.py - Configuration Hub
```
┌────────────────────────────────────────┐
│         config.py (47 lines)           │
├────────────────────────────────────────┤
│  Environment Variable Getters:         │
│  • get_openai_api_key()                │
│  • get_pushover_user_key()             │
│  • get_pushover_api_token()            │
│  • get_chat_backend()                  │
│  • get_ollama_url()                    │
│                                        │
│  Constants:                            │
│  • CORS_ORIGINS                        │
└────────────────────────────────────────┘
```

### models.py - Data Models
```
┌────────────────────────────────────────┐
│         models.py (18 lines)           │
├────────────────────────────────────────┤
│  Pydantic Models:                      │
│                                        │
│  ChatRequest:                          │
│    ├── message: str                    │
│    ├── model: Optional[str]            │
│    ├── use_basic: Optional[bool]       │
│    └── use_tools: Optional[bool]       │
│                                        │
│  ChatResponse:                         │
│    ├── reply: str                      │
│    └── used_tools: Optional[bool]      │
└────────────────────────────────────────┘
```

### openai_client.py - OpenAI Integration
```
┌────────────────────────────────────────┐
│    openai_client.py (124 lines)        │
├────────────────────────────────────────┤
│  OpenAI Functions:                     │
│  • make_openai_client()                │
│  • extract_chat_content()              │
│  • initialize_openai_client()          │
│                                        │
│  Alternative Backend:                  │
│  • call_ollama()                       │
│                                        │
│  Imports: config.py                    │
└────────────────────────────────────────┘
```

### notifications.py - Alert System
```
┌────────────────────────────────────────┐
│    notifications.py (102 lines)        │
├────────────────────────────────────────┤
│  Pushover Functions:                   │
│  • send_pushover_notification()        │
│  • detect_insufficient_information()   │
│  • notify_insufficient_information()   │
│                                        │
│  Detection Patterns:                   │
│    ├── "I don't have"                  │
│    ├── "I don't know"                  │
│    ├── "Not available"                 │
│    └── 15+ more patterns...            │
│                                        │
│  Imports: config.py                    │
└────────────────────────────────────────┘
```

### tools.py - Function Calling
```
┌────────────────────────────────────────┐
│        tools.py (204 lines)            │
├────────────────────────────────────────┤
│  Tool Implementations:                 │
│  • get_current_weather()               │
│  • get_current_time()                  │
│  • calculate()                         │
│                                        │
│  Tool Definitions:                     │
│  • TOOLS (OpenAI JSON schema)          │
│  • AVAILABLE_FUNCTIONS (mapping)       │
│                                        │
│  Execution:                            │
│  • execute_function_call()             │
│                                        │
│  No external dependencies              │
└────────────────────────────────────────┘
```

## Request Flow Diagram

```
HTTP Request
    ↓
┌─────────────────────────┐
│   app.py                │
│   FastAPI Endpoint      │
│   (POST /chat)          │
└──────────┬──────────────┘
           │
           │ 1. Import models
           ▼
┌─────────────────────────┐
│   models.py             │
│   ChatRequest validated │
└──────────┬──────────────┘
           │
           │ 2. Get config
           ▼
┌─────────────────────────┐
│   config.py             │
│   get_openai_api_key()  │
└──────────┬──────────────┘
           │
           │ 3. Initialize client
           ▼
┌─────────────────────────┐
│   openai_client.py      │
│   make_openai_client()  │
└──────────┬──────────────┘
           │
           │ 4. Call OpenAI with tools
           ▼
┌─────────────────────────┐
│   OpenAI API            │
│   (returns tool_calls)  │
└──────────┬──────────────┘
           │
           │ 5. Execute tools
           ▼
┌─────────────────────────┐
│   tools.py              │
│   execute_function_call │
└──────────┬──────────────┘
           │
           │ 6. Check response
           ▼
┌─────────────────────────┐
│   notifications.py      │
│   detect_insufficient   │
└──────────┬──────────────┘
           │
           │ 7. Return response
           ▼
┌─────────────────────────┐
│   models.py             │
│   ChatResponse          │
└──────────┬──────────────┘
           │
           ▼
    HTTP Response
```

## Dependency Graph

```
app.py (Main)
  ├── depends on → config.py
  ├── depends on → models.py
  ├── depends on → openai_client.py
  │                  └── depends on → config.py
  ├── depends on → notifications.py
  │                  └── depends on → config.py
  └── depends on → tools.py
                     (no dependencies)

Legend:
→ = imports from
```

## File Size Comparison

```
Before Refactoring:
┌───────────────────────────────────────┐
│ app.py                      554 lines │
│ ███████████████████████████████████   │
└───────────────────────────────────────┘

After Refactoring:
┌───────────────────────────────────────┐
│ app.py                      365 lines │
│ ███████████████████████               │
├───────────────────────────────────────┤
│ tools.py                    204 lines │
│ ████████████                          │
├───────────────────────────────────────┤
│ openai_client.py            124 lines │
│ ███████                               │
├───────────────────────────────────────┤
│ notifications.py            102 lines │
│ ██████                                │
├───────────────────────────────────────┤
│ config.py                    47 lines │
│ ██                                    │
├───────────────────────────────────────┤
│ models.py                    18 lines │
│ █                                     │
└───────────────────────────────────────┘
Total: 860 lines (better organized!)
```

## Module Responsibilities

```
┌────────────────────────────────────────────────────────┐
│                   Single Responsibility                │
├────────────────────────────────────────────────────────┤
│                                                        │
│  config.py          → Environment & Configuration      │
│  models.py          → Data Validation & Schemas        │
│  openai_client.py   → AI Integration                   │
│  notifications.py   → Alerting & Monitoring            │
│  tools.py           → Function Calling                 │
│  app.py             → HTTP API Layer                   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Testing Strategy

```
Unit Tests:
├── test_config.py
│   └── Test environment variable access
├── test_models.py
│   └── Test Pydantic validation
├── test_openai_client.py
│   └── Test client creation (mocked)
├── test_notifications.py
│   ├── Test detection logic
│   └── Test Pushover API calls (mocked)
├── test_tools.py
│   ├── Test weather function
│   ├── Test time function
│   └── Test calculator function
└── test_app.py
    └── Test FastAPI endpoints (integration)
```

## Benefits Summary

```
┌─────────────────────────────────────────┐
│          Before → After                 │
├─────────────────────────────────────────┤
│  1 file     →  6 modules               │
│  554 lines  →  Average 143 lines/file  │
│  Hard to    →  Easy to test            │
│  test                                   │
│  Difficult  →  Simple to add features  │
│  to extend                              │
│  Merge      →  Minimal conflicts       │
│  conflicts                              │
│  Hard to    →  Easy to navigate        │
│  navigate                               │
└─────────────────────────────────────────┘
```

## Quick Reference

### To add a new tool:
1. Edit `tools.py` - Add function implementation
2. Edit `tools.py` - Add to TOOLS list
3. Edit `tools.py` - Add to AVAILABLE_FUNCTIONS
4. Rebuild: `docker-compose up -d --build backend`

### To add a new notification service:
1. Edit `notifications.py` - Add send function
2. Edit `config.py` - Add config getters
3. Update `.env.example` - Add new keys

### To add a new endpoint:
1. Edit `app.py` - Add @app.get/post decorator
2. Import from modules as needed
3. Rebuild and test

---

🎉 **Clean, Maintainable, Professional Code Structure!**
