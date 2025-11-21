from datetime import datetime, timezone

from fastapi.testclient import TestClient


def authenticate(client: TestClient, email: str, password: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    return response.json()["token"]["access_token"]


def test_indicator_flow(client: TestClient, admin_user):
    token = authenticate(client, admin_user["email"], admin_user["password"])
    headers = {"Authorization": f"Bearer {token}"}

    zone_payload = {"name": "Zone Test", "postal_code": "75000"}
    zone_resp = client.post("/api/v1/zones/", json=zone_payload, headers=headers)
    assert zone_resp.status_code == 201
    zone_id = zone_resp.json()["id"]

    source_payload = {"name": "Sensor A", "url": "https://example.com"}
    source_resp = client.post("/api/v1/sources/", json=source_payload, headers=headers)
    assert source_resp.status_code == 201
    source_id = source_resp.json()["id"]

    indicator_payload = {
        "type": "pm25",
        "value": 12.5,
        "unit": "µg/m3",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "zone_id": zone_id,
        "source_id": source_id,
    }
    indicator_resp = client.post("/api/v1/indicators/", json=indicator_payload, headers=headers)
    assert indicator_resp.status_code == 201

    list_resp = client.get("/api/v1/indicators?indicator_type=pm25", headers=headers)
    assert list_resp.status_code == 200
    payload = list_resp.json()
    assert payload["total"] == 1
    assert payload["items"][0]["type"] == "pm25"
