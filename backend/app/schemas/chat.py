from pydantic import BaseModel
from typing import List, Literal, Optional


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    level: Literal["beginner", "intermediate", "advanced"]
    topic: str
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    reply: str
