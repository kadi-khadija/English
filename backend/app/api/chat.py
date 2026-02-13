from fastapi import APIRouter, HTTPException, Depends
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.ai_engine import get_ai_reply
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest, current_user=Depends(get_current_user)):
    try:
        ai_reply = get_ai_reply(
            conversation_history=[m.dict() for m in request.messages],
            level=request.level,
            topic_key=request.topic
        )
        return ChatResponse(reply=ai_reply)

    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid level or topic")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
