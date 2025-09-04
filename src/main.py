# src/main.py
import logging
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.models import Answer, Question
from src.schemas import AnswerCreate, AnswerResponse, QuestionCreate, QuestionResponse

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
) -> list[QuestionResponse]:
    """
    Получение списка всех вопросов
    """
    logger.info("Запрос списка всех вопросов")
    questions = db.query(Question).all()
    return questions


@app.post("/questions/", response_model=QuestionResponse)
def create_question(
    question: QuestionCreate,
    db: Annotated[Session, Depends(get_db)]
) -> QuestionResponse:
    """
    Создание нового вопроса
    """
    logger.info(f"Создание вопроса: \"{question.text}\"")
    db_question = Question(
       text=question.text
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    logger.info(f"Создан вопрос с ID = {db_question.id}")
    return db_question


@app.post("/questions/{id}/answers/", response_model=AnswerResponse)
def create_answer(
    id: int,
    answer: AnswerCreate,
    db: Annotated[Session, Depends(get_db)]
) -> AnswerResponse:
    """
    Добавление ответа к вопросу по ID
    """
    logger.info(
        f"Создание пользователем {answer.user_id} "
        "ответа \"{answer.text}\" к вопросу ID = {id}"
    )
    question = db.query(Question).filter(Question.id == id).first()
    if not question:
        logger.info(f"Не существует вопроса с ID = {id}")
        raise HTTPException(status_code=404, detail=f"Вопрос с ID = {id} не найден")

    db_answer = Answer(
        question_id=id,
        user_id=answer.user_id,
        text=answer.text
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    logger.info(f"Создан ответ с ID = {db_answer.id}")
    return db_answer
