from playwright.sync_api import expect, Playwright
from utils.pages.dashboardPage import DashboardPage
from utils.pages.cartPage import CartPage
from utils.api_utills.session_token import get_token
import pytest
import os
from dotenv import load_dotenv
load_dotenv()
from json import load
import re

with open(os.getenv("DATA_PATH"), "r", encoding="utf-8") as user_credentials:
    creds = load(user_credentials)
    user_credentials = creds["credentials"]["valid_users"]

@pytest.mark.regression
@pytest.mark.parametrize("user_credentials", user_credentials, indirect=True)
def test_add_item_to_cart(playwright: Playwright, playwright_setup, user_credentials):
    test_item: str = re.compile(re.escape("ZARA COAT 3"), re.IGNORECASE)

    token = get_token(playwright, user_credentials)
    
    dashboard_page: DashboardPage = DashboardPage(playwright_setup)
    dashboard_page.page.add_init_script(f"localStorage.setItem('token', '{token}')")
    dashboard_page.navigate()
    dashboard_page.add_item_to_cart(test_item)

    cart_page: CartPage = dashboard_page.goto_cart_page()
    
    cart_page.validate_item(test_item)