"""Pytest configuration and shared fixtures.

This module provides reusable fixtures for all tests.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db
from app.models import Base


# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine.

    Uses in-memory SQLite with StaticPool for thread safety.
    """
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_engine):
    """Create a fresh database session for each test.

    Clears all data and rolls back after each test to ensure isolation.
    """
    # Clear all tables before test
    with test_engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        # Clear all tables after test
        with test_engine.connect() as conn:
            for table in reversed(Base.metadata.sorted_tables):
                conn.execute(table.delete())
            conn.commit()


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database dependency override.

    Provides an isolated test client for each test.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_trend_data():
    """Provide sample trend data for tests."""
    return {
        "radar_date": "2026-02-17",
        "focus_area": "voice_ai_ux",
        "tool_name": "Test Tool",
        "classification": "signal",
        "confidence_score": 85,
        "technical_insight": "A test technical insight",
        "signal_evidence": '["evidence1", "evidence2"]',
        "noise_indicators": '["noise1"]',
        "architectural_verdict": 8,
        "timestamp": "2026-02-17T10:00:00Z"
    }


@pytest.fixture
def multiple_trends_data():
    """Provide multiple trend records for testing."""
    return [
        {
            "radar_date": "2026-02-17",
            "focus_area": "voice_ai_ux",
            "tool_name": "Voice AI Tool",
            "classification": "signal",
            "confidence_score": 90,
            "technical_insight": "Voice AI insight",
            "signal_evidence": '["evidence1"]',
            "noise_indicators": None,
            "architectural_verdict": 9,
            "timestamp": "2026-02-17T10:00:00Z"
        },
        {
            "radar_date": "2026-02-17",
            "focus_area": "agent_orchestration",
            "tool_name": "Agent Framework",
            "classification": "noise",
            "confidence_score": 60,
            "technical_insight": "Agent orchestration insight",
            "signal_evidence": None,
            "noise_indicators": '["too complex"]',
            "architectural_verdict": 4,
            "timestamp": "2026-02-17T11:00:00Z"
        },
        {
            "radar_date": "2026-02-17",
            "focus_area": "durable_runtime",
            "tool_name": "Runtime Tool",
            "classification": "signal",
            "confidence_score": 75,
            "technical_insight": "Durable runtime insight",
            "signal_evidence": '["stable", "performant"]',
            "noise_indicators": None,
            "architectural_verdict": 7,
            "timestamp": "2026-02-17T12:00:00Z"
        }
    ]
