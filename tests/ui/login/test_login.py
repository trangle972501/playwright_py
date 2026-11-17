EMAIL =  "trangle972501+1@gmail.com"
PASSWORD =  "123456789"

from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)

class TestLogin:
    def test_login_successfully(self, login_page: LoginPage):
        logger.info("Test started: successful login")
        login_page.login(EMAIL, PASSWORD)
        login_page.header.expect_logout_button()
        logger.info("Test passed: successful login")

    def test_login_with_invalid_email(self, login_page: LoginPage):
        login_page.login("invalid_email@example.com", PASSWORD)
        login_page.expect_error_message(
            "Your email or password is incorrect hahah!"
        )

    def test_login_with_invalid_password(self, login_page: LoginPage):
        login_page.login(EMAIL, "invalid_password")
        login_page.expect_error_message(
            "Your email or password is incorrect!"
        )
