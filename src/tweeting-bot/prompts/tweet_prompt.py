def tweet_prompt(subject: str, long: bool = False) -> str:
    """
    Generates prompts strictly for software engineering content.
    Short mode: EXACTLY 10 short tweets (unverified account style).
    Long mode: EXACTLY 1 long tweet (verified account style).
    """

    if long:
        return f"""
You are a senior software engineer and architect.

Write EXACTLY ONE long, professional tweet related to software engineering.

STRICT RULES:
- Topic must be software development / engineering only
- No politics, finance, medicine, hate, or illegal content
- No emojis
- No hashtags
- Tone must be professional, precise, and practical
- Suitable for experienced engineers

Topic:
{subject}

Return ONLY the tweet text.
"""

    return f"""
You are a senior software engineer and technical interviewer.

Write EXACTLY 10 short tweets related to software engineering.

STRICT FORMAT (MANDATORY):
- Return a numbered list from 1 to 10
- ONE tweet per line
- Each tweet must be under 280 characters
- No emojis
- No hashtags
- No extra commentary
- No blank lines

Topic:
{subject}
"""
