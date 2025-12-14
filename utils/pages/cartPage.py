from playwright.sync_api import Page, Locator, expect
from typing import Pattern
from .checkoutPage import CheckoutPage

class CartPage:
    def __init__(self, page: Page):
        self.page = page

    def validate_item_in_cart(self, item: str | Pattern[str]) -> None:
        locate_item: Locator = self.page.get_by_text(item)
        expect(locate_item).to_be_visible()

    def locate_item_id(self, id: str) -> Locator:
        locate_id: Locator = self.page.get_by_text(f"#{id}")
        return locate_id
    
    def press_checkout(self) -> CheckoutPage:
        checkout_btn: Locator = self.page.get_by_role("button", name = "Checkout")
        checkout_btn.click()
        return CheckoutPage(self.page)