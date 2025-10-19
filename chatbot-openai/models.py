"""Pydantic models for API request/response."""

from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    model: Optional[str] = "gpt-3.5-turbo"
    use_basic: Optional[bool] = False
    use_tools: Optional[bool] = True  # Enable function calling by default


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    reply: str
    used_tools: Optional[bool] = False
