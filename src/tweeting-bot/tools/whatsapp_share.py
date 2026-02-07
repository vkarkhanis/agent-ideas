import urllib.parse

def whatsapp_share_url(message: str) -> str:
    """
    Returns a WhatsApp share URL with the message pre-filled.
    Works on desktop and mobile (WhatsApp Web / App).
    """
    encoded = urllib.parse.quote(message)
    return f"https://wa.me/?text={encoded}"
