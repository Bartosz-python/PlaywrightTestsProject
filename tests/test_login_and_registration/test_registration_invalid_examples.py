from utils.pages.loginPage import LoginPage
from utils.pages.registrationPage import RegistrationPage, RegistrationData 
import os
from dotenv import load_dotenv
load_dotenv()
from playwright.sync_api import expect, Locator
import pytest
import random
import string

@pytest.mark.validation
def test_registration_invalid_data(playwright_setup, request):
    #TODO Seed random values from outside csv or similar file
    registration_data = RegistrationData(
        first_name="".join(random.choice(string.ascii_uppercase + string.ascii_letters) for _ in range(10)),
        last_name="".join(random.choice(string.ascii_letters + string.ascii_uppercase) for _ in range(10)),
        email="".join(random.choice(string.ascii_letters + string.ascii_uppercase) for _ in range(10)) + "gmail.com",
        phone_number= int("".join(random.choice(string.digits) for _ in range(10))),
        occupation="Engineer",
        gender="Male",
        password="randomPassword123!!",
        confirm_password = "randomPassword123!!",
        confirmation_checkbox=True 
    )
    login_page: LoginPage = LoginPage(playwright_setup)
    login_page.navigate()
    registration_page: RegistrationPage = login_page.swap_to_registration()
    
    registration_page.fill_form(registration_data)
    email_error = registration_page.submit()
    email_error_locator: Locator = email_error.page.get_by_text("*Enter Valid Email") 
    expect(email_error_locator).to_be_visible(timeout = 5000)
    expect(email_error_locator).to_contain_text("*Enter Valid Email") #TODO fix selector
    email_error_locator.highlight()