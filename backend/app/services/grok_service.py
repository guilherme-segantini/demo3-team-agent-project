"""Grok AI service for trend discovery and classification.

Implements LiteLLM integration with xAI/Grok API for analyzing
technology trends and classifying them as Signal or Noise.
"""

import json
import os
from pathlib import Path
from typing import Optional

import litellm
from litellm import completion


class GrokService:
    """Service for interacting with Grok AI via LiteLLM."""

    FOCUS_AREAS = ["voice_ai_ux", "agent_orchestration", "durable_runtime"]

    def __init__(self):
        """Initialize the Grok service."""
        self.api_key = os.getenv("XAI_API_KEY")
        self.model = "xai/grok-beta"
        self._prompt_cache: dict[str, str] = {}

        # Configure LiteLLM
        if self.api_key:
            litellm.xai_key = self.api_key

    def _load_prompt_template(self, focus_area: str) -> Optional[str]:
        """Load a prompt template from the prompts directory.

        Args:
            focus_area: One of voice_ai_ux, agent_orchestration, durable_runtime

        Returns:
            The prompt template content or None if not found.
        """
        if focus_area in self._prompt_cache:
            return self._prompt_cache[focus_area]

        prompt_mapping = {
            "voice_ai_ux": "voice_ai_prompt.md",
            "agent_orchestration": "agent_orchestration_prompt.md",
            "durable_runtime": "durable_runtime_prompt.md",
        }

        if focus_area not in prompt_mapping:
            return None

        # Get the prompts directory path (relative to this file)
        prompts_dir = Path(__file__).parent.parent.parent.parent / "prompts"
        prompt_path = prompts_dir / prompt_mapping[focus_area]

        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                content = f.read()
                self._prompt_cache[focus_area] = content
                return content
        except FileNotFoundError:
            return None

    def _build_system_prompt(self) -> str:
        """Build the system prompt for Grok.

        Returns:
            The system prompt string.
        """
        return """You are an AI research analyst specializing in emerging technology trends.
Your task is to discover and classify technology tools as either SIGNAL (worth evaluating)
or NOISE (hype without substance).

When analyzing tools, focus on:
1. Concrete technical specifications and benchmarks
2. Real-world production usage evidence
3. Active technical community engagement
4. Architectural implementation details

Always provide structured JSON output matching the specified format."""

    async def analyze_trends(self, focus_area: str, custom_prompt: Optional[str] = None) -> Optional[dict]:
        """Analyze trends for a focus area using Grok.

        Args:
            focus_area: One of voice_ai_ux, agent_orchestration, durable_runtime
            custom_prompt: Optional custom prompt to override the template

        Returns:
            Analysis results or None if API call fails.
        """
        if not self.api_key:
            return {"error": "XAI_API_KEY not configured", "trends": []}

        if focus_area not in self.FOCUS_AREAS:
            return {"error": f"Invalid focus area: {focus_area}", "trends": []}

        # Load the prompt template or use custom prompt
        prompt = custom_prompt or self._load_prompt_template(focus_area)
        if not prompt:
            return {"error": f"Prompt template not found for {focus_area}", "trends": []}

        try:
            response = await self._call_grok(prompt)
            return self._parse_response(response, focus_area)
        except Exception as e:
            return {"error": str(e), "trends": []}

    async def _call_grok(self, prompt: str) -> str:
        """Make an API call to Grok via LiteLLM.

        Args:
            prompt: The user prompt to send.

        Returns:
            The response content from Grok.

        Raises:
            Exception: If the API call fails.
        """
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": prompt},
        ]

        response = await litellm.acompletion(
            model=self.model,
            messages=messages,
            temperature=0.3,  # Lower temperature for more consistent analysis
            max_tokens=4000,
        )

        return response.choices[0].message.content

    def _parse_response(self, response: str, focus_area: str) -> dict:
        """Parse the Grok response into structured data.

        Args:
            response: The raw response from Grok.
            focus_area: The focus area being analyzed.

        Returns:
            Parsed response with trends array.
        """
        try:
            # Try to extract JSON from the response
            json_start = response.find("[")
            json_end = response.rfind("]") + 1

            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                trends = json.loads(json_str)

                # Validate and enrich each trend
                validated_trends = []
                for trend in trends:
                    validated_trend = self._validate_trend(trend, focus_area)
                    if validated_trend:
                        validated_trends.append(validated_trend)

                return {
                    "focus_area": focus_area,
                    "trends": validated_trends,
                    "raw_response": response,
                }
            else:
                return {
                    "focus_area": focus_area,
                    "trends": [],
                    "raw_response": response,
                    "parse_error": "No JSON array found in response",
                }
        except json.JSONDecodeError as e:
            return {
                "focus_area": focus_area,
                "trends": [],
                "raw_response": response,
                "parse_error": f"JSON decode error: {str(e)}",
            }

    def _validate_trend(self, trend: dict, focus_area: str) -> Optional[dict]:
        """Validate and normalize a trend object.

        Args:
            trend: The trend dictionary to validate.
            focus_area: The focus area for context.

        Returns:
            Validated trend dict or None if invalid.
        """
        required_fields = ["tool_name", "classification"]

        # Check required fields
        for field in required_fields:
            if field not in trend:
                return None

        # Normalize classification
        classification = trend.get("classification", "").lower()
        if classification not in ["signal", "noise"]:
            return None

        return {
            "tool_name": trend.get("tool_name", ""),
            "classification": classification,
            "confidence_score": min(max(int(trend.get("confidence_score", 50)), 1), 100),
            "technical_insight": trend.get("technical_insight", ""),
            "signal_evidence": trend.get("signal_evidence", []),
            "noise_indicators": trend.get("noise_indicators", []),
            "architectural_verdict": bool(trend.get("architectural_verdict", False)),
            "focus_area": focus_area,
        }

    def get_available_focus_areas(self) -> list[str]:
        """Get list of available focus areas.

        Returns:
            List of focus area identifiers.
        """
        return self.FOCUS_AREAS.copy()

    def is_configured(self) -> bool:
        """Check if the service is properly configured.

        Returns:
            True if API key is set, False otherwise.
        """
        return bool(self.api_key)


# Singleton instance for application use
_grok_service: Optional[GrokService] = None


def get_grok_service() -> GrokService:
    """Get the singleton GrokService instance.

    Returns:
        The GrokService instance.
    """
    global _grok_service
    if _grok_service is None:
        _grok_service = GrokService()
    return _grok_service
