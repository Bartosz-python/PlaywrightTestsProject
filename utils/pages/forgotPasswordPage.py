from playwright.sync_api import Page, Locator

class ForgotPasswordPage:
    def __init__(self, page: Page):
        self.page = page

    def fill_credentials(self, email: str, password: str, confirm_password: str) -> None:
        email_field: Locator = self.page.query_selector("input[placeholder='Enter your email address']")
        email_field.fill(email)

        password_field: Locator = self.page.locator("#userPassword")
        password_field.fill(password)

        confirm_password_field = self.page.locator("#confirmPassword")
        confirm_password_field.fill(confirm_password)
    
    def save_new_password(self) -> None:
        save_btn = self.page.get_by_role("button", name = "Save New Password")
        save_btn.click()