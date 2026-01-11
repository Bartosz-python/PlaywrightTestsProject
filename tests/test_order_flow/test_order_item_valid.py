from playwright.sync_api import expect, Playwright
import os, re, pytest
from dotenv import load_dotenv
load_dotenv()
from utils.pages.dashboardPage import DashboardPage
from utils.pages.ordersPage import OrdersPage
from utils.pages.ordersDetailsPage import OrdersDetailPage
from utils.api_utills.session_token import create_order, get_token
from json import load
from typing import Pattern

with open(os.getenv("DATA_PATH"), "r", encoding="utf-8") as creds:
    data = load(creds)
    valid_credentials = data["credentials"]["valid_users"]

@pytest.mark.regression
@pytest.mark.parametrize("user_credentials", valid_credentials, indirect=True)
def test_order_item_valid(playwright_setup, playwright: Playwright, user_credentials):
    order_id: str = create_order(playwright, user_credentials)
    token: str = get_token(playwright, user_credentials)
    product_header: Pattern[str] = re.compile(re.escape("ZARA COAT 3"), re.IGNORECASE)

    dashboard_page: DashboardPage = DashboardPage(playwright_setup)
    dashboard_page.page.add_init_script(f"localStorage.setItem('token', '{token}')")
    
    dashboard_page.navigate()
    orders_page: OrdersPage = dashboard_page.goto_orders_page()
    order_details_page: OrdersDetailPage = orders_page.show_details_via_orderId(order_id)
    
    order_details_page.verify_ordered_product_title(product_header)
    expect(order_details_page.page).to_have_url(os.getenv("CURRENT_ORDER_DETAILS_URL") + order_id)