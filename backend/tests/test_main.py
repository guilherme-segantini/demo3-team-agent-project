"""Tests for the main FastAPI application."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "CodeScale Research Radar API"


def test_radar_endpoint(client):
    """Test the radar endpoint returns valid structure."""
    response = client.get("/api/radar")
    assert response.status_code == 200
    data = response.json()
    assert "radar_date" in data
    assert "trends" in data
    assert isinstance(data["trends"], list)
