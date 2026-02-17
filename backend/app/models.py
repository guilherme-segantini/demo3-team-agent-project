"""Database models for the Research Radar.

Implements SQLAlchemy ORM models matching the Golden Contract schema from PRD.md.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Integer,
    String,
    Text,
    Boolean,
    create_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Trend(Base):
    """Trend model representing a tool classification in the Research Radar.

    Fields match the Golden Contract JSON schema:
    - focus_area: One of voice_ai_ux, agent_orchestration, durable_runtime
    - classification: signal or noise
    - confidence_score: 1-100 integer
    - signal_evidence/noise_indicators: JSON arrays stored as text
    """

    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, autoincrement=True)
    radar_date = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD format
    focus_area = Column(
        String(50),
        nullable=False,
        index=True,
    )
    tool_name = Column(String(200), nullable=False)
    classification = Column(String(10), nullable=False)
    confidence_score = Column(Integer, nullable=False)
    technical_insight = Column(Text, nullable=False)
    signal_evidence = Column(Text, default="[]")  # JSON array stored as text
    noise_indicators = Column(Text, default="[]")  # JSON array stored as text
    architectural_verdict = Column(Boolean, nullable=False)
    timestamp = Column(String(30), nullable=False)  # ISO 8601 format

    __table_args__ = (
        CheckConstraint(
            "classification IN ('signal', 'noise')",
            name="check_classification_valid",
        ),
        CheckConstraint(
            "focus_area IN ('voice_ai_ux', 'agent_orchestration', 'durable_runtime')",
            name="check_focus_area_valid",
        ),
        CheckConstraint(
            "confidence_score >= 1 AND confidence_score <= 100",
            name="check_confidence_score_range",
        ),
    )

    def __repr__(self) -> str:
        """String representation of the Trend."""
        return (
            f"<Trend(id={self.id}, tool_name='{self.tool_name}', "
            f"classification='{self.classification}', "
            f"confidence_score={self.confidence_score})>"
        )

    def to_dict(self) -> dict:
        """Convert trend to dictionary matching Golden Contract schema."""
        import json

        return {
            "id": self.id,
            "focus_area": self.focus_area,
            "tool_name": self.tool_name,
            "classification": self.classification,
            "confidence_score": self.confidence_score,
            "technical_insight": self.technical_insight,
            "signal_evidence": json.loads(self.signal_evidence or "[]"),
            "noise_indicators": json.loads(self.noise_indicators or "[]"),
            "architectural_verdict": self.architectural_verdict,
            "timestamp": self.timestamp,
        }


class RadarAnalysis(Base):
    """Represents a radar analysis run/session.

    Tracks when analysis was performed and provides metadata
    for grouping trends by date.
    """

    __tablename__ = "radar_analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    radar_date = Column(String(10), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(
        String(20),
        nullable=False,
        default="completed",
    )
    trend_count = Column(Integer, default=0)

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'running', 'completed', 'failed')",
            name="check_status_valid",
        ),
    )

    def __repr__(self) -> str:
        """String representation of the RadarAnalysis."""
        return (
            f"<RadarAnalysis(id={self.id}, radar_date='{self.radar_date}', "
            f"status='{self.status}', trend_count={self.trend_count})>"
        )
