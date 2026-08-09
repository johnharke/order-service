from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_version():
    response = client.get("/version")

    assert response.status_code == 200
    assert "version" in response.json()


def test_create_order():
    response = client.post(
        "/orders",
        json={
            "customer": "John",
            "amount": 42.50
        }
    )

    assert response.status_code == 200
    assert response.json()["customer"] == "John"