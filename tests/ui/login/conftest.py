import pytest
from playwright.sync_api import sync_playwright, Page, Browser
from pages.login_page import LoginPage

@pytest.fixture
def login_page(page: Page, base_url: str) -> LoginPage:
    """Navigate to the site and open the login form before each test."""
    lp = LoginPage(page)
    lp.navigate(base_url)
    lp.header.click_login_button()
    return lp