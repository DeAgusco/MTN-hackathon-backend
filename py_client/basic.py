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
        "Authorization":"Bearer ad55517b6a0611c5a931e28a5532a173fd5795da"
    }
    response = requests.post(endpoint,headers=headers, json=data)
    response_data = response.json()
    print(response_data)
except Exception as e:
    print("Error:", e)
    print("Response Content:", response.text)
