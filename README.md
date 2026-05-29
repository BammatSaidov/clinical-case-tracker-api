# Clinical Case Tracker API

Backend pet-project на FastAPI для управления медицинскими/стоматологическими кейсами.

Проект показывает навыки Python backend-разработки: REST API, JWT-авторизация, PostgreSQL, SQLAlchemy, Docker, тесты, Swagger и mock AI-summary без платных сервисов.

## Стек

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Pydantic
- JWT auth
- Pytest
- Docker Compose
- Mock AI provider

## Быстрый запуск через Docker

Скопируйте переменные окружения:

```bash
cp .env.example .env
```

Запустите проект:

```bash
docker compose up --build
```

API будет доступно здесь:

```text
http://localhost:8000
```

Swagger-документация:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

## Как проверить руками в Swagger

1. Откройте `http://localhost:8000/docs`.
2. Вызовите `POST /api/v1/auth/register`.
3. Вызовите `POST /api/v1/auth/login` и скопируйте `access_token`.
4. Нажмите `Authorize` в Swagger и вставьте токен в формате:

```text
Bearer your_token_here
```

5. Создайте кейс через `POST /api/v1/cases`.
6. Добавьте комментарий через `POST /api/v1/cases/{case_id}/comments`.
7. Добавьте пункт чек-листа через `POST /api/v1/cases/{case_id}/checklist`.
8. Сгенерируйте AI summary через `POST /api/v1/cases/{case_id}/ai/summary`.

## Пример пользователя

```json
{
  "email": "tech@example.com",
  "password": "password123",
  "full_name": "Test Technician",
  "role": "technician"
}
```

## Пример кейса

```json
{
  "title": "Проверка 3D модели перед ревью",
  "patient_code": "CASE-001",
  "description": "Нужно проверить качество модели, границы и готовность к передаче на ревью.",
  "priority": "high"
}
```

## Запуск тестов локально

Создайте виртуальное окружение:

```bash
python -m venv .venv
```

Активируйте его:

```bash
source .venv/bin/activate
```

На Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Запустите тесты:

```bash
pytest
```

## Основные эндпоинты

| Метод | URL | Описание |
|---|---|---|
| GET | `/health` | Проверка API |
| POST | `/api/v1/auth/register` | Регистрация |
| POST | `/api/v1/auth/login` | Логин |
| POST | `/api/v1/cases` | Создать кейс |
| GET | `/api/v1/cases` | Список кейсов |
| GET | `/api/v1/cases/{case_id}` | Получить кейс |
| PATCH | `/api/v1/cases/{case_id}` | Обновить кейс |
| DELETE | `/api/v1/cases/{case_id}` | Удалить кейс |
| POST | `/api/v1/cases/{case_id}/comments` | Добавить комментарий |
| GET | `/api/v1/cases/{case_id}/comments` | Список комментариев |
| POST | `/api/v1/cases/{case_id}/checklist` | Добавить пункт чек-листа |
| PATCH | `/api/v1/cases/{case_id}/checklist/{item_id}` | Обновить пункт чек-листа |
| POST | `/api/v1/cases/{case_id}/ai/summary` | Сгенерировать mock AI-summary |

## Что можно улучшить следующим этапом

- Добавить Alembic-миграции.
- Добавить роли и ограничения доступа.
- Подключить frontend на React.
- Добавить GitHub Actions.
- Добавить реальный AI provider через Ollama или внешний API.
- Добавить загрузку файлов STL/OBJ как metadata без хранения персональных данных.
