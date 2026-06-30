# services/sentiment_service.py

from collections import Counter
from repositories.post_repo import PostRepository
from services.sentiment_model import predict_sentiment
from schemas.hashtags import HashtagSentimentResponse


class SentimentService:
    def __init__(self, conn):
        self.repo = PostRepository(conn)

    def get_hashtag_sentiment(self, tag: str, hours: int):
        tag = tag.lstrip("#").lower()

        rows = self.repo.get_posts_by_hashtag(tag, hours)

        counter = Counter({"positive": 0, "neutral": 0, "negative": 0})
        total = 0

        for (content,) in rows:
            if not content:
                continue

            sentiment = predict_sentiment(content)
            counter[sentiment] += 1
            total += 1

        if total == 0:
            return HashtagSentimentResponse(
                tag=tag,
                period_hours=hours,
                positive=0,
                neutral=0,
                negative=0,
            )

        return HashtagSentimentResponse(
            tag=tag,
            period_hours=hours,
            positive=counter["positive"] / total,
            neutral=counter["neutral"] / total,
            negative=counter["negative"] / total,
        )