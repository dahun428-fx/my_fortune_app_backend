from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_fortune():
    response = client.post("/api/v1/fortune", json={
        "name": "홍길동",
        "gender": "남성",
        "birth": "1990-01-01",
        "birth_time": "13:00",
        "calendar_type": "solar",
        "topic": "연애운"
    })
    assert response.status_code == 200
    assert "result" in response.json()
