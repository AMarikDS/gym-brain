from unittest.mock import patch

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.api.endpoints.ml_service")
def test_recommend_endpoint(mock_ml_service):
    # Setup mock return value
    mock_ml_service.recommend.return_value = [
        {
            "exercise_name": "Bench Press",
            "exercise_id": 324,
            "final_score": 0.95,
            "bert_score": 0.88,
            "equipment": "Barbell",
        }
    ]

    payload = {
        "history_ids": [10, 20],
        "profile": {
            "sex": "Male",
            "age": 25.0,
            "bw": 80.0,
            "level": "Intermediate",
            "goal": "Bodybuilding",
            "equipment": "All (Gym Mixed)",
            "sbd": [100.0, 80.0, 120.0],
        },
        "top_k": 5,
    }

    response = client.post("/api/v1/recommend", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) == 1
    assert data["recommendations"][0]["exercise_name"] == "Bench Press"

    # Ensure our mock was called correctly
    mock_ml_service.recommend.assert_called_once()


@patch("app.api.endpoints.ml_service")
def test_predict_weight_endpoint(mock_ml_service):
    # Setup mock return value
    mock_ml_service.predict_weight.return_value = (60.0, 10)

    payload = {
        "profile": {
            "sex": "Male",
            "age": 25.0,
            "bw": 80.0,
            "level": "Intermediate",
            "goal": "Bodybuilding",
            "equipment": "All (Gym Mixed)",
            "sbd": [100.0, 80.0, 120.0],
        },
        "exercise_name": "Bench Press",
        "base_lift": "Bench",
        "raw_equipment": "Barbell",
    }

    response = client.post("/api/v1/predict_weight", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "weight" in data
    assert "reps" in data
    assert data["weight"] == 60.0
    assert data["reps"] == 10

    mock_ml_service.predict_weight.assert_called_once()
