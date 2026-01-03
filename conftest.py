import pytest
from playwright.sync_api import Playwright, Page
import datetime
import os
import requests, json
from requests import Response
from dotenv import load_dotenv
load_dotenv()

# Load data once at module level
with open(os.getenv("DATA_PATH"), "r", encoding="utf-8") as creds:
    data: dict = json.load(creds)
    valid_user_credentials: dict[str, str] = data["credentials"]["valid_users"][1]

@pytest.fixture(scope="session")
def url_login() -> str:
    return f"{os.getenv('URL')}{os.getenv('LOGIN_ENDPOINT')}"

@pytest.fixture(scope="session")
def payload_credentials() -> dict[str, str]:
    return {
        "userEmail": valid_user_credentials["userEmail"],
        "userPassword": valid_user_credentials["userPassword"]
    }

@pytest.fixture(scope="session")
def headers_login() -> dict[str, str]:
    return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0"}

@pytest.fixture(scope="session")
def auth_token_and_user_id(url_login: str, payload_credentials: dict[str, str], headers_login: dict[str, str]) -> tuple[str, str]:
    response: Response = requests.post(url=url_login, data=payload_credentials, headers=headers_login)
    
    try:
        assert response.status_code == 200, f"Login failed: {response.status_code} - {response.text}"
        
        response_body = response.json()
        token = response_body.get("token")
        user_id = response_body.get("userId")
        
        assert token, "Token missing in response"
        assert user_id, "User ID missing in response"
        
        return token, user_id
    except (requests.RequestException, ValueError) as e:
        pytest.fail(f"Login error: {e}")
    finally:
        response.close()

def pytest_addoption(parser) -> None:
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