# src/schemas.py
"""
Pydantic-схемы для FastAPI
"""
from pydantic import BaseModel
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

    class Config:
        from_attributes = True
