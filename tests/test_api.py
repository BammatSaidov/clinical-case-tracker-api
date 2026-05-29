import os

os.environ["DATABASE_URL"] = "sqlite:///./test_clinical_cases.db"
os.environ["SECRET_KEY"] = "test-secret"

from fastapi.testclient import TestClient  # noqa: E402

from app.db.base import Base  # noqa: E402
from app.db.session import engine  # noqa: E402
from app.main import app  # noqa: E402


def setup_function() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def auth_headers(client: TestClient) -> dict[str, str]:
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "tech@example.com",
            "password": "password123",
            "full_name": "Test Technician",
            "role": "technician",
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "tech@example.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_health_check() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_login_create_case_and_generate_summary() -> None:
    with TestClient(app) as client:
        headers = auth_headers(client)

        case_response = client.post(
            "/api/v1/cases",
            headers=headers,
            json={
                "title": "Проверка 3D модели",
                "patient_code": "CASE-001",
                "description": "Нужно проверить качество модели перед передачей на ревью.",
                "priority": "high",
            },
        )
        assert case_response.status_code == 201
        case_id = case_response.json()["id"]

        comment_response = client.post(
            f"/api/v1/cases/{case_id}/comments",
            headers=headers,
            json={"text": "Есть подозрение на дефект границы."},
        )
        assert comment_response.status_code == 201

        checklist_response = client.post(
            f"/api/v1/cases/{case_id}/checklist",
            headers=headers,
            json={"title": "Проверить границы модели"},
        )
        assert checklist_response.status_code == 201

        summary_response = client.post(f"/api/v1/cases/{case_id}/ai/summary", headers=headers)
        assert summary_response.status_code == 201
        assert "Краткая сводка" in summary_response.json()["summary"]


def test_update_case_status_creates_history_record() -> None:
    with TestClient(app) as client:
        headers = auth_headers(client)
        case_response = client.post(
            "/api/v1/cases",
            headers=headers,
            json={
                "title": "Кейс для смены статуса",
                "description": "Достаточно длинное описание тестового кейса.",
            },
        )
        case_id = case_response.json()["id"]

        update_response = client.patch(
            f"/api/v1/cases/{case_id}",
            headers=headers,
            json={"status": "needs_review"},
        )
        assert update_response.status_code == 200
        assert update_response.json()["status"] == "needs_review"

        history_response = client.get(f"/api/v1/cases/{case_id}/status-history", headers=headers)
        assert history_response.status_code == 200
        assert len(history_response.json()) == 2
