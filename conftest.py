import pytest
from playwright.sync_api import Playwright
import datetime
from json import load

def pytest_addoption(parser):
    """hooks for global variables"""
    parser.addoption(
        "--browser_name", action = "store", default = "chrome", choices = ["firefox", "chrome"]
    )

@pytest.fixture(scope = "function")
def playwright_setup(playwright: Playwright, request):
    """fixture for the new instance of the playwright with setup and tear down"""
    browser_name = request.config.getoption("browser_name")

    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=True)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=True)

    context = browser.new_context()
    context.tracing.start(screenshots= True, snapshots = True)

    page = context.new_page()

    yield page

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