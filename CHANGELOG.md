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
- Comprehensive test framework setup (Issue #6):
  - Enhanced pytest configuration with coverage (70% minimum threshold)
  - Test markers for unit/integration/slow tests
  - Shared fixtures in conftest.py (test client, database sessions, sample data)
  - Test utilities module with assertion helpers
  - Unit tests for models (Trend CRUD operations)
  - Unit tests for services (GrokService initialization and API key handling)
  - Integration tests for API endpoints (health, radar, CORS, OpenAPI)
  - Testing guidelines documentation (docs/TESTING.md)

### Changed

### Deferred
