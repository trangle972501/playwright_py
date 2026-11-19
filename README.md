# playwright_py

This repository contains my Playwright with Python learning notes and test automation framework setup.

## Project Structure

```text
playwright_py/
├── config/          # Environment, URL, timeout, and browser settings
├── pages/           # Page Object Model — locators and actions for each page
├── components/      # Reusable UI components (navbar, modal, table, etc.)
├── tests/           # Test cases organized by feature
├── test_data/       # Test data (JSON, CSV) and environment-specific datasets
├── utils/           # Helpers, logger, and data generators
├── fixtures/        # Browser, context, page initialization, and test dependencies
├── api/             # API client and helpers for API testing integration
├── reports/         # Test reports, screenshots, and traces
├── scripts/         # Utility scripts to run and manage the framework
├── conftest.py      # Pytest fixtures and common hooks
├── pytest.ini       # Pytest configuration and markers
├── pyproject.toml   # Dependencies, tool configuration, and project metadata
├── .env.example     # Example environment variables
└── .gitignore       # Ignored cache, secrets, and generated artifacts

```

## Installation
1. Install dependencies from pyproject.toml:
- `uv pip install -r pyproject.toml`

2. Install required browsers:
- All browsers:
    `uv run playwright install`
- Specific browser (e.g., Chromium):
    `uv run playwright install chromium`

## Virtual Environment
- Activate (macOS / Linux):
    `source .venv/bin/activate`
- Activate (Windows):
    `.venv\Scripts\activate`
- Deactivate:
    `deactivate`

## Running Tests
- Run a specific test:
    `pytest <path_to_test> -v`
- Run all tests:
    `Run all tests:`
- Run all tests and generate a self-contained HTML report:
    `pytest --html=reports/report.html --self-contained-html`

## Reports & Debugging
- Open HTML test report (macOS):
    `open reports/report.html`
- View Playwright trace:
    `uv run playwright show-trace test-results/<trace-file>.zip`