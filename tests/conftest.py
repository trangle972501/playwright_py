from datetime import datetime
import pytest
from playwright.sync_api import Page, Browser, expect
from utils.logger import get_logger
import os
from constants.timeouts import TIMEOUTS

logger = get_logger(__name__)

def pytest_addoption(parser):
    parser.addini("base_url", help="Base URL for tests", default="https://www.automationexercise.com/")

# Assertion timeout: needs to be set at module level, takes effect globally
expect.set_options(timeout=TIMEOUTS["EXPECT_TIMEOUT"])

#Add lunch browser fixture
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": ["--start-maximized"],
    }

'''
Disables Playwright's default fixed viewport (1280×720). 
Without disabling the viewport, the browser will appear maximized but the page will still render at the small window size
'''
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "no_viewport": True,
    }

@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getini("base_url")

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    page.set_default_timeout(TIMEOUTS["DEFAULT_TIMEOUT"])
    page.set_default_navigation_timeout(TIMEOUTS["DEFAULT_NAVIGATION_TIMEOUT"])
    yield page

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    # Only take a screenshot if the test failed during the call phase (not setup or teardown errors)
    if rep.when == "call" and rep.failed:
        # Access the 'page' fixture from the test function's arguments
        page: Page = item.funcargs.get("page")
        if page:
            #1. Prepare a directory for screenshots if it doesn't exist
            # (Use the directory name "screenshots" in the current working directory)
            html_path = item.config.getoption("--html", default="report.html")
            report_dir = os.path.dirname(os.path.abspath(html_path)) or "."
            screenshot_dir = os.path.join(report_dir, "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

            #2. Create a unique filename for the screenshot based on the test node
            clean_name = item.name.replace(":", "_").replace("/", "_").replace("[", "_").replace("]", "_")
            file_name = f"fail_{clean_name}_{datetime.now().strftime('%H%M%S')}.png"
            file_path = os.path.join(screenshot_dir, file_name)

            # 3. Take the screenshot
            page.screenshot(path=file_path)

            # 4. Attach it to the pytest-html report
            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                # Use a relative path so the HTML can locate the image
                relative_path = os.path.join("screenshots", file_name)
                extra = getattr(rep, "extras", [])
                # Embed an <img> tag that opens full-size on click
                html = (
                    f'<div><img src="{relative_path}" alt="screenshot" '
                    f'style="width:25%;height:228px;" '
                    f'onclick="window.open(this.src)" align="right"/></div>'
                )
                extra.append(pytest_html.extras.html(html))
                rep.extras = extra


