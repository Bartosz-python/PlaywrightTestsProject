from utils.pages.dashboardPage import DashboardPage
from utils.pages.cartPage import CartPage
from utils.pages.checkoutPage import CheckoutPage
from utils.api_utills.session_token import get_token
import os, re, pytest
from dotenv import load_dotenv
load_dotenv()
from typing import Pattern
from playwright.sync_api import expect, Playwright
from json import load

with open(os.getenv("DATA_PATH"), "r", encoding="utf-8") as creds:
    data = load(creds)
    valid_user_credentials = data["credentials"]["valid_users"]

@pytest.mark.validation
@pytest.mark.parametrize("user_credentials", valid_user_credentials, indirect=True)
def test_order_item_invalid(playwright: Playwright, playwright_setup, user_credentials):
    token = get_token(playwright, user_credentials)
    product_item: Pattern[str] = re.compile(re.escape("ZARA COAT 3"), re.IGNORECASE)

    dashboard_page: DashboardPage = DashboardPage(playwright_setup)
    dashboard_page.page.add_init_script(f"localStorage.setItem('token', '{token}')")
    dashboard_page.navigate()
    dashboard_page.add_item_to_cart(product_item)

    cart_page: CartPage = dashboard_page.goto_cart_page()
    cart_page.validate_item_in_cart(product_item)

    checkout_page: CheckoutPage = cart_page.press_checkout()
    checkout_page.fill_shipping_info("India")
    checkout_page.press_create_order()

    checkout_page.valdiate_toast_invalid_info_message()