# Testing Guidelines

This document outlines the testing approach and best practices for the CodeScale Research Radar project.

## Test Framework Overview

### Backend (Python/FastAPI)

- **Framework**: pytest
- **Coverage Tool**: pytest-cov
- **Async Support**: pytest-asyncio

### Frontend (SAPUI5)

- **Framework**: QUnit (built into SAPUI5)
- **Integration Testing**: OPA5
- **E2E Testing**: Playwright MCP

## Directory Structure

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # Shared fixtures
│   ├── utils.py         # Test utilities
│   ├── test_main.py     # Main app tests
│   ├── test_models.py   # Model unit tests
│   ├── test_services.py # Service unit tests
│   └── test_api.py      # API integration tests
```

## Running Tests

### Backend Tests

```bash
cd backend
source .venv/bin/activate

# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_main.py

# Run tests by marker
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_main.py::TestHealthCheck::test_root_endpoint_returns_healthy
```

### Frontend Tests

```bash
# Run UI5 linter
npm run lint

# Use Playwright MCP for UI testing
# Navigate to http://localhost:8080 and test interactively
```

## Test Markers

Use pytest markers to categorize tests:

- `@pytest.mark.unit` - Fast, isolated unit tests
- `@pytest.mark.integration` - Tests that use database or external services
- `@pytest.mark.slow` - Long-running tests

## Writing Tests

### Test Organization

1. Group related tests in classes
2. Use descriptive test names
3. Follow AAA pattern (Arrange, Act, Assert)

### Example Unit Test

```python
import pytest

class TestHealthCheck:
    @pytest.mark.unit
    def test_health_endpoint_returns_healthy(self, client):
        # Arrange - handled by fixture

        # Act
        response = client.get("/")

        # Assert
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
```

### Example Integration Test

```python
import pytest

class TestTrendModel:
    @pytest.mark.integration
    def test_create_trend(self, db_session, sample_trend_data):
        # Arrange
        trend = Trend(**sample_trend_data)

        # Act
        db_session.add(trend)
        db_session.commit()

        # Assert
        assert trend.id is not None
```

## Using Fixtures

### Available Fixtures (conftest.py)

- `client` - FastAPI test client with database override
- `db_session` - Fresh database session for each test
- `test_engine` - SQLAlchemy engine with in-memory database
- `sample_trend_data` - Sample trend data dictionary
- `multiple_trends_data` - List of sample trends

### Using Test Utilities (utils.py)

```python
from tests.utils import (
    assert_valid_response,
    assert_json_structure,
    assert_radar_response,
    create_test_trend
)

def test_example(client):
    response = client.get("/api/radar")
    assert_valid_response(response, 200)
    assert_radar_response(response.json())
```

## Coverage Requirements

- Minimum coverage: 70%
- Coverage reports generated in `htmlcov/` directory

### Viewing Coverage Report

```bash
# After running tests
open htmlcov/index.html
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Use Fixtures**: Avoid code duplication with fixtures
3. **Mock External Services**: Don't call real APIs in tests
4. **Test Edge Cases**: Include negative and boundary tests
5. **Keep Tests Fast**: Unit tests should be < 1 second
6. **Clear Names**: Test names should describe what is being tested

## CI/CD Integration

Tests are run automatically in CI:

1. All PRs must pass `pytest`
2. All PRs must pass `npm run lint`
3. Coverage must meet minimum threshold

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're in the correct virtual environment
2. **Database Errors**: Check that fixtures are properly scoped
3. **Async Errors**: Use `@pytest.mark.asyncio` for async tests

### Debug Tips

```bash
# Run tests with print output
pytest -s

# Run tests with full traceback
pytest --tb=long

# Stop on first failure
pytest -x
```
