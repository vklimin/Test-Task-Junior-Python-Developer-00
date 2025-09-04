# src/main.py
import logging
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.models import Question
from src.schemas import QuestionCreate, QuestionResponse


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s UTC [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Инициализация FastAPI-приложения
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
    logger.info("Запрос корневого эндпоинта")
    return {"message": "Hello, world!"}


@app.get("/questions/", response_model=list[QuestionResponse])
def get_questions(
    db: Annotated[Session, Depends(get_db)]
):
    """
    Получение списка всех вопросов
    """
    logger.info("Запрос списка всех вопросов")
    return db.query(Question).all()

@app.post("/questions/", response_model=QuestionResponse)
def create_question(
    question: QuestionCreate,
    db: Annotated[Session, Depends(get_db)]
) -> QuestionResponse:
    """
    Создание нового вопроса
    """
    logger.info(f"Создание вопроса: \"{question.text}\"")
    db_question = Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    logger.info(f"Создан вопрос с ID = {db_question.id}")
    return db_question
