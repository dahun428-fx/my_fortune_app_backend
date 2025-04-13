import logging
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

logger = logging.getLogger(__name__)


def test_fortune_with_minimal_fields():
    response = client.post(
        "/api/v1/fortune",
        json={"gender": "남성", "birth": "1990-01-01"},
    )
    logger.info("[DEBUG] 응답 결과: %s", response.json())

    assert response.status_code == 200
    assert "result" in response.json()
    assert isinstance(response.json()["result"], str)
