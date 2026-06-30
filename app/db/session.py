import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent / "mastodon_posts.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    try:
        yield conn
    finally:
        conn.close()