from tools.tweet_generator import generate_short_tweets, generate_long_tweet
from tools.tweet_validator import is_valid

def generate_short_form_tweets(subject: str):
    tweets = generate_short_tweets(subject)
    return [t for t in tweets if is_valid(t)]

def generate_long_form_tweet(subject: str):
    return generate_long_tweet(subject)
