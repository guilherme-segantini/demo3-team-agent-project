"""Tests for the Prompt service."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.services.prompt_service import (
    PromptService,
    PromptTester,
    get_prompt_service,
    get_prompt_tester,
)


class TestPromptService:
    """Tests for PromptService class."""

    def test_list_templates(self):
        """Test listing available templates."""
        service = PromptService()
        templates = service.list_templates()
        # Should find the existing prompt templates
        assert isinstance(templates, list)
        # Check for expected templates (without _prompt suffix)
        expected = ["agent_orchestration", "durable_runtime", "voice_ai"]
        for template in expected:
            assert template in templates, f"Expected template {template} not found"

    def test_load_template_existing(self):
        """Test loading an existing template."""
        service = PromptService()
        content = service.load_template("voice_ai")
        assert content is not None
        assert "Voice AI" in content
        assert "DISCOVER" in content

    def test_load_template_nonexistent(self):
        """Test loading a non-existent template."""
        service = PromptService()
        content = service.load_template("nonexistent_template")
        assert content is None

    def test_load_template_caching(self):
        """Test that templates are cached after first load."""
        service = PromptService()
        content1 = service.load_template("voice_ai")
        content2 = service.load_template("voice_ai")
        assert content1 == content2
        assert "voice_ai" in service._templates

    def test_validate_template_valid(self):
        """Test validation of a valid template."""
        service = PromptService()
        content = service.load_template("voice_ai")
        result = service.validate_template(content)
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_validate_template_missing_sections(self):
        """Test validation detects missing sections."""
        service = PromptService()
        content = "# Test Template\nSome content without required sections"
        result = service.validate_template(content)
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        # Should report missing required sections
        assert any("DISCOVER" in error for error in result["errors"])

    def test_validate_template_warnings(self):
        """Test validation generates warnings for missing optional content."""
        service = PromptService()
        content = """# Test
## STEP 1 - DISCOVER
## STEP 2 - CLASSIFY
### SIGNAL criteria
### NOISE criteria
## Output Format
No JSON block here
"""
        result = service.validate_template(content)
        # Should have warnings about missing JSON block
        assert len(result["warnings"]) > 0

    def test_get_template_metadata(self):
        """Test getting template metadata."""
        service = PromptService()
        metadata = service.get_template_metadata("voice_ai")
        assert metadata is not None
        assert metadata["name"] == "voice_ai"
        assert "title" in metadata
        assert "length" in metadata
        assert "lines" in metadata
        assert "validation" in metadata

    def test_get_template_metadata_nonexistent(self):
        """Test getting metadata for non-existent template."""
        service = PromptService()
        metadata = service.get_template_metadata("nonexistent")
        assert metadata is None


class TestPromptTester:
    """Tests for PromptTester class."""

    def test_test_template_syntax_valid(self):
        """Test syntax testing of a valid template."""
        tester = PromptTester()
        result = tester.test_template_syntax("voice_ai")
        assert result["success"] is True
        assert result["template"] == "voice_ai"

    def test_test_template_syntax_nonexistent(self):
        """Test syntax testing of non-existent template."""
        tester = PromptTester()
        result = tester.test_template_syntax("nonexistent")
        assert result["success"] is False
        assert "error" in result

    def test_test_all_templates(self):
        """Test testing all templates."""
        tester = PromptTester()
        result = tester.test_all_templates()
        assert "success" in result
        assert "templates_tested" in result
        assert result["templates_tested"] > 0
        assert "results" in result

    def test_generate_test_input(self):
        """Test generating test input for focus areas."""
        tester = PromptTester()

        voice_input = tester.generate_test_input("voice_ai")
        assert "voice" in voice_input.lower() or "latency" in voice_input.lower()

        agent_input = tester.generate_test_input("agent_orchestration")
        assert "agent" in agent_input.lower() or "knowledge" in agent_input.lower()

        durable_input = tester.generate_test_input("durable_runtime")
        assert "serverless" in durable_input.lower() or "cold start" in durable_input.lower()

        # Unknown focus area should return generic input
        unknown_input = tester.generate_test_input("unknown")
        assert "trend" in unknown_input.lower() or "test" in unknown_input.lower()


class TestSingletons:
    """Tests for singleton accessor functions."""

    def test_get_prompt_service_returns_instance(self):
        """Test that get_prompt_service returns a PromptService."""
        import app.services.prompt_service as module
        module._prompt_service = None

        service = get_prompt_service()
        assert isinstance(service, PromptService)

    def test_get_prompt_service_singleton(self):
        """Test that get_prompt_service returns same instance."""
        import app.services.prompt_service as module
        module._prompt_service = None

        service1 = get_prompt_service()
        service2 = get_prompt_service()
        assert service1 is service2

    def test_get_prompt_tester_returns_instance(self):
        """Test that get_prompt_tester returns a PromptTester."""
        import app.services.prompt_service as module
        module._prompt_tester = None

        tester = get_prompt_tester()
        assert isinstance(tester, PromptTester)

    def test_get_prompt_tester_singleton(self):
        """Test that get_prompt_tester returns same instance."""
        import app.services.prompt_service as module
        module._prompt_tester = None

        tester1 = get_prompt_tester()
        tester2 = get_prompt_tester()
        assert tester1 is tester2
