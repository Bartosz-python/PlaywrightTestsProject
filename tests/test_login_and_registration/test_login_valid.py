from playwright.sync_api import expect
from json import load
import pytest
from dotenv import load_dotenv
import os
load_dotenv()

with open(os.getenv("DATA_PATH"), "r", encoding= "utf-8") as creds:
    data = load(creds)
    valid_credentials = data["credentials"]["valid_users"]

@pytest.mark.smoke
@pytest.mark.parametrize("user_credentials", valid_credentials, indirect=True)
def test_valid_credentials(playwright_setup, user_credentials):
    try:
        from utils.pages.loginPage import LoginPage
    except ImportError as e:
        print(f"Error occurred during import of the object: {e}")

    loginPage: LoginPage = LoginPage(playwright_setup)
    loginPage.navigate()
    logging_with_credentials: LoginPage = loginPage.login(user_credentials["userEmail"], user_credentials["userPassword"])
    logging_with_credentials.sign_in()

    expect(loginPage.page).to_have_url(os.getenv("DASHBOARD_URL"))