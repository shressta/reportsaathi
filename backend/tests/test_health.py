import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    json_data = response.json()
    assert "medicines_count" in json_data
    # Count should be integer >=0
    assert isinstance(json_data["medicines_count"], int)
    assert json_data["medicines_count"] >= 0
