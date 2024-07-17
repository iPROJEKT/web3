import json
import os

import requests
from dotenv import load_dotenv


load_dotenv()


URL = "https://api.nowpayments.io/v1/invoice"
HEADERS = {
    'x-api-key': os.getenv('NOWPAYMENT'),
    'Content-Type': 'application/json'
}


def create_pay(amount):
    payload = json.dumps(
        {
            "price_amount": amount,
            "price_currency": "usd",
            "order_id": "RGDBP-21314",
            "order_description": "$USDC",
            "ipn_callback_url": "https://nowpayments.io",
            "success_url": "https://nowpayments.io",
            "cancel_url": "https://nowpayments.io"
        }
    )
    response = requests.request("POST", URL, headers=HEADERS, data=payload)
    return response.json()

