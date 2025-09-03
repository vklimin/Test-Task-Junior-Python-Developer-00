# src/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src import models, database, schemas

app = FastAPI(title="Тестовое задание: API-сервис для вопросов и ответов")

# Зависимость для сессии БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


@app.post("/questions/", response_model=schemas.QuestionResponse)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    """
    Создание нового вопроса
    """
    db_question = models.Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
