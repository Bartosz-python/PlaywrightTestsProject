from playwright.sync_api import Page, expect
from typing import List

class OrdersDetailPage:
    def __init__(self, page: Page):
        self.page = page

    def address_details(self) -> List[str]:
        address_object = self.page.locator(".address")
        address_items = address_object.all_text_contents()[1:]
        return address_items
    
    def verify_ordered_product_title(self, title: str) -> None:
        expect(self.page.locator(".title")).to_have_text(title)