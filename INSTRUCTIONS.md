# 🚀 Инструкция: Запуск FastAPI + PostgreSQL в Docker
## Оглавление
- [Объективная оценка задания](#объективная-оценка-задания)
- [Шаг 01. Создание SSH-ключа безопасности](#шаг-01-создание-ssh-ключа-безопасности)
- [Шаг 02. Связывание рабочего устройства и GitHub](#шаг-02-связывание-рабочего-устройства-и-github)
- [Шаг 03. Создание нового репозитория на GitHub](#шаг-03-создание-нового-репозитория-на-github)
- [Шаг 04. Клонирование репозитория на рабочее устройство](#шаг-04-клонирование-репозитория-на-рабочее-устройство)
- [Шаг 05. Запуск СУБД PostgreSQL внутри контейнера](#шаг-05-запуск-субд-postgresql-внутри-контейнера)
- [Шаг 06. Добавление контейнера с приложением](#шаг-06-добавление-контейнера-с-приложением)
- [Шаг 07. Запуск и проверка работоспособности](#шаг-07-запуск-и-проверка-работоспособности)
- [Шаг 08. Настройка миграции с помощью Alembic](#шаг-08-настройка-миграции-с-помощью-alembic)
- [Шаг 09. Подготовка к использованию Pydantic](#шаг-09-подготовка-к-использованию-pydantic)
- [Шаг 10. Средства анализа качества кода](#шаг-10-средства-анализа-качества-кода)
- [Шаг 11. Подготовка к тестированию Pytest](#шаг-11-подготовка-к-тестированию-pytest)
- [Шаг 12. Автоматизация тестирования с помощью CI/CD](#шаг-12-автоматизация-тестирования-с-помощью-cicd)
- [Шаг 13. Настройка логирования Logging](#шаг-13-настройка-логирования-logging)
- [Шаг 14. Создание эндпоинтов API](#шаг-14-создание-эндпоинтов-api)

## Объективная оценка задания

### 🛠️ Стек технологий

| Технологии | Уровень → Специализация |
|------------|-------------------------|
| SSH | Trainee → DevOps & Security |
| Git, GitHub | Junior → Version Control |
| Docker | Junior+ → DevOps & Infrastructure |
| Docker Compose | pre-Middle → DevOps & Infrastructure |
| Python, FastAPI, Pydantic | Junior+ → Python Backend Development |
| SQL | Junior → Database Engineering |
| Alembic, PostgreSQL | Junior+ → Database Engineering |
| SQLAlchemy | Junior++ → Python Backend Development |
| Uvicorn | Trainee → Python Backend Development |
| Python logging | Junior → Observability & Monitoring |
| Ruff | Trainee → Code Quality & Maintenance |
| mypy | Junior → Code Quality & Maintenance |
| pytest | Junior → Software Testing |
| GitHub Actions (CI/CD) | Junior → DevOps & CI/CD |

---

### 💡 Итоговый уровень разработчика по данному проекту
> Разработчик переходит от базового уровня **Junior+** к **pre-Middle**, осваивая практики проектирования API, работу с базами данных, миграции, контейнеризацию и подготовку приложения к продакшену

---

## Шаг 01. Создание SSH-ключа безопасности
> ⚠️ Пропустите этот шаг, если ключ уже существует в папке ~/.ssh

* Создайте SSH-ключ для безопасного подключения к GitHub:
```bash
ssh-keygen
```
> Команда создаст комплект ключей в папке ~/.ssh: приватный и публичный

---

## Шаг 02. Связывание рабочего устройства и GitHub
> ⚠️ Пропустите, если ключ уже добавлен на GitHub

* Скопируйте публичный ключ:
```bash
 cat ~/.ssh/*.pub
 ```
> Команда выведет на экран публичный ключ, который можно будет скопировать в буфер обмена.

* Перейдите в GitHub → Settings → SSH and GPG keys → New SSH key
* Вставьте ключ, укажите название (например, My Notebook)
* Сохраните
* Проверьте подключение:
```bash
ssh -T git@github.com
```
> При первом контакте ваше устройство запросит разрешение на установку связи с удалённым устройством. Необходимо ответить словом **yes**. Если проблем нет, должна появиться фраза *"You've successfully authenticated"*.

---

## Шаг 03. Создание нового репозитория на GitHub
* Перейдите в раздел Repositories
* Нажмите New
* Укажите Repository name, Description
* Укажите публичность репозитория Private или Public

---

## Шаг 04. Клонирование репозитория на рабочее устройство
* Скопируйте SSH-ссылку на репозиторий GitHub → Code → Local → SSH
* Выберите каталог, куда будет клонироваться репозиторий
* Клонируйте:
```bash
git clone <ссылка на репозиторий>
```
* Зайдите в каталог проекта
* Создайте ветку разработки:
```bash
git checkout -b develop
```
> ⚠️ Все изменения - в develop, main - только для релизов
* Проверьте текущую ветку:
```bash
git branch
```
* Сохраните изменения в репозитории
```bash
git add -A
git commit -m "Первый push"
git push --set-upstream origin develop
```

---

## Шаг 05. Запуск СУБД PostgreSQL внутри контейнера

### 01. Создание файла окружения для хранения пароля
> ⚠️ Пароли и чувствительную информацию принято хранить в отдельном специальном файле .env

> ⚠️⚠️ Пароли и секреты никогда не коммитятся в Git

* Убедитесь, что файл .gitignore содержит:
```text
.env
```
* В корне проекта создайте шаблон .env.example:
```bash
nano .env.example
```
```env
# .env.example
#
# Это шаблон файла окружения. Не используйте напрямую.
# Скопируйте его в .env и подставьте свои значения:
#
#   cp .env.example .env
#
# Затем отредактируйте .env, указав реальные (или тестовые) пароли.
# Файл .env добавлен в .gitignore — он не попадёт в репозиторий.

POSTGRES_DB=myapp
POSTGRES_USER=myuser
POSTGRES_PASSWORD=your_secure_password_here
```
> Этот шаблон необходим для удобства будущих пользователей проекта
* Создайте реальный .env:
```bash
cp .env.example .env
```
> При необходимости измените название БД, имя и пароль пользователя

### 02. Создание конфигурации для Docker Compose
* В корне проекта создайте конфигурационный файл:
```bash
nano docker-compose.yml
```
```yaml
version: '3.8'

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 2s
      timeout: 5s
      retries: 15
    volumes:
      - postgres_data:/var/lib/postgresql/data  
    restart: unless-stopped

volumes:
  postgres_data:
```
> Образ postgres:16 - официальный и готов к использованию. Для других ситуаций может не оказаться удачного образа и его придётся собирать вручную с помощью файла конфигурации Dockerfile\
> Переменные окружения POSTGRES_... будут автоматически подключены из файла .env

---

## Шаг 06. Добавление контейнера с приложением
Для того, чтобы работать с базой данных, обычно добавляют контейнер с каким-либо приложением. Эти два независимых контейнера будут работать в тандеме. В рамках задания добавим программу на Python

### 01. Создание файла зависимостей
* Перейдите в корень проекта и создайте файл requirements.txt:
```bash
nano requirements.txt
```
с базовым списком пакетов, которые потребуются FastAPI-приложению, например:
```text
fastapi
uvicorn[standard]
sqlalchemy
alembic
psycopg2-binary
```

### 02. Создание рабочего каталога
* В корневом каталоге создайте папку для исходного кода, выполнив команду:
```bash
mkdir src
```

### 03. Подключение к БД
* Создайте базовый скрипт для подключения к БД:
```bash
nano src/database.py
```
```python
# src/database.py
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

# Описание параметров движка БД (адрес, логин, пароль)
engine = create_engine(DATABASE_URL)
# Соединение с БД (сессия)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Это будущий родитель всех таблиц проекта
Base = declarative_base()

# Зависимость для сессии БД
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
> Этот простейший базовый скрипт легко гуглится

### 04. Создание модели данных
> Модель данных описывает таблицы проекта: столбцы, индексы, реляционные отношения

* Создайте модель данных:
```bash
nano src/models.py
```
```python
# src/models.py
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from src.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False) # Текст вопроса
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
    user_id = Column(String, nullable=False)  # UUID пользователя
    text = Column(String, nullable=False)     # Текст ответа
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    # Обратная связь к вопросу
    question = relationship(
        "Question",
        back_populates="answers"
    )
```

### 05. Создание основного модуля приложения
* Создайте основной модуль приложения. В нашем случае - это простейшее FastAPI веб-приложение:
```bash
nano src/main.py
```
```python
# src/main.py
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db

app = FastAPI(title="Тестовое задание: API-сервис для вопросов и ответов")

@app.get("/")
def read_root() -> dict:
    return {"message": "Hello, world!"}
```

### 06. Создание конфигурации контейнера приложения
* В корне проекта создайте конфигурационный файл Dockerfile:
```bash
nano Dockerfile
```
```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /opt/app/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

### 07. Подключение приложения в Docker Compose
* Обновите файл docker-compose.yml:
```yaml
services:
  db:
    # ... (оставьте как есть)

  app:
    build: .
    depends_on:
      db:
        condition: service_healthy
    environment:
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - ./:/opt/app/
    ports:
      - "8000:8000"
    command: sh -c "uvicorn src.main:app --host 0.0.0.0 --port 8000"
    restart: unless-stopped

volumes:
    # ... (тут тоже ничего не меняем)
```

## Шаг 07. Запуск и проверка работоспособности
* Запустите контейнер
```bash
docker-compose up -d --build
```
> -d запускает контейнер как службу (daemon)\
> --build пересобирает образ приложения (используйте, когда в приложении были какие-либо изменения)

* Проверьте работоспособность приложения:
```bash
curl http://localhost:8000
```
> Ответ: {"message":"Hello, world!"}
* Просмотрите Swagger-документацию приложения:
```
http://localhost:8000/docs
```
* Остановите контейнер с удалением БД
```
docker-compose down -v
```

---

## Шаг 08. Настройка миграции с помощью Alembic
> Прежде чем что-либо делать с БД, необходимо настроить инструмент, который будет отслеживать изменения в структуре таблиц. Это важно для свободной переносимости проекта на любой сервер.

### 01. Инициализация Alembic
* В корне проекта выполните команду:
```bash
docker-compose run --rm app alembic init alembic
```
> В корне проекта появится папка alembic и файл alembic.ini

### 02. Корректировка скриптов миграции под нашу задачу
* Откройте скрипт alembic/env.py и добавьте в начало:
```python
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
```
> Это позволит окружению Alembic видеть папку проекта src
* Замените переменную target_metadata и ниже добавьте чтение переменных окружения с данными о БД:
```python
from urllib.parse import quote_plus
from src.models import Base
target_metadata = Base.metadata

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

config.set_main_option("sqlalchemy.url", DATABASE_URL)
```
> Это подскажет Alembic откуда брать путь к нашей БД и познакомит с таблицами нашего проекта

### 03. Создание миграции
* Выполните команду в корне проекта
```bash
docker-compose run --rm app alembic revision --autogenerate -m "initial"
```
> После выполнения в папке alembic/versions появится новый файл с автоматически сгенерированными инструкциями для миграции

### 04. Автоматическое использование миграций
* Чтобы в будущем при запуске новых контейнеров все сохранённые миграции автоматически применялись к базе данных обновите команду в docker-compose.yml:
```yaml
# ...
command: sh -c "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"
# ...
```

---

## Шаг 09. Подготовка к использованию Pydantic

### 01. Добавление модуля
* Обновите содержимое файла requirements.txt, добавив название модуля в конец списка:
```text
pydantic
```

### 02. Подготовка файл для Pydantic-схем 
* Создайте файл схем:
```bash
nano src/schemas.py
```
```python
# src/schemas.py
"""
Pydantic-схемы для FastAPI
"""
from pydantic import BaseModel, ConfigDict, Field, field_validator
```

---

## Шаг 10. Средства анализа качества кода

### 01. Ruff - линтер для проверки качества и стиля кода
* Установите модуль:
```bash
pip install ruff
```
* Для запуска теста в корне проекта выполните команду:
```bash
ruff check src/
```

### 02. MyPy - инструмент для контроля типов
* Установите модуль:
```bash
pip install mypy
```
* В корне проекта создайте файл конфигурации pyproject.toml:
```bash
nano pyproject.toml
```
```toml
# pyproject.toml
[tool.mypy]
mypy_path = ["src"]
explicit_package_bases = true
follow_imports = "skip"
```
* Для запуска теста в корне проекта выполните команду:
```bash
mypy src/
```

---

## Шаг 11. Подготовка к тестированию Pytest

### 01. Добавление модуля
* Обновите содержимое файла requirements.txt, добавив перечисленные модули в конец списка:
```text
...
# Тестирование
pytest
pytest-cov
httpx
```

### 02. Создание каталога для тестов
* Выполните команду:
```bash
mkdir tests
```

### 03. Создание тестов
* Создайте файл:
```bash
nano tests/test_api.py
```
```python
# tests/test_api.py
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Базовая проверка доступности сервера
def test_read_root() -> None:
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello, world!"}
```

### 04. Запуск тестов ручном режиме
```bash
docker-compose run --rm -e PYTHONPATH=/opt/app app pytest tests/
```
> Важно. Проводить тесты необходимо до первого рабочего запуска контейнера. Иначе возникнет конфликт тестовой и рабочей баз данных

---

## Шаг 12. Автоматизация тестирования с помощью CI/CD
* Перейдите в ветку develop репозитория на GitHub, затем Actions → New workflow → Skip this and set up a workflow yourself
* Введите имя файла, например, CI.yml
* Добавьте план интеграции:
```text
name: CI

on:
  push:
    branches: [ develop, main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install ruff mypy fastapi sqlalchemy

      - name: Check code style locally
        run: |
          ruff check src/
          mypy src/

      - name: Run tests
        run: |
          docker compose --env-file .env.example run --rm -e PYTHONPATH=/opt/app app pytest tests/ -v
```
> Теперь при любом пуше в репозиторий будет производится тестирование поступившего кода. В случае ошибки на e-mail владельца репоизтория будет поступать уведомление о сбое

---

## Шаг 13. Настройка логирования Logging

### 01. Доработка основного скрипта
* В основной модуль src/main.py добавьте код:
```python
import logging
# ...
# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s UTC [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```
* Там же в каждый обработчик добавьте вызов логирования, например, вот так:
```python
def read_root() -> dict:
    logger.info("Запрос корневого эндпоинта")
    # ...
```

### 02. Настройки параметров логирования контейнера
* Добавьте в файл docker-compose.yml параметры:
```yaml
  app:
    build: .
    # ...
    logging:
      driver: local
      options:
        max-size: "10m"
        max-file: "5"
```
> Эти настройки предохранят контейнер от переполнения диска лог-файлами

---

## Шаг 14. Создание эндпоинтов API

### 01. Эндпоинт POST /questions/ — создать новый вопрос 
* В модуль схем src/schemas.py добавьте код, который описывает типы входных и выходных данных для вопросов:
```python
from datetime import datetime
from typing import Self


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
        if not v or (v := v.strip()) == "":
            raise ValueError(
                "Текст вопроса не может быть пустым или состоять только из пробелов"
            )
        return v


class QuestionResponse(BaseModel):
    """
    В HTTP-ответе возвращаем поля созданной записи
    """
    id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```
* В основной модуль src/main.py добавьте вызов новых модулей:
```python
from typing import Annotated

from src.models import Question
from src.schemas import QuestionCreate, QuestionResponse
```
и код эндпоинта:
```python
@app.post("/questions/", response_model=QuestionResponse)
def create_question(
    question: QuestionCreate, 
    db: Annotated[Session, Depends(get_db)]
) -> QuestionResponse:
    db_question = Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
```
* Сгенерируйте тесты для этого обработчика и сохрание в файле tests/test_api.py:
```python
# Обеспечение чистого состояния базы данных до и после каждого теста
@pytest.fixture(autouse=True)
def setup_and_teardown() -> None:
    from src.database import Base, engine
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Тест создания вопроса
def test_create_question() -> None:
    question_data = {"text": "Кто такие глокие куздры?"}
    response = client.post("/questions/", json=question_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["text"] == question_data["text"]
    assert "id" in data
    assert "created_at" in data
```

### 02. Эндпоинт GET /questions/ - список всех вопросов
* В основной модуль src/main.py добавьте код эндпоинта:
```python
@app.get("/questions/", response_model=list[QuestionResponse])
def get_questions(
    db: Annotated[Session, Depends(get_db)]
):
    return db.query(Question).all()
```
* В модуль тестирования tests/test_api.py добавьте функцию:
```python
# Тест получения списка вопросов
def test_get_questions() -> None:
    question_data = {"text": "Кто такие бокры?"}
    client.post("/questions/", json=question_data)

    response = client.get("/questions/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert any(q["text"] == question_data["text"] for q in data)
```

### 03. Эндпоинт POST /questions/{id}/answers/ — добавление ответа к вопросу
* В модуль схем src/schemas.py добавьте код, который описывает типы входных и выходных данных для ответов:
```python
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
```
* В основной модуль src/main.py импортируйте новые схемы:
```python
from src.models import Answer, # ...
from src.schemas import AnswerCreate, AnswerResponse, # ...
```
и создайте код эндпоинта:
```python
@app.post("/questions/{id}/answers/", response_model=AnswerResponse)
def create_answer(
    id: int,
    answer: AnswerCreate,
    db: Annotated[Session, Depends(get_db)]
) -> AnswerResponse:
    logger.info(f"Создание пользователем {answer.user_id} ответа \"{answer.text}\" к вопросу ID = {id}")

    db_question = db.query(Question).filter(Question.id == id).first()
    if not db_question:
        logger.info(f"Не существует вопроса с ID = {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    db_answer = Answer(
        question_id=id,
        user_id=answer.user_id,
        text=answer.text
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)

    logger.info(f"Создан ответ с ID = {db_answer.id}")
    return db_answer
```
* В модуль тестирования tests/test_api.py добавьте функцию:
```python
# Тест создания ответа к вопросу
def test_create_answer() -> None:
    question_data = {"text": "Что такое будлануть?"}
    response = client.post("/questions/", json=question_data)
    question_id = response.json()["id"]

    answer_data = {"user_id": "Будлатель", "text": "Очень напоминает слово 'поддать'."}
    response = client.post(f"/questions/{question_id}/answers/", json=answer_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["question_id"] == question_id
    assert data["user_id"] == answer_data["user_id"]
    assert data["text"] == answer_data["text"]
    assert "id" in data
    assert "created_at" in data

# Тест создания ответа к несуществующему вопросу
def test_create_answer_question_not_found() -> None:
    answer_data = {
        "user_id": "Koshka Musya",
        "text": "Я прошлась по клавиатуре и создала неверный запрос."
    }
    response = client.post("/questions/999/answers/", json=answer_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Question not found"
```

### 04. Эндпоинт GET /answers/{id}/ — получение конкретного ответа
* В основном модуле src/main.py создайте код:
```python
@app.get("/answers/{id}/", response_model=AnswerResponse)
def get_answer(
    id: int,
    db: Annotated[Session, Depends(get_db)]
) -> AnswerResponse:
    logger.info(f"Запрос ответа с ID = {id}")

    db_answer = db.query(Answer).filter(Answer.id == id).first()
    if not db_answer:
        logger.info(f"Не существует ответа с ID = {id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )

    return db_answer
```
* В модуль тестирования tests/test_api.py добавьте функцию:
```python
# Тест получения ответа по номеру
def test_get_answer() -> None:
    question_data = {"text": "Где живут куздры и бокры с бокрятами?"}
    response = client.post("/questions/", json=question_data)
    question_id = response.json()["id"]

    answer_data = {"user_id": "Мастер Йода", "text": "В таинственном мире живут они."}
    response = client.post(f"/questions/{question_id}/answers/", json=answer_data)
    answer_id = response.json()["id"]

    response = client.get(f"/answers/{answer_id}/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == answer_id
    assert data["text"] == answer_data["text"]
    assert data["user_id"] == answer_data["user_id"]

# Тест несуществующего ответа
def test_get_answer_not_found() -> None:
    response = client.get("/answers/999/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Answer not found"
```

### 05. Эндпоинт DELETE /answers/{id}/ — удаление ответа
* В основном модуле src/main.py создайте код:
```python
@app.delete("/answers/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
    id: int,
    db: Annotated[Session, Depends(get_db)]
) -> None:
    logger.info(f"Запрос на удаление ответа с ID = {id}")

    db_answer = db.query(Answer).filter(Answer.id == id).first()
    if not db_answer:
        logger.info(f"Ответ с ID = {id} не найден при попытке удаления")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found"
        )

    db.delete(db_answer)
    db.commit()

    logger.info(f"Ответ с ID = {id} успешно удалён")
    return None
```
* В модуль тестирования tests/test_api.py добавьте функцию:
```python
# Тест удаления ответа
def test_delete_answer() -> None:
    question_data = {"text": "Достал ли я код-ревьюера своими бокрами?"}
    response = client.post("/questions/", json=question_data)
    question_id = response.json()["id"]

    answer_data = {"user_id": "Код-ревьюер", "text": "Да, порядком."}
    response = client.post(f"/questions/{question_id}/answers/", json=answer_data)
    answer_id = response.json()["id"]

    response = client.delete(f"/answers/{answer_id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(f"/answers/{answer_id}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
```

### 06. Эндпоинт GET /questions/{id}/ — получение вопроса и всех его ответов
* В схемах создайте класс:
```python
class QuestionWithAnswersResponse(BaseModel):
    """
    В HTTP-ответе возвращаем вопрос и все ответы на него
    """
    id: int
    text: str
    created_at: datetime
    answers: list[AnswerResponse] = []

    model_config = ConfigDict(from_attributes=True)
```
* В основном модуле src/main.py импортируйте новую схему:
```python
from src.schemas import QuestionWithAnswersResponse
```
* и создайте код:
```python
@app.get("/questions/{id}/", response_model=QuestionWithAnswersResponse)
def get_question_with_answers(
    id: int,
    db: Annotated[Session, Depends(get_db)]
) -> QuestionWithAnswersResponse:
    logger.info(f"Запрос вопроса с ID = {id} и всех ответов")

    db_question = db.query(Question).filter(Question.id == id).first()
    if not db_question:
        logger.info(f"Вопрос с ID = {id} не найден")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    return db_question
```
* В модуль тестирования tests/test_api.py добавьте функцию:
```python
# Тест получения вопроса и его ответов
def test_get_question_with_answers() -> None:
    question_data = {"text": "Кто родственник бокрёнка?"}
    response = client.post("/questions/", json=question_data)
    question_id = response.json()["id"]

    answer_data = {"user_id": "Vitaliy Klimin", "text": "Его родоственник - бокр."}
    client.post(f"/questions/{question_id}/answers/", json=answer_data)

    response = client.get(f"/questions/{question_id}/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == question_id
    assert data["text"] == question_data["text"]
    assert len(data["answers"]) == 1
    assert data["answers"][0]["text"] == answer_data["text"]
    assert data["answers"][0]["user_id"] == answer_data["user_id"]

# Тест несуществующего вопроса
def test_get_question_not_found() -> None:
    response = client.get("/questions/999/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Question not found"
```

### 07. Эндпоинт DELETE /questions/{id}/ — удаление вопроса и связанных ответов
* В основном модуле src/main.py создайте код:
```python
@app.delete("/questions/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    id: int,
    db: Annotated[Session, Depends(get_db)]
) -> None:
    logger.info(f"Запрос на удаление вопроса с ID = {id}")

    db_question = db.query(Question).filter(Question.id == id).first()
    if not db_question:
        logger.info(f"Вопрос с ID = {id} не найден при попытке удаления")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    # Удаление связанных с вопросом ответов гарантируется
    # установленными реляционными отношениями между таблицами
    db.delete(db_question)
    db.commit()

    logger.info(f"Вопрос с ID = {id} и все связанные ответы успешно удалены")
    return None
```
* В модуль тестирования tests/test_api.py добавьте функцию:
```python
# Тест удаления вопроса
def test_delete_question() -> None:
    question_data = {"text": "Когда уже кончтся тесты?"}
    response = client.post("/questions/", json=question_data)
    question_id = response.json()["id"]

    answer_data = {"user_id": "Опять я", "text": "Скоро, терпи."}
    response = client.post(f"/questions/{question_id}/answers/", json=answer_data)
    answer_id = response.json()["id"]

    response = client.delete(f"/questions/{question_id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(f"/questions/{question_id}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.get(f"/answers/{answer_id}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
```

---
