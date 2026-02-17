# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Data Display Table component (Issue #2)
  - DataTable.view.xml with sap.m.Table for displaying technology trends
  - DataTable.controller.js with sorting and filtering functionality
  - TrendDetail.view.xml for detailed trend information view
  - TrendDetail.controller.js for detail page data binding
  - Search functionality across tool names and technical insights
  - Filter by focus area (Voice AI, Agent Orchestration, Durable Runtime)
  - Filter by classification (Signal/Noise)
  - Sort by confidence score or tool name
  - Navigation from table to detail view
  - All i18n labels for new components
  - Routing configuration for dataTable and trendDetail routes
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
