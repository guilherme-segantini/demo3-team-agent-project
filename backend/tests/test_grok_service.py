"""Tests for the Grok service."""

import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.services.grok_service import GrokService, get_grok_service


class TestGrokService:
    """Tests for GrokService class."""

    def test_init_without_api_key(self):
        """Test initialization without API key."""
        with patch.dict("os.environ", {}, clear=True):
            service = GrokService()
            assert service.api_key is None
            assert not service.is_configured()

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        with patch.dict("os.environ", {"XAI_API_KEY": "test-key"}):
            service = GrokService()
            assert service.api_key == "test-key"
            assert service.is_configured()

    def test_get_available_focus_areas(self):
        """Test getting available focus areas."""
        service = GrokService()
        areas = service.get_available_focus_areas()
        assert "voice_ai_ux" in areas
        assert "agent_orchestration" in areas
        assert "durable_runtime" in areas
        assert len(areas) == 3

    def test_build_system_prompt(self):
        """Test system prompt generation."""
        service = GrokService()
        prompt = service._build_system_prompt()
        assert "AI research analyst" in prompt
        assert "SIGNAL" in prompt
        assert "NOISE" in prompt

    def test_validate_trend_valid(self):
        """Test trend validation with valid data."""
        service = GrokService()
        trend = {
            "tool_name": "TestTool",
            "classification": "signal",
            "confidence_score": 85,
            "technical_insight": "Great benchmarks",
            "signal_evidence": ["evidence1"],
            "noise_indicators": [],
            "architectural_verdict": True,
        }
        result = service._validate_trend(trend, "voice_ai_ux")
        assert result is not None
        assert result["tool_name"] == "TestTool"
        assert result["classification"] == "signal"
        assert result["confidence_score"] == 85
        assert result["focus_area"] == "voice_ai_ux"

    def test_validate_trend_missing_required_field(self):
        """Test trend validation with missing required field."""
        service = GrokService()
        trend = {"tool_name": "TestTool"}  # Missing classification
        result = service._validate_trend(trend, "voice_ai_ux")
        assert result is None

    def test_validate_trend_invalid_classification(self):
        """Test trend validation with invalid classification."""
        service = GrokService()
        trend = {
            "tool_name": "TestTool",
            "classification": "invalid",
        }
        result = service._validate_trend(trend, "voice_ai_ux")
        assert result is None

    def test_validate_trend_normalizes_classification(self):
        """Test that classification is normalized to lowercase."""
        service = GrokService()
        trend = {
            "tool_name": "TestTool",
            "classification": "SIGNAL",
            "confidence_score": 75,
        }
        result = service._validate_trend(trend, "voice_ai_ux")
        assert result is not None
        assert result["classification"] == "signal"

    def test_validate_trend_clamps_confidence_score(self):
        """Test that confidence score is clamped to valid range."""
        service = GrokService()

        # Test score above 100
        trend = {"tool_name": "Test", "classification": "signal", "confidence_score": 150}
        result = service._validate_trend(trend, "voice_ai_ux")
        assert result["confidence_score"] == 100

        # Test score below 1
        trend = {"tool_name": "Test", "classification": "signal", "confidence_score": -10}
        result = service._validate_trend(trend, "voice_ai_ux")
        assert result["confidence_score"] == 1

    def test_parse_response_valid_json(self):
        """Test parsing a valid JSON response."""
        service = GrokService()
        response = """Here are the results:
[
  {
    "tool_name": "TestTool",
    "classification": "signal",
    "confidence_score": 85,
    "technical_insight": "Good benchmarks",
    "signal_evidence": ["evidence1"],
    "noise_indicators": [],
    "architectural_verdict": true
  }
]
Additional commentary here."""
        result = service._parse_response(response, "voice_ai_ux")
        assert result["focus_area"] == "voice_ai_ux"
        assert len(result["trends"]) == 1
        assert result["trends"][0]["tool_name"] == "TestTool"

    def test_parse_response_no_json(self):
        """Test parsing a response with no JSON."""
        service = GrokService()
        response = "This response has no JSON array."
        result = service._parse_response(response, "voice_ai_ux")
        assert result["focus_area"] == "voice_ai_ux"
        assert len(result["trends"]) == 0
        assert "parse_error" in result

    def test_parse_response_invalid_json(self):
        """Test parsing a response with invalid JSON."""
        service = GrokService()
        response = "[{invalid json}]"
        result = service._parse_response(response, "voice_ai_ux")
        assert "parse_error" in result
        assert len(result["trends"]) == 0


class TestGrokServiceAsync:
    """Async tests for GrokService."""

    @pytest.mark.asyncio
    async def test_analyze_trends_no_api_key(self):
        """Test analyze_trends returns error when no API key."""
        with patch.dict("os.environ", {}, clear=True):
            service = GrokService()
            result = await service.analyze_trends("voice_ai_ux")
            assert "error" in result
            assert "not configured" in result["error"]

    @pytest.mark.asyncio
    async def test_analyze_trends_invalid_focus_area(self):
        """Test analyze_trends with invalid focus area."""
        with patch.dict("os.environ", {"XAI_API_KEY": "test-key"}):
            service = GrokService()
            result = await service.analyze_trends("invalid_area")
            assert "error" in result
            assert "Invalid focus area" in result["error"]

    @pytest.mark.asyncio
    async def test_analyze_trends_success(self):
        """Test successful analyze_trends call."""
        mock_response = """[
            {
                "tool_name": "TestTool",
                "classification": "signal",
                "confidence_score": 90,
                "technical_insight": "Great tool"
            }
        ]"""

        with patch.dict("os.environ", {"XAI_API_KEY": "test-key"}):
            service = GrokService()
            service._call_grok = AsyncMock(return_value=mock_response)

            result = await service.analyze_trends("voice_ai_ux")

            assert "error" not in result
            assert result["focus_area"] == "voice_ai_ux"
            assert len(result["trends"]) == 1

    @pytest.mark.asyncio
    async def test_analyze_trends_api_error(self):
        """Test analyze_trends handles API errors."""
        with patch.dict("os.environ", {"XAI_API_KEY": "test-key"}):
            service = GrokService()
            service._call_grok = AsyncMock(side_effect=Exception("API Error"))

            result = await service.analyze_trends("voice_ai_ux")

            assert "error" in result
            assert "API Error" in result["error"]


class TestGetGrokService:
    """Tests for get_grok_service singleton."""

    def test_get_grok_service_returns_instance(self):
        """Test that get_grok_service returns a GrokService instance."""
        # Reset the singleton
        import app.services.grok_service as module
        module._grok_service = None

        service = get_grok_service()
        assert isinstance(service, GrokService)

    def test_get_grok_service_returns_same_instance(self):
        """Test that get_grok_service returns the same instance."""
        import app.services.grok_service as module
        module._grok_service = None

        service1 = get_grok_service()
        service2 = get_grok_service()
        assert service1 is service2
