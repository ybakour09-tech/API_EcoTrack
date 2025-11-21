from fastapi.testclient import TestClient


def test_register_and_login(client: TestClient):
    payload = {
        "email": "user@example.com",
        "password": "User12345!",
        "full_name": "Test User",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["id"] > 0

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": payload["email"], "password": payload["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["token"]["access_token"]
    assert token
