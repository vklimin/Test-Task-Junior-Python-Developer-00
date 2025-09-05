# Test-Task-Junior-Python-Developer-00
Тестовое задание работодателя "Хайталент" на соискание должности "Junior Python разработчик"

## Требования
* Проверьте, что установлены Docker, Docker Compose, Git
## Подготовка к первому запуску
* Клонируйте репозиторий
* Скопируйте файл с примером переменных окружения:
```bash
cp .env.example .env
```
* При необходимости внесите изменения в конфиденциальные данные:
```bash
nano .env
```
## Запуск
* Выполните команду:
```bash
docker-compose up -d
```
## Использование
* API доступно по адресу:
`http://localhost:8000`
## Swagger-документация
* Документация доступна по адресу:
`http://localhost:8000/docs`
## Остановка
* Для остановки контейнера выполните команду:
```bash
docker-compose down
```
* Для остановки с удалением файлов БД выполните:
```bash
docker-compose down -v
```
## Запуск тестов
* Выполните команду:
```bash
docker-compose run --rm -e PYTHONPATH=/opt/app app pytest tests/ -v
```
* Чтобы проверить покрытие кода тестами, выполните команду:
```bash
docker-compose run --rm -e PYTHONPATH=/opt/app app pytest tests/ --cov=src
```
## Проверка стиля кода
* Выполните команды:
```bash
ruff check src/ --select ANN,B,C,E,F,I,W
```
