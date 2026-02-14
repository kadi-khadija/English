from fastapi import APIRouter
from app.schemas.feedback import FeedbackRequest, FeedbackResponse
from app.core.feedback_logic import generate_feedback
from app.core.dependencies import get_current_user

router = APIRouter( tags=["Feedback"])


@router.post("/", response_model=FeedbackResponse)
def feedback(request: FeedbackRequest,
             current_user: dict = Depends(get_current_user)
            ):
    result = generate_feedback(request.messages)
    return FeedbackResponse(feedback=result["feedback"])
