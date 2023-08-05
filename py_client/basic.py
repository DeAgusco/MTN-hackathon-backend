import requests

endpoint = "http://localhost:8000/api/"

response = requests.post(endpoint, json={"title":"corn"})
print(response.json())