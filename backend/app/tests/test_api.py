import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_financials():
    response = client.get("/v1/financials/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "AAPL"
    assert "revenue_growth" in data
    assert len(data["quarterly_index"]) > 0

def test_get_drift():
    response = client.get("/v1/drift/NVDA")
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "NVDA"
    assert "drift_score" in data
    assert "explanation" in data
