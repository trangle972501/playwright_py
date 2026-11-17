
from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from utils.logger import get_logger
from constants.timeouts import TIMEOUTS

logger = get_logger(__name__)


def pytest_addoption(parser):
    parser.addini(
        "base_url",
        help="Base URL for tests",
        default="https://www.automationexercise.com/"
    )


# Global assertion timeout
expect.set_options(timeout=TIMEOUTS["EXPECT_TIMEOUT"])


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, request):
    """
    Configure browser launch arguments.

    Headed mode: maximize browser window.
    Headless mode: use default launch arguments.
    """
    args = list(browser_type_launch_args.get("args", []))

    if request.config.getoption("--headed"):
        args.append("--start-maximized")

    return {
        **browser_type_launch_args,
        "args": args,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, request):
    """
    Configure browser viewport.

    Local headed execution: use actual browser window size.
    CI headless execution: use fixed viewport.
    """
    if request.config.getoption("--headed"):
        return {
            **browser_context_args,
            "no_viewport": True,
        }

    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720,
        },
    }


@pytest.fixture(scope="session")
def base_url(pytestconfig):
    return pytestconfig.getini("base_url")


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()

    page.set_default_timeout(TIMEOUTS["DEFAULT_TIMEOUT"])
    page.set_default_navigation_timeout(
        TIMEOUTS["DEFAULT_NAVIGATION_TIMEOUT"]
    )

    yield page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshots when a test fails and attach them
    to pytest-html reports.
    """
    outcome = yield
    report = outcome.get_result()

    # Capture screenshots only for test execution failures
    if report.when != "call" or not report.failed:
        return

    # Get page fixture
    page: Page = item.funcargs.get("page")

    if page is None:
        logger.warning(
            "Cannot capture screenshot: page fixture not available for %s",
            item.nodeid
        )
        return

    try:
        # Create screenshot directory
        screenshot_dir = Path("test-results") / "screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique screenshot filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        clean_name = (
            item.nodeid
            .replace("/", "_")
            .replace("::", "_")
            .replace("[", "_")
            .replace("]", "_")
            .replace(":", "_")
        )

        file_name = f"failed_{clean_name}_{timestamp}.png"
        file_path = screenshot_dir / file_name

        # Capture screenshot
        page.screenshot(
            path=str(file_path),
            full_page=True
        )

        logger.info(
            "Failure screenshot saved: %s",
            file_path
        )

        # Attach screenshot to pytest-html report
        pytest_html = item.config.pluginmanager.getplugin("html")

        if pytest_html:
            extra = getattr(report, "extras", [])

            extra.append(
                pytest_html.extras.image(
                    str(file_path),
                    name=f"Failure screenshot: {item.name}"
                )
            )

            report.extras = extra

    except Exception:
        logger.exception(
            "Failed to capture or attach failure screenshot for %s",
            item.nodeid
        )
