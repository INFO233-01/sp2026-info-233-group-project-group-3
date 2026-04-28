import requests
from config import CLIENT_ID, CLIENT_SECRET

def get_token():
    url = "https://oauth.fatsecret.com/connect/token"
    response = requests.post(
        url,
        data={"grant_type": "client_credentials", "scope": "basic"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    token = response.json()["access_token"]
    print("Connected to FatSecret successfully!")
    return token

def search_food(query, token):
    url = "https://platform.fatsecret.com/rest/server.api"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "method": "foods.search",
        "search_expression": query,
        "format": "json",
        "max_results": 10
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()