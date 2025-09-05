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
    # TO-DO: Уточнить и внедрить допустимую длину вопроса
    # при необходимости внести изменения в схему
    # TO-DO: Уточнить, должны ли быть вопросы уникальными
    # при необходимости добавить unique=True
    text = Column(String, nullable=False) # Текст вопроса
    # TO-DO: добавить индекс по дате, если будут выборки или сортировки по полю
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    # Один вопрос - много ответов
    answers = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan", # Удалять ответы без "родителя"
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
        nullable=False,
        index=True
    )
    # TO-DO: Уточнить и внедрить максимальную длину идентификатора
    # при необходимости внести изменения в схему
    # TO-DO: Добавить индексацию, если будут выборки по пользователю
    user_id = Column(String, nullable=False)  # UUID пользователя
    # TO-DO: Уточнить и внедрить максимальную длину ответа
    # при необходимости внести изменения в схему
    text = Column(String, nullable=False)     # Текст ответа
    # TO-DO: добавить индекс по дате, если будут выборки или сортировки по полю
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    # Обратная связь к вопросу
    question = relationship(
        "Question",
        back_populates="answers"
    )
