from fastapi import APIRouter, Query, Depends
from services.hashtag_service import HashtagService
from services.sentiment_service import SentimentService
from services.popular_posts_service import PopularPostsService
from api.dependencies import get_hashtag_service, get_sentiment_service, get_popular_posts_service
from schemas.hashtags import TopHashtagsResponse, HashtagHistoryResponse, PopularPostsResponse, LivePostEntry, CorrelatedHashtagsResponse, HashtagLanguageResponse

router = APIRouter()


@router.get("/hashtags/top", response_model=TopHashtagsResponse)
def top_hashtags(
    limit: int = Query(10, ge=1, le=100),
    hours: int = Query(1, ge=1, le=720),
    service: HashtagService = Depends(get_hashtag_service),
):
    return service.get_top_hashtags(limit, hours)

@router.get("/hashtags/{hashtag}/popular", response_model=PopularPostsResponse)
def popular_posts(
    hashtag: str,
    hours: int = Query(1, ge=1, le=168),
    limit: int = Query(3, ge=1, le=50),
    pages: int = Query(3, ge=1, le=10),
    service: PopularPostsService = Depends(get_popular_posts_service),
):
    return service.get_popular_posts(hashtag, hours, limit, pages)

@router.get("/hashtags/{hashtag}/history", response_model=HashtagHistoryResponse)
def hashtag_history(
    hashtag: str,
    bucket_minutes: int = Query(60, ge=1, le=1440),
    buckets: int = Query(6, ge=2, le=48),
    service: HashtagService = Depends(get_hashtag_service),
):
    return service.get_hashtag_history(hashtag, bucket_minutes, buckets)

@router.get("/hashtags/{hashtag}/poll", response_model=list[LivePostEntry])
def poll_hashtag(
    hashtag: str,
    since_id: str = Query(None),
    limit: int = Query(20, ge=1, le=40),
    service: PopularPostsService = Depends(get_popular_posts_service),
):
    return service.poll_hashtag(hashtag, since_id, limit)

@router.get("/hashtags/{hashtag}/sentiment")
def hashtag_sentiment(
    hashtag: str,
    hours: int = Query(24, ge=1, le=720),
    service: SentimentService = Depends(get_sentiment_service),
):
    return service.get_hashtag_sentiment(hashtag, hours)

@router.get("/hashtags/{hashtag}/correlated", response_model=CorrelatedHashtagsResponse)
def correlated_hashtags(
    hashtag: str,
    limit: int = Query(5, ge=1, le=50),
    hours: int = Query(24, ge=1, le=720),
    service: HashtagService = Depends(get_hashtag_service),
):
    return service.get_correlated_hashtags(hashtag, limit, hours)

@router.get("/hashtags/{hashtag}/languages", response_model=HashtagLanguageResponse)
def hashtag_languages(
    hashtag: str,
    hours: int = Query(24, ge=1, le=720),
    service: HashtagService = Depends(get_hashtag_service),
):
    return service.get_hashtag_languages(hashtag, hours)