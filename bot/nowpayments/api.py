import json
import os

import requests
from dotenv import load_dotenv


load_dotenv()


URL = "https://api-sandbox.nowpayments.io/v1/invoice"
HEADERS = {
    'x-api-key': os.getenv('TEST_KEY'),
    'Content-Type': 'application/json'
}


def create_pay():
    payload = json.dumps(
        {
            "price_amount": 1000,
            "price_currency": "usd",
            "order_id": "RGDBP-21314",
            "order_description": "Apple Macbook Pro 2019 x 1",
            "ipn_callback_url": "https://nowpayments.io",
            "success_url": "https://nowpayments.io",
            "cancel_url": "https://nowpayments.io"
        }
    )

    response = requests.request("POST", URL, headers=HEADERS, data=payload)
    return response.json()


print(create_pay())