import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    # Using TestClient as a context manager triggers the FastAPI lifespan
    # (startup/shutdown) events, so the model gets loaded before each test.
    with TestClient(app) as c:
        yield c


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_happy_path(client):
    payload = {
        "location": "Sector 12, Noida",
        "carpet_area_sqft": 1200,
        "floor_num": 3,
        "bathroom": 2,
        "balcony": 1,
        "furnishing": "Semi-Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "East",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "predicted_price" in body
    assert body["predicted_price"] > 0


def test_predict_invalid_input(client):
    # carpet_area_sqft must be > 0
    payload = {
        "location": "Sector 12, Noida",
        "carpet_area_sqft": -5,
        "floor_num": 3,
        "bathroom": 2,
        "balcony": 1,
        "furnishing": "Semi-Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "East",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_unknown_location_falls_back_gracefully(client):
    payload = {
        "location": "A Totally Unknown Neighborhood, Nowhere",
        "carpet_area_sqft": 900,
        "floor_num": 1,
        "bathroom": 1,
        "balcony": 0,
        "furnishing": "Unfurnished",
        "transaction": "New Property",
        "ownership": "Freehold",
        "facing": None,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert response.json()["predicted_price"] > 0
