"""Test utilities and helper functions.

This module provides reusable utility functions for tests.
"""

from datetime import datetime
from typing import Any


def assert_valid_response(response, expected_status: int = 200):
    """Assert that a response has the expected status code.

    Args:
        response: The HTTP response object
        expected_status: Expected HTTP status code

    Raises:
        AssertionError: If status code doesn't match
    """
    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, got {response.status_code}. "
        f"Response: {response.text}"
    )


def assert_json_structure(data: dict, required_keys: list[str]):
    """Assert that a JSON response contains required keys.

    Args:
        data: The parsed JSON response
        required_keys: List of keys that must be present

    Raises:
        AssertionError: If any required key is missing
    """
    missing = [key for key in required_keys if key not in data]
    assert not missing, f"Missing required keys: {missing}"


def assert_trend_structure(trend: dict):
    """Assert that a trend object has valid structure.

    Args:
        trend: A trend dictionary

    Raises:
        AssertionError: If trend structure is invalid
    """
    required_keys = [
        "focus_area",
        "tool_name",
        "classification",
        "confidence_score",
        "technical_insight"
    ]
    assert_json_structure(trend, required_keys)

    # Validate classification value
    valid_classifications = ["signal", "noise"]
    assert trend["classification"] in valid_classifications, (
        f"Invalid classification: {trend['classification']}. "
        f"Must be one of: {valid_classifications}"
    )

    # Validate confidence score range
    assert 0 <= trend["confidence_score"] <= 100, (
        f"Confidence score {trend['confidence_score']} out of range [0, 100]"
    )


def assert_radar_response(data: dict):
    """Assert that a radar response has valid structure.

    Args:
        data: The radar response dictionary

    Raises:
        AssertionError: If radar response structure is invalid
    """
    assert_json_structure(data, ["radar_date", "trends"])
    assert isinstance(data["trends"], list), "trends must be a list"

    # Validate each trend if present
    for trend in data["trends"]:
        assert_trend_structure(trend)


def create_test_trend(overrides: dict[str, Any] = None) -> dict:
    """Create a test trend with default values.

    Args:
        overrides: Dictionary of values to override defaults

    Returns:
        A complete trend dictionary
    """
    defaults = {
        "radar_date": datetime.now().strftime("%Y-%m-%d"),
        "focus_area": "voice_ai_ux",
        "tool_name": "Test Tool",
        "classification": "signal",
        "confidence_score": 75,
        "technical_insight": "Test insight",
        "signal_evidence": '["evidence"]',
        "noise_indicators": None,
        "architectural_verdict": 7,
        "timestamp": datetime.now().isoformat()
    }

    if overrides:
        defaults.update(overrides)

    return defaults


def validate_date_format(date_str: str, format_str: str = "%Y-%m-%d") -> bool:
    """Validate that a date string matches expected format.

    Args:
        date_str: The date string to validate
        format_str: Expected date format

    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, format_str)
        return True
    except ValueError:
        return False
