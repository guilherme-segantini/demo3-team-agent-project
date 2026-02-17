"""Database models for the Research Radar.

To be implemented in issue #4.
"""

from sqlalchemy import Column, Integer, String, Text, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Trend(Base):
    """Trend model representing a tool classification."""

    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, autoincrement=True)
    radar_date = Column(String, nullable=False)
    focus_area = Column(String, nullable=False)
    tool_name = Column(String, nullable=False)
    classification = Column(
        String,
        nullable=False,
        info={"check": CheckConstraint("classification IN ('signal', 'noise')")}
    )
    confidence_score = Column(Integer, nullable=False)
    technical_insight = Column(Text, nullable=False)
    signal_evidence = Column(Text)  # JSON string
    noise_indicators = Column(Text)  # JSON string
    architectural_verdict = Column(Integer, nullable=False)
    timestamp = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint("classification IN ('signal', 'noise')"),
    )
