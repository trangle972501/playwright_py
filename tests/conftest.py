import pytest
from playwright.sync_api import sync_playwright, Page, Browser

def pytest_addoption(parser):
    parser.addini("base_url", help="Base URL for tests", default="https://www.automationexercise.com/")

# These hooks run once for the entire test session (or module)
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getini("base_url")