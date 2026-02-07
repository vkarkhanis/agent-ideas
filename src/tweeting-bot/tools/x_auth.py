import urllib.parse

AUTH_URL = "https://twitter.com/i/oauth2/authorize"

def build_auth_url(client_id, redirect_uri, state):
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "tweet.read tweet.write users.read offline.access",
        "state": state,
        "code_challenge": "challenge",
        "code_challenge_method": "plain"
    }

    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
