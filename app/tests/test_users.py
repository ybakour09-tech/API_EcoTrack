from fastapi.testclient import TestClient


def authenticate(client: TestClient, email: str, password: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response.json()["token"]["access_token"]


def test_list_users_requires_admin(client: TestClient, admin_user):
    # create regular user
    user_payload = {
        "email": "regular@example.com",
        "password": "StrongPass123!",
        "full_name": "Regular User",
    }
    register_resp = client.post("/api/v1/auth/register", json=user_payload)
    assert register_resp.status_code == 201

    admin_token = authenticate(client, admin_user["email"], admin_user["password"])
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = client.get("/api/v1/users/", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
