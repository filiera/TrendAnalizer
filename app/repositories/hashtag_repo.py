class HashtagRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_top_hashtags(self, limit: int, hours: int):
        return self.conn.execute("""
            SELECT h.tag, COUNT(*) as cnt
            FROM hashtags h
            JOIN posts p ON h.post_id = p.id
            WHERE p.created_at >= datetime('now', ?)
            GROUP BY h.tag
            ORDER BY cnt DESC
            LIMIT ?
        """, (f"-{hours} hours", limit)).fetchall()

    def get_hashtag_count_in_period(self, tag: str, offset_from: int, offset_to: int):
        return self.conn.execute("""
            SELECT COUNT(*)
            FROM hashtags h
            JOIN posts p ON h.post_id = p.id
            WHERE h.tag = ?
              AND p.created_at >= datetime('now', ? || ' minutes')
              AND p.created_at <  datetime('now', ? || ' minutes')
        """, (tag, f"-{offset_from}", f"-{offset_to}")).fetchone()[0]

    def get_correlated_hashtags(self, tag: str, limit: int, hours: int):
        return self.conn.execute("""
            SELECT h2.tag, COUNT(*) as cnt
            FROM hashtags h1
            JOIN hashtags h2 ON h1.post_id = h2.post_id
            JOIN posts p ON h1.post_id = p.id
            WHERE h1.tag = ?
              AND h2.tag != ?
              AND p.created_at >= datetime('now', ?)
            GROUP BY h2.tag
            ORDER BY cnt DESC
            LIMIT ?
        """, (tag, tag, f"-{hours} hours", limit)).fetchall()

    def get_language_distribution(self, tag: str, hours: int):
        return self.conn.execute("""
            SELECT p.language, COUNT(*) as cnt
            FROM hashtags h
            JOIN posts p ON h.post_id = p.id
            WHERE h.tag = ?
              AND p.created_at >= datetime('now', ?)
            GROUP BY p.language
            ORDER BY cnt DESC
        """, (tag, f"-{hours} hours")).fetchall()

