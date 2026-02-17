"""Tests for API endpoints."""

import pytest
from tests.utils import (
    assert_valid_response,
    assert_json_structure,
    assert_radar_response
)


class TestRadarAPI:
    """Tests for the Radar API endpoints."""

    @pytest.mark.integration
    def test_get_radar_success(self, client):
        """Test successful radar retrieval."""
        response = client.get("/api/radar")
        assert_valid_response(response, 200)
        assert_radar_response(response.json())

    @pytest.mark.integration
    def test_get_radar_with_valid_date(self, client):
        """Test radar retrieval with valid date parameter.

        Note: Currently returns placeholder data. When implemented,
        this will verify the date parameter is properly used.
        """
        response = client.get("/api/radar?date=2026-02-17")
        assert_valid_response(response, 200)
        data = response.json()
        # Placeholder returns default date - will be updated when implemented
        assert "radar_date" in data

    @pytest.mark.integration
    def test_get_radar_returns_trends_list(self, client):
        """Test that radar returns a list of trends."""
        response = client.get("/api/radar")
        data = response.json()
        assert isinstance(data["trends"], list)


class TestAPIErrorHandling:
    """Tests for API error handling."""

    @pytest.mark.integration
    def test_invalid_endpoint_returns_404(self, client):
        """Test that invalid endpoints return 404."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

    @pytest.mark.integration
    def test_method_not_allowed(self, client):
        """Test that invalid methods return 405."""
        response = client.post("/")
        assert response.status_code == 405


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    @pytest.mark.integration
    def test_openapi_schema_available(self, client):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert_valid_response(response, 200)
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "CodeScale Research Radar API"

    @pytest.mark.integration
    def test_docs_endpoint(self, client):
        """Test that Swagger docs endpoint is available."""
        response = client.get("/docs")
        assert response.status_code == 200

    @pytest.mark.integration
    def test_redoc_endpoint(self, client):
        """Test that ReDoc endpoint is available."""
        response = client.get("/redoc")
        assert response.status_code == 200
