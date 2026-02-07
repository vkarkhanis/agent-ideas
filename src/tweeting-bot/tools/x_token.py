import requests
from base64 import b64encode

TOKEN_URL = "https://api.twitter.com/2/oauth2/token"

def exchange_code(client_id, client_secret, code, redirect_uri):
    auth = b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": "challenge"
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    response.raise_for_status()
    return response.json()
