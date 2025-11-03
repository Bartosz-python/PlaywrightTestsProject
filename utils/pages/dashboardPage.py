from playwright.sync_api import Page

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page

    def add_item_to_cart(self, item: str):
        card = self.page.get_by_text(item)
        card_add_to_cart_btn = card.get_by_role("button", name = "Add To Cart")
        card_add_to_cart_btn.click()
    
    def goto_orders_page(self):
        self.page.get_by_role("button", name = "ORDERS")
    
    def goto_cart_page(self):
        self.page.get_by_role("button", name = "Cart")
