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
        from utils.pages.forgotPasswordPage import ForgotPasswordPage
        from utils.pages.loginPage import LoginPage
    except ImportError as e:
        print(f"Error occurred during import of the object: {e}")
    
    loginPage: LoginPage = LoginPage(playwright_setup)
    loginPage.navigate()
    forgot_password_page: ForgotPasswordPage = loginPage.swap_to_forgot_password()
    forgot_password_page.fill_credentials(user_credentials["userEmail"], user_credentials["userPassword"], user_credentials["userPassword"])
    forgot_password_page.save_new_password()

    expect(playwright_setup).to_have_url(os.getenv("LOGIN_PAGE_URL"))
    expect(loginPage.page.locator("div.toast-container")).to_contain_text("Password Changed Successfully")

    back_to_login_page: LoginPage = loginPage.login(user_credentials["userEmail"], user_credentials["userPassword"])
    back_to_login_page.sign_in()

    expect(playwright_setup).to_have_url(os.getenv("DASHBOARD_URL"))