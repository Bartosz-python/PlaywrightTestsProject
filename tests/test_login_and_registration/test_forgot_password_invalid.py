from playwright.sync_api import expect
import pytest
import random
import string

@pytest.mark.validation
def test_invalid_credentials_forgot_password(playwright_setup):
    try:
        from utils.pages.loginPage import LoginPage
    except ImportError as e:
        print(f"Error occurred during import of the object: {e}")
    
    random_email_name = "".join(random.choice(string.ascii_letters + string.ascii_uppercase + string.digits) 
                                for _ in range(20))
    random_email = f"{random_email_name}@gmail.com"
    some_password = "123"
    
    loginpage: LoginPage = LoginPage(playwright_setup)
    loginpage.navigate()
    forgot_password_page = loginpage.swap_to_forgot_password()
    forgot_password_page.fill_credentials(email = random_email, 
                                          password = some_password, 
                                          confirm_password = some_password)
    forgot_password_page.save_new_password()

    user_not_found_toast = forgot_password_page.page.locator("#toast-container")

    expect(user_not_found_toast).to_be_visible()
    expect(user_not_found_toast).to_contain_text("User Not found.")