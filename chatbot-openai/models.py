from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = "gpt-3.5-turbo"
    use_basic: Optional[bool] = False
    use_tools: Optional[bool] = True


class ChatResponse(BaseModel):
    reply: str
    used_tools: Optional[bool] = False
