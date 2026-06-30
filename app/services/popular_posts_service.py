from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from mastodon import Mastodon
from schemas.hashtags import PopularPostEntry, PopularPostsResponse, LivePostEntry

MAX_PAGES = 3


class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
    def handle_data(self, data):
        self.text.append(data)
    def get_text(self):
        return " ".join(self.text)

def _strip_html(html: str) -> str:
    s = _HTMLStripper()
    s.feed(html)
    return s.get_text()

def _score(s) -> int:
    return (s.get("favourites_count") or 0) + (s.get("reblogs_count") or 0) * 2 + (s.get("replies_count") or 0)


class PopularPostsService:
    def __init__(self, mastodon: Mastodon):
        self.mastodon = mastodon

    def get_popular_posts(self, hashtag: str, hours: int, limit: int, pages: int = MAX_PAGES) -> PopularPostsResponse:
        tag = hashtag.lstrip("#").lower()
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

        statuses = []
        page = self.mastodon.timeline_hashtag(tag, since_id=cutoff, limit=40)

        for _ in range(pages):
            if not page:
                break
            statuses.extend(page)
            page = self.mastodon.fetch_next(page)

        statuses.sort(key=_score, reverse=True)

        return PopularPostsResponse(
            tag=tag,
            period_hours=hours,
            limit=limit,
            posts=[
                PopularPostEntry(
                    id=str(s["id"]),
                    url=s.get("url") or "",
                    account=s.get("account", {}).get("acct", ""),
                    content=_strip_html(s.get("content") or ""),
                    created_at=s["created_at"].isoformat(),
                    favourites_count=s.get("favourites_count") or 0,
                    reblogs_count=s.get("reblogs_count") or 0,
                    replies_count=s.get("replies_count") or 0,
                    score=_score(s),
                )
                for s in statuses[:limit]
            ],
        )

    def poll_hashtag(self, hashtag: str, since_id: str | None, limit: int) -> list[LivePostEntry]:
        tag = hashtag.lstrip("#").lower()

        kwargs = {"limit": limit}
        if since_id:
            kwargs["since_id"] = since_id

        statuses = self.mastodon.timeline_hashtag(tag, **kwargs) or []

        return [
            LivePostEntry(
                id=str(s["id"]),
                account=(s.get("account") or {}).get("acct", ""),
                content=_strip_html(s.get("content") or ""),
                url=s.get("url") or "",
                created_at=s["created_at"].isoformat(),
            )
            for s in statuses
        ]
