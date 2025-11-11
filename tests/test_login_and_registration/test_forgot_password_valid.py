from playwright.sync_api import expect
import os
from dotenv import load_dotenv
import pytest
from json import load
load_dotenv()

with open(os.getenv("DATA_PATH"), "r", encoding= "utf-8") as creds:
    data = load(creds)
    valid_credentials = data["credentials"]["valid_users"]

@pytest.mark.validation
@pytest.mark.parametrize("user_credentials", valid_credentials, indirect=True)
def test_valid_credentials_forgot_password(playwright_setup, user_credentials):
    try:
        from utils.pages.loginPage import LoginPage
    except ImportError as e:
        print(f"Error occurred during import of the object: {e}")
    
    loginPage: LoginPage = LoginPage(playwright_setup)
    loginPage.navigate()
    forgot_password_page = loginPage.swap_to_forgot_password()
    forgot_password_page.fill_credentials(user_credentials["userEmail"], user_credentials["userPassword"], user_credentials["userPassword"])
    forgot_password_page.save_new_password()

    loginPage.login(user_credentials["userEmail"], user_credentials["userPassword"])
    loginPage.sign_in()
    expect(loginPage.page).to_have_url(os.getenv("DASHBOARD_URL"))