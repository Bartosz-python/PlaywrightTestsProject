import pytest
from playwright.sync_api import Playwright

def pytest_addotpion(parser):
    """hooks for global variables"""
    parser.addoption(
        "--browser_name", action = "store", default = "chrome", choices = ["firefox", "chrome"]
    )

@pytest.fixture
def playwright_setup(playwright: Playwright, request):
    """fixture for the new instance of the playwright with setup and tear down"""
    browser_name = request.config.getoption("browser_name")

    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=False)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()

    yield page

    context.close()
    browser.close()

@pytest.fixture
def user_credentials(request):
    """returns currently used parameter with modifications if provided"""
    return request.param