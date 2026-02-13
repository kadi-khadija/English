from fastapi import FastAPI
from app.api import auth, chat, feedback
from app.database.base import Base
from app.database.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI English Immersion Platform")

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(feedback.router)


@app.get("/")
def health_check():
    return {"status": "Backend running successfully"}
