import requests

endpoint = "http://localhost:8000/api/wallet/topup/"
data = {
    "amount": 100,
    "currency": "EUR",  # Change to "EUR" if you want to specify EUR as the currency
    "txt_ref": "stillo",
    "phone_number": "4656473839",
    "payer_message":"Wallet topup"
}

try:
    headers = {
        "Authorization":"Bearer 6c17c65c0c3b21b5ed9ffb37a3f1bf081d11f05c"
    }
    response = requests.post(endpoint,headers=headers, json=data)
    response_data = response.json()
    print(response_data)
except Exception as e:
    print("Error:", e)
    print("Response Content:", response.text)
