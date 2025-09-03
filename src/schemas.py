# src/schemas.py
"""
Pydantic-схемы для FastAPI
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class QuestionCreate(BaseModel):
    """
    В HTTP-запросе ожидаем текст вопроса
    """
    text: str


class QuestionResponse(BaseModel):
    """
    В HTTP-ответе возвращаем поля созданной записи
    """
    id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
