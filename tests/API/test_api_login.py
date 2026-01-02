import requests
from requests import Response
from dotenv import load_dotenv
load_dotenv()
import os
from json import load
import pytest
from playwright.sync_api import Playwright
from utils.api_utills.session_token import get_token

with open(os.getenv("DATA_PATH"), "r", encoding="utf-8") as creds:
    data: list[dict[str]] = load(creds)
    valid_user_credentials: dict[str, str] = data["credentials"]["valid_users"]
    valid_single_user_credentials: dict[str, str] = data["credentials"]["valid_users"][0]

@pytest.mark.smoke
@pytest.mark.parametrize("user_credentials", valid_user_credentials, indirect=True)
def test_api_login_valid_data(playwright: Playwright, user_credentials):
    """This test is generic as api util 'token' is already making an API call and retrieves a token"""
    token: str = get_token(playwright, user_credentials)

    url = f"{os.getenv("URL")}{os.getenv("LOGIN_ENDPOINT")}"
    data = {"userEmail": user_credentials["userEmail"], "userPassword": user_credentials["userPassword"]}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0"}
    
    response: Response = requests.post(url = url, 
                                       data = data,
                                       headers = headers)
    assert response.status_code == 200    
    assert token is not None
    assert "token" in response.json()

@pytest.mark.regression
def test_api_login_invalid_password():

    wrong_password_test: str = "test_password123"

    url = f"{os.getenv("URL")}{os.getenv("LOGIN_ENDPOINT")}"
    data = {"userEmail": valid_single_user_credentials["userEmail"], "userPassword": wrong_password_test}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
               "Content-Type": "application/json"}

    response: Response = requests.post(url = url,
                                       json = data,
                                       headers = headers)
    
    assert response.status_code == 401 #Unauthtorized
    #! Test pokazuje ze login endpoint zwraca 400 przy niepoprawnym haśle.
    print(response.headers["Authorization"])