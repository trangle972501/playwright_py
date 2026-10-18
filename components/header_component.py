from playwright.sync_api import Page, expect
from components.base_component import BaseComponent


class HeaderComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

        # Locators
        self.logout_button = page.get_by_text("Logout")
        self.login_button = page.get_by_text("Signup / Login")

    def logout(self) -> None:
        self.logout_button.click()

    def is_logout_button_visible(self) -> bool:
        return self.logout_button.is_visible()

    def is_login_button_visible(self) -> bool:
        return self.login_button.is_visible()

    def expect_logout_button(self) -> None:
        expect(self.logout_button).to_be_visible()

    def click_login_button(self) -> None:
        self.login_button.click()