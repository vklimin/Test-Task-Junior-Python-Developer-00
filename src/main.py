# src/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src import models, database, schemas
from typing import Annotated

app = FastAPI(title="Тестовое задание: API-сервис для вопросов и ответов")

# Зависимость для сессии БД
def get_db() -> Session:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root() -> dict:
    return {"message": "Hello, world!"}


@app.post("/questions/", response_model=schemas.QuestionResponse)
def create_question(
    question: schemas.QuestionCreate, 
    db: Annotated[Session, Depends(get_db)]
) -> schemas.QuestionResponse:
    """
    Создание нового вопроса
    """
    db_question = models.Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
