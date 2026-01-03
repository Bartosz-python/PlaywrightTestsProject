import pytest, requests, os, json
from requests import Response
from dotenv import load_dotenv
load_dotenv()

with open(os.getenv("DATA_PATH"),"r", encoding="utf-8") as creds:
    data: dict[list[str, str]] = json.load(creds)
    valid_user_credentials: dict[str, str] = data["credentials"]["valid_users"][1]
    add_item_to_cart_payload: dict = data["payloads"]["request_payloads"][0]
    item_id = data["payloads"]["request_payloads"][0]["product"]["_id"]

@pytest.mark.smoke
def test_add_item_api(auth_token_and_user_id):
    token, user_id = auth_token_and_user_id

    # add item endpoint-----------------------------------------------
    url_add_item = f"{os.getenv('URL')}{os.getenv('ADD_ITEM_TO_CART')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
               "Content-Type": "application/json",
               "Authorization": token}
    payload_add_item = add_item_to_cart_payload

    response_add_item: Response = requests.post(url=url_add_item,
                                                json=payload_add_item,
                                                headers=headers)
    response_body = response_add_item.json()

    assert response_add_item.status_code == 200
    assert response_body["message"] == "Product Added To Cart"

    cart_response: Response = requests.get(url = f"{os.getenv("URL")}{os.getenv("GET_CART_PRODUCTS")}{user_id}",
                                           headers=headers)
    assert item_id in cart_response.json()["products"][0]["_id"]
    assert cart_response.json().get("count") == 1

    requests.delete(url = f"{os.getenv("URL")}{os.getenv("REMOVE_FROM_CART")}{user_id}/{item_id}",
                    headers=headers)

    cart_response_again: Response = requests.get(url = f"{os.getenv("URL")}{os.getenv("GET_CART_PRODUCTS")}{user_id}",
                                                 headers=headers)
    assert cart_response_again.json().get("message") == "No Product in Cart"