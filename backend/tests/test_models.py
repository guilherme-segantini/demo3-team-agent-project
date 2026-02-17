"""Tests for database models and database operations."""

import json
import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Trend, RadarAnalysis


class TestTrendModel:
    """Tests for the Trend model."""

    def test_create_signal_trend(self, test_session):
        """Test creating a signal trend."""
        trend = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="LiveKit Agents",
            classification="signal",
            confidence_score=92,
            technical_insight="Sub-200ms voice-to-voice latency with WebRTC.",
            signal_evidence=json.dumps(["Published benchmarks", "Production usage"]),
            noise_indicators=json.dumps([]),
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        test_session.add(trend)
        test_session.commit()

        # Verify the trend was created
        assert trend.id is not None
        assert trend.classification == "signal"
        assert trend.architectural_verdict is True

    def test_create_noise_trend(self, test_session):
        """Test creating a noise trend."""
        trend = Trend(
            radar_date="2026-01-30",
            focus_area="agent_orchestration",
            tool_name="AutoAgent Pro",
            classification="noise",
            confidence_score=78,
            technical_insight="Promises autonomous agents but lacks documentation.",
            signal_evidence=json.dumps([]),
            noise_indicators=json.dumps(["No integration specs", "Marketing claims"]),
            architectural_verdict=False,
            timestamp="2026-01-30T08:00:00Z",
        )
        test_session.add(trend)
        test_session.commit()

        assert trend.id is not None
        assert trend.classification == "noise"
        assert trend.architectural_verdict is False

    def test_trend_to_dict(self, test_session):
        """Test converting a trend to dictionary."""
        trend = Trend(
            radar_date="2026-01-30",
            focus_area="durable_runtime",
            tool_name="Temporal.io",
            classification="signal",
            confidence_score=94,
            technical_insight="Workflow durability with automatic retries.",
            signal_evidence=json.dumps(["SLA docs", "Enterprise usage"]),
            noise_indicators=json.dumps([]),
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        test_session.add(trend)
        test_session.commit()

        trend_dict = trend.to_dict()

        assert trend_dict["tool_name"] == "Temporal.io"
        assert trend_dict["classification"] == "signal"
        assert trend_dict["confidence_score"] == 94
        assert isinstance(trend_dict["signal_evidence"], list)
        assert "SLA docs" in trend_dict["signal_evidence"]

    def test_trend_repr(self, test_session):
        """Test trend string representation."""
        trend = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="TestTool",
            classification="signal",
            confidence_score=80,
            technical_insight="Test insight",
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        test_session.add(trend)
        test_session.commit()

        repr_str = repr(trend)
        assert "TestTool" in repr_str
        assert "signal" in repr_str
        assert "80" in repr_str

    def test_query_by_focus_area(self, test_session):
        """Test querying trends by focus area."""
        # Create trends in different focus areas
        for focus_area in ["voice_ai_ux", "agent_orchestration", "durable_runtime"]:
            trend = Trend(
                radar_date="2026-01-30",
                focus_area=focus_area,
                tool_name=f"Tool for {focus_area}",
                classification="signal",
                confidence_score=85,
                technical_insight="Test insight",
                architectural_verdict=True,
                timestamp="2026-01-30T08:00:00Z",
            )
            test_session.add(trend)
        test_session.commit()

        # Query by focus area
        voice_trends = test_session.query(Trend).filter(
            Trend.focus_area == "voice_ai_ux"
        ).all()

        assert len(voice_trends) == 1
        assert voice_trends[0].focus_area == "voice_ai_ux"

    def test_query_by_radar_date(self, test_session):
        """Test querying trends by radar date."""
        # Create trends for different dates
        for date in ["2026-01-28", "2026-01-29", "2026-01-30"]:
            trend = Trend(
                radar_date=date,
                focus_area="voice_ai_ux",
                tool_name=f"Tool for {date}",
                classification="signal",
                confidence_score=85,
                technical_insight="Test insight",
                architectural_verdict=True,
                timestamp=f"{date}T08:00:00Z",
            )
            test_session.add(trend)
        test_session.commit()

        # Query by date
        jan30_trends = test_session.query(Trend).filter(
            Trend.radar_date == "2026-01-30"
        ).all()

        assert len(jan30_trends) == 1
        assert jan30_trends[0].radar_date == "2026-01-30"

    def test_confidence_score_in_range(self, test_session):
        """Test that confidence scores are properly stored."""
        trend = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="Test Tool",
            classification="signal",
            confidence_score=100,  # Max value
            technical_insight="Test insight",
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        test_session.add(trend)
        test_session.commit()

        assert trend.confidence_score == 100

        trend2 = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="Test Tool 2",
            classification="signal",
            confidence_score=1,  # Min value
            technical_insight="Test insight",
            architectural_verdict=True,
            timestamp="2026-01-30T08:00:00Z",
        )
        test_session.add(trend2)
        test_session.commit()

        assert trend2.confidence_score == 1


class TestRadarAnalysisModel:
    """Tests for the RadarAnalysis model."""

    def test_create_radar_analysis(self, test_session):
        """Test creating a radar analysis record."""
        analysis = RadarAnalysis(
            radar_date="2026-01-30",
            status="completed",
            trend_count=6,
        )
        test_session.add(analysis)
        test_session.commit()

        assert analysis.id is not None
        assert analysis.radar_date == "2026-01-30"
        assert analysis.status == "completed"
        assert analysis.trend_count == 6
        assert analysis.created_at is not None

    def test_radar_analysis_repr(self, test_session):
        """Test radar analysis string representation."""
        analysis = RadarAnalysis(
            radar_date="2026-01-30",
            status="completed",
            trend_count=5,
        )
        test_session.add(analysis)
        test_session.commit()

        repr_str = repr(analysis)
        assert "2026-01-30" in repr_str
        assert "completed" in repr_str
        assert "5" in repr_str

    def test_unique_radar_date(self, test_session):
        """Test that radar_date is unique."""
        analysis1 = RadarAnalysis(
            radar_date="2026-01-30",
            status="completed",
            trend_count=6,
        )
        test_session.add(analysis1)
        test_session.commit()

        # Try to create another with same date
        analysis2 = RadarAnalysis(
            radar_date="2026-01-30",
            status="completed",
            trend_count=3,
        )
        test_session.add(analysis2)

        with pytest.raises(IntegrityError):
            test_session.commit()


class TestDatabaseCRUD:
    """Tests for CRUD operations."""

    def test_update_trend(self, test_session):
        """Test updating a trend."""
        trend = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="UpdateTest",
            classification="noise",
            confidence_score=50,
            technical_insight="Initial insight",
            architectural_verdict=False,
            timestamp="2026-01-30T08:00:00Z",
        )
        test_session.add(trend)
        test_session.commit()

        # Update the trend
        trend.classification = "signal"
        trend.confidence_score = 85
        trend.architectural_verdict = True
        test_session.commit()

        # Verify update
        updated = test_session.query(Trend).filter(Trend.id == trend.id).first()
        assert updated.classification == "signal"
        assert updated.confidence_score == 85
        assert updated.architectural_verdict is True

    def test_delete_trend(self, test_session):
        """Test deleting a trend."""
        trend = Trend(
            radar_date="2026-01-30",
            focus_area="voice_ai_ux",
            tool_name="DeleteTest",
            classification="noise",
            confidence_score=50,
            technical_insight="To be deleted",
            architectural_verdict=False,
            timestamp="2026-01-30T08:00:00Z",
        )
        test_session.add(trend)
        test_session.commit()

        trend_id = trend.id

        # Delete the trend
        test_session.delete(trend)
        test_session.commit()

        # Verify deletion
        deleted = test_session.query(Trend).filter(Trend.id == trend_id).first()
        assert deleted is None

    def test_bulk_insert_trends(self, test_session):
        """Test bulk inserting multiple trends."""
        trends = [
            Trend(
                radar_date="2026-01-30",
                focus_area="voice_ai_ux",
                tool_name=f"BulkTool{i}",
                classification="signal" if i % 2 == 0 else "noise",
                confidence_score=80 + i,
                technical_insight=f"Insight {i}",
                architectural_verdict=i % 2 == 0,
                timestamp="2026-01-30T08:00:00Z",
            )
            for i in range(10)
        ]

        test_session.add_all(trends)
        test_session.commit()

        # Verify all were inserted
        count = test_session.query(Trend).count()
        assert count == 10

        # Check signal/noise distribution
        signals = test_session.query(Trend).filter(Trend.classification == "signal").count()
        noise = test_session.query(Trend).filter(Trend.classification == "noise").count()
        assert signals == 5
        assert noise == 5
