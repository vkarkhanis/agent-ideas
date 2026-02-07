import requests

POST_TWEET_URL = "https://api.twitter.com/2/tweets"

def post_tweet(access_token: str, text: str):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {"text": text}

    response = requests.post(
        POST_TWEET_URL,
        headers=headers,
        json=payload
    )

    response.raise_for_status()
    return response.json()
