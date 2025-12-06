from playwright.sync_api import expect, Playwright
from utils.pages.dashboardPage import DashboardPage
from utils.pages.cartPage import CartPage
import pytest
import os
from dotenv import load_dotenv
load_dotenv()
from json import load
from utils.api_utills.session_token import get_token

with open(os.getenv("DATA_PATH"), "r", encoding="utf-8") as creds:
    data = load(creds)
    user_credentials = data["credentials"]["valid_users"]
    item_id = data["payloads"]["request_payloads"][0]["product"]["_id"]

@pytest.mark.regression
@pytest.mark.parametrize("user_credentials", user_credentials, indirect=True)
def test_if_item_id_is_visible(playwright_setup, playwright: Playwright, user_credentials):
    token = get_token(playwright, user_credentials)

    dashboard_page: DashboardPage = DashboardPage(playwright_setup)
    dashboard_page.page.add_init_script(f"localStorage.setItem('token','{token}')")
    dashboard_page.navigate()

    dashboard_page.add_item_to_cart("ZARA COAT 3")
    
    cart_page: CartPage = dashboard_page.goto_cart_page()
    
    expect(cart_page.locate_item_id(item_id)).to_be_visible()