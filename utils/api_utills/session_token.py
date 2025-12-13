from playwright.sync_api import Playwright, APIRequestContext, APIResponse
from dotenv import load_dotenv
import os
from typing import Any
load_dotenv()
import json

with open(os.getenv("DATA_PATH"), "r", encoding="utf-8") as creds:
    data = json.load(creds)
    mock_payload_for_create_api = data["payloads"]["request_payloads"][1]["orders"] #! To fix, wrongly fetched data to variable

def get_token(playwright: Playwright, user_credentials) -> str | Any:
    """Function that returns session token for the logged user"""
    api_context: APIRequestContext = playwright.request.new_context(base_url = os.getenv("URL"))
    response: APIResponse = api_context.post(url = os.getenv("LOGIN_ENDPOINT"),
                                                   data = {"userEmail": user_credentials["userEmail"],
                                                           "userPassword": user_credentials["userPassword"]})
    assert response.ok

    response_body = response.json()
    token: str = response_body["token"]
    
    api_context.dispose()
    return token


def create_order(playwright: Playwright, user_credentials: list[dict[str, str]]) -> str:
    """Create order via respective API post request"""
    token: str = get_token(playwright, user_credentials)

    request_create_order_context: APIRequestContext = playwright.request.new_context(base_url=os.getenv("URL"))
    create_order_api_response: APIResponse = request_create_order_context.post(
                                                                                url = os.getenv("CREATE_ORDER"),
                                                                                data = mock_payload_for_create_api,
                                                                                headers = {"Authorization" : token,
                                                                                          "Content-Type": "application/json"})
    assert create_order_api_response.status == 201

    responseBody = create_order_api_response.json()
    order_id: str = responseBody["orders"][0]

    request_create_order_context.dispose()
    return order_id