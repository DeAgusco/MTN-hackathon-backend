import requests

endpoint = "http://localhost:8000/product/1/unlike/"
headers = {
        "Authorization":"Token 7df01d8099b78b1f816f6dee7eed2a634a9f76d7"
}
response = requests.post(endpoint, headers=headers)
print(response.json())