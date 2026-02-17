"""Tests for the items CRUD API endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db
from app.models import Base


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """Create a test client with fresh database for each test."""
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Drop tables after test
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture
def sample_item():
    """Return sample item data for testing."""
    return {
        "radar_date": "2026-02-17",
        "focus_area": "AI/ML",
        "tool_name": "LiteLLM",
        "classification": "signal",
        "confidence_score": 85,
        "technical_insight": "Strong adoption in enterprise settings",
        "signal_evidence": '["high github stars", "active community"]',
        "noise_indicators": None,
        "architectural_verdict": 4,
        "timestamp": "2026-02-17T10:00:00Z"
    }


def test_get_items_empty(client):
    """Test getting items when database is empty."""
    response = client.get("/api/items")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_create_item(client, sample_item):
    """Test creating a new item."""
    response = client.post("/api/items", json=sample_item)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["tool_name"] == sample_item["tool_name"]
    assert data["classification"] == sample_item["classification"]


def test_get_items_after_create(client, sample_item):
    """Test getting items after creating one."""
    # Create an item
    client.post("/api/items", json=sample_item)

    # Get all items
    response = client.get("/api/items")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["tool_name"] == sample_item["tool_name"]


def test_get_item_by_id(client, sample_item):
    """Test getting a single item by ID."""
    # Create an item
    create_response = client.post("/api/items", json=sample_item)
    item_id = create_response.json()["id"]

    # Get the item
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["tool_name"] == sample_item["tool_name"]


def test_get_item_not_found(client):
    """Test getting a non-existent item."""
    response = client.get("/api/items/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_item(client, sample_item):
    """Test updating an existing item."""
    # Create an item
    create_response = client.post("/api/items", json=sample_item)
    item_id = create_response.json()["id"]

    # Update the item
    update_data = {
        "classification": "noise",
        "confidence_score": 30
    }
    response = client.put(f"/api/items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["classification"] == "noise"
    assert data["confidence_score"] == 30
    # Unchanged fields should remain
    assert data["tool_name"] == sample_item["tool_name"]


def test_update_item_not_found(client):
    """Test updating a non-existent item."""
    update_data = {"classification": "noise"}
    response = client.put("/api/items/999", json=update_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_item(client, sample_item):
    """Test deleting an item."""
    # Create an item
    create_response = client.post("/api/items", json=sample_item)
    item_id = create_response.json()["id"]

    # Delete the item
    response = client.delete(f"/api/items/{item_id}")
    assert response.status_code == 204

    # Verify item is deleted
    get_response = client.get(f"/api/items/{item_id}")
    assert get_response.status_code == 404


def test_delete_item_not_found(client):
    """Test deleting a non-existent item."""
    response = client.delete("/api/items/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_pagination(client, sample_item):
    """Test pagination with skip and limit."""
    # Create multiple items
    for i in range(5):
        item = sample_item.copy()
        item["tool_name"] = f"Tool_{i}"
        client.post("/api/items", json=item)

    # Test skip
    response = client.get("/api/items?skip=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3
    assert data["total"] == 5

    # Test limit
    response = client.get("/api/items?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5


def test_create_item_invalid_classification(client, sample_item):
    """Test creating item with invalid classification."""
    sample_item["classification"] = "invalid"
    response = client.post("/api/items", json=sample_item)
    assert response.status_code == 422  # Validation error


def test_create_item_invalid_confidence_score(client, sample_item):
    """Test creating item with invalid confidence score."""
    sample_item["confidence_score"] = 150  # Out of range
    response = client.post("/api/items", json=sample_item)
    assert response.status_code == 422  # Validation error


def test_create_item_invalid_architectural_verdict(client, sample_item):
    """Test creating item with invalid architectural verdict."""
    sample_item["architectural_verdict"] = 10  # Out of range (1-5)
    response = client.post("/api/items", json=sample_item)
    assert response.status_code == 422  # Validation error
