"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .models import Base
from .routers import items

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CodeScale Research Radar API",
    description="Signal vs Noise classification API for engineering teams",
    version="1.0.0"
)

# CORS middleware for UI5 frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(items.router, prefix="/api")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "CodeScale Research Radar API"}


@app.get("/api/radar")
async def get_radar():
    """Get the latest radar analysis.

    Returns mock data for scaffolding. Will be implemented in issue #3.
    """
    return {
        "radar_date": "2026-01-30",
        "trends": []
    }
