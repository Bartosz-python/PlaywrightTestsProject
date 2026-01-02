from playwright.sync_api import expect
from utils.pages.loginPage import LoginPage
from utils.pages.registrationPage import RegistrationData, RegistrationPage
from utils.pages.dashboardPage import DashboardPage
from dotenv import load_dotenv
load_dotenv()
import os
import pytest
import random
import string

@pytest.mark.regression
def test_registration_valid_data(playwright_setup):
    #TODO fetch test data from seperate json or similar
    #TODO add ID field
    #TODO migrate RegistrationData to utils
    registration_data: RegistrationData = RegistrationData(
        first_name="".join(random.choice(string.ascii_uppercase + string.ascii_letters) for _ in range(10)),
        last_name="".join(random.choice(string.ascii_letters + string.ascii_uppercase) for _ in range(10)),
        email="".join(random.choice(string.ascii_letters + string.ascii_uppercase) for _ in range(10)) + "@gmail.com",
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

    login_page_again: LoginPage = registration_page.submit()

    expect(login_page_again.page).to_have_url(os.getenv("LOGIN_PAGE_URL"))

    login_page_again.login(email = registration_data.email, password = registration_data.password)

    dashboard_page: DashboardPage = login_page_again.sign_in()

    #? Temporary saving created test accounts to the seperate file
    with open("data/registeredTestUsers.txt", "a", encoding="utf-8") as registered_test_users_file:
        registered_test_users_file.write(f"{repr(registration_data)}\r\n")

    expect(dashboard_page.page).to_have_url(os.getenv("DASHBOARD_URL"))