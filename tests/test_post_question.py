# tests/test_01_post_question.py
"""
Эти тесты сгенерированы QWEN AI
"""

import pytest
from pydantic import ValidationError

from src.schemas import QuestionCreate


def test_question_create_valid() -> None:
    """Тест: корректный текст — валидация проходит"""
    schema = QuestionCreate(text="Как работает FastAPI?")
    assert schema.text == "Как работает FastAPI?"


def test_question_create_empty_string() -> None:
    """Тест: пустая строка — ошибка валидации"""
    with pytest.raises(ValidationError) as exc_info:
        QuestionCreate(text="")

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("text",)
    assert "не может быть пустым" in errors[0]["msg"]


def test_question_create_whitespace_only() -> None:
    """Тест: только пробелы — ошибка валидации"""
    with pytest.raises(ValidationError) as exc_info:
        QuestionCreate(text="   ")

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("text",)
    assert "не может быть пустым" in errors[0]["msg"]


def test_question_create_leading_trailing_spaces() -> None:
    """Тест: пробелы в начале и конце — обрезаются, валидация проходит"""
    schema = QuestionCreate(text="  Вопрос с пробелами  ")
    assert schema.text == "Вопрос с пробелами"  # Пробелы убраны


def test_question_create_tabs_or_newlines() -> None:
    """Тест: табуляция или перенос строки — тоже считаются пробелами"""
    with pytest.raises(ValidationError):
        QuestionCreate(text="\t\n  ")

    with pytest.raises(ValidationError):
        QuestionCreate(text="\n")


def test_question_create_none() -> None:
    """Тест: None — ошибка валидации"""
    with pytest.raises(ValidationError):
        QuestionCreate(text=None)
