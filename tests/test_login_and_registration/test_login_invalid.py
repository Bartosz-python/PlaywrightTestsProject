from playwright.sync_api import expect, Locator
from json import load
import pytest
from dotenv import load_dotenv
import os
load_dotenv()

with open(os.getenv("DATA_PATH"), "r", encoding= "utf-8") as creds:
    data = load(creds)
    invalid_credentials = data["credentials"]["invalid_users"]


@pytest.mark.validation
@pytest.mark.parametrize("user_credentials", invalid_credentials, indirect=True)
def test_invalid_credentials(playwright_setup, user_credentials):
    try:
        from utils.pages.loginPage import LoginPage
    except ImportError as e:
        print(f"Error occurred during import of the object: {e}")

    loginPage: LoginPage = LoginPage(playwright_setup)
    loginPage.navigate()
    logging_with_credentials: LoginPage = loginPage.login(user_credentials["userEmail"], 
                                                          user_credentials["userPassword"])
    logging_with_credentials.sign_in()

    toast_popup: Locator = loginPage.page.locator("div.toast-container")

    expect(loginPage.page).to_have_url(os.getenv("LOGIN_PAGE_URL"))
    expect(toast_popup).to_be_visible()
    expect(toast_popup).to_contain_text("Incorrect email or password.") 
    # TODO API test to check payload content being correct