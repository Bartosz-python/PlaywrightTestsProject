import pytest
from playwright.sync_api import Playwright, Page
import datetime
import os

def pytest_addoption(parser):
    """hooks for global variables"""
    parser.addoption(
        "--browser_name", action = "store", default = "chrome", choices = ["firefox", "chrome", "webkit"]  
    )

@pytest.fixture(scope = "function")
def playwright_setup(playwright: Playwright, request):
    """fixture for the new instance of the playwright with setup and tear down"""
    browser_name = request.config.getoption("browser_name")

    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=False)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=True)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=True)

    context = browser.new_context()
    context.tracing.start(screenshots= True, snapshots = True)

    page: Page = context.new_page()
    page.set_default_navigation_timeout(20000)
    page.set_default_timeout(10000)

    try:
        yield page
    finally:
        os.makedirs("trace", exist_ok = True)

        context.tracing.stop(path = f"trace/{request.node.name}.zip")
        context.close()
        browser.close()

@pytest.fixture
def user_credentials(request):
    """returns currently used parameter with modifications if provided"""
    return request.param

def pytest_configure(config):
    timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = f"report/report_{timestamp}.html"