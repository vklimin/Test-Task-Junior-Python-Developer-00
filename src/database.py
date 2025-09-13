# src/database.py
"""
Настройка подключения к базе данных с использованием SQLAlchemy
- DATABASE_URL: переменная окружения для подключения к PostgreSQL
- Base: базовый класс для декларативных моделей
- SessionLocal: фабрика сессий для работы с БД
"""
import os

from typing import Generator
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

if not all([DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME]):
    raise ValueError(
       "Отсутствуют переменные окружения с информацией для подключения к базе данных"
    )

DB_PASS = quote_plus(DB_PASS or "")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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

