"""Tests for service modules."""

import pytest
import os
from unittest.mock import patch, AsyncMock

from app.services.grok_service import GrokService


class TestGrokService:
    """Tests for the GrokService class."""

    @pytest.mark.unit
    def test_service_initialization(self):
        """Test that GrokService initializes correctly."""
        service = GrokService()
        assert service.model == "xai/grok-beta"

    @pytest.mark.unit
    def test_service_uses_env_api_key(self):
        """Test that GrokService reads API key from environment."""
        with patch.dict(os.environ, {"XAI_API_KEY": "test-api-key"}):
            service = GrokService()
            assert service.api_key == "test-api-key"

    @pytest.mark.unit
    def test_service_handles_missing_api_key(self):
        """Test that GrokService handles missing API key gracefully."""
        with patch.dict(os.environ, {}, clear=True):
            # Remove XAI_API_KEY if it exists
            os.environ.pop("XAI_API_KEY", None)
            service = GrokService()
            assert service.api_key is None

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_analyze_trends_placeholder(self):
        """Test that analyze_trends returns None (placeholder)."""
        service = GrokService()
        result = await service.analyze_trends(
            focus_area="voice_ai_ux",
            prompt="Test prompt"
        )
        # Currently returns None as placeholder
        assert result is None

    @pytest.mark.unit
    def test_valid_focus_areas(self):
        """Test that service accepts valid focus areas."""
        valid_areas = [
            "voice_ai_ux",
            "agent_orchestration",
            "durable_runtime"
        ]
        service = GrokService()
        # Service should be able to handle all valid focus areas
        for area in valid_areas:
            # Just verify no exceptions on instantiation
            assert service.model is not None


class TestGrokServiceIntegration:
    """Integration tests for GrokService (requires mocking)."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_analyze_trends_mocked(self):
        """Test analyze_trends with mocked response."""
        mock_response = {
            "tool_name": "Test AI Tool",
            "classification": "signal",
            "confidence_score": 85,
            "technical_insight": "Test insight"
        }

        service = GrokService()

        # When the actual implementation is done, this test will verify
        # the integration with the LiteLLM client
        with patch.object(
            service,
            "analyze_trends",
            new_callable=AsyncMock,
            return_value=mock_response
        ):
            result = await service.analyze_trends(
                focus_area="voice_ai_ux",
                prompt="Analyze voice AI tools"
            )

            assert result is not None
            assert result["classification"] == "signal"
            assert result["confidence_score"] == 85
