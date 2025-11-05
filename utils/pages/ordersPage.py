from playwright.sync_api import Page, expect, Locator
from typing import List

class OrdersPage:
    def __init__(self, page: Page):
        self.page = page

    def verify_no_orders_message(self) -> None:
        expect(self.page.get_by_text(" You have No Orders to show at this time.")).to_be_visible()
    
    def go_back_to_shop_btn(self) -> None:
        to_shop_btn = self.page.get_by_role("button", name = "Go Back to Shop")
        to_shop_btn.click()
    
    def go_back_to_cart_btn(self) -> None:
        to_cart_btn = self.page.get_by_role("button", name = "Go Back to Cart")
        to_cart_btn.click()

    def pick_table_row_via_order_id(self, order_id: str) -> Locator:
        row = self.page.locator("tr").filter(has_text = order_id)
        return row
    
    def row_items_via_id(self, order_id: str) -> List[str]:
        # TODO distribute items to distinct variables
        row = self.pick_table_row_via_order_id(order_id)
        row_items = row.all_inner_texts()
        return row_items
    
    def show_details_via_orderId(self, order_id: str) -> None:
        row = self.pick_table_row_via_order_id(order_id)
        orders_view_btn = row.get_by_role("button", name = "View")
        orders_view_btn.click()
    
    def delete_row_via_order_id(self, order_id: str) -> None:
        row = self.pick_table_row_via_order_id(order_id)
        delete_btn = row.get_by_role("button", name = "Delete")
        delete_btn.click()