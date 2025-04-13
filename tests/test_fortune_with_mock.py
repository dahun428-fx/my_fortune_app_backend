import logging
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

logger = logging.getLogger(__name__)


@patch("app.services.fortune_service.get_fortune_llm_answer")
def test_fortune_with_minimal_fields(mock_llm):
    mock_llm.return_value = "기본 정보만으로도 충분한 운세를 제공할 수 있습니다."

    response = client.post(
        "/api/v1/fortune",
        json={"gender": "남성", "birth": "1990-01-01"},
    )
    logging.info("[DEBUG] 응답 결과: %s", response.json())

    assert response.status_code == 200
    assert "result" in response.json()
    assert isinstance(response.json()["result"], str)


@patch("app.services.fortune_service.get_fortune_llm_answer")
def test_missing_required_fields(mock_llm):
    response = client.post("/api/v1/fortune", json={"gender": "남성"})

    assert response.status_code == 422
    assert response.json()["status"] == "error"
    assert response.json()["code"] == 422
    assert response.json()["message"] == "Validation failed"
    assert any(err["loc"][-1] == "birth" for err in response.json()["detail"])


@patch("app.services.fortune_service.get_fortune_llm_answer")
def test_invalid_gender(mock_llm):
    payload = {"gender": "중성", "birth": "1990-01-01"}
    response = client.post("/api/v1/fortune", json=payload)

    assert response.status_code == 422
    assert response.json()["status"] == "error"
    assert "gender" in str(response.json()["detail"])


@patch("app.services.fortune_service.get_fortune_llm_answer")
def test_invalid_birth_format(mock_llm):
    payload = {"gender": "남성", "birth": "90-01-01"}
    response = client.post("/api/v1/fortune", json=payload)

    assert response.status_code == 422
    assert any("birth" in str(err["loc"]) for err in response.json()["detail"])


@patch("app.services.fortune_service.get_fortune_llm_answer")
def test_invalid_birth_time_format(mock_llm):
    payload = {"gender": "남성", "birth": "1990-01-01", "birth_time": "1시"}
    response = client.post("/api/v1/fortune", json=payload)

    assert response.status_code == 422
    assert "birth_time" in str(response.json()["detail"])


@patch("app.services.fortune_service.get_fortune_llm_answer")
def test_invalid_language(mock_llm):
    payload = {"gender": "남성", "birth": "1990-01-01", "language": "jp"}
    response = client.post("/api/v1/fortune", json=payload)

    assert response.status_code == 422
    assert "language" in str(response.json()["detail"])


@patch("app.services.fortune_service.get_fortune_llm_answer")
def test_fortune_korean(mock_llm):
    mock_llm.return_value = "홍길동님의 연애운은 매우 좋습니다."

    response = client.post(
        "/api/v1/fortune",
        json={
            "name": "홍길동",
            "gender": "남성",
            "birth": "1990-01-01",
            "birth_time": "13:00",
            "calendar_type": "solar",
            "topic": "연애운",
        },
    )
    assert response.status_code == 200
    logging.info("[Korean Response] %s", response.json())
    assert response.json()["result"] == "홍길동님의 연애운은 매우 좋습니다."


@patch("app.services.fortune_service.get_fortune_llm_answer")
def test_fortune_english(mock_llm):
    mock_llm.return_value = "John Doe's love fortune is very positive."

    response = client.post(
        "/api/v1/fortune",
        json={
            "name": "John Doe",
            "gender": "남성",
            "birth": "1990-01-01",
            "birth_time": "13:00",
            "calendar_type": "solar",
            "topic": "love",
            "language": "en",
        },
    )
    assert response.status_code == 200
    logging.info("[English Response] %s", response.json())
    assert response.json()["result"] == "John Doe's love fortune is very positive."
