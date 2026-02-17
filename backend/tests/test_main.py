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


def test_radar_endpoint_empty(client):
    """Test the radar endpoint with empty database."""
    response = client.get("/api/radar")
    assert response.status_code == 200
    data = response.json()
    assert data["radar_date"] is None
    assert data["trends"] == []


def test_radar_endpoint_with_data(client, seeded_db):
    """Test the radar endpoint returns valid structure with data."""
    response = client.get("/api/radar")
    assert response.status_code == 200
    data = response.json()
    assert data["radar_date"] == "2026-01-30"
    assert isinstance(data["trends"], list)
    assert len(data["trends"]) == 2


def test_radar_endpoint_with_date_filter(client, seeded_db):
    """Test the radar endpoint with date filter."""
    response = client.get("/api/radar?date=2026-01-30")
    assert response.status_code == 200
    data = response.json()
    assert data["radar_date"] == "2026-01-30"
    assert len(data["trends"]) == 2


def test_radar_endpoint_with_nonexistent_date(client, seeded_db):
    """Test the radar endpoint with non-existent date."""
    response = client.get("/api/radar?date=2025-01-01")
    assert response.status_code == 200
    data = response.json()
    assert data["radar_date"] == "2025-01-01"
    assert data["trends"] == []


def test_radar_trend_structure(client, seeded_db):
    """Test that returned trends have the Golden Contract structure."""
    response = client.get("/api/radar")
    data = response.json()
    trend = data["trends"][0]

    # Verify Golden Contract fields
    assert "focus_area" in trend
    assert "tool_name" in trend
    assert "classification" in trend
    assert trend["classification"] in ["signal", "noise"]
    assert "confidence_score" in trend
    assert isinstance(trend["confidence_score"], int)
    assert "technical_insight" in trend
    assert "signal_evidence" in trend
    assert isinstance(trend["signal_evidence"], list)
    assert "noise_indicators" in trend
    assert isinstance(trend["noise_indicators"], list)
    assert "architectural_verdict" in trend
    assert isinstance(trend["architectural_verdict"], bool)
    assert "timestamp" in trend
