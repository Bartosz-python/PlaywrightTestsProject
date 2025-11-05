from dotenv import load_dotenv
import os
from playwright.sync_api import Page, ElementHandle, Locator
from typing import Self

load_dotenv()

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self) -> None:
        self.page.goto(os.getenv("URL"))

    def login(self, email: str, password: str) -> Self:
        emailInputField: ElementHandle | None = self.page.query_selector("#userEmail")
        emailInputField.fill(email)

        passwordInputField: ElementHandle | None = self.page.query_selector("#userPassword")
        passwordInputField.fill(password)
        return self

    def sign_in(self) -> None:
        sign_in_btn: Locator = self.page.get_by_role("button", name = "Login")
        sign_in_btn.click()

    def swap_to_registration(self):
        register_btn: ElementHandle | None = self.page.query_selector(".btn1")
        register_btn.click()
        from pages.registrationPage import RegistrationPage
        return RegistrationPage(self.page)
        