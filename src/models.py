# src/models.py
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from src.database import Base

"""
Логика:
* Нельзя создать ответ к несуществующему вопросу.
* Один и тот же пользователь может оставлять несколько ответов на один вопрос.
* При удалении вопроса должны удаляться все его ответы (каскадно).
"""

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False) # Текст вопроса
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    # Один вопрос - много ответов
    answers = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan", # Удалять ответы без вопросов
        lazy="select"
    )


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(
        Integer,
        # Внешний ключ для автоматического удаления ответа
        # в случае удаления связанного вопроса
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id = Column(String, nullable=False)  # UUID пользователя
    text = Column(String, nullable=False)     # Текст ответа
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    # Обратная связь к вопросу
    question = relationship(
        "Question",
        back_populates="answers"
    )
