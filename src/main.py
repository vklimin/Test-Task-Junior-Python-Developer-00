# src/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src import models, database

app = FastAPI(title="Тестовое задание: API-сервис для вопросов и ответов")

# Зависимость для сессии БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

