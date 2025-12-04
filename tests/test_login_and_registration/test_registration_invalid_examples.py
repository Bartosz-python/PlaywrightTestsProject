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
def test_registration_invalid_email(playwright_setup):
    #TODO move RegistrationData to utils
    registration_data = RegistrationData(
        first_name="".join(random.choice(string.ascii_uppercase + string.ascii_letters) for _ in range(10)),
        last_name="".join(random.choice(string.ascii_letters + string.ascii_uppercase) for _ in range(10)),
        email="".join(random.choice(string.ascii_letters + string.ascii_uppercase) for _ in range(10)) + "gmail.com",
        phone_number= int("".join(random.choice(string.digits) for _ in range(10))),
        occupation="Engineer",
        gender="Male",
        password="randomPassword123!!",
        confirm_password ="randomPassword123!!",
        confirmation_checkbox=True 
    )
    login_page: LoginPage = LoginPage(playwright_setup)
    login_page.navigate()
    registration_page: RegistrationPage = login_page.swap_to_registration()
    
    registration_page.fill_form(registration_data)
    registration_page.submit()

    email_error_locator: Locator = registration_page.page.get_by_text("*Enter Valid Email")
    expect(email_error_locator).to_be_visible(timeout = 5000)
    expect(email_error_locator).to_contain_text("*Enter Valid Email")


@pytest.mark.validation
def test_registration_empty_form(playwright_setup):
    login_page: LoginPage = LoginPage(playwright_setup)
    login_page.navigate()
    registration_page: RegistrationPage = login_page.swap_to_registration()
    
    registration_page.submit()

    first_name_error: Locator = registration_page.page.get_by_text("*First Name is required")
    phone_number_error: Locator = registration_page.page.get_by_text("*Phone Number is required")
    password_error: Locator = registration_page.page.get_by_text("*Password is required")
    confirm_password_error: Locator = registration_page.page.get_by_text("Confirm Password is required")
    checbox_error: Locator = registration_page.page.get_by_text("*Please check above checkbox")
    email_error_locator: Locator = registration_page.page.get_by_text("*Email is required")

    expect(first_name_error).to_be_visible(timeout = 5000)
    expect(phone_number_error).to_be_visible(timeout = 5000)
    expect(password_error).to_be_visible(timeout = 5000)
    expect(confirm_password_error).to_be_visible(timeout = 5000)
    expect(checbox_error).to_be_visible(timeout = 5000)
    expect(email_error_locator).to_be_visible(timeout = 5000)