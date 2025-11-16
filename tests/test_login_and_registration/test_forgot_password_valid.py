from playwright.sync_api import expect
import os
from dotenv import load_dotenv
import pytest
load_dotenv()
import random, string
from typing import LiteralString

@pytest.mark.validation
def test_valid_credentials_forgot_password(playwright_setup):
    """Custom user is desired to be exclusive for this test"""
    try:
        from utils.pages.forgotPasswordPage import ForgotPasswordPage
        from utils.pages.loginPage import LoginPage
    except ImportError as e:
        print(f"Error occurred during import of the object: {e}")

    random_password: LiteralString = "".join((random.choice(string.ascii_letters + string.ascii_uppercase + string.digits) 
                                              for _ in range(10)))
    
    loginPage: LoginPage = LoginPage(playwright_setup)
    loginPage.navigate()
    forgot_password_page: ForgotPasswordPage = loginPage.swap_to_forgot_password()
    forgot_password_page.fill_credentials(email = os.getenv("USER_EMAIL_FORGOT_PASSWORD_TEST"),
                                          password = random_password,
                                          confirm_password = random_password)
    forgot_password_page.save_new_password()

    expect(forgot_password_page.page).to_have_url(os.getenv("LOGIN_PAGE_URL"))
    expect(loginPage.page.locator("div.toast-container")).to_contain_text("Password Changed Successfully")

    login_to_dashboard_page: LoginPage = loginPage.login(os.getenv("USER_EMAIL_FORGOT_PASSWORD_TEST"), 
                                                         random_password)
    login_to_dashboard_page.sign_in()

    expect(login_to_dashboard_page.page).to_have_url(os.getenv("DASHBOARD_URL"))