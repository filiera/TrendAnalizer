from datetime import datetime
from pydantic import BaseModel


class HashtagEntry(BaseModel):
    rank: int
    tag: str
    count: int


class TopHashtagsResponse(BaseModel):
    limit: int
    hours: int
    total_posts: int
    hashtags: list[HashtagEntry]


class HashtagBucketEntry(BaseModel):
    bucket: int
    from_time: datetime
    to_time: datetime
    count: int


class HashtagHistoryResponse(BaseModel):
    tag: str
    bucket_minutes: int
    buckets: int
    data: list[HashtagBucketEntry]


class HashtagSentimentResponse(BaseModel):
    tag: str
    period_hours: int
    positive: float
    neutral: float
    negative: float



class LivePostEntry(BaseModel):
    id: str
    account: str
    content: str
    url: str
    created_at: str


class PopularPostEntry(BaseModel):
    id: str
    url: str
    account: str
    content: str
    created_at: str
    favourites_count: int
    reblogs_count: int
    replies_count: int
    score: int


class PopularPostsResponse(BaseModel):
    tag: str
    period_hours: int
    limit: int
    posts: list[PopularPostEntry]

class CorrelatedHashtagEntry(BaseModel):
    tag: str
    count: int

class CorrelatedHashtagsResponse(BaseModel):
    tag: str
    correlated_hashtags: list[CorrelatedHashtagEntry]

class HashtagLanguageEntry(BaseModel):
    language: str | None
    count: int
    percentage: float

class HashtagLanguageResponse(BaseModel):
    tag: str
    languages: list[HashtagLanguageEntry]