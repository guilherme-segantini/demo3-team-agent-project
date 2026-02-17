# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Initial project scaffolding for CodeScale Research Radar
- SAPUI5 frontend structure with Component.js, manifest.json, and routing
- Base views (App.view.xml, Main.view.xml) with i18n support
- BaseController with common utilities (getRouter, getModel, getText, navTo)
- Formatter module for signal/noise classification display
- Mock data (mock_radar.json) matching Golden Contract schema
- CSS styles for signal/noise visual distinction
- FastAPI backend with health check and /api/radar endpoint
- SQLAlchemy models for Trend entity
- Database configuration with SQLite
- Grok service placeholder for LiteLLM integration
- Backend tests with pytest
- Prompt templates for all three focus areas (Voice AI, Agent Orchestration, Durable Runtime)
- requirements.txt with all Python dependencies
- Complete database schema with SQLAlchemy models (Issue #3)
  - Trend model with Golden Contract fields (focus_area, tool_name, classification, confidence_score, etc.)
  - RadarAnalysis model for tracking radar analysis runs
  - Database constraints for classification (signal/noise), focus_area, and confidence_score (1-100)
  - to_dict() method for JSON serialization with proper list parsing
- Database initialization and session management (Issue #3)
  - init_db() and drop_db() functions for database lifecycle
  - get_db() dependency injection for FastAPI
  - get_db_context() context manager for scripts
  - PRAGMA foreign_keys enabled for SQLite
- Seed data script (seed_data.py) with 6 sample trends (Issue #3)
- Comprehensive model tests (19 tests) covering CRUD operations (Issue #3)
- Test fixtures with proper database isolation (conftest.py) (Issue #3)

### Changed

### Deferred
