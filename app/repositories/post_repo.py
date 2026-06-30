class PostRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_total_post_count(self, hours: int):
        return self.conn.execute("""
            SELECT COUNT(*)
            FROM posts
            WHERE created_at >= datetime('now', ?)
        """, (f"-{hours} hours",)).fetchone()[0]
    
    def get_posts_by_hashtag(self, tag: str, hours: int):
        return self.conn.execute("""
            SELECT p.content
            FROM posts p
            JOIN hashtags h ON h.post_id = p.id
            WHERE h.tag = ?
              AND p.created_at >= datetime('now', ?)
        """, (tag, f"-{hours} hours")).fetchall()