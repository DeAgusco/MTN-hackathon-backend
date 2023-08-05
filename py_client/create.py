import requests

endpoint = "http://localhost:8000/api/products/"

data = {
    "title":"Nunu",
    "price":24.50
}
response = requests.post(endpoint, json=data)
print(response.json())