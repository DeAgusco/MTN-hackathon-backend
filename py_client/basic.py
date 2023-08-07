import requests

endpoint = "http://localhost:8000/api/momo/disburse/"
data = {
    "amount": 100,
    "currency": "EUR",  # Change to "EUR" if you want to specify EUR as the currency
    "txt_ref": "stillo",
    "phone_number": "4656473839",
}

try:
    response = requests.post(endpoint, json=data)
    response_data = response.json()
    print(response_data)
except Exception as e:
    print("Error:", e)
    print("Response Content:", response.text)
