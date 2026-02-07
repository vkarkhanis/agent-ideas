from config.settings import MAX_UNVERIFIED_CHARS

def is_valid(tweet: str) -> bool:
    return len(tweet) <= MAX_UNVERIFIED_CHARS
