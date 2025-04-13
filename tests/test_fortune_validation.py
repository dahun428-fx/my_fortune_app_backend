from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_missing_required_fields():
    #
    # gender는 있으나 birth가 빠진 요청
    response = client.post("/api/v1/fortune", json={"gender": "남성"})

    assert response.status_code == 422
    assert response.json()["status"] == "error"
    assert response.json()["code"] == 422
    assert response.json()["message"] == "Validation failed"
    assert any(err["loc"][-1] == "birth" for err in response.json()["detail"])


def test_invalid_gender():
    # gender 값이 허용된 값이 아닐 경우
    payload = {"gender": "중성", "birth": "1990-01-01"}
    response = client.post("/api/v1/fortune", json=payload)

    assert response.status_code == 422
    assert response.json()["status"] == "error"
    assert "gender" in str(response.json()["detail"])


def test_invalid_birth_format():
    # 잘못된 생년월일 형식
    payload = {"gender": "남성", "birth": "90-01-01"}
    response = client.post("/api/v1/fortune", json=payload)

    assert response.status_code == 422
    assert any("birth" in str(err["loc"]) for err in response.json()["detail"])


def test_invalid_birth_time_format():
    # 잘못된 출생 시각 형식
    payload = {"gender": "남성", "birth": "1990-01-01", "birth_time": "1시"}
    response = client.post("/api/v1/fortune", json=payload)

    assert response.status_code == 422
    assert "birth_time" in str(response.json()["detail"])


def test_invalid_language():
    # 허용되지 않은 언어 코드
    payload = {"gender": "남성", "birth": "1990-01-01", "language": "jp"}
    response = client.post("/api/v1/fortune", json=payload)

    assert response.status_code == 422
    assert "language" in str(response.json()["detail"])
