# Clinical Case Tracker API

![Tests](https://github.com/BammatSaidov/clinical-case-tracker-api/actions/workflows/tests.yml/badge.svg)

FastAPI backend project for managing clinical and dental laboratory cases.

The project demonstrates practical Python backend development skills: REST API design, JWT authentication, PostgreSQL, SQLAlchemy ORM, Docker, Swagger documentation, testing, status history tracking, checklists, comments and mock AI summaries without paid external services.

## Project Overview

Clinical Case Tracker API is a backend service for managing clinical or dental case workflows.

A user can create a case, add comments, maintain a checklist, update case status and generate a short AI-style summary based on the case data. The AI summary currently uses a mock provider, so the project can be launched for free without API keys or paid cloud services.

This project is designed as a portfolio backend API and can be extended with a frontend, real AI provider, file uploads and role-based access control.

## Tech Stack

* Python 3.12
* FastAPI
* PostgreSQL
* SQLAlchemy 2.0
* Pydantic
* JWT authentication
* Pytest
* Docker
* Docker Compose
* Swagger / OpenAPI
* Mock AI provider

## Features

* User registration
* JWT-based authentication
* Clinical case CRUD
* Case status workflow
* Status history tracking
* Comments for each case
* Checklist items for case review
* Mock AI summary generation
* Filtering and searching cases
* PostgreSQL database
* Docker-based local setup
* Swagger API documentation
* Basic automated tests

## Case Workflow

Available case statuses:

```text
new → in_progress → needs_review → done
```

A case can also be marked as:

```text
rejected
```

Every status change is saved in the status history table. This makes it possible to track how a case moved through the workflow.

## Project Structure

```text
clinical-case-tracker-api/
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   └── routes/
│   │       ├── ai.py
│   │       ├── auth.py
│   │       ├── cases.py
│   │       ├── checklists.py
│   │       ├── comments.py
│   │       └── health.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   │   └── ai/
│   │       ├── base.py
│   │       ├── mock_provider.py
│   │       └── provider.py
│   └── main.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start with Docker

Clone the repository:

```bash
git clone https://github.com/BammatSaidov/clinical-case-tracker-api.git
cd clinical-case-tracker-api
```

Create an environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
copy .env.example .env
```

Run the project:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

Expected health check response:

```json
{
  "status": "ok"
}
```

## How to Test the API in Swagger

Open Swagger:

```text
http://localhost:8000/docs
```

### 1. Register a user

Endpoint:

```text
POST /api/v1/auth/register
```

Example request:

```json
{
  "email": "tech@example.com",
  "password": "password123",
  "full_name": "Test Technician",
  "role": "technician"
}
```

### 2. Authorize in Swagger

Click the `Authorize` button and use:

```text
username: tech@example.com
password: password123
```

Swagger will automatically receive and use the JWT access token.

### 3. Create a clinical case

Endpoint:

```text
POST /api/v1/cases
```

Example request:

```json
{
  "title": "Проверка 3D модели перед ревью",
  "patient_code": "CASE-001",
  "description": "Нужно проверить качество модели, границы и готовность к передаче на ревью.",
  "priority": "high"
}
```

### 4. Add a comment

Endpoint:

```text
POST /api/v1/cases/{case_id}/comments
```

Example request:

```json
{
  "text": "При первичной проверке нужно обратить внимание на качество границ и отсутствие дефектов модели."
}
```

### 5. Add checklist items

Endpoint:

```text
POST /api/v1/cases/{case_id}/checklist
```

Example request:

```json
{
  "title": "Проверить качество границ модели"
}
```

### 6. Generate mock AI summary

Endpoint:

```text
POST /api/v1/cases/{case_id}/ai/summary
```

The summary is generated using a mock AI provider. No external AI API key is required.

## Main API Endpoints

| Method | URL                                           | Description                 |
| ------ | --------------------------------------------- | --------------------------- |
| GET    | `/health`                                     | Health check                |
| POST   | `/api/v1/auth/register`                       | Register user               |
| POST   | `/api/v1/auth/login`                          | Login and receive JWT token |
| POST   | `/api/v1/cases`                               | Create case                 |
| GET    | `/api/v1/cases`                               | List cases                  |
| GET    | `/api/v1/cases/{case_id}`                     | Get case by ID              |
| PATCH  | `/api/v1/cases/{case_id}`                     | Update case                 |
| DELETE | `/api/v1/cases/{case_id}`                     | Delete case                 |
| GET    | `/api/v1/cases/{case_id}/status-history`      | Get case status history     |
| POST   | `/api/v1/cases/{case_id}/comments`            | Add comment                 |
| GET    | `/api/v1/cases/{case_id}/comments`            | List comments               |
| POST   | `/api/v1/cases/{case_id}/checklist`           | Add checklist item          |
| PATCH  | `/api/v1/cases/{case_id}/checklist/{item_id}` | Update checklist item       |
| POST   | `/api/v1/cases/{case_id}/ai/summary`          | Generate mock AI summary    |
| GET    | `/api/v1/cases/{case_id}/ai/summaries`        | List generated summaries    |

## Mock AI Provider

The project includes a mock AI provider by default.

This approach keeps the project free and easy to run locally. The AI provider is isolated in a separate service layer, so it can later be replaced with:

* Ollama local model
* OpenAI API
* GigaChat
* YandexGPT
* any other LLM provider

Current default provider:

```text
AI_PROVIDER=mock
```

## Running Tests

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest
```

## Environment Variables

Use `.env.example` as a template.

Example:

```text
PROJECT_NAME=Clinical Case Tracker API
API_V1_PREFIX=/api/v1
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/clinical_cases
SECRET_KEY=change-me
ACCESS_TOKEN_EXPIRE_MINUTES=10080
AI_PROVIDER=mock
```

The real `.env` file is ignored by Git and should not be committed.

## Roadmap

Planned improvements:

* Add Alembic database migrations
* Add role-based permissions
* Add GitHub Actions CI
* Add more automated tests
* Add React frontend
* Add real AI provider integration
* Add file metadata for STL/OBJ models without storing personal data
* Add pagination metadata for list endpoints

## Portfolio Notes

This project was built as a backend portfolio project focused on a medical/dental workflow domain.

It demonstrates:

* API design with FastAPI
* relational database modeling
* authentication and protected endpoints
* business workflow modeling
* status history audit trail
* clean project structure
* Dockerized local development
* extensible service layer for AI providers
