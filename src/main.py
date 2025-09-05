# src/main.py
import logging
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Answer, Question
from src.schemas import (
    AnswerCreate,
    AnswerResponse,
    QuestionCreate,
    QuestionResponse,
    QuestionWithAnswersResponse,
)

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


# Обрабочики обращений
@app.get("/")
def read_root() -> dict:
    logger.info("Запрос корневого эндпоинта")
    return {"message": "Hello, world!"}


# === QUESTIONS ===

@app.get("/questions/", response_model=list[QuestionResponse])
def get_questions(
    db: Annotated[Session, Depends(get_db)]
) -> list[QuestionResponse]:
    """
    Получение списка всех вопросов
    """
    logger.info("Запрос списка всех вопросов")

    db_questions = db.query(Question).all()
    return db_questions


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


@app.get("/questions/{id}/", response_model=QuestionWithAnswersResponse)
def get_question_with_answers(
    id: int,
    db: Annotated[Session, Depends(get_db)]
) -> QuestionWithAnswersResponse:
    """
    Получение вопроса по ID и всех связанных с ним ответов
    """
    logger.info(f"Запрос вопроса с ID = {id} и всех ответов")

    db_question = db.query(Question).filter(Question.id == id).first()
    if not db_question:
        logger.info(f"Вопрос с ID = {id} не найден")
        raise HTTPException(status_code=404, detail="Question not found")

    return db_question


@app.delete("/questions/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    id: int,
    db: Annotated[Session, Depends(get_db)]
) -> None:
    """
    Удаление вопроса по ID вместе с ответами
    """
    logger.info(f"Запрос на удаление вопроса с ID = {id}")

    db_question = db.query(Question).filter(Question.id == id).first()
    if not db_question:
        logger.info(f"Вопрос с ID = {id} не найден при попытке удаления")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    # Удаление связанных с вопросом ответов должно гарантироваться
    # установленными реляционными отношениями между таблицами
    # TO-DO: продумать тесты и убедиться, что это точно работает
    db.delete(db_question)
    db.commit()

    logger.info(f"Вопрос с ID = {id} и все связанные ответы успешно удалены")
    return None


# === ANSWERS ==

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

    db_question = db.query(Question).filter(Question.id == id).first()
    if not db_question:
        logger.info(f"Не существует вопроса с ID = {id}")
        raise HTTPException(status_code=404, detail="Question not found")

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


@app.get("/answers/{id}/", response_model=AnswerResponse)
def get_answer(
    id: int,
    db: Annotated[Session, Depends(get_db)]
) -> AnswerResponse:
    """
    Получение конкретного ответа
    """
    logger.info(
        f"Запрос ответа с ID = {id}"
    )

    db_answer = db.query(Answer).filter(Answer.id == id).first()
    if not db_answer:
        logger.info(f"Не существует ответа с ID = {id}")
        raise HTTPException(status_code=404, detail="Answer not found")

    return db_answer


@app.delete("/answers/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
    id: int,
    db: Annotated[Session, Depends(get_db)]
) -> None:
    """
    Удаление ответа по ID
    """
    logger.info(f"Запрос на удаление ответа с ID = {id}")

    db_answer = db.query(Answer).filter(Answer.id == id).first()
    if not db_answer:
        logger.info(f"Ответ с ID = {id} не найден при попытке удаления")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )

    db.delete(db_answer)
    db.commit()

    logger.info(f"Ответ с ID = {id} успешно удалён")
    return None
