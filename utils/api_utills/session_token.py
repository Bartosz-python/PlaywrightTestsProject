from playwright.sync_api import Playwright, APIRequestContext, APIResponse, Page
from dotenv import load_dotenv
import os
from typing import Any
load_dotenv()

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