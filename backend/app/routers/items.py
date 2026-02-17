"""CRUD API endpoints for trend items."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Trend, Base
from ..schemas import (
    TrendCreate,
    TrendUpdate,
    TrendResponse,
    TrendListResponse,
)

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=TrendListResponse)
async def get_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all trend items with pagination.

    Args:
        skip: Number of items to skip (default: 0)
        limit: Maximum number of items to return (default: 100)
        db: Database session

    Returns:
        List of trend items with total count
    """
    items = db.query(Trend).offset(skip).limit(limit).all()
    total = db.query(Trend).count()
    return TrendListResponse(items=items, total=total)


@router.get("/{item_id}", response_model=TrendResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a single trend item by ID.

    Args:
        item_id: The ID of the item to retrieve
        db: Database session

    Returns:
        The trend item

    Raises:
        HTTPException: If item not found
    """
    item = db.query(Trend).filter(Trend.id == item_id).first()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item


@router.post("", response_model=TrendResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: TrendCreate, db: Session = Depends(get_db)):
    """Create a new trend item.

    Args:
        item: The trend data to create
        db: Database session

    Returns:
        The created trend item
    """
    db_item = Trend(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/{item_id}", response_model=TrendResponse)
async def update_item(
    item_id: int,
    item: TrendUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing trend item.

    Args:
        item_id: The ID of the item to update
        item: The updated trend data
        db: Database session

    Returns:
        The updated trend item

    Raises:
        HTTPException: If item not found
    """
    db_item = db.query(Trend).filter(Trend.id == item_id).first()
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

    update_data = item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a trend item.

    Args:
        item_id: The ID of the item to delete
        db: Database session

    Raises:
        HTTPException: If item not found
    """
    db_item = db.query(Trend).filter(Trend.id == item_id).first()
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

    db.delete(db_item)
    db.commit()
    return None
