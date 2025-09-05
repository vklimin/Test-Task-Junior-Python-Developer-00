# src/schemas.py
"""
Pydantic-схемы для FastAPI
"""
from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator


class QuestionCreate(BaseModel):
    """
    В HTTP-запросе ожидаем текст вопроса
    """
    text: str = Field(
        ...,
        description=(
            "Текст вопроса (обязательный, "
            "не может быть пустым или состоять только из пробелов)"
        )
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls: type[Self], v: str) -> str:
        # TO-DO: при необходимости можно усилить валидацию текста
        # с помощью регулярных выражений
        # Например, можно избавляться от спаренных пробелов в тексте вопроса
        if not v or (v := v.strip()) == "":
            raise ValueError(
                "Текст вопроса не может быть пустым или состоять только из пробелов"
            )
        return v


class QuestionResponse(BaseModel):
    """
    В HTTP-ответе возвращаем поля записи о вопросе
    """
    id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnswerCreate(BaseModel):
    user_id: str = Field(
        ...,
        description=(
            "Идентификатор пользователя (обязательный, "
            "не может быть пустым или состоять только из пробелов)"
        )
    )
    text: str = Field(
        ...,
        description=(
            "Текст ответа (обязательный, "
            "не может быть пустым или состоять только из пробелов)"
        )
    )


    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls: type[Self], v: str) -> str:
        if not v or (v := v.strip()) == "":
            raise ValueError(
                "Идентификатор пользователя не может быть "
                "пустым или состоять только из пробелов"
            )
        return v

    @field_validator("text")
    @classmethod
    def validate_text(cls: type[Self], v: str) -> str:
        if not v or (v := v.strip()) == "":
            raise ValueError(
                "Текст ответа не может быть пустым или состоять только из пробелов"
            )
        return v


class AnswerResponse(BaseModel):
    """
    В HTTP-ответе возвращаем поля записи об ответе
    """
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionWithAnswersResponse(BaseModel):
    """
    В HTTP-ответе возвращаем вопрос и все ответы на него
    """
    id: int
    text: str
    created_at: datetime
    answers: list[AnswerResponse] = []

    model_config = ConfigDict(from_attributes=True)
