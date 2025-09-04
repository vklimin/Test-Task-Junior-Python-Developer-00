# src/main.py
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.models import Question
from src.schemas import QuestionCreate, QuestionResponse

app = FastAPI(title="Тестовое задание: API-сервис для вопросов и ответов")

# Зависимость для сессии БД
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root() -> dict:
    return {"message": "Hello, world!"}


@app.post("/questions/", response_model=QuestionResponse)
def create_question(
    question: QuestionCreate,
    db: Annotated[Session, Depends(get_db)]
) -> QuestionResponse:
    """
    Создание нового вопроса
    """
    db_question = Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
