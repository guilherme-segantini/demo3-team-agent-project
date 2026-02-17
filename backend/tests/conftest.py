"""Pytest configuration and shared fixtures."""

import json
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Trend, RadarAnalysis
from app.database import get_db
from app.main import app


# Create test database engine - use file-based SQLite for consistent behavior
TEST_DATABASE_URL = "sqlite:///./test_radar.db"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override database dependency for tests."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apply override
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_test_db():
    """Set up test database before each test."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def test_session():
    """Create a test database session."""
    session = TestSessionLocal()
    yield session
    session.close()


@pytest.fixture
def seeded_db():
    """Seed the test database with sample data."""
    db = TestSessionLocal()

    # Create radar analysis
    analysis = RadarAnalysis(
        radar_date="2026-01-30",
        status="completed",
        trend_count=2,
    )
    db.add(analysis)

    # Create trends
    trend1 = Trend(
        radar_date="2026-01-30",
        focus_area="voice_ai_ux",
        tool_name="LiveKit Agents",
        classification="signal",
        confidence_score=92,
        technical_insight="Sub-200ms voice-to-voice latency",
        signal_evidence=json.dumps(["Published benchmarks"]),
        noise_indicators=json.dumps([]),
        architectural_verdict=True,
        timestamp="2026-01-30T08:00:00Z",
    )
    trend2 = Trend(
        radar_date="2026-01-30",
        focus_area="voice_ai_ux",
        tool_name="VoiceHype AI",
        classification="noise",
        confidence_score=85,
        technical_insight="No benchmarks available",
        signal_evidence=json.dumps([]),
        noise_indicators=json.dumps(["No published benchmarks"]),
        architectural_verdict=False,
        timestamp="2026-01-30T08:00:00Z",
    )
    db.add(trend1)
    db.add(trend2)
    db.commit()
    db.close()
