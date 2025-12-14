from playwright.sync_api import Page, Locator
import os
from .cartPage import CartPage
from .ordersPage import OrdersPage
from dotenv import load_dotenv
load_dotenv()
from typing import Pattern

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self) -> None:
        self.page.goto(os.getenv("DASHBOARD_URL"))

    def add_item_to_cart(self, item: str | Pattern[str]) -> None:
        card = self.page.locator(".card-body").filter(has_text=item)
        card_add_to_cart_btn: Locator = card.get_by_role("button", name = "Add To Cart")
        card_add_to_cart_btn.click()
    
    def goto_orders_page(self) -> OrdersPage:
        orders_btn: Locator = self.page.get_by_role("button", name = "ORDERS")
        orders_btn.click()

        return OrdersPage(self.page)
    
    def goto_cart_page(self) -> CartPage:
        cart_page_btn: Locator = self.page.get_by_text("  Cart ", exact=True)
        cart_page_btn.scroll_into_view_if_needed()
        cart_page_btn.click()
        
        return CartPage(self.page)