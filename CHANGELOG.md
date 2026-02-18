# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- LiteLLM integration with xAI/Grok API for AI-powered trend analysis (#5)
- GrokService class with async support for analyzing trends across focus areas
- PromptService for managing and validating prompt templates
- PromptTester utility for testing prompt template syntax and structure
- Configuration module with environment variable support for LiteLLM settings
- Comprehensive test suite for GrokService (18 tests) and PromptService (17 tests)
- Updated .env.example with LiteLLM configuration options
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
