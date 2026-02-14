from pydantic import BaseModel
from app.schemas.chat import ChatMessage

class FeedbackRequest(BaseModel):
    messages: list[ChatMessage]

class FeedbackResponse(BaseModel):
    feedback: str
