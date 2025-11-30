from playwright.sync_api import Page, Locator, TimeoutError as pr_timeout_error
from dataclasses import dataclass, field
from typing import Literal, Self, List
from .loginPage import LoginPage
import os
from dotenv import load_dotenv
load_dotenv()

@dataclass
class RegistrationData:
    """Registration data model for the arguments of the fill_form method of the RegistrationPage object"""
    first_name: str
    last_name: str
    email: str
    phone_number: int        
    occupation: Literal["Doctor", "Student", "Engineer", "Scientist"]
    gender: Literal["Male", "Female"]
    password: str
    confirm_password: str
    confirmation_checkbox: bool


class RegistrationPage:
    def __init__(self, page: Page):
        self.page = page

    @property
    def first_name_input(self) -> Locator: return self.page.locator('input[placeholder="First Name"]')
    @property
    def last_name_input(self) -> Locator: return self.page.locator('input[placeholder="Last Name"]')
    @property
    def email_input(self) -> Locator: return self.page.locator('#userEmail')
    @property
    def phone_input(self) -> Locator: return self.page.locator('input[placeholder="enter your number"]')
    @property
    def occupation_dropdown(self) -> Locator: return self.page.locator('select')
    @property
    def gender_male_radio(self) -> Locator: return self.page.get_by_label("Male", exact=True)
    @property
    def gender_female_radio(self) -> Locator: return self.page.get_by_label("Female", exact=True)
    @property
    def password_input(self) -> Locator: return self.page.locator('#userPassword')
    @property
    def confirm_password_input(self) -> Locator: return self.page.locator('#confirmPassword')
    @property
    def confirmation_checkbox(self) -> Locator: return self.page.get_by_role("checkbox")
    @property
    def register_button(self) -> Locator: return self.page.get_by_role("button", name="Register")

    def fill_form(self, data: RegistrationData) -> Self:

        self.first_name_input.fill(data.first_name)
        self.last_name_input.fill(data.last_name)
        self.email_input.fill(data.email)
        self.phone_input.fill(str(data.phone_number))
        self.occupation_dropdown.select_option(data.occupation)

        if data.gender.lower() == "male":
            self.gender_male_radio.check()
        elif data.gender.lower() == "female":
            self.gender_female_radio.check()

        self.password_input.fill(data.password)
        self.confirm_password_input.fill(data.confirm_password)

        if data.confirmation_checkbox:
            self.confirmation_checkbox.check()

        return self
    
    def submit(self) -> LoginPage | Self:
        register_btn: Locator = self.page.get_by_role("button", name = "Register")
        register_btn.click()
        try:
            self.page.wait_for_url(os.getenv("LOGIN_PAGE_URL"))
            return LoginPage(self.page)
        except pr_timeout_error:
            return self