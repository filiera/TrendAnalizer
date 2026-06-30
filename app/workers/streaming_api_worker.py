from mastodon import Mastodon, StreamListener
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
import re
from html.parser import HTMLParser
from langdetect import detect, DetectorFactory

# Set seed for consistent results
DetectorFactory.seed = 0

MASTODON_URL = "https://techhub.social"
DB_FILE = Path(__file__).parent.parent / "db" / "mastodon_posts.db"

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
    def handle_data(self, data):
        self.text.append(data)
    def get_text(self):
        return ' '.join(self.text)
    
def strip_html(html):
    s = HTMLStripper()
    s.feed(html)
    return s.get_text()

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id          TEXT PRIMARY KEY,
            created_at  TEXT,
            account     TEXT,
            content     TEXT,
            url         TEXT,
            language    TEXT
        )
    ''')
    # Try to add the column if the table already exists
    try:
        conn.execute('ALTER TABLE posts ADD COLUMN language TEXT')
    except sqlite3.OperationalError:
        pass # Column already exists
    conn.execute('''
        CREATE TABLE IF NOT EXISTS hashtags (
            post_id TEXT,
            tag     TEXT,
            FOREIGN KEY (post_id) REFERENCES posts(id)
        )
    ''')
    conn.commit()
    conn.close()

def save_post(status):
    post_id = status.get('id')
    created_at = str(status.get('created_at', datetime.now(timezone.utc)))
    account = status.get('account', {}).get('acct', '')
    content = strip_html(status.get('content', ''))
    url = status.get('url', '')
    language = status.get('language')

    # Fallback to local language detection if API didn't provide it
    if not language and content.strip():
        try:
            language = detect(content)
        except:
            language = None

    tags = {t.lower() for t in re.findall(r'#(\w+)', content, re.IGNORECASE)}

    for t in status.get('tags', []):
        name = t.get('name', '')
        if name:
            tags.add(name.lower())

    if not tags:
        return
    
    conn = sqlite3.connect(DB_FILE)
    try:
        cursor = conn.execute(
            'INSERT OR IGNORE INTO posts VALUES (?,?,?,?,?,?)',
            (post_id, created_at, account, content, url, language)
        )
        if cursor.rowcount:
            for tag in tags:
                conn.execute(
                    'INSERT INTO hashtags VALUES (?,?)',
                    (post_id, tag)
                )
        conn.commit()
    finally:
        conn.close()

class Listener(StreamListener):
    def on_update(self, status):
        save_post(status)
        tags = [t.get('name') for t in status.get('tags', [])]
        if tags:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {status.get('account',{}).get('acct','')} -> #{', #'.join(tags)}")

if __name__ == "__main__":
    init_db()

    secret_file = 'mastodon.secret'
    
    # Check if we already have a secret file
    if not Path(secret_file).exists():
        print("Registering app...")
        Mastodon.create_app(
            'hashtag-monitor',
            api_base_url=MASTODON_URL,
            to_file=secret_file
        )
        
        mastodon = Mastodon(
            client_id=secret_file,
            api_base_url=MASTODON_URL
        )
        print("Please visit this URL to authorize the app:")
        print(mastodon.auth_request_url())
        auth_code = input("Insert OAuth code: ")
        mastodon.log_in(
            code=auth_code,
            to_file=secret_file
        )
    else:
        # Load existing credentials
        try:
            mastodon = Mastodon(
                access_token=secret_file,
                api_base_url=MASTODON_URL
            )
            # Verify if token is still valid
            mastodon.account_verify_credentials()
            print("Loaded existing credentials from mastodon.secret")
        except Exception as e:
            print(f"Existing credentials invalid: {e}")
            print("Re-registering...")
            Mastodon.create_app(
                'hashtag-monitor',
                api_base_url=MASTODON_URL,
                to_file=secret_file
            )
            mastodon = Mastodon(
                client_id=secret_file,
                api_base_url=MASTODON_URL
            )
            print(mastodon.auth_request_url())
            auth_code = input("Insert OAuth code: ")
            mastodon.log_in(
                code=auth_code,
                to_file=secret_file
            )

    print("Logged in as: ", mastodon.account_verify_credentials().username)
    print("Starting public stream...")
    mastodon.stream_public(Listener())