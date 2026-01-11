from playwright.sync_api import Playwright
from utils.pages.dashboardPage import DashboardPage
from utils.pages.ordersPage import OrdersPage
from utils.api_utills.session_token import get_token
import os
from dotenv import load_dotenv
load_dotenv()
import pytest
from json import load

with open(os.getenv("DATA_PATH"), "r", encoding="utf-8") as creds:
    data = load(creds)
    json_mock_orders_payload = data["payloads"]["response_payloads"]

def intercept_response(route):
    route.fulfill(
        json=json_mock_orders_payload
    )

@pytest.mark.regression
def test_empty_orders_message(playwright_setup, auth_token_and_user_id):
    token, user_id = auth_token_and_user_id

    dashboard_page: DashboardPage = DashboardPage(playwright_setup)
    dashboard_page.page.add_init_script(f"localStorage.setItem('token', '{token}')")
    dashboard_page.page.route(f"{os.getenv("URL")}{os.getenv("GET_ORDERS")}{user_id}", intercept_response)
    dashboard_page.navigate()
    
    orders_page: OrdersPage = dashboard_page.goto_orders_page()
    orders_page.page.wait_for_load_state("networkidle")
    orders_page.verify_no_orders_message()