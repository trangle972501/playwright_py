# playwright_py
This is a responsibility that including my learning
# Project struncture 
config/
- Manage environment, URL, timeout and browser settings

pages/
- Page Object Model — locator and action on each page


components/
- UI components reuse such as navbar, modal, table


tests/
- Test cases are organized by feature

test_data/
- Test data, JSON, CSV and data based on environments


utils/
Helper, logger, data generator and helper function


fixtures/
- init browser, context, page and test dependencies

api/
API client and API helpers if needing to integrate API testing

reports/
Test reports, screenshots and traces

scripts/
- script support to run and manage framework


conftest.py
Pytest fixtures and common hooks


pytest.ini
- Pytest configuration and markers


pyproject.toml
- Dependencies, tool configuration và project metadata


.env.example
-  environment variables


.gitignore
- ignore cache, secrets and generated artifacts

## Installation
# 1. Install from a pyproject.toml file:
    `uv pip install -r pyproject.toml`
# 2. Install require browsers
    - All browers: `uv run playwright install`
    - Specific browser: `uv run playwright install chromium`

## Activate python
MacOs: `source .venv/bin/activate`
window: `.venv\Scripts\activate`
##Deactivate python env 
`deactivate`
# Run test
## Run specific test
`pytest <path_test> -v`
## Run all test
`pytest` 
`pytest --html=report.html --self-contained-html `
