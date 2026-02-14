from fastapi import FastAPI
from app.api import auth, chat, feedback
from app.database.base import Base
from app.database.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI English Immersion Platform",  version="0.1.0")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])



@app.get("/")
def health_check():
    return {"status": "Backend running successfully"}
