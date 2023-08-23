import requests

endpoint = "http://localhost:8000/api/wallet/"
headers = {
        "Authorization":"Bearer ad55517b6a0611c5a931e28a5532a173fd5795da"
}
response = requests.get(endpoint, headers=headers)
print(response.json()['balance'])