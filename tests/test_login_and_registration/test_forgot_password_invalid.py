from playwright.sync_api import expect
import os
from dotenv import load_dotenv
import pytest
from json import load
load_dotenv()

with open(os.getenv("DATA_PATH"), "r", encoding= "utf-8") as creds:
    data = load(creds)
    invalid_credentials = data["credentials"]["invalid_users"]

# @pytest.mark.validation
# @pytest.mark.parametrize("user_credentials", invalid_credentials, indirect=True)
# def test_invalid_credentials_forgot_password(playwright_setup, user_credentials):
#     try:
#         from utils.pages.loginPage import LoginPage
#     except ImportError as e:
#         print(f"Error occurred during import of the object: {e}")
    
#     loginpage: LoginPage = LoginPage(playwright_setup)
#     forgot_password_page = loginpage.swap_to_forgot_password()
#     forgot_password_page.fill_credentials(user_credentials["userEmail"], user_credentials["userPassword"], user_credentials["userPassword"])
#     forgot_password_page.save_new_password()

    #! Bug - feature changes password to whatever password is given in the password field
    #? Test will be automated once the issue will be resolved.

