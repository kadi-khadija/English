from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.chat import ChatRequest, ChatResponse
from app.core.ai_engine import get_ai_reply
from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.conversation import Conversation
from app.models.message import Message

router = APIRouter(tags=["Chat"])


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # 1️⃣ Create conversation (for now, one per session)
    conversation = Conversation(
        user_id=current_user["sub"],
        level=request.level,
        topic=request.topic,
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    # 2️⃣ Save user messages
    for msg in request.messages:
        db_message = Message(
            conversation_id=conversation.id,
            role=msg.role,
            content=msg.content
        )
        db.add(db_message)

    # 3️⃣ Call AI
    conversation_history = [
        {"role": msg.role, "content": msg.content}
        for msg in request.messages
    ]

    ai_reply = get_ai_reply(
        conversation_history=conversation_history,
        level=request.level,
        topic_key=request.topic
    )

    # 4️⃣ Save AI reply
    ai_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=ai_reply
    )
    db.add(ai_message)

    db.commit()

    return ChatResponse(reply=ai_reply)
