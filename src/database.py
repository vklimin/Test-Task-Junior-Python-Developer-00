# src/database.py
"""
Настройка подключения к базе данных с использованием SQLAlchemy
- DATABASE_URL: переменная окружения для подключения к PostgreSQL
- Base: базовый класс для декларативных моделей
- SessionLocal: фабрика сессий для работы с БД
"""
import os

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeMeta, Session, declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
       "DATABASE_URL не задана в переменных окружения"
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Зависимость для сессии БД
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

