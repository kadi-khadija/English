from fastapi import APIRouter
from app.schemas.feedback import FeedbackRequest, FeedbackResponse
from app.core.feedback_logic import generate_feedback

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/", response_model=FeedbackResponse)
def feedback(request: FeedbackRequest):
    result = generate_feedback(request.messages)
    return FeedbackResponse(feedback=result["feedback"])
