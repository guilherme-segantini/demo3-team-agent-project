"""Prompt service for managing and testing prompt templates.

Provides utilities for loading, validating, and testing prompt templates
used for AI-powered trend analysis.
"""

import os
from pathlib import Path
from typing import Optional


class PromptService:
    """Service for managing prompt templates."""

    def __init__(self):
        """Initialize the prompt service."""
        self.prompts_dir = Path(__file__).parent.parent.parent.parent / "prompts"
        self._templates: dict[str, str] = {}

    def load_template(self, template_name: str) -> Optional[str]:
        """Load a prompt template by name.

        Args:
            template_name: Name of the template (without .md extension).

        Returns:
            Template content or None if not found.
        """
        if template_name in self._templates:
            return self._templates[template_name]

        template_path = self.prompts_dir / f"{template_name}.md"
        if not template_path.exists():
            # Try with _prompt suffix
            template_path = self.prompts_dir / f"{template_name}_prompt.md"

        if not template_path.exists():
            return None

        try:
            with open(template_path, "r", encoding="utf-8") as f:
                content = f.read()
                self._templates[template_name] = content
                return content
        except OSError:
            return None

    def list_templates(self) -> list[str]:
        """List all available prompt templates.

        Returns:
            List of template names.
        """
        templates = []
        if self.prompts_dir.exists():
            for file in self.prompts_dir.glob("*.md"):
                name = file.stem
                if name.endswith("_prompt"):
                    name = name[:-7]  # Remove _prompt suffix
                templates.append(name)
        return sorted(templates)

    def validate_template(self, template_content: str) -> dict:
        """Validate a prompt template structure.

        Args:
            template_content: The template content to validate.

        Returns:
            Validation result with status and any errors.
        """
        errors = []
        warnings = []

        # Check for required sections
        required_sections = [
            "DISCOVER",
            "CLASSIFY",
            "SIGNAL criteria",
            "NOISE criteria",
            "Output Format",
        ]

        for section in required_sections:
            if section.lower() not in template_content.lower():
                errors.append(f"Missing required section: {section}")

        # Check for JSON output format
        if "```json" not in template_content:
            warnings.append("No JSON code block found in output format")

        # Check for focus area specific criteria
        if "Focus Area Specific" not in template_content:
            warnings.append("Missing focus area specific criteria section")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    def get_template_metadata(self, template_name: str) -> Optional[dict]:
        """Get metadata about a prompt template.

        Args:
            template_name: Name of the template.

        Returns:
            Metadata dict or None if template not found.
        """
        content = self.load_template(template_name)
        if not content:
            return None

        lines = content.split("\n")
        title = ""
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                break

        return {
            "name": template_name,
            "title": title,
            "length": len(content),
            "lines": len(lines),
            "validation": self.validate_template(content),
        }


class PromptTester:
    """Utility for testing prompt templates."""

    def __init__(self, prompt_service: Optional[PromptService] = None):
        """Initialize the prompt tester.

        Args:
            prompt_service: Optional PromptService instance.
        """
        self.prompt_service = prompt_service or PromptService()

    def test_template_syntax(self, template_name: str) -> dict:
        """Test a template for syntax issues.

        Args:
            template_name: Name of the template to test.

        Returns:
            Test results dict.
        """
        content = self.prompt_service.load_template(template_name)
        if not content:
            return {"success": False, "error": f"Template not found: {template_name}"}

        validation = self.prompt_service.validate_template(content)

        return {
            "success": validation["valid"],
            "template": template_name,
            "validation": validation,
        }

    def test_all_templates(self) -> dict:
        """Test all available templates.

        Returns:
            Test results for all templates.
        """
        results = {}
        templates = self.prompt_service.list_templates()

        for template in templates:
            results[template] = self.test_template_syntax(template)

        all_passed = all(r["success"] for r in results.values())

        return {
            "success": all_passed,
            "templates_tested": len(templates),
            "results": results,
        }

    def generate_test_input(self, focus_area: str) -> str:
        """Generate test input for a focus area prompt.

        Args:
            focus_area: The focus area to generate test input for.

        Returns:
            Sample test input string.
        """
        test_inputs = {
            "voice_ai": "Test voice AI tool with WebRTC support and 150ms latency",
            "agent_orchestration": "Test agent framework with knowledge graph integration",
            "durable_runtime": "Test serverless platform with 50ms cold start",
        }

        return test_inputs.get(focus_area, "Generic test input for trend analysis")


# Singleton instances
_prompt_service: Optional[PromptService] = None
_prompt_tester: Optional[PromptTester] = None


def get_prompt_service() -> PromptService:
    """Get the singleton PromptService instance.

    Returns:
        The PromptService instance.
    """
    global _prompt_service
    if _prompt_service is None:
        _prompt_service = PromptService()
    return _prompt_service


def get_prompt_tester() -> PromptTester:
    """Get the singleton PromptTester instance.

    Returns:
        The PromptTester instance.
    """
    global _prompt_tester
    if _prompt_tester is None:
        _prompt_tester = PromptTester()
    return _prompt_tester
