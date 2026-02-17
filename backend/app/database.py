"""Database connection and session management.

Provides SQLite database setup with SQLAlchemy ORM.
"""

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base

# Database file path - defaults to project backend directory
DATABASE_DIR = Path(__file__).parent.parent
DATABASE_PATH = DATABASE_DIR / "radar.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# For testing, allow override via environment variable
if os.getenv("DATABASE_URL"):
    DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine with SQLite-specific settings
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite with threads
    echo=False,  # Set to True for SQL debugging
)


# Enable foreign key support for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable SQLite foreign key constraints."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Initialize database by creating all tables.

    Call this at application startup to ensure tables exist.
    """
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """Drop all database tables.

    USE WITH CAUTION - primarily for testing.
    """
    Base.metadata.drop_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Get database session for FastAPI dependency injection.

    Usage:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            ...

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """Get database session as a context manager.

    Usage:
        with get_db_context() as db:
            db.query(Trend).all()

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
