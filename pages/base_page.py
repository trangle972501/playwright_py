from playwright.sync_api import Page
from components.header_component import HeaderComponent


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.header = HeaderComponent(page)

    def navigate(self, url: str) -> None:
        self.page.goto(url)