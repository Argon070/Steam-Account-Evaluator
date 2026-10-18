import requests

url = "https://www.steamwebapi.com/account/me"

headers = {"X-Api-Key": "YOUR_API_KEY"}
response = requests.get(url, headers=headers)

print(response.json())