"""Pydantic schemas for request/response validation."""

from typing import Optional, List
from pydantic import BaseModel, Field


class TrendBase(BaseModel):
    """Base schema for trend data."""

    radar_date: str = Field(..., description="Date of the radar analysis")
    focus_area: str = Field(..., description="Area of focus for the tool")
    tool_name: str = Field(..., description="Name of the tool being classified")
    classification: str = Field(
        ...,
        pattern="^(signal|noise)$",
        description="Classification: 'signal' or 'noise'"
    )
    confidence_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence score (0-100)"
    )
    technical_insight: str = Field(..., description="Technical analysis insight")
    signal_evidence: Optional[str] = Field(
        None,
        description="JSON string of signal evidence"
    )
    noise_indicators: Optional[str] = Field(
        None,
        description="JSON string of noise indicators"
    )
    architectural_verdict: int = Field(
        ...,
        ge=1,
        le=5,
        description="Architectural verdict score (1-5)"
    )
    timestamp: str = Field(..., description="Timestamp of the analysis")


class TrendCreate(TrendBase):
    """Schema for creating a new trend."""

    pass


class TrendUpdate(BaseModel):
    """Schema for updating an existing trend."""

    radar_date: Optional[str] = None
    focus_area: Optional[str] = None
    tool_name: Optional[str] = None
    classification: Optional[str] = Field(
        None,
        pattern="^(signal|noise)$"
    )
    confidence_score: Optional[int] = Field(None, ge=0, le=100)
    technical_insight: Optional[str] = None
    signal_evidence: Optional[str] = None
    noise_indicators: Optional[str] = None
    architectural_verdict: Optional[int] = Field(None, ge=1, le=5)
    timestamp: Optional[str] = None


class TrendResponse(TrendBase):
    """Schema for trend response including ID."""

    id: int
    model_config = {"from_attributes": True}


class TrendListResponse(BaseModel):
    """Schema for list of trends response."""

    items: List[TrendResponse]
    total: int


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    detail: str
