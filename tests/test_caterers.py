# tests/test_caterers.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_list_caterers():
    r = client.get("/api/caterers")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 4


def test_get_caterer_detail():
    r = client.get("/api/caterers/1")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == 1
    assert "menu" in data
    assert "description" in data


def test_get_caterer_not_found():
    r = client.get("/api/caterers/9999")
    assert r.status_code == 404


def test_filter_by_cuisine():
    r = client.get("/api/caterers?cuisine=Telugu")
    assert r.status_code == 200
    data = r.json()
    assert all(
        any("telugu" in c.lower() for c in item["cuisines"])
        for item in data
    )


def test_filter_verified():
    r = client.get("/api/caterers?verified=true")
    assert r.status_code == 200
    assert all(item["verified"] for item in r.json())


def test_create_inquiry():
    r = client.post("/api/inquiries", json={
        "caterer_id": 1,
        "name": "Test User",
        "email": "test@example.com",
        "phone": "+1 408 000 0000",
        "notes": "Vegetarian, live dosa please",
        "event_type": "Engagement",
        "guest_count": 150,
        "budget": "$2500",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["status"] == "pending"
    assert data["id"] == 1


def test_inquiry_caterer_not_found():
    r = client.post("/api/inquiries", json={
        "caterer_id": 9999,
        "name": "Ghost",
        "email": "ghost@example.com",
    })
    assert r.status_code == 404


def test_event_types():
    r = client.get("/api/events/types")
    assert r.status_code == 200
    assert len(r.json()) > 0
