from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    # Locators
        self.username_input = page.locator("//input[@data-qa='login-email']")
        self.password_input = page.locator("//input[@data-qa='login-password']")
        self.login_button = page.locator("//button[@data-qa='login-button']")
        self.error_message = "//p[contains(text(), '%s')]"

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self, error: str):
        return self.page.locator(
            f"//p[contains(text(), {self._xpath_literal(error)})]"
        )
    
    @staticmethod
    def _xpath_literal(value: str) -> str:
        """Safely represent a string as an XPath literal."""
        if "'" not in value:
            return f"'{value}'"

        if '"' not in value:
            return f'"{value}"'

        parts = value.split("'")
        return "concat(" + ', "\'", '.join(
            f"'{part}'" for part in parts
        ) + ")"

    def is_error_message_visible(self, error: str) -> bool:
        return self.get_error_message(error).is_visible()

    def expect_error_message(self, error: str) -> None:
        expect(self.get_error_message(error)).to_be_visible()