import requests

endpoint = "http://localhost:8000/api/account/register/"
data = {
        "first_name":"Sammy",
        "password":"postgress",
        "mobile":"0599971083",
        "email":"n@b.com"
}
response = requests.post(endpoint, data=data)
print(response.json())