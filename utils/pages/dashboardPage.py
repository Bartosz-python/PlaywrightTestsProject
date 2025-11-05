from playwright.sync_api import Page, Locator

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page

    def add_item_to_cart(self, item: str) -> None:
        card = self.page.get_by_text(item)
        card_add_to_cart_btn: Locator = card.get_by_role("button", name = "Add To Cart")
        card_add_to_cart_btn.click()
    
    def goto_orders_page(self) -> None:
        orders_btn: Locator = self.page.get_by_role("button", name = "ORDERS")
        orders_btn.click()
    
    def goto_cart_page(self) -> None:
        cart_page: Locator = self.page.get_by_role("button", name = "Cart")
        cart_page.click()