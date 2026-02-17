"""Tests for the main FastAPI application."""

import pytest

from tests.utils import assert_valid_response, assert_json_structure


class TestHealthCheck:
    """Tests for the health check endpoint."""

    @pytest.mark.unit
    def test_root_endpoint_returns_healthy(self, client):
        """Test the health check endpoint returns healthy status."""
        response = client.get("/")
        assert_valid_response(response, 200)
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "CodeScale Research Radar API"

    @pytest.mark.unit
    def test_root_endpoint_json_structure(self, client):
        """Test the health check response has required fields."""
        response = client.get("/")
        data = response.json()
        assert_json_structure(data, ["status", "service"])


class TestRadarEndpoint:
    """Tests for the radar API endpoint."""

    @pytest.mark.integration
    def test_radar_endpoint_returns_valid_structure(self, client):
        """Test the radar endpoint returns valid structure."""
        response = client.get("/api/radar")
        assert_valid_response(response, 200)
        data = response.json()
        assert "radar_date" in data
        assert "trends" in data
        assert isinstance(data["trends"], list)

    @pytest.mark.integration
    def test_radar_endpoint_with_date_parameter(self, client):
        """Test the radar endpoint accepts date parameter.

        Note: Placeholder currently returns default date.
        """
        response = client.get("/api/radar?date=2026-02-17")
        assert_valid_response(response, 200)
        data = response.json()
        # Placeholder returns default date - will be updated when implemented
        assert "radar_date" in data

    @pytest.mark.integration
    def test_radar_endpoint_default_date(self, client):
        """Test the radar endpoint returns default date when not specified."""
        response = client.get("/api/radar")
        assert_valid_response(response, 200)
        data = response.json()
        assert data["radar_date"] is not None


class TestCORS:
    """Tests for CORS configuration."""

    @pytest.mark.unit
    def test_cors_allows_localhost(self, client):
        """Test that CORS allows requests from localhost:8080."""
        response = client.options(
            "/",
            headers={
                "Origin": "http://localhost:8080",
                "Access-Control-Request-Method": "GET"
            }
        )
        assert response.headers.get("access-control-allow-origin") == "http://localhost:8080"
