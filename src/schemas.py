# src/schemas.py
"""
Pydantic-схемы для FastAPI
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime


class QuestionCreate(BaseModel):
    """
    В HTTP-запросе ожидаем текст вопроса
    """
    text: str = Field(
        ...,
        description="Текст вопроса (обязательный, не может быть пустым или состоять только из пробелов)"
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or (v := v.strip()) == "":
            raise ValueError("Текст вопроса не может быть пустым или состоять только из пробелов")
        return v


class QuestionResponse(BaseModel):
    """
    В HTTP-ответе возвращаем поля созданной записи
    """
    id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
