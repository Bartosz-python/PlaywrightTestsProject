import pytest, requests, os, json
from requests import Response
from dotenv import load_dotenv
load_dotenv()

with open(os.getenv("DATA_PATH"),"r", encoding="utf-8") as creds:
    data: dict[list[str, str]] = json.load(creds)
    valid_user_credentials: dict[str, str] = data["credentials"]["valid_users"][1]
    add_item_to_cart_payload: dict = data["payloads"]["request_payloads"][0]

@pytest.mark.smoke
def test_add_item_api():
    # Login endpoint----------------------------------------
    #? / Works entirely /
    user_credentials: dict[str, str] = {
        "userEmail":valid_user_credentials["userEmail"],
        "userPassword":valid_user_credentials["userPassword"]
    }

    url_login = f"{os.getenv("URL")}{os.getenv("LOGIN_ENDPOINT")}"
    data_login = {"userEmail": user_credentials["userEmail"], "userPassword": user_credentials["userPassword"]}
    headers_login = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0"}
    
    response_login: Response = requests.post(url = url_login,
                                             data = data_login,
                                             headers = headers_login)
    
    assert response_login.status_code == 200
    
    token = response_login.json().get("token", None)
    print(token)

    # add item endpoint-----------------------------------------------
    url_add_item = f"{os.getenv('URL')}{os.getenv('ADD_ITEM_TO_CART')}"
    headers_add_item = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
                        "Content-Type": "application/json",
                        "Authorization": token}
    payload_add_item = add_item_to_cart_payload

    response_add_item: Response = requests.post(url=url_add_item,
                                       json=payload_add_item,
                                       headers=headers_add_item)
    response_body = response_add_item.json()

    print(response_add_item.status_code, response_add_item.text)
    assert response_add_item.status_code == 200
    assert response_body["message"] == "Product Added To Cart"