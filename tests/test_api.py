# tests/test_api.py
#
# Сделать тесты помогли QWEN AI и Google
#
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Обеспечение чистого состояния базы данных до и после каждого теста
@pytest.fixture(autouse=True)
def setup_and_teardown() -> None:
    from src.database import Base, engine
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Базовая проверка доступности сервера
def test_read_root() -> None:
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello, world!"}

# Тест создания вопроса
def test_create_question() -> None:
    question_data = {"text": "Кто такие глокие куздры?"}
    response = client.post("/questions/", json=question_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["text"] == question_data["text"]
    assert "id" in data
    assert "created_at" in data

# Тест получения списка вопросов
def test_get_questions() -> None:
    question_data = {"text": "Кто такие бокры?"}
    client.post("/questions/", json=question_data)

    response = client.get("/questions/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert any(q["text"] == question_data["text"] for q in data)

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

# Тест создания ответа к несуществующему вопросу
def test_create_answer_question_not_found() -> None:
    answer_data = {
        "user_id": "Koshka Musya",
        "text": "Я прошлась по клавиатуре и создала неверный запрос."
    }
    response = client.post("/questions/999/answers/", json=answer_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Question not found"

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
