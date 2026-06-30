from datetime import datetime, timedelta, timezone
from schemas.hashtags import (
    TopHashtagsResponse,
    HashtagEntry,
    HashtagHistoryResponse,
    HashtagBucketEntry,
    CorrelatedHashtagsResponse,
    CorrelatedHashtagEntry,
    HashtagLanguageResponse,
    HashtagLanguageEntry,
)

from repositories.hashtag_repo import HashtagRepository
from repositories.post_repo import PostRepository


class HashtagService:
    def __init__(self, conn):
        self.hashtag_repo = HashtagRepository(conn)
        self.post_repo = PostRepository(conn)

    def get_top_hashtags(self, limit: int, hours: int):
        rows = self.hashtag_repo.get_top_hashtags(limit, hours)
        total_posts = self.post_repo.get_total_post_count(hours)

        hashtags = [
            HashtagEntry(rank=i + 1, tag=tag, count=cnt)
            for i, (tag, cnt) in enumerate(rows)
        ]

        return TopHashtagsResponse(
            limit=limit,
            hours=hours,
            total_posts=total_posts,
            hashtags=hashtags
        )

    def get_hashtag_history(self, hashtag: str, bucket_minutes: int, buckets: int):
        tag = hashtag.lstrip("#").lower()
        now = datetime.now(timezone.utc)
        data = []

        for i in range(buckets):
            offset_to = i * bucket_minutes
            offset_from = (i + 1) * bucket_minutes

            count = self.hashtag_repo.get_hashtag_count_in_period(
                tag, offset_from, offset_to
            )

            data.append(HashtagBucketEntry(
                bucket=i + 1,
                from_time=now - timedelta(minutes=offset_from),
                to_time=now - timedelta(minutes=offset_to),
                count=count,
            ))

        return HashtagHistoryResponse(
            tag=tag,
            bucket_minutes=bucket_minutes,
            buckets=buckets,
            data=data,
        )

    def get_correlated_hashtags(self, hashtag: str, limit: int, hours: int):
        tag = hashtag.lstrip("#").lower()
        rows = self.hashtag_repo.get_correlated_hashtags(tag, limit, hours)

        correlated = [
            CorrelatedHashtagEntry(tag=t, count=c)
            for t, c in rows
        ]

        return CorrelatedHashtagsResponse(
            tag=tag,
            correlated_hashtags=correlated
        )

    def get_hashtag_languages(self, hashtag: str, hours: int):
        tag = hashtag.lstrip("#").lower()
        rows = self.hashtag_repo.get_language_distribution(tag, hours)

        total = sum(count for lang, count in rows)
        languages = []
        if total > 0:
            languages = [
                HashtagLanguageEntry(
                    language=lang if lang else "unknown",
                    count=count,
                    percentage=count / total
                )
                for lang, count in rows
            ]

        return HashtagLanguageResponse(
            tag=tag,
            languages=languages
        )

