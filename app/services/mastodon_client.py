from mastodon import Mastodon
from pathlib import Path

MASTODON_URL = "https://techhub.social"

_client = None

def get_mastodon_client() -> Mastodon:
    global _client
    if _client is None:
        _client = Mastodon(api_base_url=MASTODON_URL)
    return _client
