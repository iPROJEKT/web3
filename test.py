import requests
import json

url = "https://api-sandbox.nowpayments.io/v1/payment"

payload = json.dumps({
  "price_amount": 3999.5,
  "price_currency": "usd",
  "pay_amount": 0.8102725,
  "pay_currency": "btc",
  "ipn_callback_url": "https://nowpayments.io",
  "order_id": "RGDBP-21314",
  "order_description": "Apple Macbook Pro 2019 x 1"
})
headers = {
  'x-api-key': 'NP870F6-DD84D2Y-PKX9TDC-YD5XCA2',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)