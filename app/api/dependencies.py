from fastapi import Depends
from db.session import get_db
from services.hashtag_service import HashtagService
from services.sentiment_service import SentimentService
from services.popular_posts_service import PopularPostsService
from services.mastodon_client import get_mastodon_client


def get_hashtag_service(conn=Depends(get_db)):
    return HashtagService(conn)

def get_sentiment_service(conn=Depends(get_db)):
    return SentimentService(conn)

def get_popular_posts_service():
    return PopularPostsService(get_mastodon_client())