from openai import OpenAI
from config.settings import OPENAI_API_KEY
from tools.tweet_validator import is_valid
import re

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_short_tweets(subject: str):
    from prompts.tweet_prompt import tweet_prompt

    prompt = tweet_prompt(subject)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        temperature=0.8
    )

    text = response.output_text
    tweets = _extract_numbered_tweets(text)
    valid = [t for t in tweets if is_valid(t)]

    return valid[:10]


def generate_long_tweet(subject: str):
    from prompts.tweet_prompt import tweet_prompt

    prompt = tweet_prompt(subject, long=True)

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt,
        temperature=0.7
    )

    return response.output_text.strip()

def _extract_numbered_tweets(text: str) -> list[str]:
    """
    Extracts tweets from a numbered list like:
    1. Tweet
    2. Tweet
    ...
    """
    tweets = []

    for line in text.splitlines():
        match = re.match(r"^\s*\d+\.\s+(.*)", line)
        if match:
            tweets.append(match.group(1).strip())

    return tweets