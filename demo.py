import requests

url ='http://127.0.0.1:8000/api/update/'

data = {
    "name": "abihjgghfggf",
}

resp = requests.post(url, data=data)
print(resp.json())