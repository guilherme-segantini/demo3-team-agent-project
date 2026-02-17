"""Tests for database models."""

import pytest
from sqlalchemy import inspect

from app.models import Base, Trend


class TestTrendModel:
    """Tests for the Trend model."""

    @pytest.mark.unit
    def test_trend_table_exists(self, test_engine):
        """Test that the trends table is created."""
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        assert "trends" in tables

    @pytest.mark.unit
    def test_trend_columns(self, test_engine):
        """Test that the Trend model has required columns."""
        inspector = inspect(test_engine)
        columns = {col["name"] for col in inspector.get_columns("trends")}

        required_columns = {
            "id",
            "radar_date",
            "focus_area",
            "tool_name",
            "classification",
            "confidence_score",
            "technical_insight",
            "signal_evidence",
            "noise_indicators",
            "architectural_verdict",
            "timestamp"
        }

        missing = required_columns - columns
        assert not missing, f"Missing columns: {missing}"

    @pytest.mark.integration
    def test_create_trend(self, db_session, sample_trend_data):
        """Test creating a new trend record."""
        trend = Trend(**sample_trend_data)
        db_session.add(trend)
        db_session.commit()

        assert trend.id is not None
        assert trend.tool_name == sample_trend_data["tool_name"]
        assert trend.classification == sample_trend_data["classification"]

    @pytest.mark.integration
    def test_trend_query(self, db_session, sample_trend_data):
        """Test querying trend records."""
        trend = Trend(**sample_trend_data)
        db_session.add(trend)
        db_session.commit()

        queried = db_session.query(Trend).filter_by(
            tool_name=sample_trend_data["tool_name"]
        ).first()

        assert queried is not None
        assert queried.id == trend.id
        assert queried.classification == "signal"

    @pytest.mark.integration
    def test_multiple_trends(self, db_session, multiple_trends_data):
        """Test creating multiple trend records."""
        trends = [Trend(**data) for data in multiple_trends_data]
        db_session.add_all(trends)
        db_session.commit()

        count = db_session.query(Trend).count()
        assert count == len(multiple_trends_data)

    @pytest.mark.integration
    def test_filter_by_focus_area(self, db_session, multiple_trends_data):
        """Test filtering trends by focus area."""
        trends = [Trend(**data) for data in multiple_trends_data]
        db_session.add_all(trends)
        db_session.commit()

        voice_trends = db_session.query(Trend).filter_by(
            focus_area="voice_ai_ux"
        ).all()

        assert len(voice_trends) == 1
        assert voice_trends[0].tool_name == "Voice AI Tool"

    @pytest.mark.integration
    def test_filter_by_classification(self, db_session, multiple_trends_data):
        """Test filtering trends by classification."""
        trends = [Trend(**data) for data in multiple_trends_data]
        db_session.add_all(trends)
        db_session.commit()

        signals = db_session.query(Trend).filter_by(
            classification="signal"
        ).all()

        assert len(signals) == 2
        assert all(t.classification == "signal" for t in signals)

    @pytest.mark.integration
    def test_update_trend(self, db_session, sample_trend_data):
        """Test updating a trend record."""
        trend = Trend(**sample_trend_data)
        db_session.add(trend)
        db_session.commit()

        trend.classification = "noise"
        trend.confidence_score = 40
        db_session.commit()

        updated = db_session.get(Trend, trend.id)
        assert updated.classification == "noise"
        assert updated.confidence_score == 40

    @pytest.mark.integration
    def test_delete_trend(self, db_session, sample_trend_data):
        """Test deleting a trend record."""
        trend = Trend(**sample_trend_data)
        db_session.add(trend)
        db_session.commit()
        trend_id = trend.id

        db_session.delete(trend)
        db_session.commit()

        deleted = db_session.get(Trend, trend_id)
        assert deleted is None
