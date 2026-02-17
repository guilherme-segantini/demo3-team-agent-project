# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- CI/CD pipeline with GitHub Actions workflows (Issue #14)
  - `test.yml`: Automated frontend linting and backend pytest execution
  - `lint.yml`: Code quality checks (UI5 linter, Ruff for Python)
  - `deploy.yml`: Build and deployment pipeline with staging/production environments
- Workflows use `uv` for fast Python dependency management
- Coverage reporting integration with Codecov
- Manual workflow dispatch for deployment environment selection
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

### Changed

### Deferred
