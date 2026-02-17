# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Main navigation structure with ToolPage, side navigation, and shell bar (#1)
- Navigation routes for all focus areas (Voice AI, Agent Orchestration, Durable Runtime)
- App.controller.js with navigation logic and side panel toggle
- Placeholder views for VoiceAI, AgentOrch, DurableRuntime, Settings, and NotFound pages
- DynamicPage layout on Main view with statistics header
- IconTabBar for filtering by focus area on main page
- Updated i18n with all navigation and UI text entries
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
