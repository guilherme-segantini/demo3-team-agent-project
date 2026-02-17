"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import get_db, init_db
from app.models import Trend, RadarAnalysis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    init_db()
    yield


app = FastAPI(
    title="CodeScale Research Radar API",
    description="Signal vs Noise classification API for engineering teams",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware for UI5 frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "CodeScale Research Radar API"}


@app.get("/api/radar")
async def get_radar(
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db),
):
    """Get radar analysis for a specific date or the latest.

    Args:
        date: Optional date filter in YYYY-MM-DD format
        db: Database session

    Returns:
        Radar analysis with trends matching the Golden Contract schema
    """
    # Build query
    query = db.query(Trend)

    if date:
        # Filter by specific date
        query = query.filter(Trend.radar_date == date)
    else:
        # Get the latest date
        latest_analysis = db.query(RadarAnalysis).order_by(
            RadarAnalysis.radar_date.desc()
        ).first()

        if latest_analysis:
            query = query.filter(Trend.radar_date == latest_analysis.radar_date)
            date = latest_analysis.radar_date
        else:
            # No data exists, return empty response
            return {"radar_date": None, "trends": []}

    # Get trends and convert to dictionaries
    trends = query.all()

    return {
        "radar_date": date,
        "trends": [trend.to_dict() for trend in trends],
    }
