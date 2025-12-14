from playwright.sync_api import Page, expect, Locator

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

    def fill_shipping_info(self, info: str) -> None:
        """On this demo page, the shipping information requires only country which only accepts India"""
        select_country_btn: Locator = self.page.get_by_placeholder("Select Country")
        select_country_btn.fill(info)

    def press_create_order(self) -> None:
        create_order_btn: Locator = self.page.get_by_text("Place Order ")
        create_order_btn.click()

    def valdiate_toast_invalid_info_message(self) -> None:
        toast: Locator = self.page.locator("#toast-container")
        expect(toast).to_contain_text("Please Enter Full Shipping Information")