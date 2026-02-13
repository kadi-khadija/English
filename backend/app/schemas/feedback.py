from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    messages: list[dict]

class FeedbackResponse(BaseModel):
    feedback: str
